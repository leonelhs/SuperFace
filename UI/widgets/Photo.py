from PySide6.QtGui import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel


def fit_image(pixmap, size):
    return pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)


class Photo(QVBoxLayout):

    def __init__(self, face, *args):
        QVBoxLayout.__init__(self, *args)
        self.click = None
        self.doubleClick = None
        self.face = face
        self.frame = QLabel()
        self.frame.setAlignment(Qt.AlignCenter)
        self.frame.setPixmap(face.pixmap)
        self.addWidget(self.frame)
        self.label = QLabel()
        self.label.setText("Unknown")
        self.label.setAlignment(Qt.AlignCenter)
        self.addWidget(self.label)
        self.frame.mousePressEvent = self.clickEvent
        self.frame.mouseDoubleClickEvent = self.doubleClickEvent

    def getFrame(self):
        return self.frame

    def getFace(self):
        return self.face

    def getLabel(self):
        return self.label

    def setTag(self, tag):
        self.label.setText(tag)

    def setPixmap(self, pixmap):
        self.face.pixmap = pixmap
        self.frame.setPixmap(self.face.pixmap)

    def getPixmap(self):
        return self.face.pixmap

    def getFilePath(self):
        return self.face.gallery_id

    def getFileName(self):
        return self.face.face_id

    def getEncodings(self):
        return self.face.encodings

    def getLandmarks(self):
        return self.face.landmarks

    def clickEvent(self, event):
        self.click(event, self.face)

    def doubleClickEvent(self, event):
        self.doubleClick(event, self.face)

    def setClickEvent(self, callback):
        self.click = callback

    def setDoubleClickEvent(self, callback):
        self.doubleClick = callback
