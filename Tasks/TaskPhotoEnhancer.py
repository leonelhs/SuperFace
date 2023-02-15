from abc import abstractmethod

from Tasks.EnhanceWorker import EnhanceWorker
from Face import faceBuild


class TaskPhotoEnhancer:

    def __init__(self):
        self.threadpool = None
        self.progressBar = None
        self.panelOutput = None

    def startEnhanceThread(self, image):
        worker = EnhanceWorker(self.executeEnhanceWork, image)
        worker.signals.result.connect(self.enhanceDone)
        worker.signals.finished.connect(self.enhanceComplete)
        worker.signals.progress.connect(self.trackEnhanceProgress)
        self.progressBar.setValue(0)
        self.threadpool.start(worker)

    @abstractmethod
    def executeEnhanceWork(self, image, progress_callback):
        pass

    @abstractmethod
    def logger(self, param, progress):
        pass

    def trackEnhanceProgress(self, progress):
        self.progressBar.setValue(progress)
        self.logger("Scanning gallery completed: ", progress)

    def enhanceDone(self, image_result):
        self.logger("finish ", " done")
        face = faceBuild(image_result)
        self.panelOutput.appendPhoto(face)

    def enhanceComplete(self):
        self.progressBar.hide()
        self.logger("Scanning complete ", "Done")
