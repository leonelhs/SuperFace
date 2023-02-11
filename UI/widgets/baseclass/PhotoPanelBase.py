from abc import abstractmethod

from PySide6.QtWidgets import QScrollArea, QWidget

from UI.widgets.Photo import Photo


class PhotoScrollBase(QScrollArea):
    def __init__(self, face, *args):
        QScrollArea.__init__(self, *args)
        self.click = None
        self.doubleClick = None
        self.contextTagEvent = None
        self.contextLandmarksEvent = None
        self.contextNewGalleryEvent = None
        self.setWidgetResizable(True)
        self.scroll_contents = QWidget()
        self.layout = None
        self.initLayout(self.layout)
        self.setWidget(self.scroll_contents)

    @abstractmethod
    def initLayout(self, layout):
        pass

    @abstractmethod
    def clearLayout(self):
        pass

    @abstractmethod
    def appendPhoto(self, face):
        pass

    def setClickEvent(self, callback):
        self.click = callback

    def setDoubleClickEvent(self, callback):
        self.doubleClick = callback

    def setContextTagEvent(self, callback):
        self.contextTagEvent = callback

    def setContextLandmarksEvent(self, callback):
        self.contextLandmarksEvent = callback

    def setContextNewGalleryEvent(self, callback):
        self.contextNewGalleryEvent = callback

    def getWidth(self):
        return self.size().width()

    def newPhoto(self, face):
        photo = Photo(face)
        photo.setClickEvent(self.click)
        photo.setDoubleClickEvent(self.doubleClick)
        return photo

