import abc

from PySide6 import QtNetwork
from PySide6.QtCore import QUrl

from remotetasks import makeMultipart


class NetworkRequest(metaclass=abc.ABCMeta):

    def __init__(self):
        self.netaccess = None
        self.stream = None
        self.multiPart = None
        self.reply = None

    def uploadFile(self, data, url):
        if self.reply is None:
            self.stream = data
            self.multiPart = makeMultipart(self.stream)
            request = QtNetwork.QNetworkRequest(QUrl(url))
            self.reply = self.netaccess.post(request, self.multiPart)
            self.reply.uploadProgress.connect(self.handleUploadProgress)
            self.reply.errorOccurred.connect(self.handleError)
            self.reply.finished.connect(self.handleFinished)

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'handleFinished') and
                callable(subclass.handleFinished) and
                hasattr(subclass, 'handleUploadProgress') and
                callable(subclass.handleUploadProgress) and
                hasattr(subclass, 'handleError') and
                callable(subclass.handleError) or
                NotImplemented)

    @abc.abstractmethod
    def handleFinished(self):
        raise NotImplementedError

    @abc.abstractmethod
    def handleUploadProgress(self, sent, total):
        raise NotImplementedError

    @abc.abstractmethod
    def handleError(self):
        raise NotImplementedError
