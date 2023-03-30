from abc import abstractmethod

import qtawesome as qta
from PIL import ImageFilter
from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QMenuBar, QSplitter, QStatusBar,
                               QVBoxLayout, QWidget, QMainWindow,
                               QMenu, QToolBar, QGraphicsScene, QFileDialog, QComboBox)

import utils
from Actions import Action, ActionRecents
from Storage import Storage
from UI.widgets.ImageGraphicsView import ImageGraphicsView
from UI.widgets.LoadingProgressBar import LoadingProgressBar
from UI.widgets.tool_box_enhancer import ToolBoxEnhancer


def tr(label):
    return QCoreApplication.translate("MainWindow", label, None)


def displayImage(image, scene, graphics):
    scene.clear()
    scene.addPixmap(image.toqpixmap())
    graphics.setScene(scene)
    graphics.setEnabled(True)
    graphics.redraw()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.selection_box = None
        self.action_rotate = None
        self.action_zoom = None
        self.action_save = None
        self.action_open = None
        self.__image_pat = None
        self.__imageInput = None
        self.__imageOutput = None
        self.__outputPanel = None
        self.__inputPanel = None
        self.__sceneInput = None
        self.__sceneOutput = None

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
        self.page_zero_background = None
        self.page_super_resolution = None
        self.main_splitter = None
        self.main_layout = None
        self.central_widget = None

        self.action_open = Action(self, "Open", "fa.folder-open")
        self.action_save = Action(self, "Save as", "fa.save")
        self.action_zoom = Action(self, "Zoom", "ri.zoom-in-line")
        self.action_rotate = Action(self, "Rotate", "mdi6.rotate-right-variant")

        self.action_open.setOnClickEvent(self.__dialogOpenFile)
        self.action_save.setOnClickEvent(self.__dialogSaveFile)
        self.action_zoom.setOnClickEvent(self.imageZoom)
        self.action_rotate.setOnClickEvent(self.imageFlip)

        self._setupUi(self)
        self.storage = Storage()
        self.__appendFileRecents()

    def _setupUi(self, main_window):
        icon = qta.icon("fa.picture-o")
        main_window.setWindowIcon(icon)
        main_window.setWindowTitle("Super Face")
        self.central_widget = QWidget(main_window)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_splitter = QSplitter(self.central_widget)
        self.main_splitter.setOrientation(Qt.Horizontal)

        self.__createToolBox()
        self.__createImageViewers()
        self.__createProgressbar()

        main_window.setCentralWidget(self.central_widget)

        self.__createMenubar(main_window)
        self.statusbar = QStatusBar(main_window)
        main_window.setStatusBar(self.statusbar)

        # self.__createToolbar(main_window)

        self.__retranslateUI(main_window)
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

    def __createToolBox(self):

        self.toolBox = ToolBoxEnhancer(self.main_splitter)

        self.toolBox.addPage("face", u"Super Face")
        self.toolBox.addPage("color", u"Super Colorize")
        self.toolBox.addPage("hires", u"Super Resolution")
        self.toolBox.addPage("zero", u"Zero Background")
        self.toolBox.addPage("light", u"Light Enhancement")

        self.toolBox.addButton("face", "Restore faces", self.processSuperface)

        self.toolBox.addButton("color", "Colorize", self.processSuperColorize)

        scale = self.toolBox.createWidget("hires", QComboBox)
        scale.addItems(["Scale 2X", "Scale 4X", "Scale 8X"])
        scale.currentIndexChanged.connect(self.onHiresScaleChanged)

        self.toolBox.addButton("hires", "Scale image", self.processSuperResolution)

        self.toolBox.addButton("zero", "Remove background", self.processZeroBackground)
        self.toolBox.addButton("zero", "Custom background", self.setCustomBackground)
        self.toolBox.addButton("light", "Shine picture", self.processLowlight)

        self.main_splitter.addWidget(self.toolBox)
        self.toolBox.setCurrentIndex(0)

    def __createImageViewers(self):
        self.panel_splitter = QSplitter(self.main_splitter)
        self.panel_splitter.setOrientation(Qt.Horizontal)
        self.__inputPanel = ImageGraphicsView(self.panel_splitter)
        self.panel_splitter.addWidget(self.__inputPanel)
        self.__outputPanel = ImageGraphicsView(self.panel_splitter)
        self.panel_splitter.addWidget(self.__outputPanel)
        self.main_splitter.addWidget(self.panel_splitter)
        self.main_layout.addWidget(self.main_splitter)
        self.__sceneInput = QGraphicsScene()
        self.__sceneOutput = QGraphicsScene()
        self.__inputPanel.setEnabled(False)
        self.__outputPanel.setEnabled(False)

    def __createProgressbar(self):
        self.progressBar = LoadingProgressBar()
        self.progressBar.hide()
        self.main_layout.addWidget(self.progressBar)

    def __createMenubar(self, main_window):
        self.menubar = QMenuBar(main_window)
        main_window.setMenuBar(self.menubar)
        self.menuFile = QMenu(self.menubar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.action_open)
        self.menuFile.addAction(self.action_save)
        self.menuRecents = QMenu(self.menuFile)
        self.menuFile.addMenu(self.menuRecents)

    def __createToolbar(self, main_window):
        self.toolBar = QToolBar(main_window)
        main_window.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.toolBar.addAction(self.action_zoom)
        self.toolBar.addAction(self.action_rotate)

    def __retranslateUI(self, main_window):
        main_window.setWindowTitle(tr("Image AI Composer"))
        self.menuFile.setTitle(tr("File"))
        self.menuRecents.setTitle(tr("Open Recent Photo"))
        self.action_open.setShortcut(tr("Ctrl+O"))
        self.action_open.setToolTip(tr("Open Image"))

    def __appendFileRecents(self):
        recents = self.storage.fetchRecents()
        for recent in recents:
            action = ActionRecents(self, recent[0])
            action.setCallback(self.__loadPhoto)
            self.menuRecents.addAction(action)

    def __loadPhoto(self, image_path):
        image = self.readImageFile(image_path)
        self.displayImageInput(image)

    def __dialogOpenFile(self):
        image_path = self.launchDialogOpenFile()
        if image_path:
            self.show_message("Working image at: ", image_path)
            self.storage.insertRecent(image_path)
            self.__loadPhoto(image_path)

    def __dialogSaveFile(self):
        image_path = self.launchDialogSaveFile()
        if image_path:
            self.imageOutput().save(image_path, "PNG")

    @abstractmethod
    def showBoundingBox(self):
        pass

    @abstractmethod
    def getBoundingBox(self):
        pass

    @abstractmethod
    def onBoundingResizeEvent(self, rect):
        pass

    @abstractmethod
    def processSuperResolution(self):
        pass

    @abstractmethod
    def processSuperface(self):
        pass

    @abstractmethod
    def processSuperColorize(self):
        pass

    @abstractmethod
    def processZeroBackground(self):
        pass

    @abstractmethod
    def processLowlight(self):
        pass

    @abstractmethod
    def setCustomBackground(self):
        pass

    @abstractmethod
    def onHiresScaleChanged(self, index):
        pass

    def launchDialogOpenFile(self):
        return QFileDialog.getOpenFileName(self, 'Open Image')[0]

    def launchDialogSaveFile(self):
        return QFileDialog.getSaveFileName(self, 'Save Image')[0]

    def readImageFile(self, image_path):
        self.setImagePath(image_path)
        return utils.imageOpen(image_path)

    def blurryImage(self):
        image_working = self.imageInput().filter(ImageFilter.GaussianBlur(radius=25))
        self.displayImageOutput(image_working)

    def displayImageInput(self, image):
        self.__imageInput = image
        displayImage(image, self.__sceneInput, self.__inputPanel)

    def displayImageOutput(self, image):
        self.__imageOutput = image
        displayImage(image, self.__sceneOutput, self.__outputPanel)

    def imageOutput(self):
        return self.__imageOutput

    def imageInput(self):
        return self.__imageInput

    def imagePath(self):
        return self.__image_pat

    def setImagePath(self, image_path):
        self.__image_pat = image_path

    def inputPanel(self):
        return self.__inputPanel

    def outputPanel(self):
        return self.__outputPanel

    def sceneInput(self):
        return self.__sceneInput

    def sceneOutput(self):
        return self.__sceneOutput

    def show_message(self, title, message):
        self.statusbar.showMessage("{0} {1}".format(title, message))

    def showSettingsDialog(self):
        original = self.imageOutput()
        self.displayImageOutput(original)

    def onSliderBlurChanged(self, delta):
        image_working = self.imageInput().filter(ImageFilter.GaussianBlur(radius=delta))
        self.displayImageOutput(image_working)
