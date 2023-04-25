import numpy as np
from PySide6.QtCore import Qt

from UI.widgets.Slider import Slider
from UI.widgets.eraser_box import EraserBox
from UI.widgets.palettecolors import PaletteColors
from UI.toolset.Toolset import Toolset


class ToolsetFaceDrawer(Toolset):
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
        controls = self.createLayout(Slider)
        self.slider = controls.build("Pen width", row=0)
        self.slider.setOnValueChanged(self.onSliderPenWidthChanged)
        self.addButton("Undo erase", self.processUndoErase)
        self.addButton("Erase erase", self.processEraseErase)
        paletteColors = self.createLayout(PaletteColors)
        paletteColors.setOnColorPicked(self.onColorPicked)

    def processFreeErase(self):
        self.main_window.twinViewer.left.setEraser(self.eraserBox)

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

    def onImageProcessDone(self, process: str, image: np.ndarray):
        pass
