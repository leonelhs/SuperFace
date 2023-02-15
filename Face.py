import pickle

import PIL.Image
from PySide6.QtGui import QImage, QPixmap


def unRaw(raw_bytes):
    return pickle.loads(raw_bytes)


def toQPixmap(raw_bytes):
    data = raw_bytes
    image = QImage(data, data.size[0], data.size[1], QImage.Format.Format_RGB888)
    return QPixmap.fromImage(image)


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


def faceBuild(image):
    return Face(
        image_path=None,
        gallery_id=None,
        face_id=None,
        match=None,
        tags=None,
        pixmap=image,
        encodings=None,
        landmarks=None)


class Face:
    def __init__(self, image_path, gallery_id, face_id, match, tags, pixmap, encodings, landmarks):
        self.image_path = image_path
        self.gallery_id = gallery_id
        self.face_id = face_id
        self.match = match
        self.tags = tags
        self.pixmap = pil2pixmap(pixmap)
        self.encodings = encodings
        self.landmarks = landmarks
