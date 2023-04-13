from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QCursor
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem


class DrawingBox(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.cursor = QCursor()
        self.onMouseClick = None
        self.initUI()

    def initUI(self):
        self.cursor.setShape(Qt.CursorShape.PointingHandCursor)
        self.setCursor(self.cursor)
        pen = QPen()
        pen.setStyle(Qt.DashLine)
        pen.setWidth(3)
        self.setPen(pen)
        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)

    def connectMouseClick(self, callback):
        self.onMouseClick = callback

    def setRect(self, rect):
        super().setRect(rect)

    def isInside(self, position):
        if self.boundingRect().contains(position) or self.rect().contains(position):
            return True
        return False

    def hoverMoveEvent(self, event):
        mousePos = self.mapToScene(event.pos())
        if self.isInside(mousePos):
            pass

    def mousePressEvent(self, event):
        mousePos = self.mapToScene(event.pos())
        if self.isInside(mousePos):
            self.onMouseClick((int(mousePos.x()), int(mousePos.y())))

    # def mouseMoveEvent(self, event):
    #     if event.buttons() == Qt.MouseButton.LeftButton:
    #         mousePos = self.mapToScene(event.pos())
    #         if self.isInside(mousePos):
    #             self.scene().addEllipse(mousePos.x(), mousePos.y(), 20, 20)
