from PySide6.QtCore import QThreadPool

import utils
from AI.TaskColorize import TaskColorize
from AI.TaskLowLight import TaskLowLight
from AI.TaskSuperFace import TaskSuperFace
from AI.TaskSuperResolution import TaskSuperResolution
from AI.TaskZeroBackground import TaskZeroBackground
from UI.FrameWindow import FrameWindow
from UI.widgets.BoundingBoxRect import BoundingBoxRect


class MainWindow(FrameWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.selection_box = None
        self.taskLowLight = None
        self.taskZeroBackground = None
        self.taskSuperResolution = None
        self.taskSuperFace = None
        self.taskSuperColor = None
        self.threadpool = None
        self.connectProcess()
        self.setupInstances()

    def connectProcess(self):
        self.toolBox.connectLowlight(self.processLowlight)
        self.toolBox.connectCustomBackground(self.setCustomBackground)
        self.toolBox.connectZeroBackground(self.processZeroBackground)
        self.toolBox.connectSuperResolution(self.processSuperResolution)
        self.toolBox.connectHiresScaleChanged(self.onHiresScaleChanged)
        self.toolBox.connectSuperColorize(self.processSuperColorize)
        self.toolBox.connectSuperface(self.processSuperface)

    def setupInstances(self):
        self.threadpool = QThreadPool()
        args = (self.threadpool, self.taskDone, self.taskComplete, self.trackTaskProgress)
        self.taskSuperResolution = TaskSuperResolution(*args)
        self.taskZeroBackground = TaskZeroBackground(*args)
        self.taskLowLight = TaskLowLight(*args)
        self.taskSuperFace = TaskSuperFace(*args)
        self.taskSuperColor = TaskColorize(*args)

    def processSuperResolution(self):
        self.showMessage("Super resolution at: ", self.image_path)
        self.progressBar.show()
        self.taskSuperResolution.startEnhanceThread(self.twinViewer.imageInput())

    def processSuperface(self):
        self.showMessage("Super face at: ", self.image_path)
        self.progressBar.show()
        self.taskSuperFace.startEnhanceThread(self.twinViewer.imageInput())

    def processSuperColorize(self):
        self.showMessage("Super face at: ", self.image_path)
        self.progressBar.show()
        self.taskSuperColor.startEnhanceThread(self.twinViewer.imageInput())

    def onHiresScaleChanged(self, index):
        scales = {0: 2, 1: 4, 2: 8}
        self.taskSuperResolution.loadModel(scales[index])

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
        self.processSuperResolution()

    def onBoundingResizeEvent(self, rect):
        left = int(rect.left())
        top = int(rect.top())
        right = int(rect.right())
        bottom = int(rect.bottom())
        self.selection_box = (left, top, right, bottom)
