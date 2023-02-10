import pickle

from PySide6.QtGui import QImage, QPixmap


def unRaw(raw_bytes):
    return pickle.loads(raw_bytes)


def toQPixmap(raw_bytes):
    image = QImage(raw_bytes, 128, 128, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(image)


class Face:
    def __init__(self, image_path, gallery_id, face_id, match, tags, pixmap, encodings, landmarks):
        self.image_path = image_path
        self.gallery_id = gallery_id
        self.face_id = face_id
        self.match = match
        self.tags = tags
        self.pixmap = toQPixmap(pixmap)
        self.encodings = unRaw(encodings)
        self.landmarks = unRaw(landmarks)
