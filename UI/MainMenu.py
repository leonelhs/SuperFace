from PySide6.QtWidgets import QMenuBar, QMenu

from Helpers.ActionMenu import ActionMenu

TEST_MODE = True


class MainMenu(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.action_open = ActionMenu(self, "Open", "fa.folder-open")
        self.action_save = ActionMenu(self, "Save as", "fa.save")
        self.action_test1 = ActionMenu(self, "Test1", "ri.zoom-in-line")
        self.action_test2 = ActionMenu(self, "Test2", "ri.zoom-in-line")

        self.menuFile = QMenu(self)
        self.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.action_open)
        self.menuFile.addAction(self.action_save)
        self.menuRecent = QMenu(self.menuFile)
        self.menuFile.addMenu(self.menuRecent)
        self.menuTest()

        self.menuFile.setTitle("File")
        self.menuRecent.setTitle("Open Recent Photo")
        self.action_open.setShortcut("Ctrl+0")
        self.action_open.setToolTip("Open Image")

    def actionOpen(self, callback):
        self.action_open.setOnClickEvent(callback)

    def actionSave(self, callback):
        self.action_save.setOnClickEvent(callback)

    def actionTest1(self, callback):
        self.action_test1.setOnClickEvent(callback)

    def actionTest2(self, callback):
        self.action_test2.setOnClickEvent(callback)

    def menuTest(self):
        if TEST_MODE:
            self.menuFile.addAction(self.action_test1)
            self.menuFile.addAction(self.action_test2)
