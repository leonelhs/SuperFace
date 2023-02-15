from PySide6.QtWidgets import QMenu

from UI.widgets.baseclass.PhotoBase import PhotoBase


class Photo(PhotoBase):

    def __init__(self, face, *args):
        PhotoBase.__init__(self, face, *args)
        self.contextTagEvent = None
        self.contextLandmarksEvent = None
        self.contextNewGalleryEvent = None

    def setContextTagEvent(self, callback):
        self.contextTagEvent = callback

    def setContextLandmarksEvent(self, callback):
        self.contextLandmarksEvent = callback

    def setContextNewGalleryEvent(self, callback):
        self.contextNewGalleryEvent = callback

    def contextMenuEvent(self, event):
        context = QMenu(self.frame)
        tagAction = context.addAction("Tag this person")
        marksAction = context.addAction("Show face landmarks")
        newGalleryAction = context.addAction("Create new gallery")

        action = context.exec_(event.globalPos())
        if action == tagAction:
            self.contextTagEvent(event, self.face)
        elif action == marksAction:
            self.contextLandmarksEvent(event, self.face)
        elif action == newGalleryAction:
            self.contextNewGalleryEvent(event, self.face)
