import PIL.Image
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QLabel


def trackTaskProgress(progress):
    print(progress)


def taskComplete():
    print("Test done.")


# path = "./Test/image_test.jpg"
path = "/home/leonel/goyo00.jpeg"


class RemoteWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.task = None
        self.picture = QLabel()
        self.image_test = PIL.Image.open(path)
        pixmap = self.image_test.toqpixmap()
        self.picture.setPixmap(pixmap)
        self.picture.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.picture)

    def setTask(self, task):
        self.task = task()

    def runTest(self):
        image = self.task.runRemoteTask(path)
        pixmap = image.toqpixmap()
        self.picture.setPixmap(pixmap)
