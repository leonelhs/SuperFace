import abc

from PySide6 import QtNetwork
from PySide6.QtCore import QUrl
from PySide6.QtNetwork import QNetworkRequest, QHttpMultiPart


def makeMultipart(data):
    multiPart = QtNetwork.QHttpMultiPart(QHttpMultiPart.ContentType.FormDataType)
    file_data = QtNetwork.QHttpPart()
    file_data.setHeader(QNetworkRequest.ContentDispositionHeader, 'form-data; name="image"; filename="data"')
    file_data.setHeader(QNetworkRequest.ContentTypeHeader, 'application/octet-stream')
    file_data.setBody(data)
    multiPart.append(file_data)
    return multiPart


def construct_multipart(files):
    multiPart = QtNetwork.QHttpMultiPart(QHttpMultiPart.ContentType.FormDataType)
    for key, data in files.items():
        imagePart = QtNetwork.QHttpPart()
        imagePart.setHeader(QNetworkRequest.ContentDispositionHeader,
                            'form-data; name="%s"; filename="%s"' % (key, key))
        imagePart.setHeader(QNetworkRequest.ContentTypeHeader, 'application/octet-stream')
        imagePart.setBody(data)
        multiPart.append(imagePart)
    return multiPart


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
