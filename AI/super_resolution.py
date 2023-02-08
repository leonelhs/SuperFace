import os
import torch
from PIL import Image
from RealESRGAN import RealESRGAN


def super_resolution(path_to_image):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = RealESRGAN(device, scale=4)
    model.load_weights('../models/Real-ESRGAN/RealESRGAN_x4.pth', download=False)
    image = Image.open(path_to_image).convert('RGB')
    super_image = model.predict(image)
    save_image_to = os.path.splitext(path_to_image)[0] + '-super.png'
    super_image.save(save_image_to)
    return save_image_to
