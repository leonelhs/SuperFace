from fastai.layers import NormType
from fastai.torch_core import apply_init
from fastai.torch_core import to_device
from fastai.vision.learner import cnn_config, create_body
from torch import nn
from torchvision.models import resnet34
import torch.nn.functional as F

from .dataset import get_dummy_databunch
from .unet import DynamicUnetDeep
from ..fastai.basic_train import Learner


def my_gen_learner_deep():
    pretrained = True
    data = get_dummy_databunch()
    meta = cnn_config(resnet34)
    body = create_body(resnet34, pretrained)
    model = to_device(
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
        data.device,
    )
    # learn = Learner(data, model, **kwargs)
    learn = Learner(data, model, wd=0.001, loss_func=F.l1_loss)
    learn.split(ifnone(None, meta['split']))
    if pretrained:
        learn.freeze()
    apply_init(model[2], nn.init.kaiming_normal_)
    return learn
