import io
import cv2
import PIL
import PIL.Image
import PIL.ImageQt
import numpy as np
from PySide6.QtGui import QPixmap


def uint8(array):
    return np.uint8(array)


def floodFill(image, position, color):
    cv2.floodFill(image, None, position, color)


def bitWiseAnd(image, mask):
    return cv2.bitwise_and(image, image, mask=mask)


def makeMask(image, color):
    return 255 - cv2.inRange(image, color, color)


def resize(image, size):
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)


def makeImage(array) -> PIL.Image.Image:
    if isinstance(array, bytes):
        return PIL.Image.open(io.BytesIO(array))
    return PIL.Image.fromarray(array)


def image_to_bytes(image: PIL.Image.Image) -> bytes:
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    return image_bytes.getvalue()


def pixmap_to_image(pixmap, mode) -> PIL.Image.Image:
    return PIL.ImageQt.fromqpixmap(pixmap).convert(mode)


def load_pixmap(image) -> QPixmap:
    if isinstance(image, str):
        return PIL.Image.open(image).convert('RGB').toqpixmap()
    if isinstance(image, bytes):
        return PIL.Image.open(io.BytesIO(image)).toqpixmap()
    if isinstance(image, np.ndarray):
        if "int64" in image.dtype.name:
            image = uint8(image)
        return PIL.Image.fromarray(image).toqpixmap()
    if isinstance(image, PIL.Image.Image):
        return image.toqpixmap()
    if isinstance(image, QPixmap):
        return image
    else:
        raise TypeError("Unknown image format!")
