from abc import abstractmethod

from ScanWorker import ScanWorker


class PhotoScanner:

    def __init__(self):
        self.storage = None
        self.threadpool = None
        self.progressBar = None
        self.thumbnailGrid = None

    def startScanningThread(self, path):
        worker = ScanWorker(self.executeScanningWork, path)
        worker.signals.result.connect(self.scanningDone)
        worker.signals.finished.connect(self.scanningComplete)
        worker.signals.progress.connect(self.trackScanningProgress)
        self.progressBar.setValue(0)
        self.threadpool.start(worker)

    @abstractmethod
    def executeScanningWork(self, path, progress_callback):
        pass

    @abstractmethod
    def logger(self, param, progress):
        pass

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


