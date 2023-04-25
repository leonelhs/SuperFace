from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSplitter

from UI.widgets.ImageView import ImageView

STYLE_SELECT = "QGraphicsView {border: 2px solid #6CC417; background-color:#fff}"
STYLE_CLEAR = "QGraphicsView {border: 0px}"

STYLE_TRANSPARENT = """
QGraphicsView {
background-image: url(assets/chess.png);
background-repeat: repeat-xy;
}
"""


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
        self.left.setStyle(STYLE_TRANSPARENT)
        self.isCollapsed = False

    def swapImages(self):
        image_left = self.left.pixmap()
        image_right = self.right.pixmap()
        self.left.display(image_right)
        self.right.display(image_left)

    def collapse(self):
        if self.isCollapsed:
            self.right.show()
            self.isCollapsed = False
        else:
            self.right.hide()
            self.isCollapsed = True

    def onClicViewer(self, event, caller):
        pass
