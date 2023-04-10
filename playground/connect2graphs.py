########################################
#
# source from:
# https://stackoverflow.com/questions/65831884/how-to-connect-two-qgraphicsitem-by-drawing-line-between-them-using-mouse
#
#
########################################
import sys
from PySide6.QtCore import QRectF, Qt, QPointF, QLineF
from PySide6.QtGui import QPen, QColor, QBrush, QTransform
from PySide6.QtWidgets import QGraphicsItem, QGraphicsView, QGraphicsScene, QApplication


class CustomItem(QGraphicsItem):
    def __init__(self, pointONLeft=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ellipseOnLeft = pointONLeft
        self.point = None
        self.endPoint = None

        self.isStart = None

        self.line = None

        self.setAcceptHoverEvents(True)
        self.setFlag(self.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(self.GraphicsItemFlag.ItemSendsGeometryChanges)

    def addLine(self, line, isPoint):
        if not self.line:
            self.line = line
            self.isStart = isPoint

    def itemChange(self, change, value):

        if change == self.GraphicsItemChange.ItemPositionChange and self.scene():
            self.moveLineToCenter(value)

        return super(CustomItem, self).itemChange(change, value)

    def moveLineToCenter(self, newPos):  # moves line to center of the ellipse

        if self.line:

            if self.ellipseOnLeft:
                xOffset = QRectF(-5, 30, 10, 10).x() + 5
                yOffset = QRectF(-5, 30, 10, 10).y() + 5

            else:
                xOffset = QRectF(95, 30, 10, 10).x() + 5
                yOffset = QRectF(95, 30, 10, 10).y() + 5

            newCenterPos = QPointF(newPos.x() + xOffset, newPos.y() + yOffset)

            p1 = newCenterPos if self.isStart else self.line.line().p1()
            p2 = self.line.line().p2() if self.isStart else newCenterPos

            self.line.setLine(QLineF(p1, p2))

    def containsPoint(self, pos):  # checks whether the mouse is inside the ellipse
        x = self.mapToScene(QRectF(-5, 30, 10, 10).adjusted(-0.5, 0.5, 0.5, 0.5)).containsPoint(pos,
                                                                                                Qt.OddEvenFill) or \
            self.mapToScene(QRectF(95, 30, 10, 10).adjusted(0.5, 0.5, 0.5, 0.5)).containsPoint(pos,
                                                                                               Qt.OddEvenFill)

        return x

    def boundingRect(self):
        return QRectF(-5, 0, 110, 110)

    def paint(self, painter, option, widget):

        pen = QPen(Qt.red)
        pen.setWidth(2)

        painter.setPen(pen)

        painter.setBrush(QBrush(QColor(31, 176, 224)))
        painter.drawRoundedRect(QRectF(0, 0, 100, 100), 4, 4)

        painter.setBrush(QBrush(QColor(214, 13, 36)))

        if self.ellipseOnLeft:  # draws ellipse on left
            painter.drawEllipse(QRectF(-5, 30, 10, 10))

        else:  # draws ellipse on right
            painter.drawEllipse(QRectF(95, 30, 10, 10))


# ------------------------Scene Class ----------------------------------- #
class Scene(QGraphicsScene):
    def __init__(self):
        super(Scene, self).__init__()
        self.startPoint = None
        self.endPoint = None

        self.line = None
        self.graphics_line = None

        self.item1 = None
        self.item2 = None

    def mousePressEvent(self, event):
        self.line = None
        self.graphics_line = None

        self.item1 = None
        self.item2 = None

        self.startPoint = None
        self.endPoint = None

        if self.itemAt(event.scenePos(), QTransform()) and isinstance(self.itemAt(event.scenePos(),
                                                                                  QTransform()),
                                                                      CustomItem):

            self.item1 = self.itemAt(event.scenePos(), QTransform())
            self.checkPoint1(event.scenePos())

            if self.startPoint:
                self.line = QLineF(self.startPoint, self.endPoint)
                self.graphics_line = self.addLine(self.line)

                self.update_path()

        super(Scene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):

        if event.buttons() & Qt.LeftButton and self.startPoint:
            self.endPoint = event.scenePos()
            self.update_path()

        super(Scene, self).mouseMoveEvent(event)

    def filterCollidingItems(self,
                             items):  # filters out all the colliding items and returns only instances of CustomItem
        return [x for x in items if isinstance(x, CustomItem) and x != self.item1]

    def mouseReleaseEvent(self, event):

        if self.graphics_line:

            self.checkPoint2(event.scenePos())
            self.update_path()

            if self.item2 and not self.item1.line and not self.item2.line:
                self.item1.addLine(self.graphics_line, True)
                self.item2.addLine(self.graphics_line, False)

            else:
                if self.graphics_line:
                    self.removeItem(self.graphics_line)

        super(Scene, self).mouseReleaseEvent(event)

    def checkPoint1(self, pos):

        if self.item1.containsPoint(pos):

            self.item1.setFlag(self.item1.GraphicsItemFlag.ItemIsMovable, False)
            self.startPoint = self.endPoint = pos

        else:
            self.item1.setFlag(self.item1.GraphicsItemFlag.ItemIsMovable, True)

    def checkPoint2(self, pos):

        item_lst = self.filterCollidingItems(self.graphics_line.collidingItems())
        contains = False

        if not item_lst:  # checks if there are any items in the list
            return

        for self.item2 in item_lst:
            if self.item2.containsPoint(pos):
                contains = True
                self.endPoint = pos
                break

        if not contains:
            self.item2 = None

    def update_path(self):
        if self.startPoint and self.endPoint:
            self.line.setP2(self.endPoint)
            self.graphics_line.setLine(self.line)


def main():
    app = QApplication(sys.argv)
    scene = Scene()

    item1 = CustomItem(True)
    scene.addItem(item1)

    item2 = CustomItem()
    scene.addItem(item2)

    view = QGraphicsView(scene)
    view.setViewportUpdateMode(view.ViewportUpdateMode.FullViewportUpdate)
    view.setMouseTracking(True)
    view.setFixedSize(1200, 800)
    view.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
