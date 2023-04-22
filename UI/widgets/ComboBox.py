from PySide6.QtWidgets import QComboBox


class ComboBox(QComboBox):
    def __init__(self):
        super().__init__()

    def setOnIndexChanged(self, callback):
        self.currentIndexChanged.connect(callback)
