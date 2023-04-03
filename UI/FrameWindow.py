from PySide6.QtCore import (QMetaObject, Qt)
from PySide6.QtWidgets import (QSplitter)

import utils
from Actions import ActionResents
from Storage import Storage
from UI.MainMenu import MainMenu
from UI.ToolBoxEnhancer import ToolBoxEnhancer
from UI.widgets.BaseWindow import BaseWindow
from UI.widgets.TwinViewer import TwinViewer


class FrameWindow(BaseWindow):
    def __init__(self, parent=None):
        super(FrameWindow, self).__init__(parent)
        self.enhanced_image = None
        self.menubar = None
        self.toolBox = None
        self.splitter = None
        self.twinViewer = None
        self.image_path = None
        self._setupUi(self)
        self.storage = Storage()
        self.loadResentFiles()

    def _setupUi(self, main_window):
        self.splitter = QSplitter(self.mainWidget())
        self.splitter.setOrientation(Qt.Horizontal)
        self.toolBox = ToolBoxEnhancer(self.splitter)
        self.splitter.addWidget(self.toolBox)
        self.twinViewer = TwinViewer(self.splitter)
        self.splitter.addWidget(self.twinViewer)
        self.mainLayout().addWidget(self.splitter)
        self.menubar = MainMenu(main_window)

        self.menubar.actionOpen(self.openFile)
        self.menubar.actionSave(self.saveFile)

        QMetaObject.connectSlotsByName(main_window)

    def loadResentFiles(self):
        resents = self.storage.fetchRecents()
        for recent in resents:
            action = ActionResents(self, recent[0])
            action.setCallback(self.displayPhoto)
            self.menubar.menuRecent.addAction(action)

    def displayPhoto(self, image_path):
        try:
            self.image_path = image_path
            image = utils.imageOpen(image_path)
            self.twinViewer.displayInput(image)
        except FileNotFoundError:
            self.showMessage("file not found at: ", image_path)

    def openFile(self):
        image_path = self.launchDialogOpenFile()
        if image_path:
            self.showMessage("Working image at: ", image_path)
            self.storage.insertRecent(image_path)
            self.displayPhoto(image_path)

    def saveFile(self):
        image_path = self.launchDialogSaveFile()
        if image_path:
            self.twinViewer.imageOutput().save(image_path, "PNG")

    def trackTaskProgress(self, progress):
        self.progressBar.setValue(progress)
        self.showMessage("Scanning gallery completed: ", progress)

    def taskDone(self, image_result):
        self.enhanced_image = image_result.copy()
        self.showMessage("finish ", " done")
        self.twinViewer.displayOutput(image_result)

    def taskComplete(self):
        self.progressBar.hide()
        self.showMessage("Scanning complete ", "Done")
