from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSplitter

from UI.widgets.ImageView import ImageView

STYLE_SELECT = "QGraphicsView {border: 2px solid #6CC417;}"
STYLE_CLEAR = "QGraphicsView {border: 0px}"


class TwinViewer(QSplitter):

    def __init__(self, parent):
        super().__init__(parent)
        self.setOrientation(Qt.Horizontal)
        self.left = ImageView(self)
        self.right = ImageView(self)
        self.left.setOnclickView(self.onClicViewer)
        self.right.setOnclickView(self.onClicViewer)
        self.left.setObjectName("left")
        self.right.setObjectName("right")
        self.addWidget(self.left)
        self.addWidget(self.right)
        self.left.setStyle(STYLE_SELECT)
        self.active = self.left

    def swapImages(self):
        image_left = self.left.pixmap()
        image_right = self.right.pixmap()
        self.left.display(image_right)
        self.right.display(image_left)

    def setStyle(self, style):
        self.setStyleSheet()

    def onClicViewer(self, event, caller):
        if caller == "right":
            self.right.setStyle(STYLE_SELECT)
            self.left.setStyle(STYLE_CLEAR)
            self.active = self.right
        else:
            self.right.setStyle(STYLE_CLEAR)
            self.left.setStyle(STYLE_SELECT)
            self.active = self.left
