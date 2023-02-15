from abc import abstractmethod

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel


class PhotoBase(QVBoxLayout):

    def __init__(self, face, *args):
        QVBoxLayout.__init__(self, *args)
        self.face = face
        self.label = None
        self.frame = None
        self.initPhotoView()
        self.click = None
        self.doubleClick = None
        self.frame.mousePressEvent = self.clickEvent
        self.frame.mouseDoubleClickEvent = self.doubleClickEvent
        self.frame.contextMenuEvent = self.contextMenuEvent

    def initPhotoView(self):
        self.frame = QLabel()
        self.frame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame.setPixmap(self.face.pixmap)
        self.addWidget(self.frame)

    def initPhotoTag(self):
        self.label = QLabel()
        self.setTag(self.face.tags)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.label)

    def getFrame(self):
        return self.frame

    def getFace(self):
        return self.face

    def getLabel(self):
        return self.label

    def setTag(self, tag):
        if not tag:
            self.face.tags = "Unknown"
        else:
            self.face.tags = tag
        self.label.setText(self.face.tags)

    def setPixmap(self, pixmap):
        self.frame.setPixmap(pixmap)

    def getPixmap(self):
        return self.face.pixmap

    def getFilePath(self):
        return self.face.image_path

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

    @abstractmethod
    def contextMenuEvent(self, event):
        pass

