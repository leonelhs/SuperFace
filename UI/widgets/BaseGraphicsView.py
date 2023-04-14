import PIL.Image
import PIL.ImageQt
import numpy
from PySide6.QtCore import QMetaObject, QRect, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsScene

from UI.widgets import load_pixmap, pixmap_to_image, image_to_bytes


class BaseGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(BaseGraphicsView, self).__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.pixmapItem = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmapItem)
        self.AspectMode = Qt.AspectRatioMode.KeepAspectRatio
        QMetaObject.connectSlotsByName(self)
        self.__style()

    def redraw(self):
        self.fitInView(self.pixmapItem, self.AspectMode)

    def resizeEvent(self, event):
        if self.items():
            self.redraw()

    def rect(self) -> QRect:
        return self.pixmapItem.pixmap().rect()

    def display(self, image):
        pixmap = load_pixmap(image)
        self.pixmapItem.setPixmap(pixmap)
        self.setEnabled(True)
        self.redraw()

    def pixmap(self) -> QPixmap:
        return self.pixmapItem.pixmap()

    def image(self, mode="RGB") -> PIL.Image:
        pixmap = self.pixmap()
        return pixmap_to_image(pixmap, mode)

    def ndarray(self) -> numpy.array:
        return numpy.array(self.image())

    def bytes(self) -> bytes:
        return image_to_bytes(self.image())

    def width(self) -> int:
        return self.rect().width()

    def height(self) -> int:
        return self.rect().height()

    def size(self):
        return self.width(), self.height()

    def save(self, path, mode="PNG"):
        self.image().save(path, mode)

    def filter(self, image_filter, args) -> PIL.Image:
        return self.image().filter(image_filter(*args))

    def __style(self):
        self.setStyleSheet("QGraphicsView::hover"
                           "{border: 2px solid #6CC417;}")
