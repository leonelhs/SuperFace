import abc

from Helpers.EnhanceWorker import EnhanceWorker


class LongTask:

    def __init__(self):
        self.threadpool = None

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'threadpool') and
                hasattr(subclass, 'executeLongTask') and
                callable(subclass.executeLongTask) and
                hasattr(subclass, 'trackTaskProgress') and
                callable(subclass.trackTaskProgress) and
                hasattr(subclass, 'taskDone') and
                callable(subclass.taskDone) and
                hasattr(subclass, 'taskComplete') and
                callable(subclass.taskComplete) or
                NotImplemented)

    def startThread(self, image):
        worker = EnhanceWorker(self.executeLongTask, image)
        worker.signals.result.connect(self.taskDone)
        worker.signals.finished.connect(self.taskComplete)
        worker.signals.progress.connect(self.trackTaskProgress)
        self.threadpool.start(worker)

    @abc.abstractmethod
    def executeLongTask(self, image, progress_callback):
        raise NotImplementedError

    @abc.abstractmethod
    def trackTaskProgress(self, progress):
        raise NotImplementedError

    @abc.abstractmethod
    def taskDone(self, image_result):
        raise NotImplementedError

    @abc.abstractmethod
    def taskComplete(self):
        raise NotImplementedError
