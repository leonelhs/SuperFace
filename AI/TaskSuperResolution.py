import os
import sys
import torch
import logging
import numpy as np
from PIL import Image
from RealESRGAN.rrdbnet_arch import RRDBNet
from RealESRGAN.utils import pad_reflect, split_image_into_overlapping_patches, stich_together, unpad_image
from huggingface_hub import hf_hub_url, cached_download

from Tasks.TaskPhotoEnhancer import TaskPhotoEnhancer

HF_MODELS = {
    2: dict(
        repo_id='sberbank-ai/Real-ESRGAN',
        filename='./models/Real-ESRGAN/RealESRGAN_x2.pth',
    ),
    4: dict(
        repo_id='sberbank-ai/Real-ESRGAN',
        filename='./models/Real-ESRGAN/RealESRGAN_x4.pth',
    ),
    8: dict(
        repo_id='sberbank-ai/Real-ESRGAN',
        filename='./models/Real-ESRGAN/RealESRGAN_x8.pth',
    ),
}


class TaskSuperResolution(TaskPhotoEnhancer):

    def __init__(self, threadpool, enhanceDone, enhanceComplete, trackEnhanceProgress):
        super().__init__(threadpool, enhanceDone, enhanceComplete, trackEnhanceProgress)
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
        self.load_weights(HF_MODELS[scale]["filename"], download=False)
        logging.info("Model loaded to scale {0}X".format(self.scale))

    def load_weights(self, model_path, download=True):
        if not os.path.exists(model_path) and download:
            assert self.scale in [2, 4, 8], 'You can download models only with scales: 2, 4, 8'
            config = HF_MODELS[self.scale]
            cache_dir = os.path.dirname(model_path)
            local_filename = os.path.basename(model_path)
            config_file_url = hf_hub_url(repo_id=config['repo_id'], filename=config['filename'])
            cached_download(config_file_url, cache_dir=cache_dir, force_filename=local_filename)
            logging.info("Weights downloaded to: {0}".format(os.path.join(cache_dir, local_filename)))

        loadnet = torch.load(model_path)
        if 'params' in loadnet:
            self.model.load_state_dict(loadnet['params'], strict=True)
        elif 'params_ema' in loadnet:
            self.model.load_state_dict(loadnet['params_ema'], strict=True)
        else:
            self.model.load_state_dict(loadnet, strict=True)
        self.model.eval()
        self.model.to(self.device)

    @torch.cuda.amp.autocast()
    def executeEnhanceWork(self, image_low_res, progress_callback, batch_size=4, patches_size=192,
                           padding=24, pad_size=15):
        scale = self.scale
        device = self.device
        image_low_res = np.array(image_low_res)
        image_low_res = pad_reflect(image_low_res, pad_size)

        patches, p_shape = split_image_into_overlapping_patches(
            image_low_res, patch_size=patches_size, padding_size=padding
        )

        img = torch.FloatTensor(patches / 255).permute((0, 3, 1, 2)).to(device).detach()

        with torch.no_grad():
            res = self.model(img[0:batch_size])
            for i in range(batch_size, img.shape[0], batch_size):
                res = torch.cat((res, self.model(img[i:i + batch_size])), 0)

        sr_image = res.permute((0, 2, 3, 1)).clamp_(0, 1).cpu()
        np_sr_image = sr_image.numpy()

        padded_size_scaled = tuple(np.multiply(p_shape[0:2], scale)) + (3,)
        scaled_image_shape = tuple(np.multiply(image_low_res.shape[0:2], scale)) + (3,)
        np_sr_image = stich_together(
            np_sr_image, padded_image_shape=padded_size_scaled,
            target_shape=scaled_image_shape, padding_size=padding * scale
        )

        sr_img = (np_sr_image * 255).astype(np.uint8)
        sr_img = unpad_image(sr_img, pad_size * scale)
        sr_img = Image.fromarray(sr_img)

        return sr_img
