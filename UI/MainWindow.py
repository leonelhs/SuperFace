from PySide6.QtCore import (QCoreApplication, QMetaObject, Signal, QThreadPool)
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (QHBoxLayout, QMenuBar,
                               QProgressBar, QStatusBar,
                               QVBoxLayout, QWidget, QMainWindow, QMenu, QFileDialog)

import utils
from UI.widgets.PhotoGrid import PhotoGrid
from Actions import new_action, ActionRecents
from Storage import Storage
from ScanWorker import ScanWorker
from UI.Tagging import Tagging


def get_line(array):
    for i in range(0, len(array), 2):
        yield array[i:i + 2]


def grid_positions(length, max_columns):
    return [(row, column) for row in range(length) for column in range(max_columns)]


def tr(label):
    return QCoreApplication.translate("MainWindow", label, None)


class MainWindow(QMainWindow):

    galleryHandler = Signal(object)

    def __init__(self):
        super().__init__()
        self.storage = None
        self.menuRecents = None
        self.menuGallery = None
        self.menuFile = None
        self.thumbnailGrid = None
        self.statusbar = None
        self.menubar = None
        self.progressBar = None
        self.widgets_layout = None
        self.central_layout = None
        self.central_widget = None

        self.actionGalleryOpen = new_action(self, "./assets/document-open.svg")
        self.actionGalleryRecents = new_action(self, "./assets/document-open.svg")

        self.actionTagFaces = new_action(self, "./assets/edit-image-face-show.svg")
        self.actionMarksFace = new_action(self, "./assets/edit-image-face-show.svg")

        self.actionGalleryTags = new_action(self, "./assets/document-open.svg")
        self.actionNewGallery = new_action(self, "./assets/document-open.svg")
        self.actionRescanGallery = new_action(self, "./assets/document-open.svg")

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.tagFaceForm = Tagging()
        self.storage = Storage()

        self.setupUi(self)

    def setupUi(self, main_window):
        self.central_widget = QWidget(main_window)
        self.central_layout = QHBoxLayout(self.central_widget)
        self.widgets_layout = QVBoxLayout()

        self.thumbnailGrid = PhotoGrid(self.central_widget)
        self.thumbnailGrid.setClickEvent(self.onActivePhotoClicked)
        self.thumbnailGrid.setDoubleClickEvent(self.onActivePhotoDoubleClicked)
        self.thumbnailGrid.setContextTagEvent(self.onContextMenuTagClicked)
        self.thumbnailGrid.setContextLandmarksEvent(self.onContextMenuLandmarksClicked)

        self.widgets_layout.addWidget(self.thumbnailGrid)

        self.progressBar = QProgressBar(self.central_widget)
        self.progressBar.setValue(0)
        self.progressBar.hide()
        self.widgets_layout.addWidget(self.progressBar)

        self.central_layout.addLayout(self.widgets_layout)

        main_window.setCentralWidget(self.central_widget)

        # Menu creation
        self.menubar = QMenuBar(main_window)
        self.createMenus()
        self.appendFileRecents()
        main_window.setMenuBar(self.menubar)

        # Statusbar creation
        self.statusbar = QStatusBar(main_window)
        main_window.setStatusBar(self.statusbar)

        self.retranslateUI(main_window)

        QMetaObject.connectSlotsByName(main_window)
        self.galleryHandler.connect(self.tagFaceForm.onGalleryHandlerMessage)
        self.tagFaceForm.taggerHandler.connect(self.onTaggerHandlerMessage)

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

        # self.menuRecents.addAction(self.actionGalleryRecents)
        # self.menuRecents.addAction(self.actionGalleryTags)

        # actions gallery
        self.menuGallery.addAction(self.actionGalleryTags)
        self.menuGallery.addAction(self.actionNewGallery)
        self.menuGallery.addAction(self.actionRescanGallery)

        self.actionGalleryOpen.triggered.connect(self.openFolderGallery)

        self.actionTagFaces.triggered.connect(self.tagFacesByName)
        self.actionMarksFace.triggered.connect(self.drawFaceLandmarks)
        # slots gallery
        self.actionGalleryTags.triggered.connect(self.list_gallery_tags)
        self.actionNewGallery.triggered.connect(self.new_tagged_gallery)
        self.actionRescanGallery.triggered.connect(self.rescanGalleryFaces)

    def openRecentGallery(self, path):
        if self.storage.open(path):
            face_list = self.storage.fetchAllFaces()
            self.thumbnailGrid.populate_grid(face_list)

    def appendFileRecents(self):
        recents = self.storage.fetchGalleries()
        for recent in recents:
            action = ActionRecents(self, recent[0])
            action.setCallback(self.openRecentGallery)
            self.menuRecents.addAction(action)

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)

    def logger(self, tag, message):
        self.statusbar.showMessage("{0} {1}".format(tag, message))

    def onActivePhotoClicked(self, event, face):
        self.logger("Working image at: ", face.face_id)

    def onActivePhotoDoubleClicked(self, event, face):
        self.logger("Double clicked ", face.face_id)

    def onContextMenuTagClicked(self, event, face):
        self.galleryHandler.emit(face)
        self.tagFaceForm.show()

    def onContextMenuLandmarksClicked(self, event, face):
        self.galleryHandler.emit(face)
        self.tagFaceForm.show()

    def tagFacesByName(self):
        matches = []
        photo = self.activeGrid.photoAtPosition(0, 0)
        known_face = photo.getEncodings()
        print(known_face)
        for face in self.storage.fetchAllFaces():
            unknown_face = face["encodings"]
            if utils.compareFaces(known_face, unknown_face):
                matches.append(face)
        self.activeGrid.populate_grid(matches)

    def list_gallery_tags(self):
        self.storage.open()
        image_list = self.storage.fetch_tags()
        self.activeGrid.populate_grid(self.activeGrid, image_list)

    def new_tagged_gallery(self):
        new_gallery_path = QFileDialog.getExistingDirectory(self, 'Create new gallery')
        self.storage.open()
        face_list = self.storage.fetch_tagged(self.active_tag)
        for face in face_list:
            shutil.move(face['path'], new_gallery_path)
            self.storage.deleteBy(face['file'])
        self.storage.close()
        self.logger("New gallery at ", new_gallery_path)

    def rescanGalleryFaces(self):
        print("Rescanning gallery folder")
        self.scanGalleryFaces(self.path)

    def openFolderGallery(self):
        path = QFileDialog.getExistingDirectory(self, 'Open gallery')
        if self.storage.open(path):
            face_list = self.storage.fetchAllFaces()
            self.thumbnailGrid.populate_grid(face_list)
        else:
            self.progressBar.show()
            self.startScanningThread(path)
        self.logger("Working gallery at: ", path)

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

    def startScanningThread(self, path):
        worker = ScanWorker(self.executeScanningWork, path)
        worker.signals.result.connect(self.scanningDone)
        worker.signals.finished.connect(self.scanningComplete)
        worker.signals.progress.connect(self.trackScanningProgress)
        self.progressBar.setValue(0)
        self.threadpool.start(worker)

    def executeScanningWork(self, path, progress_callback):
        data = []
        files = utils.scanFolderImages(path)
        count_files = len(files)
        for file in files:
            image_file = utils.getPath(path, file)
            image = utils.imageOpen(image_file)
            np_array = utils.npArray(image)
            encodings = utils.faceEncodings(np_array)
            landmarks = utils.faceLandmarks(np_array)
            thumbnail = utils.imageThumbnail(image)
            data.append((hash(path), file, thumbnail, encodings, landmarks))
            progress_callback.emit(len(data) * 100 / count_files)
        self.storage.insertFaces(data)
        return path

    def trackScanningProgress(self, progress):
        self.progressBar.setValue(progress)
        self.logger("Scanning gallery completed: ", progress)

    def scanningDone(self, path):
        self.logger("encode ", " done")
        if self.storage.open(path):
            face_list = self.storage.fetchAllFaces()
            self.thumbnailGrid.populate_grid(face_list)

    def scanningComplete(self):
        self.progressBar.hide()
        self.logger("Scanning complete ", "Done")

    def onTaggerHandlerMessage(self, message):
        print(message)
        self.logger("Tag name", message)
