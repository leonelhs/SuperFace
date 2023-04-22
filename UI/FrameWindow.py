from PySide6.QtCore import (QMetaObject, Qt)
from PySide6.QtWidgets import (QSplitter, QToolBar, QMenuBar, QMenu)

from Helpers.ActionMenu import ActionMenu
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

        self.action_copy = ActionMenu(self, "Copy", "fa.copy")
        self.action_paste = ActionMenu(self, "Paste", "fa.paste")
        self.action_swap = ActionMenu(self, "Swap", "mdi.swap-horizontal-bold")
        self.action_split = ActionMenu(self, "Split", "mdi.table-split-cell")
        self.action_undo = ActionMenu(self, "Undo", "mdi.undo")
        self.action_redo = ActionMenu(self, "Redo", "mdi.redo")
        self.action_rotate = ActionMenu(self, "Rotate", "mdi6.rotate-right-variant")
        self.action_zoom_in = ActionMenu(self, "Zoom +", "ei.zoom-in")
        self.action_zoom_out = ActionMenu(self, "Zoom -", "ei.zoom-out")

        self._setupUi(self)
        self.storage = Storage()
        self.loadResentFiles()

    def _setupUi(self, main_window):
        self.menubar = MainMenu(main_window)
        self.menubar.actionOpen(self.openFile)
        self.menubar.actionSave(self.saveActiveViewFile)
        main_window.setMenuBar(self.menubar)

        self.toolBar = QToolBar(self.central_widget)
        self.toolBar.addAction(self.action_swap)
        self.toolBar.addAction(self.action_split)
        self.action_swap.setOnClickEvent(self.twinImageSwap)
        self.toolBar.addAction(self.action_undo)
        self.toolBar.addAction(self.action_redo)
        self.toolBar.addAction(self.action_zoom_in)
        self.toolBar.addAction(self.action_zoom_out)
        self.toolBar.addAction(self.action_rotate)
        self.addToolBar(self.toolBar)

        self.mainSplitter = QSplitter(self.central_widget)
        self.mainSplitter.setOrientation(Qt.Horizontal)
        self.toolBox = BaseToolBox(self.mainSplitter)
        self.mainSplitter.addWidget(self.toolBox)
        self.twinViewer = TwinViewer(self.mainSplitter)
        self.mainSplitter.addWidget(self.twinViewer)
        self.main_layout.addWidget(self.mainSplitter)

        # Add progressbar widget to last to keep at bottom
        self.progressBar = LoadingProgressBar()
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

    def twinImageSwap(self):
        self.twinViewer.swapImages()

    def openFile(self):
        image_path = self.launchDialogOpenFile()
        if image_path:
            self.showMessage("Working image at: ", image_path)
            self.storage.insertRecent(image_path)
            self.displayPhoto(image_path)
            self.addRecentFile(image_path)

    def saveFile(self, viewer):
        image_path = self.launchDialogSaveFile()
        if image_path:
            viewer.save(image_path)

    def saveLeftFile(self):
        if self.twinViewer.left.isEnabled():
            self.saveFile(self.twinViewer.left)
        else:
            raise TypeError("No image loaded")

    def saveRightFile(self):
        if self.twinViewer.right.isEnabled():
            self.saveFile(self.twinViewer.right)
        else:
            raise TypeError("No image loaded")

    def saveActiveViewFile(self):
        if self.twinViewer.active.isEnabled():
            self.saveFile(self.twinViewer.active)
        else:
            raise TypeError("No image loaded")
