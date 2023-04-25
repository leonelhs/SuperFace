import qtawesome as qta
from PySide6.QtWidgets import QMainWindow, QFileDialog, QWidget, QStatusBar, QVBoxLayout

path = "/home/leonel/"
file_filter = """
    *.jpg *.png;;JPG (*.jpg);;PNG (*.png);;JPEG (*.jpeg);;BMP (*.bmp);;CUR (*.cur);;
    GIF (*.gif);;ICNS (*.icns);;ICO (*.ico);;PBM (*.pbm);;PGM (*.pgm);;
    PPM (*.ppm);;SVG (*.svg);;SVGZ (*.svgz);;TGA (*.tga);;TIF (*.tif);;
    TIFF (*.tiff);;WBMP (*.wbmp);;WEBP (*.webp);;XBM (*.xbm);;XPM (*.xpm);;
    All files (*.*)
"""


class BaseWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.toolBarEdit = None
        self.toolBox = None
        self.progressBar = None
        icon = qta.icon("fa.picture-o")
        self.setWindowIcon(icon)
        self.setWindowTitle("Super Face")
        self.central_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.setCentralWidget(self.central_widget)

    def launchDialogOpenFile(self, title="Open Image"):
        return QFileDialog.getOpenFileName(self, title, path, file_filter)[0]

    def launchDialogSaveFile(self, title="Save Image"):
        return QFileDialog.getSaveFileName(self, title)[0]

    def showMessage(self, title, message):
        self.statusbar.showMessage("{0} {1}".format(title, message))
