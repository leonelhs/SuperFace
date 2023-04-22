from PySide6.QtWidgets import QPushButton


class LeftAlignButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("Text-align:left; padding:8px")
