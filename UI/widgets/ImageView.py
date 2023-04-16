from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem

from UI.widgets.drawing_box import DrawingBox
from UI.widgets.BaseGraphicsView import BaseGraphicsView
from UI.widgets.eraser_box import EraserBox


class ImageView(BaseGraphicsView):
    def __init__(self, parent=None):
        super(ImageView, self).__init__(parent)
        self.drawer = None
        self.eraser = None

    def setDrawer(self, drawer: DrawingBox):
        if self.drawer is None:
            if self.isEnabled():
                self.drawer = drawer
                self.drawer.setRect(self.rect())
                self.scene.addItem(self.drawer)
            else:
                raise TypeError("Image displayed is needed")

    def dropDrawer(self):
        if self.drawer is not None:
            self.scene.removeItem(self.drawer)
            self.drawer = None

    def setEraser(self, eraser: EraserBox):
        if self.eraser is None:
            if self.isEnabled():
                self.eraser = eraser
                self.enableCanvas()
                self.eraser.setPixmapItem(self.canvasItem)
                self.eraser.setRect(self.rect())
                self.scene.addItem(self.eraser)
            else:
                raise TypeError("Image displayed is needed")

    def dropEraser(self):
        if self.eraser is not None:
            self.scene.removeItem(self.eraser)
            self.eraser = None
