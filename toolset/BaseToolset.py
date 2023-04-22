import abc


class BaseToolset(metaclass=abc.ABCMeta):
    def __init__(self, parent):
        self.parent = parent
        self.history = list()
        self.original = None
        self.init()

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'buildPage') and
                callable(subclass.buildPage) or
                NotImplemented)

    def init(self):
        if self.parent.twinViewer is None:
            raise TypeError("MainWindow TwinViewer should not be None")
        if self.parent.toolBox is None:
            raise TypeError("MainWindow ToolBox should not be None")

    def preInit(self, message):
        self.parent.progressBar.show()
        self.parent.showMessage("Running task: ", message)

    def historyBack(self):
        if len(self.history) > 0:
            return True

    # Callbacks methods for Network request
    @abc.abstractmethod
    def onRequestResponse(self, resource, reply):
        raise NotImplementedError

    def onRequestProgress(self, sent, total):
        pass

    def onRequestError(self, message, error):
        self.parent.progressBar.hide()
        self.parent.showMessage(error, message)

    # Methods for build Toolset controls page (buttons, inputs, ...)
    @abc.abstractmethod
    def name(self):
        raise NotImplementedError

    @abc.abstractmethod
    def buildPage(self):
        raise NotImplementedError

    # Wrapper methods from ToolBox maker
    def addPage(self, title):
        self.parent.toolBox.addPage(self.name(), title)

    def addButton(self, label, action=None, args=None):
        self.parent.toolBox.addButton(self.name(), label, action, args)

    def createWidget(self, widget):
        return self.parent.toolBox.createWidget(self.name(), widget)

    def createLayout(self, widget):
        return self.parent.toolBox.createLayout(self.name(), widget)
