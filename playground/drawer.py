import sys

from PySide6.QtCore import Qt, QRectF, QPoint, QSizeF
from PySide6.QtGui import QPixmap, QPen, QColor, QCursor
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QGraphicsItem, QGraphicsRectItem, \
    QColorDialog


class MuBox(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setRect(QRectF(0.0, 400.0, 400.0, 400.0))

    def initUI(self):
        pen = QPen()
        pen.setStyle(Qt.DashLine)
        pen.setWidth(3)
        pen.setColor()
        self.setPen(pen)
        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)

    def hoverMoveEvent(self, event):
        p = event.pos()
        if self.boundingRect().contains(p) or self.rect().contains(p):
            print("inside")
        return super().hoverMoveEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            mousePos = self.mapToScene(event.pos())
            self.scene().addEllipse(mousePos.x(), mousePos.y(), 20, 20)
        return super().mouseMoveEvent(event)


def add_pixmap(scene_view):
    pixmap = QPixmap("/home/leonel/pretty02.jpg")
    scene_view.addPixmap(pixmap)


app = QApplication(sys.argv)
scene = QGraphicsScene()
dro_win = MuBox()
view = QGraphicsView()
add_pixmap(scene)
scene.addItem(dro_win)
view.setScene(scene)
view.setFixedSize(1200, 800)
color = QColorDialog.getColor()
print(color)
view.show()
sys.exit(app.exec())
