import abc

from PySide6.QtGui import QAction


class Action(QAction):
    def __init__(self, window, label, visible_in_menu=False):
        super().__init__(window)
        self.callback = None
        self.label = label
        self.setText(self.label)
        self.setIconVisibleInMenu(visible_in_menu)
        self.triggered.connect(self.onTriggered)

    def setOnClickEvent(self, callback):
        self.callback = callback

    @abc.abstractmethod
    def onTriggered(self):
        pass


