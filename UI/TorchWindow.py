import logging

from PySide6.QtCore import QThreadPool

# from AI.Pytorch.TaskEraseScratches import TaskEraseScratches
# from AI.Pytorch.TaskMaskScratches import TaskMaskScratches
# from AI.TaskColorize import TaskColorize
# from AI.TaskFaceMakeup import TaskFaceMakeup
# from AI.TaskFaceParser import TaskFaceParser
from AI.Pytorch.task_low_light import TaskLowLight
# from AI.Pytorch.superface.TaskSuperFace import TaskSuperFace
# from AI.Pytorch.superface.TaskSuperResolution import TaskSuperResolution
# from AI.Pytorch.superface.superface_gfpgan import SuperFaceGfpgan
# from AI.Pytorch.superface.upsampler_real_esrgan import RealEsrganUpsampler
from AI.Pytorch.TaskZeroBackground import TaskZeroBackground
# from AI.Pytorch.colorize.TaskDeoldify import TaskImageColorizer
from Helpers import utils
from UI.FrameWindow import FrameWindow


class TorchWindow(FrameWindow):

    def __init__(self, parent=None):
        super(TorchWindow, self).__init__(parent)
        self.background = None
        self.taskFaceMakeup = None
        self.taskEraseScratches = None
        self.taskMaskScratches = None
        self.taskFaceParser = None
        self.taskLowLight = None
        self.taskZeroBackground = None
        self.taskSuperColor = None
        self.taskSuperFace = None
        self.taskSuperResolution = None
        self.taskImageColorizer = None
        self.threadpool = QThreadPool()
        self.args = (self.threadpool, self.taskDone, self.taskComplete, self.trackTaskProgress)
        self.menubar.actionTest1(self.processZeroBackground)
        self.menubar.actionTest2(self.setCustomBackground)

    def preInit(self, message):
        self.progressBar.show()
        print(message)

    def processSuperResolution(self):
        self.preInit("Hires pytorch at:")
        self.taskSuperResolution = TaskSuperResolution(self.args)
        self.taskSuperResolution.startEnhanceThread(self.twinViewer.left.image())

    def processSuperface(self):
        self.preInit("Super face at: ")
        upsampler = RealEsrganUpsampler()
        restorer = SuperFaceGfpgan(upsampler)
        self.taskSuperFace = TaskSuperFace(self.args, restorer)
        self.taskSuperFace.startEnhanceThread(self.twinViewer.left.image())

    def processSuperColorize(self):
        self.preInit("Colorize at:")
        self.taskSuperColor = TaskColorize(self.args)
        self.taskSuperColor.startEnhanceThread(self.twinViewer.left.image())

    def processDeOldify(self):
        self.preInit("DeOldify at")
        self.taskImageColorizer = TaskImageColorizer(self.args)
        self.taskSuperColor.startEnhanceThread(self.twinViewer.left.image())

    def processZeroBackground(self):
        self.preInit("Zero background at:")
        self.taskZeroBackground = TaskZeroBackground(self.args)
        self.taskZeroBackground.startEnhanceThread(self.twinViewer.left.image())

    def setCustomBackground(self):
        image_path = self.launchDialogOpenFile()
        if image_path:
            background = utils.imageOpen(image_path)
            self.pasteForeground(background)

    def pasteForeground(self, background):
        foreground = self.twinViewer.right.image("RGBA")
        x = (background.size[0] - foreground.size[0]) / 2
        y = (background.size[1] - foreground.size[1]) / 2
        box = (x, y, foreground.size[0] + x, foreground.size[1] + y)
        crop = background.crop(box)
        final_image = crop.copy()
        # put the foreground in the centre of the background
        paste_box = (0, final_image.size[1] - foreground.size[1], final_image.size[0], final_image.size[1])
        final_image.paste(foreground, paste_box, mask=foreground)
        self.twinViewer.left.display(final_image)

    def processLowlight(self):
        self.preInit("Light enhancement at:")
        self.taskLowLight = TaskLowLight(self.args)
        self.taskLowLight.startEnhanceThread(self.twinViewer.left.image())

    def processFaceParser(self):
        self.preInit("Parse face image at:")
        self.taskFaceParser = TaskFaceParser(self.args)
        self.taskFaceParser.startEnhanceThread(self.twinViewer.left.image())

    def processFaceMakeup(self):
        self.preInit("Parse face image at: ")
        self.taskFaceMakeup = TaskFaceMakeup(self.args)
        self.taskFaceMakeup.startEnhanceThread(self.twinViewer.left.image())

    def processMaskScratches(self):
        self.preInit("Building scratches mask at: ")
        self.taskMaskScratches = TaskMaskScratches(self.args)

        def taskMaskDone(image_result):
            self.twinViewer.left.display(image_result[0])
            self.twinViewer.right.display(image_result[1])

        self.taskMaskScratches.enhanceDone = taskMaskDone
        self.taskMaskScratches.startEnhanceThread(self.twinViewer.left.image())

    def processEraseScratches(self):
        self.preInit("Erasing scratches from mask")
        self.taskEraseScratches = TaskEraseScratches(self.args)
        images = (self.twinViewer.left.image(), self.twinViewer.right.image())
        self.taskEraseScratches.startEnhanceThread(images)

    def onHiresScaleChanged(self, index):
        scales = {0: 2, 1: 4, 2: 8}
        self.taskSuperResolution.loadModel(scales[index])

    def taskDone(self, image_result):
        self.twinViewer.right.display(image_result)

    def trackTaskProgress(self, progress):
        self.showMessage("progress", progress)

    def taskComplete(self):
        print("Test done.")
        self.progressBar.hide()
