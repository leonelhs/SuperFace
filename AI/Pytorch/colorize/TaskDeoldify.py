from AI.Pytorch.colorize.deoldify.filters import BaseFilter
from Helpers.TaskPhotoEnhancer import TaskPhotoEnhancer


class TaskImageColorizer(TaskPhotoEnhancer):

    def __init__(self, args):
        super().__init__(args)
        self.colorizer = BaseFilter()
        self.colorizer.model.eval()

    def executeEnhanceWork(self, image, progress_callback):
        return self.colorizer.filter(image)

