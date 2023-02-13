from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PySide6.QtGui import (QImage, QPixmap)
from PySide6.QtWidgets import (QHBoxLayout, QMenu, QMenuBar, QSplitter,
                               QStatusBar, QToolBar, QWidget, QFileDialog, QMainWindow)

# from AI.illuminate.lowlight import lowlight
# from AI.super_resolution import super_resolution
# from AI.zero_background import ZeroBackground
from Actions import new_action
from UI.widgets.PhotoPanel import PhotoPanel


def tr(label):
    return QCoreApplication.translate("MainWindow", label, None)


def display_image(frame, image_label):
    if type(frame) == str:
        image = QImage(frame)
        pixmap = QPixmap.fromImage(image)
        pixmap = fit_image(pixmap, image_label.size().getWidth())
        image_label.setPixmap(pixmap)
    else:
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        pixmap = fit_image(pixmap, image_label.size().getWidth())
        image_label.setPixmap(pixmap)


def fit_image(pixmap, size):
    return pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)


def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


class Enhancements(QMainWindow):
    def __init__(self, parent=None):
        super(Enhancements, self).__init__(parent)
        self.image_path = None
        self.folder_path = None
        self.inputPanel = None
        self.outputPanel = None
        self.toolBar = None
        self.statusbar = None
        self.menuFile = None
        self.menubar = None
        self.splitter = None
        self.layout = None
        self.central_widget = None

        self.image_open = new_action(self, "../assets/document-open.svg")
        self.folder_open = new_action(self, "../assets/document-open.svg")
        self.super_resolution = new_action(self, "../assets/edit-image-face-show.svg")
        self.zero_background = new_action(self, "../assets/edit-image-face-show.svg")
        self.low_light = new_action(self, "../assets/edit-image-face-show.svg")
        self.face_marks = new_action(self, "../assets/edit-image-face-show.svg")

        # self.zero = ZeroBackground()
        self.setup_ui(self)

    def setup_ui(self, main_window):
        self.central_widget = QWidget(main_window)

        self.layout = QHBoxLayout(self.central_widget)
        self.splitter = QSplitter(self.central_widget)
        self.splitter.setOrientation(Qt.Horizontal)

        self.inputPanel = PhotoPanel(self.splitter)
        self.outputPanel = PhotoPanel(self.splitter)

        self.layout.addWidget(self.splitter)

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
        self.menuFile.addAction(self.folder_open)

        self.toolBar.addAction(self.super_resolution)
        self.toolBar.addAction(self.zero_background)
        self.toolBar.addAction(self.low_light)
        self.toolBar.addAction(self.face_marks)

        self.image_open.triggered.connect(self.load_file)
        self.super_resolution.triggered.connect(self.process_image)
        self.zero_background.triggered.connect(self.process_zero)
        self.low_light.triggered.connect(self.process_light)

        self.retranslate_ui(main_window)

        QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        main_window.setWindowTitle(tr("Image AI Composer"))
        self.image_open.setText(tr("Open Image"))
        self.folder_open.setText(tr("Open Folder"))
        self.image_open.setShortcut(tr("Ctrl+O"))
        self.folder_open.setShortcut(tr("Ctrl+F"))

        self.menuFile.setTitle(tr("File"))

        self.image_open.setToolTip(tr("Open Image"))
        self.folder_open.setToolTip(tr("Open Folder"))
        self.super_resolution.setToolTip(tr("Super Resolution"))
        self.zero_background.setToolTip(tr("Zero Background"))
        self.low_light.setToolTip(tr("Low Light"))
        self.face_marks.setToolTip(tr("Face Marks"))

    def resizeEvent(self, event):
        print("resize")
        QMainWindow.resizeEvent(self, event)

    def show_message(self, title, message):
        self.statusbar.showMessage("{0} {1}".format(title, message))

    def load_file(self):
        self.image_path = QFileDialog.getOpenFileName(self, 'Open Image')[0]
        print(self.image_path)
        # self.show_message("Working image at: ", self.image_path)
        # self.inputPanel.appendPhoto(self.image_path)

    def process_image(self):
        pass
        image_result = super_resolution(self.image_path)
        self.show_message("Super resolution at: ", image_result)
        display_image(image_result, self.outputPanel.face)

    def process_zero(self):
        image_result = self.zero.zero_background(self.image_path)
        self.show_message("Zero background at: ", image_result)
        display_image(image_result, self.outputPanel.face)

    def process_light(self):
        image_result = lowlight(self.image_path)
        self.show_message("Light enhancement at: ", image_result)
        display_image(image_result, self.outputPanel.face)

