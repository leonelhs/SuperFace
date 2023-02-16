from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            Qt, QThreadPool)
from PySide6.QtWidgets import (QMenuBar,
                               QSplitter, QStatusBar,
                               QToolBox, QVBoxLayout, QWidget, QMainWindow, QMenu, QToolBar, QFileDialog,
                               QGraphicsScene)

import utils
from AI.TaskLowLight import TaskLowLight
from AI.TaskSuperFace import TaskSuperFace
from AI.TaskZeroBackground import TaskZeroBackground
from Actions import Action, ActionRecents
from Storage import Storage
from UI.widgets.ImageGraphicsView import ImageGraphicsView
from UI.widgets.LoadingProgressBar import LoadingProgressBar


def tr(label):
    return QCoreApplication.translate("MainWindow", label, None)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.image_result = None
        self.threadpool = None
        self.sceneOutput = None
        self.sceneInput = None
        self.lowLight = None
        self.storage = None
        self.zeroBackground = None
        self.superFace = None
        self.image_path = None
        self.image_is_fitted = None
        self.working_image = None
        self.toolBar = None
        self.menuFile = None
        self.menuRecents = None
        self.statusbar = None
        self.menubar = None
        self.progressBar = None
        self.outputPanel = None
        self.inputPanel = None
        self.panel_splitter = None
        self.page_4 = None
        self.page_3 = None
        self.toolBox = None
        self.main_splitter = None
        self.main_layout = None
        self.central_widget = None

        self.action_open = Action(self, "Open", "fa.folder-open")
        self.action_save = Action(self, "Save", "fa.save")
        self.action_zoom = Action(self, "Zoom", "ri.zoom-in-line")
        self.action_rotate = Action(self, "Rotate", "mdi6.rotate-right-variant")
        self.action_super_resolution = Action(self, "Super Resolution", "mdi.face")
        self.action_zero_background = Action(self, "Zero Background", "mdi.eraser")
        self.action_low_light = Action(self, "Light Enhancement", "ei.adjust")
        self.action_background = Action(self, "Custom Background", "ph.selection-background")

        self.setupUi(self)

    def setupUi(self, main_window):
        self.central_widget = QWidget(main_window)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_splitter = QSplitter(self.central_widget)
        self.main_splitter.setOrientation(Qt.Horizontal)
        self.toolBox = QToolBox(self.main_splitter)
        self.page_3 = QWidget()
        self.page_3.setGeometry(QRect(0, 0, 91, 427))
        self.toolBox.addItem(self.page_3, u"Page 1")
        self.page_4 = QWidget()
        self.page_4.setGeometry(QRect(0, 0, 91, 427))
        self.toolBox.addItem(self.page_4, u"Page 2")
        self.main_splitter.addWidget(self.toolBox)
        self.panel_splitter = QSplitter(self.main_splitter)
        self.panel_splitter.setOrientation(Qt.Horizontal)

        self.inputPanel = ImageGraphicsView(self.panel_splitter)
        self.panel_splitter.addWidget(self.inputPanel)

        self.outputPanel = ImageGraphicsView(self.panel_splitter)
        self.panel_splitter.addWidget(self.outputPanel)
        self.sceneInput = QGraphicsScene()
        self.sceneOutput = QGraphicsScene()

        self.main_splitter.addWidget(self.panel_splitter)

        self.main_layout.addWidget(self.main_splitter)

        self.progressBar = LoadingProgressBar()
        self.progressBar.hide()
        self.main_layout.addWidget(self.progressBar)

        main_window.setCentralWidget(self.central_widget)
        self.menubar = QMenuBar(main_window)
        self.menubar.setGeometry(QRect(0, 0, 800, 26))
        main_window.setMenuBar(self.menubar)
        self.menuFile = QMenu(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.action_open)
        self.menuFile.addAction(self.action_save)

        self.menuRecents = QMenu(self.menuFile)
        self.menuFile.addMenu(self.menuRecents)
        self.menuRecents.setTitle(tr("Open Recent Photo"))

        self.statusbar = QStatusBar(main_window)
        main_window.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(main_window)

        main_window.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBox.setCurrentIndex(1)

        self.toolBar.addAction(self.action_zoom)
        self.toolBar.addAction(self.action_rotate)

        self.toolBar.addAction(self.action_super_resolution)
        self.toolBar.addAction(self.action_zero_background)
        self.toolBar.addAction(self.action_low_light)
        self.toolBar.addAction(self.action_background)

        self.action_open.setOnClickEvent(self.launchDialogOpenfile)
        self.action_save.setOnClickEvent(self.saveImageFile)
        self.action_background.setOnClickEvent(self.setCustomBackground)

        self.action_zoom.setOnClickEvent(self.imageZoom)
        self.action_rotate.setOnClickEvent(self.imageFlip)

        self.action_super_resolution.setOnClickEvent(self.processSuperResolution)
        self.action_zero_background.setOnClickEvent(self.processZeroBackground)
        self.action_low_light.setOnClickEvent(self.processLowlight)

        self.retranslateUI(main_window)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        args = (self.threadpool, self.enhanceDone, self.enhanceComplete, self.trackEnhanceProgress)

        self.storage = Storage()
        self.superFace = TaskSuperFace(*args)
        self.zeroBackground = TaskZeroBackground(*args)
        self.lowLight = TaskLowLight(*args)
        self.appendFileRecents()

        QMetaObject.connectSlotsByName(main_window)

    def retranslateUI(self, main_window):
        main_window.setWindowTitle(tr("Image AI Composer"))
        self.action_open.setShortcut(tr("Ctrl+O"))
        self.menuFile.setTitle(tr("File"))

        self.action_open.setToolTip(tr("Open Image"))
        self.action_super_resolution.setToolTip(tr("Super Resolution"))
        self.action_zero_background.setToolTip(tr("Zero Background"))
        self.action_low_light.setToolTip(tr("Low Light"))

    def appendFileRecents(self):
        recents = self.storage.fetchRecents()
        for recent in recents:
            action = ActionRecents(self, recent[0])
            action.setCallback(self.loadPhoto)
            self.menuRecents.addAction(action)

    def show_message(self, title, message):
        self.statusbar.showMessage("{0} {1}".format(title, message))

    def imageZoom(self):
        pass

    def imageFlip(self):
        pass

    def loadPhoto(self, image_path):
        self.working_image = utils.imageOpen(image_path)
        picture = utils.pil2Pixmap(self.working_image)
        self.sceneInput.addPixmap(picture)
        self.inputPanel.setScene(self.sceneInput)

    def launchDialogOpenfile(self):
        self.image_path = QFileDialog.getOpenFileName(self, 'Open Image')[0]
        if self.image_path:
            self.show_message("Working image at: ", self.image_path)
            self.storage.insertRecent(self.image_path)
            self.loadPhoto(self.image_path)

    def saveImageFile(self):
        image_path = QFileDialog.getSaveFileName(self, 'Save Image')[0]
        if image_path:
            self.show_message("Save image at: ", image_path)
            self.image_result.save(image_path, "PNG")

    def processSuperResolution(self):
        self.show_message("Super resolution at: ", self.image_path)
        self.progressBar.show()
        self.superFace.startEnhanceThread(self.working_image)

    def processZeroBackground(self):
        self.show_message("Zeo background at: ", self.image_path)
        self.progressBar.show()
        self.zeroBackground.startEnhanceThread(self.working_image)

    def setCustomBackground(self):
        image_path = QFileDialog.getOpenFileName(self, 'Open Image')[0]
        if image_path:
            background = utils.imageOpen(image_path)
            self.pasteForeground(background)

    def pasteForeground(self, background):
        foreground = self.image_result
        x = (background.size[0] - foreground.size[0]) / 2
        y = (background.size[1] - foreground.size[1]) / 2
        box = (x, y, foreground.size[0] + x, foreground.size[1] + y)
        crop = background.crop(box)
        final_image = crop.copy()
        # put the foreground in the centre of the background
        paste_box = (0, final_image.size[1] - foreground.size[1], final_image.size[0], final_image.size[1])
        final_image.paste(foreground, paste_box, mask=foreground)
        image = utils.pil2Pixmap(final_image)
        self.sceneOutput.addPixmap(image)
        self.outputPanel.setScene(self.sceneOutput)

    def processLowlight(self):
        self.show_message("Light enhancement at: ", self.image_path)
        self.progressBar.show()
        self.lowLight.startEnhanceThread(self.working_image)

    def trackEnhanceProgress(self, progress):
        self.progressBar.setValue(progress)
        self.show_message("Scanning gallery completed: ", progress)

    def enhanceDone(self, image_result):
        self.show_message("finish ", " done")
        self.image_result = image_result
        image = utils.pil2Pixmap(image_result)
        self.sceneOutput.addPixmap(image)
        self.outputPanel.setScene(self.sceneOutput)

    def enhanceComplete(self):
        self.progressBar.hide()
        self.show_message("Scanning complete ", "Done")
