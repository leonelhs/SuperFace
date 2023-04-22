from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton, QGridLayout

COLORS = [
    # 17 undertones https://lospec.com/palette-list/17undertones
    ['#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3'],
    ['#8fd970', '#5ebb49', '#458352', '#dcd37b', '#fffee5'],
    ['#ffd035', '#cc9245', '#a15c3e', '#a42f3b', '#f45b7a'],
    ['#c24998', '#81588d', '#bcb0c2', '#ffffff', '#ffffff']
]


class QPaletteButton(QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QSize(24, 24))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)


class PaletteColors(QGridLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.onColorPiked = None

        for i in range(4):
            for j in range(5):
                color = COLORS[i][j]
                button = QPaletteButton(color)
                button.pressed.connect(lambda c=color: self.onColorPiked(c))
                self.addWidget(button, i, j, 1, 1)

    def setOnColorPicked(self, callback):
        self.onColorPiked = callback
