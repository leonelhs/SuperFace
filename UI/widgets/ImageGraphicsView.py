from PySide6.QtCore import QMetaObject
from PySide6.QtGui import *
from PySide6.QtWidgets import QGraphicsView


class ImageGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(ImageGraphicsView, self).__init__(parent)
        QMetaObject.connectSlotsByName(self)
        self.__style()

    # FIXME or be sure the last item it's an object of QGraphicsPixmapItem
    def redraw(self):
        last = len(self.items()) - 1
        self.fitInView(self.items()[last], Qt.AspectRatioMode.KeepAspectRatio)

    def resizeEvent(self, event):
        if self.items():
            self.redraw()
        return super().resizeEvent(event)

    def __style(self):
        self.setStyleSheet("QGraphicsView::hover"
                           "{border: 2px solid #6CC417;}")
