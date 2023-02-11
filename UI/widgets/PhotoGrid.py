from PySide6.QtWidgets import QScrollArea, QWidget, QGridLayout

from UI.widgets.Photo import Photo


def grid_positions(length, max_columns):
    return [(row, column) for row in range(length) for column in range(max_columns)]


class PhotoGrid(QScrollArea):
    def __init__(self, face, *args):
        QScrollArea.__init__(self, *args)
        self.click = None
        self.doubleClick = None
        self.contextTagEvent = None
        self.contextLandmarksEvent = None
        self.contextNewGalleryEvent = None
        self.setWidgetResizable(True)
        self.scroll_contents = QWidget()
        self.layout = QGridLayout(self.scroll_contents)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setWidget(self.scroll_contents)

    def setStyle(self, style=""):
        self.setStyleSheet(u"background-color: rgb(255, 255, 255)")

    def appendThumbnail(self, face, position=(0, 0)):
        photo = self.newPhoto(face)
        self.layout.addLayout(photo, position[0], position[1])

    def populate_grid(self, thumbnails, max_columns=5):
        self.clearPhotos()
        positions = grid_positions(len(thumbnails), max_columns)
        for position, thumbnail in zip(positions, thumbnails):
            self.appendThumbnail(thumbnail, position)

    def photoAtPosition(self, row=0, column=0):
        return self.layout.itemAtPosition(row, column)

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
        photo.setContextTagEvent(self.contextTagEvent)
        photo.setContextLandmarksEvent(self.contextLandmarksEvent)
        photo.setContextNewGalleryEvent(self.contextNewGalleryEvent)
        return photo

    def clearPhotos(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.layout():
                child.layout().itemAt(0).widget().deleteLater()
                child.layout().itemAt(1).widget().deleteLater()
                child.layout().deleteLater()
