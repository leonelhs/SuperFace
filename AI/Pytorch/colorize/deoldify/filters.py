import logging
from dataclasses import field, dataclass
from functools import partial
from typing import List, Tuple, Collection, Union, Optional

import PIL
import cv2
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image as PilImage
from torch import Tensor, nn
from fastai.layers import NormType
from fastai.torch_core import to_device
from fastai.vision.learner import create_body
from torchvision.models import resnet34

from AI.Pytorch.colorize.deoldify.unet import DynamicUnetDeep
from AI.Pytorch.colorize.deoldify.dataset import get_dummy_databunch

from AI.Pytorch.colorize.fastai.basic_data import DatasetType
from AI.Pytorch.colorize.fastai.callback import CallbackHandler, Callback
from AI.Pytorch.colorize.fastai.core import camel2snake, is_listy, ifnone, noop
from AI.Pytorch.colorize.fastai.torch_core import to_detach, OptLossFunc, OptOptimizer
from AI.Pytorch.colorize.fastai.vision import normalize_funcs, pil2tensor, image2np

# from fastai.basic_data import DatasetType
# from fastai.callback import CallbackHandler, Callback
# from fastai.core import camel2snake, is_listy, ifnone, noop
# from fastai.torch_core import to_detach, OptLossFunc, OptOptimizer
# from fastai.vision import normalize_funcs, pil2tensor, image2np

render_factor = 35
stats = ([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])


def loss_batch(model: nn.Module, xb: Tensor, yb: Tensor, loss_func: OptLossFunc = None, opt: OptOptimizer = None,
               cb_handler: Optional[CallbackHandler] = None, count: [int] = [1], batch_multiplier: int = 1) -> Tuple[
    Union[Tensor, int, float, str]]:
    "Calculate loss and metrics for a batch, call out to callbacks as necessary."
    cb_handler = ifnone(cb_handler, CallbackHandler())
    if not is_listy(xb): xb = [xb]
    if not is_listy(yb): yb = [yb]
    out = model(*xb)

    if not loss_func: return to_detach(out), yb[0].detach()
    out = cb_handler.on_loss_begin(out)
    loss = loss_func(out, *yb) / batch_multiplier
    count[0] -= 1

    if opt is not None:
        loss, skip_bwd = cb_handler.on_backward_begin(loss)
        if not skip_bwd:                     loss.backward()
        if count[0] == 0:
            if not cb_handler.on_backward_end(): opt.step()
            if not cb_handler.on_step_end():     opt.zero_grad()
            count[0] = batch_multiplier

    return loss.detach().cpu()


loss_func_name2activ = {'cross_entropy_loss': F.softmax, 'nll_loss': torch.exp, 'poisson_nll_loss': torch.exp,
                        'kl_div_loss': torch.exp, 'bce_with_logits_loss': torch.sigmoid, 'cross_entropy': F.softmax,
                        'kl_div': torch.exp, 'binary_cross_entropy_with_logits': torch.sigmoid,
                        }


def _loss_func_name2activ(name: str, axis: int = -1):
    res = loss_func_name2activ[name]
    if res == F.softmax: res = partial(F.softmax, dim=axis)
    return res


def _loss_func2activ(loss_func):
    if getattr(loss_func, 'keywords', None):
        if not loss_func.keywords.get('log_input', True): return
    axis = getattr(loss_func, 'axis', -1)
    # flattened loss
    loss_func = getattr(loss_func, 'func', loss_func)
    # could have a partial inside flattened loss! Duplicate on purpose.
    loss_func = getattr(loss_func, 'func', loss_func)
    cls_name = camel2snake(loss_func.__class__.__name__)
    if cls_name == 'mix_up_loss':
        loss_func = loss_func.crit
        cls_name = camel2snake(loss_func.__class__.__name__)
    if cls_name in loss_func_name2activ:
        if cls_name == 'poisson_nll_loss' and (not getattr(loss_func, 'log_input', True)): return
        return _loss_func_name2activ(cls_name, axis)
    if getattr(loss_func, '__name__', '') in loss_func_name2activ:
        return _loss_func_name2activ(loss_func.__name__, axis)
    return noop


@dataclass
class Learner:
    "Trainer for `model` using `data` to minimize `loss_func` with optimizer `opt_func`."
    callbacks: Collection[Callback] = field(default_factory=list)


class BaseFilter:
    def __init__(self):
        super().__init__()
        self.model = None
        self.render_base = 16
        self.learn = Learner()
        self.callbacks: Collection[Callback] = field(default_factory=list)
        self.data = get_dummy_databunch()
        self.device = torch.device('cpu')
        self.norm, self.denorm = normalize_funcs(*stats)
        self.load_model()

    def load_model(self):
        body = create_body(resnet34)
        self.model = to_device(
            DynamicUnetDeep(
                body,
                n_classes=3,
                blur=True,
                blur_final=True,
                self_attention=True,
                y_range=(-3.0, 3.0),
                norm_type=NormType.Spectral,
                last_cross=True,
                bottle=False,
                nf_factor=1.5,
            ),
            self.device,
        )
        source = "./dummy/models/ColorizeArtistic_gen.pth"
        state = torch.load(source, map_location=self.device)
        model_state = state['model']
        self.model.load_state_dict(model_state, strict=True)

    def _transform(self, image: PilImage) -> PilImage:
        return image.convert('LA').convert('RGB')

    def _scale_to_square(self, orig: PilImage, targ: int) -> PilImage:
        # a simple stretch to fit a square really makes a big difference in rendering quality/consistency.
        # I've tried padding to the square as well (reflect, symetric, constant, etc).  Not as good!
        targ_sz = (targ, targ)
        return orig.resize(targ_sz, resample=PIL.Image.BILINEAR)

    def _get_model_ready_image(self, orig: PilImage, sz: int) -> PilImage:
        result = self._scale_to_square(orig, sz)
        result = self._transform(result)
        return result

    def _model_process(self, orig: PilImage, sz: int) -> PilImage:
        model_image = self._get_model_ready_image(orig, sz)
        x = pil2tensor(model_image, np.float32)
        x = x.to(self.device)
        x.div_(255)
        x, y = self.norm((x, x), do_x=True)

        try:
            result = self.pred_batch(
                ds_type=DatasetType.Valid, batch=(x[None], y[None]), reconstruct=True
            )
        except RuntimeError as rerr:
            if 'memory' not in str(rerr):
                raise rerr
            logging.warn(
                'Warning: render_factor was set too high, and out of memory error resulted. Returning original image.')
            return model_image

        out = result[0]
        out = self.denorm(out.px, do_x=False)
        out = image2np(out * 255).astype(np.uint8)
        return PilImage.fromarray(out)

    def _unsquare(self, image: PilImage, orig: PilImage) -> PilImage:
        targ_sz = orig.size
        image = image.resize(targ_sz, resample=PIL.Image.BILINEAR)
        return image

    def pred_batch(self, ds_type: DatasetType = DatasetType.Valid, batch: Tuple = None, reconstruct: bool = False,
                   with_dropout: bool = False) -> List[Tensor]:
        with torch.no_grad():
            training = False
            self.model.train(False)
            "Return output of the model on one batch from `ds_type` dataset."
            if batch is not None:
                xb, yb = batch
            else:
                xb, yb = self.data.one_batch(ds_type, detach=False, denorm=False)
            cb_handler = CallbackHandler(self.learn.callbacks)
            # xb,yb = cb_handler.on_batch_begin(xb,yb, train=False)
            if not with_dropout:
                preds = loss_batch(self.model.eval(), xb, yb, cb_handler=cb_handler)
            else:
                preds = loss_batch(self.model.eval().apply(self.learn.apply_dropout), xb, yb,
                                   cb_handler=cb_handler)
            res = _loss_func2activ(F.l1_loss)(preds[0])
            self.model.train(training)
            if not reconstruct: return res
            res = res.detach().cpu()
            ds = self.dl(ds_type).dataset
            norm = getattr(self.data, 'norm', False)
            if norm and norm.keywords.get('do_y', False):
                res = self.data.denorm(res, do_x=True)
            return [ds.reconstruct(o) for o in res]

    def dl(self, ds_type: DatasetType = DatasetType.Valid):
        "Return DataLoader for DatasetType `ds_type`."
        return self.data.dl(ds_type)

    def filter(self, filtered_image: PilImage) -> PilImage:
        orig_image = filtered_image.copy()
        render_sz = render_factor * self.render_base
        model_image = self._model_process(orig=filtered_image, sz=render_sz)
        raw_color = self._unsquare(model_image, orig_image)
        return raw_color
    # This takes advantage of the fact that human eyes are much less sensitive to
    # imperfections in chrominance compared to luminance.  This means we can
    # save a lot on memory and processing in the model, yet get a great high
    # resolution result at the end.  This is primarily intended just for
    # inference

    # Post proxes takes colored image resulted as first argument and the original b&w image
    def _post_process(self, raw_color: PilImage, orig: PilImage) -> PilImage:
        color_np = np.asarray(raw_color)
        orig_np = np.asarray(orig)
        color_yuv = cv2.cvtColor(color_np, cv2.COLOR_BGR2YUV)
        # do a black and white transform first to get better luminance values
        orig_yuv = cv2.cvtColor(orig_np, cv2.COLOR_BGR2YUV)
        hires = np.copy(orig_yuv)
        hires[:, :, 1:3] = color_yuv[:, :, 1:3]
        final = cv2.cvtColor(hires, cv2.COLOR_YUV2BGR)
        final = PilImage.fromarray(final)
        return final
