from PySide6.QtWidgets import QMenuBar, QMenu

from Helpers.ActionMenu import ActionMenu


class MainMenu(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.action_open = ActionMenu(self, "Open", "fa.folder-open")
        self.action_save = ActionMenu(self, "Save as", "fa.save")
        # self.action_zoom = Action(self, "Zoom", "ri.zoom-in-line")
        # self.action_rotate = Action(self, "Rotate", "mdi6.rotate-right-variant")

        self.menuFile = QMenu(self)
        self.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.action_open)
        self.menuFile.addAction(self.action_save)
        self.menuRecent = QMenu(self.menuFile)
        self.menuFile.addMenu(self.menuRecent)

        self.menuFile.setTitle("File")
        self.menuRecent.setTitle("Open Recent Photo")
        self.action_open.setShortcut("Ctrl+O")
        self.action_open.setToolTip("Open Image")

    def actionOpen(self, callback):
        self.action_open.setOnClickEvent(callback)

    def actionSave(self, callback):
        self.action_save.setOnClickEvent(callback)



