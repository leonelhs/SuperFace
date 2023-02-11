from abc import ABC

from PySide6.QtWidgets import QHBoxLayout

from UI.widgets.baseclass.PhotoPanelBase import PhotoScrollBase


class PhotoPanel(PhotoScrollBase):

    def initLayout(self, layout):
        self.layout = QHBoxLayout(self.scroll_contents)
        self.layout.setContentsMargins(0, 0, 0, 0)
        pass

    def clearLayout(self):
        pass

    def appendPhoto(self, face):
        photo = self.newPhoto(face)
        self.layout.addLayout(photo)
