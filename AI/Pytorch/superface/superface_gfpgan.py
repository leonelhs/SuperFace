import PIL.Image
import numpy as np

from AI.Pytorch.superface.base_enhancer import Enhancer
from AI.Pytorch.superface.base_upsampler import Upsampler
from AI.Pytorch.superface.new_gfpgan import NewGFPGAN


class SuperFaceGfpgan(Enhancer):
    def __init__(self, upsampler: Upsampler = None):
        self.model_path = "./models/GFPGAN/GFPGANv1.4.pth"
        self.restorer = NewGFPGAN(self.model_path, bg_upsampler=upsampler)

    def enhance(self, image=None, outscale=None) -> PIL.Image.Image:
        image = np.array(image)
        cropped_faces, restored_faces, restored_img = self.restorer.enhance(image)
        return PIL.Image.fromarray(restored_img)
