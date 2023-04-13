import PIL.Image
import cv2
import numpy as np

from Toolset import Toolset
from UI.drawing_box import DrawingBox
from UI.widgets.BoundingBoxRect import BoundingBoxRect
from remotetasks.tensorflow.tasksegmentation import TaskSegmentation

erase_color = (255, 0, 0)


class ToolsetFast(Toolset):
    def __init__(self, args):
        super().__init__(args)
        self.drawingBox = None
        self.taskSegment = None
        self.overlay = None
        self.colormap = None
        self.history = list()
        self.original = None
        self.initTool()

    def initTool(self):
        args = (self.onRequestResponse, self.onRequestProgress, self.onRequestError)
        self.drawingBox = DrawingBox()
        self.drawingBox.connectMouseClick(self.onRightImageClick)
        self.taskSegment = TaskSegmentation(args)

    def onRightImageClick(self, position):
        self.historyPush()
        cv2.floodFill(self.colormap, None, position, erase_color)
        mask = 255 - cv2.inRange(self.colormap, erase_color, erase_color)
        self.overlay = cv2.bitwise_and(self.overlay, self.overlay, mask=mask)
        self.twinViewer.right.display(self.overlay)

    def processParseFace(self):
        if self.twinViewer.left.isEnabled():
            self.preInit("Parsing face")
            image = self.twinViewer.left.bytes()
            self.original = image[:]
            self.taskSegment.runRemoteTask(image)
        else:
            raise print("No image loaded")

    def processEraseArea(self):
        if self.twinViewer.right.isEnabled():
            self.twinViewer.right.setDrawer(self.drawingBox)
        else:
            raise print("No image loaded")

    def processMakeAlpha(self):
        if self.twinViewer.right.isEnabled():
            self.historyPush()
            image = self.twinViewer.left.imageAlpha()
            size = self.twinViewer.left.size()
            mask = 255 - cv2.inRange(self.colormap, erase_color, erase_color)
            mask = cv2.resize(mask, size, interpolation=cv2.INTER_AREA)
            mask = PIL.Image.fromarray(mask)
            image.putalpha(mask)
            self.twinViewer.left.display(image)

    def processParseReset(self):
        if len(self.history) > 0:
            self.overlay, self.colormap = self.history.pop()
            self.twinViewer.right.display(self.overlay)
            self.twinViewer.left.display(self.original)

    def processMakeSelect(self):
        if self.twinViewer.inputView().isEnabled():
            boundingBox = BoundingBoxRect()
            # boundingBox.setOnBoundingResizeEvent(self.onBoundingResizeEvent)
            self.twinViewer.sceneInput().addItem(boundingBox)

    def historyPush(self):
        self.history.append((self.overlay.copy(), self.colormap.copy()))

    def onRequestResponse(self, reply):
        overlay, colormap, _ = reply
        self.overlay = np.uint8(overlay)
        self.colormap = np.uint8(colormap)
        self.twinViewer.right.display(self.overlay)
        self.progressBar.hide()

    def onRequestProgress(self, sent, total):
        pass

    def onRequestError(self, message, error):
        pass
