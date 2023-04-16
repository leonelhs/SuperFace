from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QCursor, QColor, QPainter, QBrush
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem


class EraserBox(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.pixmapItem = None
        self.last_x, self.last_y = None, None
        self.pen_width = 4
        self.painter_mode = "circle"
        self.pen_color = QColor('#000000')
        self.brush = QBrush(Qt.GlobalColor.red, Qt.BrushStyle.CrossPattern)
        self.cursor = QCursor()
        self.initUI()

    def initUI(self):
        self.cursor.setShape(Qt.CursorShape.CrossCursor)
        self.setCursor(self.cursor)
        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)

    def setPixmapItem(self, pixmapItem):
        self.pixmapItem = pixmapItem

    def pixmap(self):
        return self.pixmapItem.pixmap()

    def isInside(self, position):
        if self.boundingRect().contains(position) or self.rect().contains(position):
            return True
        return False

    def hoverMoveEvent(self, event):
        mousePos = self.mapToScene(event.pos())
        if self.isInside(mousePos):
            pass

    def setBasicPen(self, color, width):
        self.setPencolor(color)
        self.setPenWidth(width)

    def setPencolor(self, color):
        self.pen_color = QColor(color)

    def setPenWidth(self, width):
        self.pen_width = width

    def painterMode(self, mode):
        self.painter_mode = mode

    def mouseMoveEvent(self, event):
        mousePos = self.mapToScene(event.pos())
        if self.last_x is None:  # First event.
            if self.isInside(mousePos):
                self.last_x = mousePos.x()
                self.last_y = mousePos.y()
                return  # Ignore the first time.

        canvas = self.pixmap()
        painter = QPainter(canvas)
        pen = painter.pen()
        pen.setWidth(self.pen_width)
        pen.setColor(self.pen_color)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        if self.painter_mode is "line":
            painter.drawLine(self.last_x, self.last_y, mousePos.x(), mousePos.y())
        else:
            painter.drawEllipse(mousePos.x(), mousePos.y(), self.pen_width, self.pen_width)
        painter.end()
        self.pixmapItem.setPixmap(canvas)
        print("drawing")
        # Update the origin for next time.
        self.last_x = mousePos.x()
        self.last_y = mousePos.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None
