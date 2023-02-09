import sys
from PySide6 import QtWidgets

from UI.MainWindow import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(1200, 800)

    widget.show()

    sys.exit(app.exec())
