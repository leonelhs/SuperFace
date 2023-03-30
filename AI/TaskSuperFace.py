import PIL.Image
import numpy as np
from gfpgan import GFPGANer

from Tasks.TaskPhotoEnhancer import TaskPhotoEnhancer


class TaskSuperFace(TaskPhotoEnhancer):

    def __init__(self, threadpool, enhanceDone, enhanceComplete, trackEnhanceProgress):
        super().__init__(threadpool, enhanceDone, enhanceComplete, trackEnhanceProgress)
        self.model_path = "./models/GFPGANv1.4.pth"
        self.restorer = self.loadModel()

    def loadModel(self, upscale=2, arch="clean", channel_multiplier=2, bg_upsampler=None):
        return GFPGANer(self.model_path, upscale, arch, channel_multiplier, bg_upsampler)

    def executeEnhanceWork(self, image, progress_callback):
        image = np.array(image)
        _, _, restored_img = self.restorer.enhance(
            image,
            has_aligned=False,
            only_center_face=False,
            paste_back=True,
            weight=0.5)

        return PIL.Image.fromarray(restored_img)
