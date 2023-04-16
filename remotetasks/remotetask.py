import abc
import json
from PySide6 import QtNetwork
from remotetasks.networkrequest import NetworkRequest

endpoint = 'http://127.0.0.1:{0}/{1}'
port = 5001


class RemoteTask(NetworkRequest, metaclass=abc.ABCMeta):
    def __init__(self):
        super().__init__()
        self.netaccess = QtNetwork.QNetworkAccessManager()

    def endpoint(self):
        return endpoint.format(port, self.resource())

    def request(self, data):
        self.uploadFile(data, self.endpoint())

    def handleUploadProgress(self, sent, total):
        self.onRequestProgress(sent, total)

    def handleFinished(self):
        reply = self.reply.readAll()
        reply = json.loads(str(reply, "utf-8"))
        self.onRequestResponse(reply)
        self.multiPart.deleteLater()
        self.reply.deleteLater()
        self.reply = None

    def handleError(self):
        self.onRequestError(self.reply.errorString(), self.reply.error())

    @abc.abstractmethod
    def resource(self) -> str:
        raise NotImplementedError

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
