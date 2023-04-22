import abc
import json
from PySide6 import QtNetwork
from remotetasks.network_request import NetworkRequest


class BaseRemoteTask(NetworkRequest, metaclass=abc.ABCMeta):
    def __init__(self):
        super().__init__()
        self.reply = None
        self.netaccess = QtNetwork.QNetworkAccessManager()

    def request(self, data, service):
        self.uploadFile(data, service)

    def handleUploadProgress(self, sent, total):
        self.onRequestProgress(sent, total)

    def handleFinished(self):
        reply = self.reply.readAll()
        try:
            reply = json.loads(str(reply, "utf-8"))
            self.onRequestResponse(reply)
            self.multiPart.deleteLater()
            self.reply.deleteLater()
            self.reply = None
        except json.decoder.JSONDecodeError:
            self.onRequestError(reply, "bad-json")

    def handleError(self):
        self.onRequestError(self.reply.errorString(), self.reply.error())

    @abc.abstractmethod
    def runRemoteTask(self, image):
        raise NotImplementedError

    @abc.abstractmethod
    def onRequestResponse(self, reply):
        raise NotImplementedError

    @abc.abstractmethod
    def onRequestProgress(self, sent, total):
        raise NotImplementedError

    @abc.abstractmethod
    def onRequestError(self, message, error):
        raise NotImplementedError
