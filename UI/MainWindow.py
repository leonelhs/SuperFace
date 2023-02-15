from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt, QThreadPool)
from PySide6.QtWidgets import (QHBoxLayout, QMenu, QMenuBar, QSplitter,
                               QStatusBar, QToolBar, QWidget, QFileDialog, QMainWindow, QVBoxLayout)

import utils
from AI.TaskLowLight import TaskLowLight
from AI.TaskSuperFace import TaskSuperFace
from AI.TaskZeroBackground import TaskZeroBackground
from Actions import Action, ActionRecents
from Face import faceBuild
from Storage import Storage
from UI.widgets.LoadingProgressBar import LoadingProgressBar
from UI.widgets.PhotoPanel import PhotoPanel


def tr(label):
    return QCoreApplication.translate("MainWindow", label, None)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.lowLight = None
        self.superFace = None
        self.zeroBackground = None

        self.storage = None
        self.menuRecents = None
        self.central_layout = None
        self.widgets_layout = None

        self.progressBar = None
        self.workingImage = None
        self.image_path = None
        self.folder_path = None
        self.inputPanel = None
        self.outputPanel = None
        self.toolBar = None
        self.statusbar = None
        self.menuFile = None
        self.menubar = None
        self.splitter = None
        self.splitLayout = None
        self.central_widget = None

        self.image_open = Action(self, "Open Image", "fa.folder-open")
        self.image_save = Action(self, "Save Image", "fa.save")
        self.super_resolution = Action(self, "Super Resolution", "mdi.face")
        self.zero_background = Action(self, "Zero Background", "mdi.face-recognition")
        self.low_light = Action(self, "Light Enhancement", "mdi.face-shimmer")

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.setupUI(self)

    def setupUI(self, main_window):
        self.central_widget = QWidget(main_window)
        self.central_layout = QVBoxLayout(self.central_widget)

        self.splitLayout = QHBoxLayout(self.central_widget)
        self.splitter = QSplitter(self.central_widget)
        self.splitter.setOrientation(Qt.Horizontal)

        self.inputPanel = PhotoPanel(self.splitter)
        self.outputPanel = PhotoPanel(self.splitter)
        self.splitLayout.addWidget(self.splitter)
        self.central_layout.addLayout(self.splitLayout)

        self.progressBar = LoadingProgressBar()
        self.progressBar.hide()
        self.central_layout.addWidget(self.progressBar)

        main_window.setCentralWidget(self.central_widget)
        self.menubar = QMenuBar(main_window)

        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        self.menuFile = QMenu(self.menubar)

        main_window.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(main_window)

        main_window.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(main_window)

        main_window.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.image_open)
        self.menuFile.addAction(self.image_save)

        self.menuRecents = QMenu(self.menuFile)
        self.menuFile.addMenu(self.menuRecents)
        self.menuRecents.setTitle(tr("Open Recent Photo"))

        self.toolBar.addAction(self.super_resolution)
        self.toolBar.addAction(self.zero_background)
        self.toolBar.addAction(self.low_light)

        self.image_open.setOnClickEvent(self.loadImageFile)
        self.image_save.setOnClickEvent(self.saveImageFile)

        self.super_resolution.setOnClickEvent(self.process_super_resolution)
        self.zero_background.setOnClickEvent(self.process_zero_background)
        self.low_light.setOnClickEvent(self.process_lowlight)

        self.retranslateUI(main_window)

        self.storage = Storage()
        args = (self.threadpool, self.progressBar, self.outputPanel)
        self.superFace = TaskSuperFace(*args)
        self.zeroBackground = TaskZeroBackground(*args)
        self.lowLight = TaskLowLight(*args)
        self.appendFileRecents()

        QMetaObject.connectSlotsByName(main_window)

    def retranslateUI(self, main_window):
        main_window.setWindowTitle(tr("Image AI Composer"))
        self.image_open.setShortcut(tr("Ctrl+O"))
        self.menuFile.setTitle(tr("File"))

        self.image_open.setToolTip(tr("Open Image"))
        self.super_resolution.setToolTip(tr("Super Resolution"))
        self.zero_background.setToolTip(tr("Zero Background"))
        self.low_light.setToolTip(tr("Low Light"))

    def resizeEvent(self, event):
        print("resize")
        QMainWindow.resizeEvent(self, event)

    def openRecentPhoto(self, image_path):
        self.workingImage = utils.imageOpen(image_path)
        face = faceBuild(self.workingImage)
        self.inputPanel.appendPhoto(face)
            
    def appendFileRecents(self):
        recents = self.storage.fetchRecents()
        for recent in recents:
            action = ActionRecents(self, recent[0])
            action.setCallback(self.openRecentPhoto)
            self.menuRecents.addAction(action)

    def show_message(self, title, message):
        self.statusbar.showMessage("{0} {1}".format(title, message))

    def loadImageFile(self):
        self.image_path = QFileDialog.getOpenFileName(self, 'Open Image')[0]
        if self.image_path:
            self.storage.insertRecent(self.image_path)
            self.show_message("Working image at: ", self.image_path)
            self.workingImage = utils.imageOpen(self.image_path)
            face = faceBuild(self.workingImage)
            self.inputPanel.appendPhoto(face)

    def saveImageFile(self):
        image_path = QFileDialog.getSaveFileName(self, 'Save Image')[0]
        if image_path:
            self.show_message("Save image at: ", self.image_path)
            pixmap = self.outputPanel.getPhoto()
            image = pixmap.toImage()
            image.save(image_path, "PNG", -1)

    def process_super_resolution(self):
        self.show_message("Super resolution at: ", self.image_path)
        self.progressBar.show()
        self.superFace.startEnhanceThread(self.workingImage)

    def process_zero_background(self):
        self.show_message("Zeo background at: ", self.image_path)
        self.progressBar.show()
        self.zeroBackground.startEnhanceThread(self.workingImage)

    def process_lowlight(self):
        self.show_message("Light enhancement at: ", self.image_path)
        self.progressBar.show()
        self.lowLight.startEnhanceThread(self.workingImage)
