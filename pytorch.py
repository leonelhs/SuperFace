import sys

from PySide6 import QtWidgets

from UI.TorchWindow import TorchWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = TorchWindow()
    widget.resize(1200, 800)
    widget.show()
    sys.exit(app.exec())
