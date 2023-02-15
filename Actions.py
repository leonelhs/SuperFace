import qtawesome as qta
from PySide6.QtGui import QAction


class Action(QAction):
    def __init__(self, window, text, icon, visible_in_menu=True):
        super().__init__(window)
        self.callback = None
        self.setText(text)
        icon = qta.icon(icon)
        self.setIcon(icon)
        self.setIconVisibleInMenu(visible_in_menu)
        self.triggered.connect(self.onTriggered)

    def setOnClickEvent(self, callback):
        self.callback = callback

    def onTriggered(self):
        self.callback()


class ActionRecents(QAction):
    def __init__(self, window, recent, visible_in_menu=False):
        super().__init__(window)
        self.callback = None
        self.recent = recent
        self.setText(self.recent)
        self.setIconVisibleInMenu(visible_in_menu)
        self.triggered.connect(self.onTriggered)

    def setCallback(self, callback):
        self.callback = callback

    def onTriggered(self):
        self.callback(self.recent)
