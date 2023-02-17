from abc import abstractmethod

import qtawesome as qta
from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import (QMenuBar,
                               QSplitter, QStatusBar,
                               QToolBox, QVBoxLayout, QWidget, QMainWindow, QMenu, QToolBar, QGraphicsScene, QLayout,
                               QPushButton, QLabel, QSizePolicy, QFileDialog)

import utils
from Actions import Action, ActionRecents
from Storage import Storage
from UI.widgets.ImageGraphicsView import ImageGraphicsView
from UI.widgets.LoadingProgressBar import LoadingProgressBar


def tr(label):
    return QCoreApplication.translate("MainWindow", label, None)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.action_rotate = None
        self.action_zoom = None
        self.action_save = None
        self.action_open = None
        self._image_pat = None
        self._working_image = None
        self._sceneOutput = None
        self._sceneInput = None
        self._outputPanel = None
        self._inputPanel = None

        self.toolBar = None
        self.menuFile = None
        self.menuRecents = None
        self.statusbar = None
        self.menubar = None
        self.progressBar = None
        self.toolBox = None

        self.button_superface = None
        self.indicator_super_resolution = None
        self.controls_super_resolution = None
        self.panel_splitter = None
        self.page_4 = None
        self.page_super_resolution = None
        self.main_splitter = None
        self.main_layout = None
        self.central_widget = None

        self.action_open = Action(self, "Open", "fa.folder-open")
        self.action_save = Action(self, "Save", "fa.save")
        self.action_zoom = Action(self, "Zoom", "ri.zoom-in-line")
        self.action_rotate = Action(self, "Rotate", "mdi6.rotate-right-variant")

        self.action_open.setOnClickEvent(self._dialogOpenFile)
        self.action_save.setOnClickEvent(self._dialogSaveFile)
        self.action_zoom.setOnClickEvent(self.imageZoom)
        self.action_rotate.setOnClickEvent(self.imageFlip)

        self._setupUi(self)
        self.storage = Storage()
        self._appendFileRecents()

    def _setupUi(self, main_window):
        self.central_widget = QWidget(main_window)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_splitter = QSplitter(self.central_widget)
        self.main_splitter.setOrientation(Qt.Horizontal)

        self._createToolBox()
        self._createImageViewers()
        self._createProgressbar()

        main_window.setCentralWidget(self.central_widget)

        self._createMenubar(main_window)
        self.statusbar = QStatusBar(main_window)
        main_window.setStatusBar(self.statusbar)

        self._createToolbar(main_window)

        self._retranslateUI(main_window)
        QMetaObject.connectSlotsByName(main_window)

    @abstractmethod
    def imageZoom(self):
        pass

    @abstractmethod
    def imageFlip(self):
        pass

    @abstractmethod
    def trackEnhanceProgress(self, progress):
        pass

    @abstractmethod
    def enhanceDone(self, image_result):
        pass

    @abstractmethod
    def enhanceComplete(self):
        pass

    def _createToolBox(self):
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.toolBox = QToolBox(self.main_splitter)
        self.page_super_resolution = QWidget()
        self.toolBox.addItem(self.page_super_resolution, u"Page 1")
        self.page_4 = QWidget()
        self.toolBox.addItem(self.page_4, u"Page 2")
        self.main_splitter.addWidget(self.toolBox)

        self.controls_super_resolution = QVBoxLayout(self.page_super_resolution)
        sizePolicy.setHeightForWidth(self.page_super_resolution.sizePolicy().hasHeightForWidth())
        self.page_super_resolution.setSizePolicy(sizePolicy)

        self.controls_super_resolution.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.indicator_super_resolution = QLabel(self.page_super_resolution)
        icon = qta.icon("mdi.high-definition-box")
        image = QImage("./assets/hd.png")
        pixmap = QPixmap.fromImage(image)
        self.indicator_super_resolution.setPixmap(pixmap)
        self.controls_super_resolution.addWidget(self.indicator_super_resolution)

        self.button_superface = QPushButton(self.page_super_resolution)
        self.button_superface.setText("Super Resolution")

        self.controls_super_resolution.addWidget(self.button_superface)
        self.toolBox.setCurrentIndex(0)

    def _createImageViewers(self):
        self.panel_splitter = QSplitter(self.main_splitter)
        self.panel_splitter.setOrientation(Qt.Horizontal)
        self._inputPanel = ImageGraphicsView(self.panel_splitter)
        self.panel_splitter.addWidget(self._inputPanel)
        self._outputPanel = ImageGraphicsView(self.panel_splitter)
        self.panel_splitter.addWidget(self._outputPanel)
        self._sceneInput = QGraphicsScene()
        self._sceneOutput = QGraphicsScene()
        self.main_splitter.addWidget(self.panel_splitter)
        self.main_layout.addWidget(self.main_splitter)

    def _createProgressbar(self):
        self.progressBar = LoadingProgressBar()
        self.progressBar.hide()
        self.main_layout.addWidget(self.progressBar)

    def _createMenubar(self, main_window):
        self.menubar = QMenuBar(main_window)
        main_window.setMenuBar(self.menubar)
        self.menuFile = QMenu(self.menubar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.action_open)
        self.menuFile.addAction(self.action_save)
        self.menuRecents = QMenu(self.menuFile)
        self.menuFile.addMenu(self.menuRecents)

    def _createToolbar(self, main_window):
        self.toolBar = QToolBar(main_window)
        main_window.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.toolBar.addAction(self.action_zoom)
        self.toolBar.addAction(self.action_rotate)

    def _retranslateUI(self, main_window):
        main_window.setWindowTitle(tr("Image AI Composer"))
        self.menuFile.setTitle(tr("File"))
        self.menuRecents.setTitle(tr("Open Recent Photo"))
        self.action_open.setShortcut(tr("Ctrl+O"))
        self.action_open.setToolTip(tr("Open Image"))

    def _appendFileRecents(self):
        recents = self.storage.fetchRecents()
        for recent in recents:
            action = ActionRecents(self, recent[0])
            action.setCallback(self._loadPhoto)
            self.menuRecents.addAction(action)

    def _loadPhoto(self, image_path):
        image = self.readImageFile(image_path)
        self.displayImageInput(image)

    def _displayImage(self, image, scene, graphics):
        self._working_image = image
        pixmap = utils.pil2Pixmap(image)
        scene.addPixmap(pixmap)
        graphics.setScene(scene)

    def _dialogOpenFile(self):
        image_path = self.launchDialogOpenFile()
        if image_path:
            self.show_message("Working image at: ", image_path)
            self.storage.insertRecent(image_path)
            self._loadPhoto(image_path)

    def _dialogSaveFile(self):
        image_path = self.launchDialogSaveFile()
        if image_path:
            self._working_image.save(image_path, "PNG")

    def launchDialogOpenFile(self):
        return QFileDialog.getOpenFileName(self, 'Open Image')[0]

    def launchDialogSaveFile(self):
        return QFileDialog.getSaveFileName(self, 'Save Image')[0]

    def readImageFile(self, image_path):
        self._image_pat = image_path
        return utils.imageOpen(image_path)

    def displayImageInput(self, image):
        self._displayImage(image, self._sceneInput, self._inputPanel)

    def displayImageOutput(self, image):
        self._displayImage(image, self._sceneOutput, self._outputPanel)

    def workingImage(self):
        return self._working_image

    def imagePath(self):
        return self._image_pat

    def show_message(self, title, message):
        self.statusbar.showMessage("{0} {1}".format(title, message))
