from PySide6.QtWidgets import QScrollArea, QWidget, QGridLayout

from UI.widgets.Photo import Photo


def grid_positions(length, max_columns):
    return [(row, column) for row in range(length) for column in range(max_columns)]


def get_line(array):
    for i in range(0, len(array), 2):
        yield array[i:i + 2]


class PhotoGrid(QScrollArea):
    def __init__(self, face, *args):
        QScrollArea.__init__(self, *args)
        self.doubleClick = None
        self.click = None
        self.setWidgetResizable(True)
        self.scroll_contents = QWidget()
        self.layout = QGridLayout(self.scroll_contents)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setWidget(self.scroll_contents)
        self.setStyle()

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

    def getWidth(self):
        return self.size().width()

    def newPhoto(self, face):
        photo_layout = Photo(face)
        photo_layout.setClickEvent(self.click)
        photo_layout.setDoubleClickEvent(self.doubleClick)
        return photo_layout

    def clearPhotos(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.layout():
                child.layout().itemAt(0).widget().deleteLater()
                child.layout().itemAt(1).widget().deleteLater()
                child.layout().deleteLater()
