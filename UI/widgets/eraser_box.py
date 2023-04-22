from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QColor, QPainter, QBrush, QPen
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem


# NoPen                    : Qt.PenStyle = ... # 0x0
# SolidLine                : Qt.PenStyle = ... # 0x1
# DashLine                 : Qt.PenStyle = ... # 0x2
# DotLine                  : Qt.PenStyle = ... # 0x3
# DashDotLine              : Qt.PenStyle = ... # 0x4
# DashDotDotLine           : Qt.PenStyle = ... # 0x5
# CustomDashLine           : Qt.PenStyle = ... # 0x6
# MPenStyle                : Qt.PenStyle = ... # 0xf
# pen = QPen(Qt.GlobalColor.black, self.pen_width, Qt.PenStyle.DotLine, Qt.PenCapStyle.RoundCap)

# painter.setBrush(self._brush)

class EraserBox(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.pixmapItem = None
        self.last_x, self.last_y = None, None
        self.pen_width = 4
        self.painter_mode = "circle"
        self.brush = QBrush(Qt.GlobalColor.red, Qt.BrushStyle.CrossPattern)
        self.cursor = QCursor()
        self.history = list()
        self.pen_color = QColor('#0000FF')
        self._pen = QPen(self.pen_color, 1)
        self._brush = QBrush(QColor(self.pen_color.red(), self.pen_color.green(), self.pen_color.blue(), 256))
        self.initUI()

    def initUI(self):
        self.cursor.setShape(Qt.CursorShape.CrossCursor)
        self.setCursor(self.cursor)
        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)

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
        self.pen_color.setAlpha(180)
        # self._brush = QBrush(QColor(self.pen_color.red(), self.pen_color.green(), self.pen_color.blue(), 180))

    def setPenWidth(self, width):
        self.pen_width = width

    def mousePressEvent(self, event):
        self.history.append(self.pixmap())

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
        # painter.setBrush(self._brush)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        if self.painter_mode in "line":
            painter.drawLine(self.last_x, self.last_y, mousePos.x(), mousePos.y())
        else:
            painter.drawEllipse(mousePos.x(), mousePos.y(), self.pen_width, self.pen_width)
        painter.end()
        self.pixmapItem.setPixmap(canvas)
        # Update the origin for next time.
        self.last_x = mousePos.x()
        self.last_y = mousePos.y()

    def mouseReleaseEvent(self, event):
        self.last_x = None
        self.last_y = None

    def undo(self):
        if self.history:
            self.pixmapItem.setPixmap(self.history.pop())
