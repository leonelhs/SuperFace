import io

import PIL.Image
import numpy as np
from PySide6.QtGui import QPixmap


def uint8(array):
    return np.uint8(array)


def load_pixmap(image) -> QPixmap:
    print("Image type is %s" % type(image))
    if isinstance(image, str):
        return PIL.Image.open(image).convert('RGB').toqpixmap()
    if isinstance(image, bytes):
        return PIL.Image.open(io.BytesIO(image)).toqpixmap()
    if isinstance(image, np.ndarray):
        print("Image ndarray is %s " % image.dtype.name)
        if "int64" in image.dtype.name:
            image = uint8(image)
        return PIL.Image.fromarray(image).toqpixmap()
    if isinstance(image, PIL.Image.Image):
        return image.toqpixmap()
    if isinstance(image, QPixmap):
        return image
    else:
        raise TypeError("Unknown image format!")
