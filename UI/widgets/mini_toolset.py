import qtawesome as qta
from PySide6.QtCore import QSize

from PySide6.QtWidgets import QGroupBox, QGridLayout, QToolButton, QDialogButtonBox, QPushButton

Ok = QDialogButtonBox.StandardButton.Ok
Cancel = QDialogButtonBox.StandardButton.Cancel


class MiniToolset(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

    def setTitle(self, title):
        super().setTitle(title)

    def addButton(self, image_icon, row, column, span=(1, 1), callback=None):
        button = QToolButton(self)
        icon = qta.icon(image_icon)
        button.setIcon(icon)
        button.setIconSize(QSize(30, 30))
        button.clicked.connect(callback)
        self.layout.addWidget(button, row, column, *span)
        return button

    def addDialogButton(self, row, column, span=(1, 1)):
        buttonBox = QDialogButtonBox(self)
        buttonBox.setStandardButtons(Cancel | Ok)
        self.layout.addWidget(buttonBox, row, column, *span)
        return buttonBox

    def addPushButton(self, title, row, column, span=(1, 1), callback=None):
        button = QPushButton(self)
        button.setText(title)
        button.clicked.connect(callback)
        self.layout.addWidget(button, row, column, *span)
        return button
