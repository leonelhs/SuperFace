from abc import ABC

from PySide6.QtCore import Qt

from UI.widgets.GridSliders import GridSliders
from UI.widgets.eraser_box import EraserBox
from UI.widgets.palettecolors import PaletteColors
from toolset.BaseToolset import BaseToolset


class ToolsetFaceDrawer(BaseToolset, ABC):
    def __init__(self, parent):
        super().__init__(parent)
        self.eraserBox = None
        self.slider = None
        self.initTool()
        self.buildPage()

    def name(self):
        return "eraser"

    def initTool(self):
        self.eraserBox = EraserBox()

    def buildPage(self):
        self.addPage("Draw Operations")
        self.addButton("Free erase", self.processFreeErase)
        controls = self.createLayout(GridSliders)
        self.slider = controls.addSlider("Pen width", row=0)
        self.slider.setOnValueChanged(self.onSliderPenWidthChanged)
        self.addButton("Undo erase", self.processUndoErase)
        self.addButton("Erase erase", self.processEraseErase)
        paletteColors = self.createLayout(PaletteColors)
        paletteColors.setOnColorPicked(self.onColorPicked)

    def processFreeErase(self):
        self.parent.twinViewer.left.setEraser(self.eraserBox)

    def processEraseErase(self):
        self.eraserBox.setPencolor(Qt.GlobalColor.transparent)
        self.eraserBox.painter_mode = "line"

    def processUndoErase(self):
        self.eraserBox.undo()

    def onSliderPenWidthChanged(self, radius):
        self.eraserBox.setPenWidth(radius)
        self.slider.value.setText(str(radius))

    def onColorPicked(self, color):
        self.eraserBox.setPencolor(color)

    def onRequestResponse(self, resource, reply):
        pass
