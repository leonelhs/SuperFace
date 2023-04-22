#############################################################################
#
#   Source from:
#   https://github.com/leonelhs/Real-ESRGAN-1
#   Forked from:
#   https://github.com/ai-forever/Real-ESRGAN
#   Reimplemented by: Leonel Hernández
#
##############################################################################

import numpy as np
import torch

from RealESRGAN.rrdbnet_arch import RRDBNet
from RealESRGAN.utils import pad_reflect, split_image_into_overlapping_patches, stich_together, unpad_image
from AI.Pytorch.superface.base_upsampler import Upsampler

HF_MODELS = {
    2: './models/Real-ESRGAN/RealESRGAN_x2.pth',
    4: './models/Real-ESRGAN/RealESRGAN_x4.pth',
    8: './models/Real-ESRGAN/RealESRGAN_x8.pth'
}


class RealEsrganUpsampler(Upsampler):
    def __init__(self):
        super().__init__()

        self.model = None
        self.scale = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.loadModel()

    def loadModel(self, scale=2):
        self.scale = scale
        self.model = RRDBNet(
            num_in_ch=3, num_out_ch=3, num_feat=64,
            num_block=23, num_grow_ch=32, scale=scale
        )

        loadnet = torch.load(HF_MODELS[scale])
        self.model.load_state_dict(loadnet, strict=True)
        self.model.eval()
        self.model.to(self.device)

    @torch.cuda.amp.autocast()
    def enhance(self, image_lowres=None, outscale=None):
        batch_size = 4
        patches_size = 192
        padding = 24
        pad_size = 15

        scale = self.scale
        device = self.device
        image_lowres = np.array(image_lowres)
        image_lowres = pad_reflect(image_lowres, pad_size)

        patches, p_shape = split_image_into_overlapping_patches(
            image_lowres, patch_size=patches_size, padding_size=padding
        )

        img = torch.FloatTensor(patches / 255).permute((0, 3, 1, 2)).to(device).detach()

        with torch.no_grad():
            res = self.model(img[0:batch_size])
            for i in range(batch_size, img.shape[0], batch_size):
                res = torch.cat((res, self.model(img[i:i + batch_size])), 0)

        sr_image = res.permute((0, 2, 3, 1)).clamp_(0, 1).cpu()
        np_sr_image = sr_image.numpy()

        padded_size_scaled = tuple(np.multiply(p_shape[0:2], scale)) + (3,)
        scaled_image_shape = tuple(np.multiply(image_lowres.shape[0:2], scale)) + (3,)
        np_sr_image = stich_together(
            np_sr_image, padded_image_shape=padded_size_scaled,
            target_shape=scaled_image_shape, padding_size=padding * scale
        )

        sr_img = (np_sr_image * 255).astype(np.uint8)
        return [unpad_image(sr_img, pad_size * scale)]
