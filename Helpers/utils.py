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
    image = PIL.Image.open(image_file)
    return image.convert('RGB')


def imageThumbnail(image):
    image.thumbnail((128, 128), PIL.Image.ANTIALIAS)
    return image.tobytes()


def npArray(image):
    return np.array(image)


def unRaw(raw_bytes):
    return pickle.loads(raw_bytes)


