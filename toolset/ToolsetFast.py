from abc import ABC

from toolset.Toolset import Toolset
from UI.widgets.BoundingBoxRect import BoundingBoxRect
from UI.widgets.drawing_box import DrawingBox
from remotetasks.tensorflow.tasksegmentation import TaskSegmentation
from toolset import makeMask, resize, makeImage, bitWiseAnd, floodFill, ndArray

erase_color = (255, 0, 0)


class ToolsetFast(Toolset, ABC):
    def __init__(self, parent):
        super().__init__(parent)
        self.drawingBox = None
        self.taskSegment = None
        self.overlay = None
        self.colormap = None
        self.initTool()
        self.buildPage()

    def name(self):
        return "fast"

    def buildPage(self):
        self.addPage("Fast Operations")
        self.addButton("Parse face", self.processParseFace)
        self.addButton("Erase area", self.processEraseArea)
        self.addButton("Make alpha", self.processMakeAlpha)
        self.addButton("Undo erase", self.processParseReset)

    def initTool(self):
        args = (self.onRequestResponse, self.onRequestProgress, self.onRequestError)
        self.drawingBox = DrawingBox()
        self.drawingBox.connectMouseClick(self.onRightImageClick)
        self.taskSegment = TaskSegmentation(args)

    def onRightImageClick(self, position):
        self.historyPush()
        floodFill(self.colormap, position, erase_color)
        partial_mask = makeMask(self.colormap, erase_color)
        self.overlay = bitWiseAnd(self.overlay, partial_mask)
        self.parent.twinViewer.right.display(self.overlay)

    def processParseFace(self):
        if self.parent.twinViewer.left.isEnabled():
            self.preInit("Parsing face")
            image = self.parent.twinViewer.left.bytes()
            self.original = image[:]
            self.taskSegment.runRemoteTask(image)
        else:
            raise TypeError("No image loaded")

    def processEraseArea(self):
        if self.parent.twinViewer.right.isEnabled():
            self.parent.twinViewer.right.setDrawer(self.drawingBox)
        else:
            raise TypeError("No image loaded")

    def processMakeAlpha(self):
        if self.parent.twinViewer.right.isEnabled():
            self.historyPush()
            image = self.parent.twinViewer.left.image("RGBA")
            full_mask = makeMask(self.colormap, erase_color)
            full_mask = resize(full_mask, (image.width, image.height))
            full_mask = makeImage(full_mask)
            image.putalpha(full_mask)
            self.parent.twinViewer.left.display(image)
            self.parent.twinViewer.right.dropDrawer()

    def processParseReset(self):
        if self.historyBack():
            self.overlay, self.colormap = self.history.pop()
            self.parent.twinViewer.right.display(self.overlay)
            self.parent.twinViewer.left.display(self.original)

    def processMakeSelect(self):
        if self.parent.twinViewer.inputView().isEnabled():
            boundingBox = BoundingBoxRect()
            # boundingBox.setOnBoundingResizeEvent(self.onBoundingResizeEvent)
            self.parent.twinViewer.sceneInput().addItem(boundingBox)

    def historyPush(self):
        self.history.append((self.overlay.copy(), self.colormap.copy()))

    def onRequestResponse(self, reply):
        overlay, colormap, _ = reply
        self.overlay = ndArray(overlay)
        self.colormap = ndArray(colormap)
        self.parent.twinViewer.right.display(self.overlay)
        self.parent.progressBar.hide()

    def onRequestProgress(self, sent, total):
        pass

    def onRequestError(self, message, error):
        pass
