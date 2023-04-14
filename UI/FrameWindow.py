from PySide6.QtCore import (QMetaObject, Qt)
from PySide6.QtWidgets import (QSplitter)

from Helpers.ActionSubmenu import ActionSubmenu
from Helpers.Storage import Storage
from UI.MainMenu import MainMenu
from UI.widgets.BaseWindow import BaseWindow
from UI.widgets.LoadingProgressBar import LoadingProgressBar
from UI.widgets.TwinViewer import TwinViewer
from toolset.BaseToolBox import BaseToolBox


class FrameWindow(BaseWindow):
    def __init__(self, parent=None):
        super(FrameWindow, self).__init__(parent)
        self.enhanced_image = None
        self.menubar = None
        self.toolBox = None
        self.mainSplitter = None
        self.twinViewer = None
        self.image_path = None
        self._setupUi(self)
        self.storage = Storage()
        self.loadResentFiles()

    def _setupUi(self, main_window):
        self.mainSplitter = QSplitter(self.mainWidget())
        self.mainSplitter.setOrientation(Qt.Horizontal)
        self.toolBox = BaseToolBox(self.mainSplitter)
        self.mainSplitter.addWidget(self.toolBox)
        self.twinViewer = TwinViewer(self.mainSplitter)
        self.mainSplitter.addWidget(self.twinViewer)
        self.mainLayout().addWidget(self.mainSplitter)

        self.menubar = MainMenu(main_window)

        self.menubar.actionOpen(self.openFile)
        self.menubar.actionSave(self.saveFile)
        self.progressBar = LoadingProgressBar()
        self.progressBar.hide()
        self.main_layout.addWidget(self.progressBar)

        QMetaObject.connectSlotsByName(main_window)

    def setSpliterSize(self, left, right):
        size = self.mainSplitter.size().height()
        self.mainSplitter.setSizes([size * left, size * right])

    def addRecentFile(self, path):
        action = ActionSubmenu(self, path)
        action.setOnClickEvent(self.displayPhoto)
        self.menubar.menuRecent.addAction(action)

    def loadResentFiles(self):
        resents = self.storage.fetchRecents()
        for recent in resents:
            self.addRecentFile(recent[0])

    def displayPhoto(self, image_path):
        try:
            self.twinViewer.left.display(image_path)
        except FileNotFoundError:
            self.showMessage("file not found at: ", image_path)

    def openFile(self):
        image_path = self.launchDialogOpenFile()
        if image_path:
            self.showMessage("Working image at: ", image_path)
            self.storage.insertRecent(image_path)
            self.displayPhoto(image_path)
            self.addRecentFile(image_path)

    def saveFile(self):
        image_path = self.launchDialogSaveFile()
        if image_path:
            self.twinViewer.left.save(image_path)

    def trackTaskProgress(self, progress):
        pass

    def taskDone(self, image_result):
        pass

    def taskComplete(self):
        pass
