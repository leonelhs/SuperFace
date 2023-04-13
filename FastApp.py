import sys

from PySide6.QtWidgets import QApplication

from FastWindow import FastWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = FastWindow()
    main.resize(1200, 800)
    main.show()
    sys.exit(app.exec())
