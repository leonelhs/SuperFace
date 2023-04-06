#############################################################################
#
#   Source from:
#   https://github.com/idealo/image-super-resolution
#   Forked from:
#   Reimplemented by: Leonel Hernández
#
##############################################################################
import PIL.Image
from ISR.models import RDN

from Helpers.TaskPhotoEnhancer import TaskPhotoEnhancer


class TaskHiresTensorflow(TaskPhotoEnhancer):

    def __init__(self, args):
        super().__init__(args)
        self.model = RDN(weights='psnr-small')

    def executeEnhanceWork(self, image, progress_callback):
        result = self.model.predict(image)
        return PIL.Image.fromarray(result)
