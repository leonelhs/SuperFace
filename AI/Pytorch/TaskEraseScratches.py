#############################################################################
#
#   Source from:
#
#   Forked from:
#
#   Reimplemented by: Leonel Hernández
#
##############################################################################
import cv2
import torchvision.transforms as transforms
from PIL import Image
from torchvision.utils import make_grid

from Helpers.TaskPhotoEnhancer import TaskPhotoEnhancer
from .zero_scratches.detection_util.util import *
from .zero_scratches.models.mapping_model import Pix2PixHDModel_Mapping
from .zero_scratches.options import Options


# ########## Scratches Methods ##############

def resize_transforms(img, method=Image.BILINEAR, scale=False):
    ow, oh = img.size
    pw, ph = ow, oh
    if scale:
        if ow < oh:
            ow = 256
            oh = ph / pw * 256
        else:
            oh = 256
            ow = pw / ph * 256

    h = int(round(oh / 4) * 4)
    w = int(round(ow / 4) * 4)

    if (h == ph) and (w == pw):
        return img

    return img.resize((w, h), method)


def data_transforms_rgb_old(img):
    w, h = img.size
    A = img
    if w < 256 or h < 256:
        A = transforms.Scale(256, Image.BILINEAR)(img)
    return transforms.CenterCrop(256)(A)


def irregular_hole_synthesize(img, mask):
    img_np = np.array(img).astype("uint8")
    mask_np = np.array(mask).astype("uint8")
    mask_np = mask_np / 255
    img_new = img_np * (1 - mask_np) + mask_np * 255

    hole_img = Image.fromarray(img_new.astype("uint8")).convert("RGB")

    return hole_img


def tensor_to_image(tensor):
    grid = make_grid(tensor, nrow=1, padding=0, normalize=True)
    ndarr = grid.mul(255).add_(0.5).clamp_(0, 255).permute(1, 2, 0).to("cpu", torch.uint8).numpy()
    return Image.fromarray(ndarr)


model_path_scratches = "./models/zero_scratches/checkpoints/restoration"


class TaskEraseScratches(TaskPhotoEnhancer):

    def __init__(self, args):
        super().__init__(args)
        self.options = Options(model_path_scratches)
        self.model_scratches = Pix2PixHDModel_Mapping()
        self.model_scratches.initialize(self.options)
        self.model_scratches.eval()

    def erase_scratches(self, transformed, mask):

        img_transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
        )
        mask_transform = transforms.ToTensor()

        if self.options.NL_use_mask:
            if self.options.mask_dilation != 0:
                kernel = np.ones((3, 3), np.uint8)
                mask = np.array(mask)
                mask = cv2.dilate(mask, kernel, iterations=self.options.mask_dilation)
                mask = Image.fromarray(mask.astype('uint8'))
            origin = transformed
            transformed = irregular_hole_synthesize(transformed, mask)
            mask = mask_transform(mask)
            mask = mask[:1, :, :]  # Convert to single channel
            mask = mask.unsqueeze(0)
            transformed = img_transform(transformed)
            transformed = transformed.unsqueeze(0)
        else:
            if self.options.test_mode == "Scale":
                transformed = resize_transforms(transformed, scale=True)
            if self.options.test_mode == "Full":
                transformed = resize_transforms(transformed, scale=False)
            if self.options.test_mode == "Crop":
                transformed = data_transforms_rgb_old(transformed)
            origin = transformed
            transformed = img_transform(transformed)
            transformed = transformed.unsqueeze(0)
            mask = torch.zeros_like(transformed)
        # Necessary input

        try:
            with torch.no_grad():
                generated = self.model_scratches.inference(transformed, mask)
        except Exception as ex:
            print("Skip photo due to an error:\n%s" % str(ex))

        tensor_scratch = (transformed + 1.0) / 2.0
        image_scratches = tensor_to_image(tensor_scratch)

        tensor_restored = (generated.data.cpu() + 1.0) / 2.0
        image_restored = tensor_to_image(tensor_restored)
        return image_scratches, image_restored

    def executeEnhanceWork(self, images, progress_callback):
        scratches, restored = self.erase_scratches(transformed=images[0], mask=images[1])
        return restored
