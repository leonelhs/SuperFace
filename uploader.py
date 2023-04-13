import abc

from PySide6 import QtNetwork
from PySide6.QtCore import QUrl
from PySide6.QtNetwork import QNetworkRequest, QHttpMultiPart


def makeMultipart(data):
    multiPart = QtNetwork.QHttpMultiPart(QHttpMultiPart.ContentType.FormDataType)
    imagePart = QtNetwork.QHttpPart()
    imagePart.setHeader(QNetworkRequest.ContentDispositionHeader, 'form-data; name="file"; filename="data"')
    imagePart.setHeader(QNetworkRequest.ContentTypeHeader, 'application/octet-stream')
    imagePart.setBody(data)
    multiPart.append(imagePart)
    return multiPart


class Uploader(metaclass=abc.ABCMeta):

    def __init__(self):
        self.netaccess = None
        self.stream = None
        self.multiPart = None
        self.reply = None

    def upload(self, data, url):
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
                callable(subclass.handleUploadProgress) or
                hasattr(subclass, 'handleError') and
                callable(subclass.handleError) or
                NotImplemented)

    @abc.abstractmethod
    def handleFinished(self, finish):
        raise NotImplementedError

    @abc.abstractmethod
    def handleUploadProgress(self, sent, total):
        raise NotImplementedError

    @abc.abstractmethod
    def handleError(self):
        raise NotImplementedError
