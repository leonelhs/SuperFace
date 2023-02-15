import pickle
import shutil

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt, QThreadPool, Signal)
from PySide6.QtGui import (QPainter, QColor)
from PySide6.QtWidgets import (QHBoxLayout, QMenu, QMenuBar, QSplitter,
                               QStatusBar, QToolBar, QWidget, QFileDialog, QMainWindow, QProgressBar, QVBoxLayout)

import utils
from Actions import new_action
from Storage import Storage
from Tasks.EnhanceWorker import EnhanceWorker
from thumbnail_grid import ThumbnailGrid
from UI.Tagging import Tagging


def tr(label):
    return QCoreApplication.translate("MainWindow", label, None)


def grid_positions(length, max_columns):
    return [(row, column) for row in range(length) for column in range(max_columns)]


def populate_thumbnails_grid(panel, thumbnails, max_columns=5):
    panel.clearPhotos()
    positions = grid_positions(len(thumbnails), max_columns)
    for position, thumbnail in zip(positions, thumbnails):
        panel.appendThumbnail(thumbnail, position)


def get_line(array):
    for i in range(0, len(array), 2):
        yield array[i:i + 2]


def serialize(data):
    return pickle.dumps(data, protocol=5)


class MainWindow(QMainWindow):

    galleryHandler = Signal(object)

    def __init__(self):
        super().__init__()
        self.tagFaceForm = None
        self.progressBar = None
        self.loadingLabel = None
        self.loaderLayout = None
        self.face_list = None
        self.menuRecents = None
        self.menuGallery = None
        self.faceDetect = None
        self.dbGallery = None

        self.passiveGrid = None
        self.activeGrid = None

        self.active_tag = None

        self.toolBar = None
        self.statusbar = None
        self.menuFile = None
        self.menubar = None
        self.splitter = None
        self.layout = None
        self.central_widget = None

        self.actionGalleryOpen = new_action(self, "../assets/document-open.svg")
        self.actionGalleryRecents = new_action(self, "../assets/document-open.svg")

        self.actionTagFaces = new_action(self, "../assets/edit-image-face-show.svg")
        self.actionMarksFace = new_action(self, "../assets/edit-image-face-show.svg")

        self.actionGalleryTags = new_action(self, "../assets/document-open.svg")
        self.actionNewGallery = new_action(self, "../assets/document-open.svg")
        self.actionRescanGallery = new_action(self, "../assets/document-open.svg")

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.tagFaceForm = Tagging()

        self.setupUI(self)

    def setupUI(self, main_window):
        self.central_widget = QWidget(main_window)

        self.layout = QVBoxLayout(self.central_widget)
        self.splitter = QSplitter(self.central_widget)
        self.splitter.setOrientation(Qt.Horizontal)

        self.passiveGrid = ThumbnailGrid(self.splitter)
        self.activeGrid = ThumbnailGrid(self.splitter)

        self.passiveGrid.setClickEvent(self.onPassivePhotoClicked)
        self.passiveGrid.setDoubleClickEvent(self.onPassivePhotoDoubleClicked)
        self.activeGrid.setClickEvent(self.onActivePhotoClicked)

        self.layout.addWidget(self.splitter)

        self.loaderLayout = QHBoxLayout()
        self.progressBar = QProgressBar(self.central_widget)
        self.progressBar.setValue(0)
        self.progressBar.hide()
        self.loaderLayout.addWidget(self.progressBar)
        self.layout.addLayout(self.loaderLayout)

        main_window.setCentralWidget(self.central_widget)
        self.menubar = QMenuBar(main_window)

        self.menubar.setGeometry(QRect(0, 0, 800, 24))

        self.createMenus()

        main_window.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(main_window)

        main_window.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(main_window)
        self.toolBar.addAction(self.actionTagFaces)
        self.toolBar.addAction(self.actionMarksFace)

        main_window.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.retranslateUI(main_window)

        QMetaObject.connectSlotsByName(main_window)

        self.galleryHandler.connect(self.tagFaceForm.onGalleryHandlerMessage)
        self.tagFaceForm.taggerHandler.connect(self.onTaggerHandlerMessage)

    def createMenus(self):
        # Menus
        self.menuFile = QMenu(self.menubar)
        self.menuGallery = QMenu(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuGallery.menuAction())
        # actions file
        self.menuFile.addAction(self.actionGalleryOpen)

        self.menuRecents = QMenu(self.menuFile)
        self.menuFile.addMenu(self.menuRecents)

        self.menuRecents.addAction(self.actionGalleryRecents)
        self.menuRecents.addAction(self.actionGalleryTags)

        # actions gallery
        self.menuGallery.addAction(self.actionGalleryTags)
        self.menuGallery.addAction(self.actionNewGallery)
        self.menuGallery.addAction(self.actionRescanGallery)

        self.actionGalleryOpen.triggered.connect(self.openFolderGallery)

        self.actionGalleryRecents.triggered.connect(self.open_politics)

        self.actionTagFaces.triggered.connect(self.tagFacesByName)
        self.actionMarksFace.triggered.connect(self.drawFaceLandmarks)
        # slots gallery
        self.actionGalleryTags.triggered.connect(self.list_gallery_tags)
        self.actionNewGallery.triggered.connect(self.new_tagged_gallery)
        self.actionRescanGallery.triggered.connect(self.rescanGalleryFaces)

    def retranslateUI(self, main_window):
        main_window.setWindowTitle(tr("Image AI Composer"))
        self.menuFile.setTitle(tr("File"))
        self.menuRecents.setTitle(tr("Open Recent Gallery"))
        self.actionGalleryOpen.setText(tr("Open Gallery"))
        self.actionGalleryOpen.setToolTip(tr("Open Gallery"))
        self.actionGalleryOpen.setShortcut(tr("Ctrl+O"))

        self.actionGalleryRecents.setText("politica")

        self.menuGallery.setTitle(tr("Gallery"))
        self.actionRescanGallery.setText(tr("Rescan gallery"))
        self.actionGalleryTags.setText(tr("Faces tagged"))
        self.actionNewGallery.setText(tr("New gallery"))

        self.actionTagFaces.setToolTip(tr("Tag Faces"))

    def resizeEvent(self, event):
        print("resize")
        QMainWindow.resizeEvent(self, event)

    def logger(self, tag, message):
        self.statusbar.showMessage("{0} {1}".format(tag, message))

    def onPassivePhotoClicked(self, event, face):
        self.activeGrid.clearPhotos()
        # self.activeGrid.appendPhoto(face)
        self.logger("Working image at: ", face["file"])

    def onPassivePhotoDoubleClicked(self, event, face):
        print("type(face)")
        print(type(face))
        self.galleryHandler.emit(face)
        self.tagFaceForm.show()

    def onActivePhotoClicked(self, event, face):
        self.active_tag = face["match"]
        self.logger("Active tag: ", self.active_tag)

    def scanGalleryFaces(self, gallery_path):
        self.passiveGrid.clearPhotos()
        if self.dbGallery.exists():
            print("Open gallery folder")
            self.dbGallery.open()
            self.face_list = self.dbGallery.fetchAllFaces()
            populate_thumbnails_grid(self.passiveGrid, self.face_list)
        else:
            print("Encoding gallery folder...")
            self.startEncodingThread(gallery_path)

    def tagFacesByName(self):
        matches = []
        photo = self.activeGrid.photoAtPosition(0, 0)
        known_face = photo.getEncodings()
        print(known_face)
        for face in self.dbGallery.fetchAllFaces():
            unknown_face = face["encodings"]
            if utils.compareFaces(known_face, unknown_face):
                matches.append(face)
        populate_thumbnails_grid(self.activeGrid, matches)

    def list_gallery_tags(self):
        self.dbGallery.open()
        self.activeGrid.clearPhotos()
        image_list = self.dbGallery.fetch_tags()
        populate_thumbnails_grid(self.activeGrid, image_list)

    def new_tagged_gallery(self):
        new_gallery_path = QFileDialog.getExistingDirectory(self, 'Create new gallery')
        self.dbGallery.open()
        face_list = self.dbGallery.fetch_tagged(self.active_tag)
        for face in face_list:
            shutil.move(face['path'], new_gallery_path)
            self.dbGallery.deleteBy(face['file'])
        self.dbGallery.close()
        self.logger("New gallery at ", new_gallery_path)

    def rescanGalleryFaces(self):
        print("Rescanning gallery folder")
        self.scanGalleryFaces(self.gallery_path)

    def openFolderGallery(self):
        gallery_path = QFileDialog.getExistingDirectory(self, 'Open gallery')
        self.dbGallery = Storage(gallery_path)
        self.scanGalleryFaces(gallery_path)
        self.logger("Working gallery at: ", gallery_path)

    def drawFaceLandmarks(self):
        photo = self.activeGrid.photoAtPosition(0, 0)
        pixmap = photo.getPixmap()
        painter = QPainter(pixmap)
        painter.setPen(QColor(255, 255, 0))
        for marks in photo.getLandmarks():
            for positions in marks:
                for position in get_line(marks[positions]):
                    if len(position) > 1:
                        painter.drawLine(*position[0], *position[1])
        photo.setPixmap(pixmap)

    def open_politics(self):
        # self.scanGalleryFaces("/home/leonel/politica")
        self.tagFaceForm.show()
        # self.raise_()

    def startEncodingThread(self, gallery_path):
        worker = EnhanceWorker(self.executeEncodings, gallery_path)
        worker.signals.result.connect(self.encodingDone)
        worker.signals.finished.connect(self.scanningComplete)
        worker.signals.progress.connect(self.trackScanningProgress)
        self.threadpool.start(worker)

    def executeEncodings(self, gallery_path, progress_callback):
        data = []
        self.progressBar.show()
        files = utils.scanFolderImages(gallery_path)
        count_files = len(files)
        positions = grid_positions(count_files, 5)
        for position, file in zip(positions, files):
            image_file = utils.getPath(gallery_path, file)
            image = utils.imageOpen(image_file)
            np_array = utils.npArray(image)
            encodings = utils.faceEncodings(np_array)
            landmarks = utils.faceLandmarks(np_array)
            thumbnail = utils.imageThumbnail(image)
            data.append((file, thumbnail, encodings, landmarks))
            progress_callback.emit(len(data) * 100 / count_files)
        self.dbGallery.open()
        self.dbGallery.insertFaces(data)
        self.dbGallery.close()
        return gallery_path

    def trackScanningProgress(self, progress):
        self.progressBar.setValue(progress)
        self.logger("Scanning gallery completed: ", progress)

    def encodingDone(self, gallery_path):
        self.logger("encode ", " done")
        self.scanGalleryFaces(gallery_path)

    def scanningComplete(self):
        self.progressBar.hide()
        self.logger("Scanning complete ", "Done")

    def onTaggerHandlerMessage(self, message):
        print("from frame")
        self.logger("Tag name", message)
        # self.raise_()

