import numpy
import PIL.Image
from PySide6.QtCore import QMetaObject, QRect, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsScene

from utils import load_pixmap, pixmap_to_image, image_to_bytes


class BaseGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(BaseGraphicsView, self).__init__(parent)
        self.setEnabled(False)
        self.canvas = None
        self.canvasItem = None
        self.onclick = None
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.pixmapItem = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmapItem)
        self.AspectMode = Qt.AspectRatioMode.KeepAspectRatio
        QMetaObject.connectSlotsByName(self)

    def canvas(self):
        return self.canvasItem.pixmap()

    def enableCanvas(self):
        self.canvas = QPixmap(self.width(), self.height())
        self.canvas.fill(Qt.GlobalColor.transparent)
        self.canvasItem = QGraphicsPixmapItem()
        self.canvasItem.setPixmap(self.canvas)
        self.scene.addItem(self.canvasItem)

    def redraw(self):
        self.fitInView(self.pixmapItem, self.AspectMode)

    def resizeEvent(self, event):
        if self.items():
            self.redraw()

    def rect(self) -> QRect:
        return self.pixmapItem.pixmap().rect()

    def display(self, image: any):
        pixmap = load_pixmap(image)
        self.pixmapItem.setPixmap(pixmap)
        self.setEnabled(True)
        self.redraw()

    def pixmap(self) -> QPixmap:
        return self.pixmapItem.pixmap()

    def image(self, mode="RGB") -> PIL.Image.Image:
        pixmap = self.pixmap()
        if pixmap is not None:
            return pixmap_to_image(pixmap, mode)
        else:
            raise TypeError("No image loaded before")

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

    def filter(self, image_filter, args) -> PIL.Image.Image:
        return self.image().filter(image_filter(*args))
