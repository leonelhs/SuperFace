import PIL.Image
from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtWidgets import QMainWindow, QLabel

from Test.TestTask import TestTask


def trackTaskProgress(progress):
    print(progress)


def taskComplete():
    print("Test done.")


# path = "./Test/image_test.jpg"
path = "/home/leonel/goyo00.jpeg"


class TestWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.threadpool = QThreadPool()
        self.args = (self.threadpool, self.taskDone, taskComplete, trackTaskProgress)
        self.testTask = None
        self.picture = QLabel()
        self.image_test = PIL.Image.open(path)
        pixmap = self.image_test.toqpixmap()
        self.picture.setPixmap(pixmap)
        self.picture.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.picture)

    def setTask(self, task):
        self.testTask = TestTask(task, self.args)

    def taskDone(self, image_result):
        pixmap = image_result[1].toqpixmap()
        self.picture.setPixmap(pixmap)

    def runTest(self):
        self.testTask.runRemoteTask(self.image_test)
