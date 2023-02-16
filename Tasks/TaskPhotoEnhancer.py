from abc import abstractmethod

from Tasks.EnhanceWorker import EnhanceWorker


class TaskPhotoEnhancer:

    def __init__(self, threadpool, enhanceDone, enhanceComplete, trackEnhanceProgress):
        self.threadpool = threadpool
        self.enhanceDone = enhanceDone
        self.enhanceComplete = enhanceComplete
        self.trackEnhanceProgress = trackEnhanceProgress

    def startEnhanceThread(self, image):
        worker = EnhanceWorker(self.executeEnhanceWork, image)
        worker.signals.result.connect(self.enhanceDone)
        worker.signals.finished.connect(self.enhanceComplete)
        worker.signals.progress.connect(self.trackEnhanceProgress)
        self.threadpool.start(worker)

    @abstractmethod
    def executeEnhanceWork(self, image, progress_callback):
        pass
