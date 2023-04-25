import PIL.Image
import numpy as np

from UI.widgets.drawing_box import DrawingBox
from UI.widgets.eraser_box import EraserBox
from UI.widgets.mini_toolset import MiniToolset
from remotetasks.remote_task import RemoteTask
from UI.toolset import vis_parsing_maps, decode_segmentation_masks
from UI.toolset.Toolset import Toolset
from utils import makeMask, resize, image_from_bytes, bitWiseAnd, floodFill

erase_color = (255, 0, 0)


class ToolsetParser(Toolset):

    def __init__(self, main_window):
        Toolset.__init__(self, main_window)
        self.action_redo = None
        self.action_undo = None
        self.form_parse = None
        self.eraserBox = None
        self.drawingBox = None
        self.overlay = None
        self.colormap = None
        self.history_undo = list()
        self.history_redo = list()
        self.buildPage()
        self.initTool()

    def name(self):
        return "fast"

    def initTool(self):
        self.drawingBox = DrawingBox()
        self.eraserBox = EraserBox()
        self.drawingBox.connectMouseClick(self.onViewImageClick)

    def buildPage(self):
        self.addPage("Image parser")
        self.addButton("Parse all", self.processParseAll)
        self.addButton("Parse face", self.processParseFace)
        form_parse: MiniToolset = self.createWidget(MiniToolset)
        self.action_undo = form_parse.addButton("mdi.undo", 0, 0, callback=self.editionUndo)
        self.action_redo = form_parse.addButton("mdi.redo", 0, 1, callback=self.editionRedo)
        form_parse.addButton("mdi.eraser", 0, 2, callback=self.activeEditMode)
        form_parse.addButton("mdi.brush", 0, 3)
        form_parse.addPushButton("Ok", 1, 0, (1, 2), callback=self.makeAlpha)
        form_parse.addPushButton("Cancel", 1, 2, (1, 2))
        self.form_parse = form_parse
        self.form_parse.hide()

    def processParseAll(self):
        process = self.process("segment_all")
        self.requestImageProcess(process)

    def processParseFace(self):
        process = self.process("segment_face")
        self.requestImageProcess(process)

    def onImageProcessDone(self, process: str, image: np.ndarray):
        self.overlay, self.colormap = self.makeOverlay(image)
        self.viewer().right.display(self.overlay)
        self.viewer().swapImages()
        self.form_parse.show()
        self.main_window.progressBar.hide()

    def onViewImageClick(self, position):
        self.historyPush()
        self.action_undo.setEnabled(True)
        floodFill(self.colormap, position, erase_color)
        partial_mask = makeMask(self.colormap, erase_color)
        self.overlay = bitWiseAnd(self.overlay, partial_mask)
        self.viewer().left.display(self.overlay)

    def activeEditMode(self):
        self.viewer().left.setDrawer(self.drawingBox)

    def makeOverlay(self, reply):
        prediction_mask = np.asarray(reply)
        image = self.viewer().left.image()
        image = image.resize((512, 512), PIL.Image.BILINEAR)
        dark_map, overlay = vis_parsing_maps(image, prediction_mask)
        colormap = decode_segmentation_masks(dark_map)
        return overlay, colormap

    def makeAlpha(self):
        if self.viewer().left.isEnabled():
            self.historyPush()
            image = self.viewer().right.image("RGBA")
            full_mask = makeMask(self.colormap, erase_color)
            full_mask = resize(full_mask, (image.width, image.height))
            full_mask = image_from_bytes(full_mask)
            image.putalpha(full_mask)
            self.viewer().left.display(image)
            self.viewer().left.dropDrawer()
            self.form_parse.hide()

    def editionUndo(self):
        if len(self.history_undo) > 0:
            self.action_redo.setEnabled(True)
            self.overlay, self.colormap = self.history_undo.pop()
            self.history_redo.append([self.overlay, self.colormap].copy())
            self.viewer().left.display(self.overlay)
        else:
            self.action_undo.setEnabled(False)

    def editionRedo(self):
        if len(self.history_redo) > 0:
            images_back = self.history_redo.pop()
            self.overlay, self.colormap = images_back
            self.history_undo.append(images_back.copy())
            self.viewer().left.display(self.overlay)
        else:
            self.action_redo.setEnabled(False)
            self.action_undo.setEnabled(True)

    def historyPush(self):
        self.history_undo.append([self.overlay, self.colormap].copy())
