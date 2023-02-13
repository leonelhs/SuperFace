import sys
from PySide6 import QtWidgets

from UI.Enhancements import Enhancements

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Enhancements()
    widget.resize(1200, 800)

    widget.show()

    sys.exit(app.exec())
