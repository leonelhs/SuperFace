from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSplitter

from UI.widgets.ImageGraphicsView import ImageGraphicsView


class TwinViewer(QSplitter):

    def __init__(self, parent):
        super().__init__(parent)
        self.setOrientation(Qt.Horizontal)
        self.left = ImageGraphicsView(self)
        self.right = ImageGraphicsView(self)
        self.left.setEnabled(False)
        self.right.setEnabled(False)
        self.addWidget(self.left)
        self.addWidget(self.right)
