import io

import PIL
import PIL.Image
import PIL.ImageQt
import numpy
from PySide6.QtGui import QPixmap


def image_to_bytes(image: PIL.Image) -> bytes:
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    return image_bytes.getvalue()


def pixmap_to_image(pixmap, mode):
    return PIL.ImageQt.fromqpixmap(pixmap).convert(mode)


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
        raise TypeError("Unknown image format!")
