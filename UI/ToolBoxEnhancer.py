from PySide6.QtWidgets import QComboBox

from UI.widgets.ToolBoxMaker import ToolBoxMaker


class ToolBoxEnhancer(ToolBoxMaker):

    def __init__(self, parent):
        super().__init__(parent)
        self.addPage("face", u"Super Face")
        self.addPage("color", u"Super Colorize")
        self.addPage("hires", u"Super Resolution")
        self.addPage("zero", u"Zero Background")
        self.addPage("light", u"Light Enhancement")
        self.setCurrentIndex(0)

    def connectSuperface(self, callback):
        self.addButton("face", "Restore faces", callback)

    def connectSuperColorize(self, callback):
        self.addButton("color", "Colorize", callback)

    def connectHiresScaleChanged(self, callback):
        scale = self.createWidget("hires", QComboBox)
        scale.addItems(["Scale 2X", "Scale 4X", "Scale 8X"])
        scale.currentIndexChanged.connect(callback)

    def connectSuperResolution(self, callback):
        self.addButton("hires", "Scale image", callback)

    def connectZeroBackground(self, callback):
        self.addButton("zero", "Remove background", callback)

    def connectCustomBackground(self, callback):
        self.addButton("zero", "Custom background", callback)

    def connectLowlight(self, callback):
        self.addButton("light", "Shine picture", callback)





