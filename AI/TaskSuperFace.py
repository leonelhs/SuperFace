#############################################################################
#
#   Source from:
#   https://github.com/TencentARC/GFPGAN
#   Forked from:
#   https://github.com/TencentARC/GFPGAN
#   Reimplemented by: Leonel Hernández
#
##############################################################################
import PIL.Image
import numpy as np

from AI.gfpgan.NewGFPGAN import NewGFPGAN
from Helpers.TaskPhotoEnhancer import TaskPhotoEnhancer


class TaskSuperFace(TaskPhotoEnhancer):

    def __init__(self, args):
        super().__init__(args)
        self.model_path = "./models/GFPGAN/GFPGANv1.4.pth"
        self.restorer = self.loadModel()

    def loadModel(self, upscale=2, arch="clean", channel_multiplier=2, bg_upsampler=None):
        return NewGFPGAN(self.model_path, upscale, arch, channel_multiplier, bg_upsampler)

    def executeEnhanceWork(self, image, progress_callback):
        image = np.array(image)
        _, _, restored_img = self.restorer.enhance(
            image,
            has_aligned=False,
            only_center_face=False,
            paste_back=True,
            weight=0.5)

        return PIL.Image.fromarray(restored_img)
