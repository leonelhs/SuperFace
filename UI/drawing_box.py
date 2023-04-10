from PySide6.QtCore import QRectF, QSizeF, Qt, QPoint
from PySide6.QtGui import QCursor, QPen, QColor
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsView


class DrawingBox(QGraphicsRectItem):
    def __init__(self, parent=None):
        QGraphicsRectItem.__init__(self, parent)

    def mousePressEvent(self, event):
        mousePos = self.mapToScene(event.pos())
        self.scene().addRect(mousePos.x(), mousePos.y(), 10, 10)
