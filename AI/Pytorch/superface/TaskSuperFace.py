#############################################################################
#
#   Source from:
#   https://github.com/TencentARC/GFPGAN
#   Forked from:
#   https://github.com/TencentARC/GFPGAN
#   Reimplemented by: Leonel Hernández
#
##############################################################################
from AI.Pytorch.superface.base_enhancer import Enhancer
from Helpers.TaskPhotoEnhancer import TaskPhotoEnhancer


class TaskSuperFace(TaskPhotoEnhancer):

    def __init__(self, args, restorer: Enhancer):
        super().__init__(args)
        self.restorer = restorer

    def executeEnhanceWork(self, image, progress_callback):
        return self.restorer.enhance(image)
