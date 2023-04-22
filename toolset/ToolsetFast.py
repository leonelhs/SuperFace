from abc import ABC

from PySide6.QtWidgets import QComboBox

from UI.widgets.BoundingBoxRect import BoundingBoxRect
from UI.widgets.ComboBox import ComboBox
from UI.widgets.drawing_box import DrawingBox
from UI.widgets.eraser_box import EraserBox
from remotetasks.Segementation.tasksegmentation import TaskSegmentation
from toolset.BaseToolset import BaseToolset
from utils import makeMask, resize, makeImage, bitWiseAnd, floodFill

erase_color = (255, 0, 0)


class ToolsetFast(BaseToolset, ABC):
    def __init__(self, parent):
        super().__init__(parent)
        self.eraserBox = None
        self.drawingBox = None
        self.taskSegment = None
        self.overlay = None
        self.colormap = None
        self.initTool()
        self.buildPage()
        self.parseMethod = 0

    def name(self):
        return "fast"

    def buildPage(self):
        self.addPage("Fast Operations")
        parser = self.createWidget(QComboBox)
        parser.addItems(["Parse face", "Parse objects"])

        def onSelectParserChanged(index):
            self.parseMethod = index
            print(self.parseMethod)

        parser.currentIndexChanged.connect(onSelectParserChanged)
        # parser.setOnIndexChanged(onSelectParserChanged)
        self.addButton("Parse image", self.processParseFace)
        self.addButton("Erase area", self.processEraseArea)
        self.addButton("Make alpha", self.processMakeAlpha)
        self.addButton("Undo erase", self.processParseReset)

    def initTool(self):
        self.drawingBox = DrawingBox()
        self.eraserBox = EraserBox()
        self.drawingBox.connectMouseClick(self.onRightImageClick)
        self.taskSegment = TaskSegmentation(self)

    def onRightImageClick(self, position):
        self.historyPush()
        floodFill(self.colormap, position, erase_color)
        partial_mask = makeMask(self.colormap, erase_color)
        self.overlay = bitWiseAnd(self.overlay, partial_mask)
        self.parent.twinViewer.right.display(self.overlay)

    def processParseFace(self):
        self.preInit("Parsing face")
        image = self.parent.twinViewer.left.bytes()
        self.original = image[:]
        if self.parseMethod == 0:
            self.taskSegment.runRemoteTask(image)
        else:
            self.taskSegment.runRemoteTask(image, port="5000")

    def processEraseArea(self):
        self.parent.twinViewer.right.setDrawer(self.drawingBox)

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

    def onRequestResponse(self, resource, reply):
        self.overlay = reply["overlay"]
        self.colormap = reply["colormap"]
        self.parent.twinViewer.right.display(self.overlay)
        self.parent.progressBar.hide()
