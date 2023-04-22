from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QPushButton
from UI.widgets.left_aligin_button import LeftAlignButton


class MiniForm(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

    def setTitle(self, title):
        super().setTitle(title)

    def addButton(self, title) -> QPushButton:
        button = LeftAlignButton(self)
        button.setText(title)
        self.layout.addWidget(button)
        return button

    def addCheckbox(self, title) -> QCheckBox:
        checkBox = QCheckBox(self)
        checkBox.setText(title)
        self.layout.addWidget(checkBox)
        return checkBox
