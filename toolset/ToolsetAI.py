from AI.Pytorch.TaskEraseScratches import TaskEraseScratches
from AI.Pytorch.TaskMaskScratches import TaskMaskScratches
from AI.TaskColorize import TaskColorize
from AI.TaskFaceMakeup import TaskFaceMakeup
from AI.TaskFaceParser import TaskFaceParser
from AI.TaskLowLight import TaskLowLight
from AI.TaskSuperFace import TaskSuperFace
from AI.TaskSuperResolution import TaskSuperResolution
from AI.TaskZeroBackground import TaskZeroBackground
from AI.Tensorflow.TaskBaldFace import TaskBaldFace
from AI.Tensorflow.TaskDeepLocalFeatures import TaskDeepLocalFeatures
from AI.Tensorflow.TaskEstimatePose import TaskEstimatePose
from AI.Tensorflow.TaskHiresTensorflow import TaskHiresTensorflow
from AI.Tensorflow.TaskInterpolateVectors import TaskInterpolateVectors
from AI.Tensorflow.TaskRetinaFace import TaskRetinaFace
from AI.Tensorflow.TaskSegmentation import TaskSegmentation
from AI.Tensorflow.TaskStyleTransfer import TaskStyleTransfer
from Helpers import utils
from toolset.Toolset import BaseToolset


class ToolsetAI(BaseToolset):
    def __init__(self, parent):
        super().__init__(parent)
        self.taskEraseScratches = None
        self.taskMaskScratches = None
        self.taskEstimatePose = None
        self.taskRetinaFace = None
        self.taskInterpolateVectors = None
        self.taskStyleTransfer = None
        self.taskLowLight = None
        self.taskZeroBackground = None
        self.taskHiresPytorch = None
        self.taskHiresTensorFlow = None
        self.taskSuperFace = None
        self.taskSuperColor = None
        self.taskSegmentation = None
        self.taskBaldFace = None
        self.taskFaceParser = None
        self.taskFaceMakeup = None
        self.taskDelf = None

    def processHiresPytorch(self):
        self.preInit("Hires pytorch at:")
        self.taskHiresPytorch = self.newInstance("hires_torch", TaskSuperResolution)
        self.taskHiresPytorch.startEnhanceThread(self.twinViewer.imageInput())

    def processHiresTensorflow(self):
        self.preInit("Hires tensorflow at: ")
        self.taskHiresTensorFlow = self.newInstance("hires_tensor", TaskHiresTensorflow)
        self.taskHiresPytorch.startEnhanceThread(self.twinViewer.imageInput())

    def processSuperface(self):
        self.preInit("Super face at: ")
        self.taskSuperFace = self.newInstance("superface", TaskSuperFace)
        self.taskSuperFace.startEnhanceThread(self.twinViewer.imageInput())

    def appendStyleImage(self, image_path):
        self.taskStyleTransfer = self.newInstance("style", TaskStyleTransfer)
        self.taskStyleTransfer.style_image = image_path
        image = utils.imageOpen(image_path)
        self.twinViewer.displayOutput(image)

    def processStyleTransfer(self):
        self.preInit("Image style transfer at:")
        self.taskStyleTransfer = self.newInstance("style", TaskStyleTransfer)
        self.taskStyleTransfer.content_image = self.getImagePath()
        self.taskStyleTransfer.startEnhanceThread(None)

    def appendDelfImage(self):
        image_path = self.launchDialogOpenFile()
        if image_path:
            self.preInit("Delf image at: ")
            self.taskDelf.setImageB(image_path)
            image = utils.imageOpen(image_path)
            self.twinViewer.displayOutput(image)

    def processDelf(self):
        self.preInit("Image delf at:")
        self.taskDelf = self.newInstance("delf", TaskDeepLocalFeatures)
        self.taskDelf.setImageA(self.getImagePath())
        self.taskDelf.startEnhanceThread(None)

    def processSuperColorize(self):
        self.preInit("Colorize at:")
        self.taskSuperColor = self.newInstance("color", TaskColorize)
        self.taskSuperColor.startEnhanceThread(self.twinViewer.imageInput())

    def processZeroBackground(self):
        self.preInit("Zero background at:")
        self.taskZeroBackground = self.newInstance("zero", TaskZeroBackground)
        self.taskZeroBackground.startEnhanceThread(self.twinViewer.imageInput())

    def setCustomBackground(self):
        image_path = self.launchDialogOpenFile()
        if image_path:
            background = utils.imageOpen(image_path)
            self.pasteForeground(background)

    def pasteForeground(self, background):
        foreground = self.enhanced_image
        x = (background.size[0] - foreground.size[0]) / 2
        y = (background.size[1] - foreground.size[1]) / 2
        box = (x, y, foreground.size[0] + x, foreground.size[1] + y)
        crop = background.crop(box)
        final_image = crop.copy()
        # put the foreground in the centre of the background
        paste_box = (0, final_image.size[1] - foreground.size[1], final_image.size[0], final_image.size[1])
        final_image.paste(foreground, paste_box, mask=foreground)
        self.twinViewer.displayOutput(final_image)

    def processLowlight(self):
        self.preInit("Light enhancement at:")
        self.taskLowLight = self.newInstance("light", TaskLowLight)
        self.taskLowLight.startEnhanceThread(self.twinViewer.imageInput())

    def processBaldFace(self):
        self.preInit("Bald face image at:")
        self.taskBaldFace = self.newInstance("bald", TaskBaldFace)
        self.taskBaldFace.startEnhanceThread(self.twinViewer.imageInput())

    def processSegmentation(self):
        self.preInit("Segmented image at:")
        self.taskSegmentation = self.newInstance("segment", TaskSegmentation)
        self.taskSegmentation.startEnhanceThread(self.twinViewer.imageInput())

    def processFaceParser(self):
        self.preInit("Parse face image at:")
        self.taskFaceParser = self.newInstance("parser", TaskFaceParser)
        self.taskFaceParser.startEnhanceThread(self.twinViewer.imageInput())

    def processFaceMakeup(self):
        self.preInit("Parse face image at: ")
        self.taskFaceMakeup = self.newInstance("makup", TaskFaceMakeup)
        self.taskFaceMakeup.startEnhanceThread(self.twinViewer.imageInput())

    def processInterpolateVectors(self):
        self.preInit("Interpolate vectors at: ")
        self.taskInterpolateVectors = self.newInstance("interpolate", TaskInterpolateVectors)
        self.taskInterpolateVectors.startEnhanceThread(self.image_path)

    def processRetinaFace(self):
        self.preInit("Draw face landmarks at: ")
        self.taskRetinaFace = self.newInstance("retina", TaskRetinaFace)
        self.taskRetinaFace.startEnhanceThread(self.twinViewer.imageInput())

    def processEstimatePose(self):
        self.preInit("Estimate pose at: ")
        self.taskEstimatePose = self.newInstance("pose", TaskEstimatePose)
        self.taskEstimatePose.startEnhanceThread(self.getImagePath())

    def processMaskScratches(self):
        self.preInit("Building scratches mask at: ")
        self.taskMaskScratches = self.newInstance("mask", TaskMaskScratches)

        def taskMaskDone(image_result):
            self.twinViewer.displayInput(image_result[0])
            self.twinViewer.displayOutput(image_result[1])

        self.taskMaskScratches.enhanceDone = taskMaskDone
        self.taskMaskScratches.startEnhanceThread(self.twinViewer.imageInput())

    def processEraseScratches(self):
        self.preInit("Erasing scratches from mask")
        self.taskEraseScratches = self.newInstance("erase", TaskEraseScratches)
        images = (self.twinViewer.imageInput(), self.twinViewer.imageOutput())
        self.taskEraseScratches.startEnhanceThread(images)

    def onHiresScaleChanged(self, index):
        scales = {0: 2, 1: 4, 2: 8}
        self.taskHiresPytorch.loadModel(scales[index])
