import io
import PIL.Image
import PIL.ImageQt
import numpy
import numpy as np
from PySide6.QtCore import QMetaObject, QRect, Qt, QByteArray, QBuffer, QIODevice
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsScene

from UI.drawing_box import DrawingBox


def image_to_bytes(image: PIL.Image) -> bytes:
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")
    return image_bytes.getvalue()


def load_pixmap(image) -> QPixmap:
    if isinstance(image, str):
        return PIL.Image.open(image).convert('RGB').toqpixmap()
    if isinstance(image, bytes):
        return PIL.Image.open(io.BytesIO(image)).toqpixmap()
    if isinstance(image, numpy.ndarray):
        return PIL.Image.fromarray(image).toqpixmap()
    if isinstance(image, PIL.Image.Image):
        return image.toqpixmap()
    if isinstance(image, QPixmap):
        return image
    else:
        raise print("Unknown image format!")


class ImageGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(ImageGraphicsView, self).__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.pixmapItem = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmapItem)
        self.AspectMode = Qt.AspectRatioMode.KeepAspectRatio
        self.drawer = None
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

    def image(self) -> PIL.Image:
        pixmap = self.pixmap()
        return PIL.ImageQt.fromqpixmap(pixmap)

    def imageAlpha(self) -> PIL.Image:
        return self.image().convert('RGBA')

    def ndarray(self) -> np.array:
        return np.array(self.image())

    def bytes(self) -> bytes:
        return image_to_bytes(self.image())

    def width(self) -> int:
        return self.rect().width()

    def height(self) -> int:
        return self.rect().height()

    def size(self):
        return self.width(), self.height()

    def save(self, path):
        self.image().save(path, "PNG")

    def filter(self, image_filter, args) -> PIL.Image:
        return self.image().filter(image_filter(*args))

    def setDrawer(self, drawer: DrawingBox):
        self.drawer = drawer
        self.drawer.setRect(self.rect())
        self.scene.addItem(self.drawer)

    def __style(self):
        self.setStyleSheet("QGraphicsView::hover"
                           "{border: 2px solid #6CC417;}")
