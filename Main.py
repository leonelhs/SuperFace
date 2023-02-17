import sys
from PySide6 import QtWidgets

from UI.WorkspaceWindow import WorkspaceWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = WorkspaceWindow()
    widget.resize(1200, 800)

    widget.show()

    sys.exit(app.exec())
