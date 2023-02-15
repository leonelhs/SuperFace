from PySide6.QtWidgets import QHBoxLayout

from UI.widgets.baseclass.PhotoContainerBase import PhotoContainerBase


def clearWidgets(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


class PhotoPanel(PhotoContainerBase):

    def __init__(self, *args):
        PhotoContainerBase.__init__(self, *args)
        self.photo = None
        self.contextTagEvent = None
        self.contextLandmarksEvent = None
        self.contextNewGalleryEvent = None

    def initLayout(self, layout):
        self.layout = QHBoxLayout(self.scroll_contents)
        self.layout.setContentsMargins(0, 0, 0, 0)
        pass

    def appendPhoto(self, face):
        self.photo = self.newPhoto(face)
        self.clearLayout()
        self.layout.addLayout(self.photo)

    def getPhoto(self):
        return self.photo.getPixmap()

    def newPhoto(self, face):
        photo = super().newPhoto(face)
        photo.setContextTagEvent(self.contextTagEvent)
        photo.setContextLandmarksEvent(self.contextLandmarksEvent)
        photo.setContextNewGalleryEvent(self.contextNewGalleryEvent)
        return photo

    def setContextTagEvent(self, callback):
        self.contextTagEvent = callback

    def setContextLandmarksEvent(self, callback):
        self.contextLandmarksEvent = callback

    def setContextNewGalleryEvent(self, callback):
        self.contextNewGalleryEvent = callback

    def clearLayout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.layout():
                clearWidgets(child.layout())
                child.layout().deleteLater()
