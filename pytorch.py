import sys

from PySide6 import QtWidgets

from UI.PytorchWindow import PytorchWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = PytorchWindow()
    widget.resize(1200, 800)
    widget.show()
    sys.exit(app.exec())
