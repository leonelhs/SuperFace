from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSplitter, QGraphicsScene

from UI.widgets.ImageGraphicsView import ImageGraphicsView


def toPixmap(image):
    if "PIL.Image" in str(image.__class__):
        return image.toqpixmap()
    return image


def displayImage(image, scene, graphics):
    scene.clear()
    image = toPixmap(image)
    scene.addPixmap(image)
    graphics.setScene(scene)
    graphics.setEnabled(True)
    graphics.redraw()


class TwinViewer(QSplitter):

    def __init__(self, parent):
        super().__init__(parent)
        self.__imageOutput = None
        self.__imageInput = None
        self.setOrientation(Qt.Horizontal)
        self.__inputView = ImageGraphicsView(self)
        self.__outputView = ImageGraphicsView(self)
        self.__sceneInput = QGraphicsScene()
        self.__sceneOutput = QGraphicsScene()
        self.__inputView.setEnabled(False)
        self.__outputView.setEnabled(False)
        self.addWidget(self.__inputView)
        self.addWidget(self.__outputView)

    def inputView(self):
        return self.__inputView

    def outputView(self):
        return self.__outputView

    def sceneInput(self):
        return self.__sceneInput

    def sceneOutput(self):
        return self.__sceneOutput

    def blurryImage(self):
        pass

    def displayInput(self, image):
        self.__imageInput = image
        displayImage(image, self.__sceneInput, self.__inputView)

    def displayOutput(self, image):
        self.__imageOutput = image
        displayImage(image, self.__sceneOutput, self.__outputView)

    def imageOutput(self):
        return self.__imageOutput

    def imageInput(self):
        return self.__imageInput

    def imageFilter(self, image_filter, args):
        image = self.imageInput().filter(image_filter(*args))
        self.displayOutput(image)

    def applyFilter(self):
        self.displayInput(self.imageOutput())


