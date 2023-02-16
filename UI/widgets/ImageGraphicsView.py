from PySide6 import Qt
from PySide6.QtCore import QMetaObject
from PySide6.QtGui import *
from PySide6.QtWidgets import QGraphicsView


class ImageGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(ImageGraphicsView, self).__init__(parent)
        QMetaObject.connectSlotsByName(self)

    def resizeEvent(self, event):
        if self.items():
            self.fitInView(self.items()[0], Qt.AspectRatioMode.KeepAspectRatio)
        return super().resizeEvent(event)
