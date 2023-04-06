import logging
from PIL import ImageFilter
from PySide6.QtCore import QThreadPool
from ToolsetAI import ToolsetAI
from ToolsetFilters import ToolsetFilters
from UI.FrameWindow import FrameWindow
from UI.widgets.BoundingBoxRect import BoundingBoxRect

debug = True


class MainWindow(FrameWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.toolset_ai = None
        self.toolset_filters = None
        self.selection_box = None
        self.threadpool = None
        self.setupInstances()

    def setupInstances(self):
        logging.info("Loading instances")
        self.threadpool = QThreadPool()
        args = (self.threadpool, self.taskDone, self.taskComplete, self.trackTaskProgress)
        controls = (self.progressBar, self.showMessage, self.twinViewer, self.getImagePath)
        self.toolset_ai = ToolsetAI(args)
        self.toolset_filters = ToolsetFilters(args)
        self.toolset_ai.setControls(controls)
        self.toolset_filters.setControls(controls)
        self.toolBox.toolset_ai = self.toolset_ai
        self.toolBox.toolset_filters = self.toolset_filters
        self.toolBox.buildPages()

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

    def getImagePath(self):
        return self.image_path

