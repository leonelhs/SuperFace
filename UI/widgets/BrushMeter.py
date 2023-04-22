from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import QLabel


class BrushMeter(QLabel):

    def __init__(self, parent):
        super().__init__(parent)
        pixmap = QPixmap(100, 100)
        pixmap.fill(Qt.GlobalColor.darkBlue)
        self.setPixmap(pixmap)
        self.center = self.rect().center()

    def increase(self, radius):
        canvas = self.pixmap()
        painter = QPainter(canvas)
        pen = painter.pen()
        pen.setWidth(4)
        pen.setColor("#0000FF")
        painter.setPen(pen)
        painter.drawEllipse(50, 50, radius, radius)
        painter.end()
        self.setPixmap(canvas)
