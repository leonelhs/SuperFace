#############################################################################
#
#   Source from:
#
#   Forked from:
#
#   Reimplemented by: Leonel Hernández
#
##############################################################################
import torch.nn.functional as F
from PIL import Image
from PIL import ImageFile
from torchvision.utils import make_grid

from Helpers.TaskPhotoEnhancer import TaskPhotoEnhancer
from .zero_scratches.detection_models import networks
from .zero_scratches.detection_util.util import *

ImageFile.LOAD_TRUNCATED_IMAGES = True


# ######### Mask methods ################

def data_transforms(img, size="full_size", method=Image.BICUBIC):
    if size == "full_size":
        ow, oh = img.size
        h = int(round(oh / 16) * 16)
        w = int(round(ow / 16) * 16)
        if (h == oh) and (w == ow):
            return img
        return img.resize((w, h), method)

    elif size == "scale_256":
        ow, oh = img.size
        pw, ph = ow, oh
        if ow < oh:
            ow = 256
            oh = ph / pw * 256
        else:
            oh = 256
            ow = pw / ph * 256

        h = int(round(oh / 16) * 16)
        w = int(round(ow / 16) * 16)
        if (h == ph) and (w == pw):
            return img
        return img.resize((w, h), method)


def scale_tensor(img_tensor, default_scale=256):
    _, _, w, h = img_tensor.shape
    if w < h:
        ow = default_scale
        oh = h / w * default_scale
    else:
        oh = default_scale
        ow = w / h * default_scale

    oh = int(round(oh / 16) * 16)
    ow = int(round(ow / 16) * 16)

    return F.interpolate(img_tensor, [ow, oh], mode="bilinear")


def blend_mask(img, mask):
    np_img = np.array(img).astype("float")

    return Image.fromarray((np_img * (1 - mask) + mask * 255.0).astype("uint8")).convert("RGB")


def tensor_to_image(tensor):
    grid = make_grid(tensor, nrow=1, padding=0, normalize=True)
    ndarr = grid.mul(255).add_(0.5).clamp_(0, 255).permute(1, 2, 0).to("cpu", torch.uint8).numpy()
    return Image.fromarray(ndarr)


model_path_mask = "./models/zero_scratches/checkpoints/detection/FT_Epoch_latest.pt"


class TaskMaskScratches(TaskPhotoEnhancer):

    def __init__(self, args):
        super().__init__(args)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_mask = networks.UNet(
            in_channels=1,
            out_channels=1,
            depth=4,
            conv_num=2,
            wf=6,
            padding=True,
            batch_norm=True,
            up_mode="upsample",
            with_tanh=False,
            sync_bn=True,
            antialiasing=True,
        )

        checkpoint = torch.load(model_path_mask, map_location=device)
        self.model_mask.load_state_dict(checkpoint["model_state"])
        self.model_mask.cpu()
        self.model_mask.eval()

    def build_mask(self, scratch_image):
        transformed_image = data_transforms(scratch_image)
        scratch_image = transformed_image.convert("L")
        scratch_image = tv.transforms.ToTensor()(scratch_image)
        scratch_image = tv.transforms.Normalize([0.5], [0.5])(scratch_image)
        scratch_image = torch.unsqueeze(scratch_image, 0)
        _, _, ow, oh = scratch_image.shape
        scratch_image_scale = scale_tensor(scratch_image)

        scratch_image_scale = scratch_image_scale.cpu()
        with torch.no_grad():
            P = torch.sigmoid(self.model_mask(scratch_image_scale))

        P = P.data.cpu()
        P = F.interpolate(P, [ow, oh], mode="nearest")

        tensor_mask = (P >= 0.4).float()
        scratches_mask_image = tensor_to_image(tensor_mask)

        return transformed_image, scratches_mask_image

    def executeEnhanceWork(self, image, progress_callback):
        return self.build_mask(image)
