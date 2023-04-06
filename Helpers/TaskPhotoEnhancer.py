from abc import abstractmethod

from Helpers.EnhanceWorker import EnhanceWorker


class TaskPhotoEnhancer:

    def __init__(self, args):
        self.threadpool = args[0]
        self.enhanceDone = args[1]
        self.enhanceComplete = args[2]
        self.trackEnhanceProgress = args[3]

    def startEnhanceThread(self, image):
        worker = EnhanceWorker(self.executeEnhanceWork, image)
        worker.signals.result.connect(self.enhanceDone)
        worker.signals.finished.connect(self.enhanceComplete)
        worker.signals.progress.connect(self.trackEnhanceProgress)
        self.threadpool.start(worker)

    @abstractmethod
    def executeEnhanceWork(self, image, progress_callback):
        pass
