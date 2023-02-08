from PySide6.QtCore import QRect
from PySide6.QtGui import Qt, QPixmap, QImage
from PySide6.QtWidgets import QScrollArea, QWidget, QGridLayout

from photo_widget import PhotoWidget


def pixmap_from_file(path):
    return QPixmap.fromImage(QImage(path))


class PhotoGrid:
    def __init__(self, splitter):
        self.click = None
        self.scroller = QScrollArea(splitter)
        # self.scroller.setStyleSheet(u"background-color: rgb(255, 255, 255)")
        self.scroller.setWidgetResizable(True)

        self.scroll_contents = QWidget()
        self.scroll_contents.setGeometry(QRect(0, 0, 383, 479))

        self.layout = QGridLayout(self.scroll_contents)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.scroller.setWidget(self.scroll_contents)
        splitter.addWidget(self.scroller)

    def appendThumbnail(self, face, position=(0, 0)):
        small_photo = self.newPhoto(face)
        self.layout.addLayout(small_photo, position[0], position[1])

    def appendPhoto(self, face, position=(0, 0)):
        big_photo = self.newPhoto(face)
        pixmap = pixmap_from_file(face["path"])
        big_photo.setPixmap(pixmap)
        self.layout.addLayout(big_photo, position[0], position[1])

    def photoAtPosition(self, row=0, column=0):
        return self.layout.itemAtPosition(row, column)

    def setClickEvent(self, callback):
        self.click = callback

    def getWidth(self):
        return self.scroller.size().width()

    def newPhoto(self, face):
        photo_layout = PhotoWidget(face)
        photo_layout.setClickEvent(self.click)
        return photo_layout

    def clearPhotos(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.layout():
                child.layout().itemAt(0).widget().deleteLater()
                child.layout().itemAt(1).widget().deleteLater()
                child.layout().deleteLater()
