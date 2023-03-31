import qtawesome as qta
from PySide6.QtWidgets import QMainWindow, QFileDialog, QWidget, QVBoxLayout, QStatusBar

from UI.widgets.LoadingProgressBar import LoadingProgressBar


class BaseWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.progressBar = None
        icon = qta.icon("fa.picture-o")
        self.setWindowIcon(icon)
        self.setWindowTitle("Super Face")
        self.central_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.createProgressBar()
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.setCentralWidget(self.central_widget)

    def createProgressBar(self):
        self.progressBar = LoadingProgressBar()
        self.progressBar.hide()
        self.main_layout.addWidget(self.progressBar)

    def mainWidget(self):
        return self.central_widget

    def mainLayout(self):
        return self.main_layout

    def launchDialogOpenFile(self, title="Open Image"):
        return QFileDialog.getOpenFileName(self, title)[0]

    def launchDialogSaveFile(self, title="Save Image"):
        return QFileDialog.getSaveFileName(self, title)[0]

    def showMessage(self, title, message):
        self.statusbar.showMessage("{0} {1}".format(title, message))
