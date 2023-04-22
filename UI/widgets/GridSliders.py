from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QSlider


def setInterval(slider, scale, data_min, data_max):
    slider.setMinimum(data_min * scale)
    slider.setMaximum(data_max * scale)
    slider.setTickInterval((data_max - data_min) / 10 * scale)


class GridSliders(QGridLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.slider = None
        self.value = None
        self.parent = parent

    def addSlider(self, title, row, callback=None):
        label = QLabel(self.parent)
        self.value = QLabel(self.parent)
        label.setText(title)
        self.value.setText("1")
        self.addWidget(label, row, 0, 1, 1)
        self.slider = QSlider(self.parent)
        self.slider.setOrientation(Qt.Horizontal)
        self.addWidget(self.slider, row, 1, 1, 1)
        self.addWidget(self.value, row, 2, 1, 1)
        setInterval(self.slider, scale=1, data_min=1, data_max=100)
        self.slider.valueChanged.connect(callback)
        return self

    def setOnValueChanged(self, callback):
        self.slider.valueChanged.connect(callback)

    def setInterval(self, scale, data_min, data_max):
        setInterval(self.slider, scale, data_min, data_max)
