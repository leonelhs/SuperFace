from AI.Pytorch.superface.base_upsampler import Upsampler
from Helpers.TaskPhotoEnhancer import TaskPhotoEnhancer


class TaskSuperResolution(TaskPhotoEnhancer):

    def __init__(self, args, upsampler: Upsampler):
        super().__init__(args)
        self.upsampler = upsampler

    def executeEnhanceWork(self, image_lowres, progress_callback):
        return self.upsampler.enhance(image_lowres)[0]
