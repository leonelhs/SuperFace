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
        self.addPage("bald", u"Bald Face")
        self.addPage("parser", u"Parse Face")
        self.addPage("makeup", u"Makeup Face")
        self.addPage("style", u"Style transfer")
        self.setCurrentIndex(0)

    def connectSuperface(self, callback):
        self.addButton("face", "Restore faces", callback)

    def connectSuperColorize(self, callback):
        self.addButton("color", "Colorize", callback)

    def connectSuperResolution(self, callbacks):
        scale = self.createWidget("hires", QComboBox)
        scale.addItems(["Scale 2X", "Scale 4X", "Scale 8X"])
        self.addButton("hires", "Pytorch code", callbacks[0])
        self.addButton("hires", "Tensorflow code", callbacks[1])
        scale.currentIndexChanged.connect(callbacks[2])

    def connectZeroBackground(self, callback):
        self.addButton("zero", "Remove background", callback)

    def connectCustomBackground(self, callback):
        self.addButton("zero", "Custom background", callback)

    def connectSegmentation(self, callback):
        self.addButton("zero", "Segment image", callback)

    def connectLowlight(self, callback):
        self.addButton("light", "Shine picture", callback)

    def connectBaldFace(self, callback):
        self.addButton("bald", " Bald face", callback)

    def connectFaceParser(self, callback):
        self.addButton("parser", " Parse face", callback)

    def connectFaceMakeup(self, callback):
        self.addButton("makeup", " Makeup face", callback)

    def connectStyleTransfer(self, callbacks):
        self.addButton("style", "Set style image", callbacks[0])
        self.addButton("style", "Transfer style", callbacks[1])




