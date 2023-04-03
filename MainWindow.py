from PySide6.QtCore import QThreadPool

import utils
from AI.TaskColorize import TaskColorize
from AI.TaskFaceMakeup import TaskFaceMakeup
from AI.TaskFaceParser import TaskFaceParser
from AI.TaskLowLight import TaskLowLight
from AI.TaskSuperFace import TaskSuperFace
from AI.TaskSuperResolution import TaskSuperResolution
from AI.TaskZeroBackground import TaskZeroBackground
from AI.Tensorflow.TaskBaldFace import TaskBaldFace
from AI.Tensorflow.TaskHiresTensorflow import TaskHiresTensorflow
from AI.Tensorflow.TaskSegmentation import TaskSegmentation
from AI.Tensorflow.TaskStyleTransfer import TaskStyleTransfer
from UI.widgets.BoundingBoxRect import BoundingBoxRect
from UI.FrameWindow import FrameWindow


class MainWindow(FrameWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
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
        self.selection_box = None

        self.threadpool = None
        self.connectProcess()
        self.setupInstances()

    def connectProcess(self):
        hires_callbacks = [
            self.processHiresPytorch,
            self.processHiresTensorflow,
            self.onHiresScaleChanged]
        self.toolBox.connectSuperResolution(hires_callbacks)
        self.toolBox.connectLowlight(self.processLowlight)
        self.toolBox.connectSuperColorize(self.processSuperColorize)
        self.toolBox.connectSuperface(self.processSuperface)
        self.toolBox.connectZeroBackground(self.processZeroBackground)
        self.toolBox.connectCustomBackground(self.setCustomBackground)
        self.toolBox.connectSegmentation(self.processSegmentation)
        self.toolBox.connectBaldFace(self.processBaldFace)
        self.toolBox.connectFaceParser(self.processFaceParser)
        self.toolBox.connectFaceMakeup(self.processFaceMakeup)
        style_callbacks = [
            self.appendStyleImage,
            self.processStyleTransfer
        ]
        self.toolBox.connectStyleTransfer(style_callbacks)

    def setupInstances(self):
        print("Loading instances")
        self.threadpool = QThreadPool()
        args = (self.threadpool, self.taskDone, self.taskComplete, self.trackTaskProgress)
        self.taskHiresPytorch = TaskSuperResolution(*args)
        self.taskHiresTensorFlow = TaskHiresTensorflow(*args)
        self.taskZeroBackground = TaskZeroBackground(*args)
        self.taskLowLight = TaskLowLight(*args)
        self.taskSuperFace = TaskSuperFace(*args)
        self.taskSuperColor = TaskColorize(*args)
        self.taskSegmentation = TaskSegmentation(*args)
        self.taskBaldFace = TaskBaldFace(*args)
        self.taskFaceParser = TaskFaceParser(*args)
        self.taskFaceMakeup = TaskFaceMakeup(*args)
        self.taskStyleTransfer = TaskStyleTransfer(*args)
        print("Load instances done!")

    def processHiresPytorch(self):
        self.showMessage("Hires pytorch at: ", self.image_path)
        self.progressBar.show()
        self.taskHiresPytorch.startEnhanceThread(self.twinViewer.imageInput())

    def processHiresTensorflow(self):
        self.showMessage("Hires tensorflow at: ", self.image_path)
        self.progressBar.show()
        self.taskHiresPytorch.startEnhanceThread(self.twinViewer.imageInput())

    def processSuperface(self):
        self.showMessage("Super face at: ", self.image_path)
        self.progressBar.show()
        self.taskSuperFace.startEnhanceThread(self.twinViewer.imageInput())

    def appendStyleImage(self):
        image_path = self.launchDialogOpenFile()
        if image_path:
            self.showMessage("Style image at: ", image_path)
            self.taskStyleTransfer.style_image = image_path
            image = utils.imageOpen(image_path)
            self.twinViewer.displayOutput(image)

    def processStyleTransfer(self):
        self.showMessage("Image style transfer at: ", self.image_path)
        self.progressBar.show()
        self.taskStyleTransfer.content_image = self.image_path
        self.taskStyleTransfer.startEnhanceThread(None)

    def processSuperColorize(self):
        self.showMessage("Super face at: ", self.image_path)
        self.progressBar.show()
        self.taskSuperColor.startEnhanceThread(self.twinViewer.imageInput())

    def onHiresScaleChanged(self, index):
        scales = {0: 2, 1: 4, 2: 8}
        self.taskHiresPytorch.loadModel(scales[index])

    def processZeroBackground(self):
        self.showMessage("Zero background at: ", self.image_path)
        self.progressBar.show()
        # self.blurryImage()
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
        self.showMessage("Light enhancement at: ", self.image_path)
        self.progressBar.show()
        self.taskLowLight.startEnhanceThread(self.twinViewer.imageInput())

    def processSegmentation(self):
        self.showMessage("Segmented image at: ", self.image_path)
        self.progressBar.show()
        self.taskSegmentation.startEnhanceThread(self.twinViewer.imageInput())

    def processBaldFace(self):
        self.showMessage("Bald face image at: ", self.image_path)
        self.progressBar.show()
        self.taskBaldFace.startEnhanceThread(self.twinViewer.imageInput())

    def processFaceParser(self):
        self.showMessage("Parse face image at: ", self.image_path)
        self.progressBar.show()
        self.taskFaceParser.startEnhanceThread(self.twinViewer.imageInput())

    def processFaceMakeup(self):
        self.showMessage("Parse face image at: ", self.image_path)
        self.progressBar.show()
        self.taskFaceMakeup.startEnhanceThread(self.twinViewer.imageInput())

    def selectImageArea(self):
        if self.twinViewer.inputView().isEnabled():
            boundingBox = BoundingBoxRect()
            boundingBox.setOnBoundingResizeEvent(self.onBoundingResizeEvent)
            self.twinViewer.sceneInput().addItem(boundingBox)

    def pasteImageArea(self):
        # image = self.readImageFile(self.imagePath())
        image = self.twinViewer.imageOutput()
        box = self.selection_box
        # background = PIL.Image.new('RGB', size=(image.size[0], image.size[1]), color="gray")
        image_crop = image.crop(box)
        # background.paste(image_crop, (box[0], box[1]))
        self.twinViewer.displayOutput(image_crop)
        self.processHiresPytorch()

    def onBoundingResizeEvent(self, rect):
        left = int(rect.left())
        top = int(rect.top())
        right = int(rect.right())
        bottom = int(rect.bottom())
        self.selection_box = (left, top, right, bottom)
