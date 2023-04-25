from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QSlider


def setInterval(slider, scale, data_min, data_max):
    slider.setMinimum(data_min)
    slider.setMaximum(data_max)
    slider.setTickInterval(scale)


class Slider(QGridLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.slider = None
        self.value = None
        self.callback = None
        self.parent = parent

    def build(self, title, row, callback=None):
        self.callback = callback
        label = QLabel(self.parent)
        self.value = QLabel(self.parent)
        label.setText(title)
        self.value.setText("1")
        self.addWidget(label, row, 0, 1, 1)
        self.slider = QSlider(self.parent)
        self.slider.setOrientation(Qt.Horizontal)
        self.addWidget(self.slider, row, 1, 1, 1)
        self.addWidget(self.value, row, 2, 1, 1)
        self.slider.sliderMoved.connect(self.onValueChanged)
        setInterval(self.slider, scale=1, data_min=-100, data_max=100)
        return self

    def onValueChanged(self, value):
        self.value.setText(str(value))
        if self.callback:
            # Fixme adjust the scale for the image enhancements
            self.callback(value/10)

    def setOnValueChanged(self, callback):
        self.callback = callback

    def setInterval(self, scale, data_min, data_max):
        setInterval(self.slider, scale, data_min, data_max)
