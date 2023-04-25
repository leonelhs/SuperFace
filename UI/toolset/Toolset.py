import abc

import numpy as np

from remotetasks.remote_task import RemoteTask


class Toolset(RemoteTask, metaclass=abc.ABCMeta):
    def __init__(self, parent):
        RemoteTask.__init__(self)
        self.main_window = parent
        self.init()

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'buildPage') and
                callable(subclass.buildPage) or
                NotImplemented)

    # Methods for build Toolset controls page (buttons, inputs, ...)
    @abc.abstractmethod
    def name(self):
        raise NotImplementedError

    @abc.abstractmethod
    def buildPage(self):
        raise NotImplementedError

    def init(self):
        if self.main_window.twinViewer is None:
            raise TypeError("MainWindow TwinViewer should not be None")
        if self.main_window.toolBox is None:
            raise TypeError("MainWindow ToolBox should not be None")

    def preInit(self, message):
        self.main_window.progressBar.show()
        self.main_window.showMessage("Running task: ", message)

    def viewer(self):
        if self.main_window.twinViewer.left.isEnabled():
            return self.main_window.twinViewer
        else:
            raise TypeError("No image loaded")

    def process(self, service):
        return self.main_window.service(service)

    def showMessage(self, title, message):
        self.main_window.showMessage(title, message)

    def onRequestResponse(self, reply, resource):
        self.onImageProcessDone(resource, reply)

    def onRequestProgress(self, sent, total):
        print("Request send {0} of Total {1}".format(sent, total))

    def onRequestError(self, message, error):
        self.main_window.progressBar.hide()
        self.main_window.showMessage(message, error)

    def requestImageProcess(self, resource):
        if self.viewer().left.isEnabled():
            self.preInit("Image parser")
            image = self.viewer().left.bytes()
            self.runRemoteTask(image, resource)
        else:
            raise TypeError("No image loaded")

    @abc.abstractmethod
    def onImageProcessDone(self, process: str, image: np.ndarray):
        raise NotImplementedError

    # Wrapper methods from ToolBox maker
    def addPage(self, title):
        self.main_window.toolBox.addPage(self.name(), title)

    def addButton(self, label, action=None, args=None):
        self.main_window.toolBox.addButton(self.name(), label, action, args)

    def addSlider(self, label, row, callback=None):
        return self.main_window.toolBox.createSlider(self.name(), label, row, callback)

    def createWidget(self, widget):
        return self.main_window.toolBox.createWidget(self.name(), widget)

    def createLayout(self, widget):
        return self.main_window.toolBox.createLayout(self.name(), widget)
