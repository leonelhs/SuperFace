import io
import json

import cv2
import PIL
import PIL.Image
import PIL.ImageQt
import numpy as np
from PySide6.QtGui import QPixmap


def read_config():
    data = open('conf.json')
    return json.load(data)


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


def image_to_bytes(image: PIL.Image.Image) -> bytes:
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    return image_bytes.getvalue()


def pixmap_to_image(pixmap, mode) -> PIL.Image.Image:
    return PIL.ImageQt.fromqpixmap(pixmap).convert(mode)


def load_image(image_path: str) -> PIL.Image.Image:
    return PIL.Image.open(image_path)


def image_from_array(image: np.ndarray) -> PIL.Image.Image:
    if "int64" in image.dtype.name:
        image = uint8(image)
    return PIL.Image.fromarray(image)


def image_from_bytes(array) -> PIL.Image.Image:
    if isinstance(array, bytes):
        return PIL.Image.open(io.BytesIO(array))
    return PIL.Image.fromarray(array)


def load_pixmap(image) -> QPixmap:
    if isinstance(image, list):
        image = uint8(image)
    if isinstance(image, str):
        return load_image(image).convert('RGB').toqpixmap()
    if isinstance(image, bytes):
        return PIL.Image.open(io.BytesIO(image)).toqpixmap()
    if isinstance(image, np.ndarray):
        return image_from_array(image).toqpixmap()
    if isinstance(image, PIL.Image.Image):
        return image.toqpixmap()
    if isinstance(image, QPixmap):
        return image
    else:
        raise TypeError("Unknown image format!")
