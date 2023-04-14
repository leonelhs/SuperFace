import abc


class Toolset(metaclass=abc.ABCMeta):
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
        pass

    def historyBack(self):
        if len(self.history) > 0:
            return True

    def addPage(self, title):
        self.parent.toolBox.addPage(self.name(), title)

    def addButton(self, label, action=None, args=None):
        self.parent.toolBox.addButton(self.name(), label, action, args)

    def createWidget(self, widget):
        return self.parent.toolBox.createWidget(self.name(), widget)

    def createLayout(self, widget):
        return self.parent.toolBox.createLayout(self.name(), widget)

    @abc.abstractmethod
    def name(self):
        raise NotImplementedError

    @abc.abstractmethod
    def buildPage(self):
        raise NotImplementedError
