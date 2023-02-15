import os
import pickle

import PIL.Image
import numpy as np
from PySide6.QtGui import QImage, QPixmap


def serialize(data):
    return pickle.dumps(data, protocol=5)


def getPath(folder_path, file):
    return os.path.join(folder_path, file)


def rawToQPixmap(raw_bytes):
    image = QImage(raw_bytes, 128, 128, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(image)


def imageOpen(image_file):
    image_file = os.path.join(image_file)
    image = PIL.Image.open(image_file)
    return image.convert('RGB')


def imageThumbnail(image):
    image.thumbnail((128, 128), PIL.Image.ANTIALIAS)
    return image.tobytes()


def npArray(image):
    return np.array(image)


def pil2pixmap(image):
    if image.mode == "RGB":
        r, g, b = image.split()
        image = PIL.Image.merge("RGB", (b, g, r))
    elif image.mode == "RGBA":
        r, g, b, a = image.split()
        image = PIL.Image.merge("RGBA", (b, g, r, a))
    elif image.mode == "L":
        image = image.convert("RGBA")
    # Bild in RGBA konvertieren, falls nicht bereits passiert
    im2 = image.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qim = QImage(data, image.size[0], image.size[1], QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(qim)
    return pixmap
