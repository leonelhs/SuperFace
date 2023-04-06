from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QSlider


def setInterval(slider, scale, data_min, data_max):
    slider.setMinimum(data_min * scale)
    slider.setMaximum(data_max * scale)
    slider.setTickInterval((data_max - data_min) / 10 * scale)


class GridSliders(QGridLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def addSlider(self, title, row, callback=None):
        label = QLabel(self.parent)
        label.setText(title)
        self.addWidget(label, row, 0, 1, 1)
        slider = QSlider(self.parent)
        slider.setOrientation(Qt.Horizontal)
        self.addWidget(slider, row, 1, 1, 1)
        setInterval(slider, scale=1, data_min=1, data_max=100)
        slider.valueChanged.connect(callback)
