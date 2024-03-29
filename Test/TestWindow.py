import PIL.Image
from PySide6.QtCore import QThreadPool, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QHBoxLayout

from Test import load_pixmap
from Test.TestTask import TestTask
from UI.widgets.BaseWindow import BaseWindow
from UI.widgets.LoadingProgressBar import LoadingProgressBar


def trackTaskProgress(progress):
    print(progress)




# path = "./Test/image_test.jpg"
path = "/home/leonel/faces.jpg"


class TestWindow(BaseWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.threadpool = QThreadPool()
        self.args = (self.threadpool, self.taskDone, self.taskComplete, trackTaskProgress)
        self.testTask = None
        self.image_test = PIL.Image.open(path)
        pixmap = self.image_test.toqpixmap()
        self.tet_layout = QHBoxLayout(self)
        self.main_layout.addLayout(self.tet_layout)
        self.addPicture(pixmap)
        self.progressBar = LoadingProgressBar()
        self.main_layout.addWidget(self.progressBar)
        self.progressBar.hide()

    def addPicture(self, pixmap: QPixmap):
        picture = QLabel()
        pixmap = pixmap.scaled(QSize(256, 256))
        picture.setPixmap(pixmap)
        self.tet_layout.addWidget(picture)

    def setTask(self, task):
        self.testTask = TestTask(task, self.args)

    def taskDone(self, image_result):
        for image in image_result:
            pixmap = load_pixmap(image)
            self.addPicture(pixmap)

    def runTest(self):
        self.progressBar.show()
        self.testTask.runTest(self.image_test)

    def taskComplete(self):
        print("Test done.")
        self.progressBar.hide()
