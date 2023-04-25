import abc
import json

from PySide6 import QtNetwork

from remotetasks.network_request import NetworkRequest

BAD_CONNECTION = "Error, remote host seems down."


class RemoteTask(NetworkRequest, metaclass=abc.ABCMeta):
    def __init__(self):
        super().__init__()
        self.reply = None
        self.service = None
        self.netaccess = QtNetwork.QNetworkAccessManager()

    def handleUploadProgress(self, sent, total):
        self.onRequestProgress(sent, total)

    def clearRequest(self):
        self.multiPart.deleteLater()
        self.reply.deleteLater()
        self.reply = None

    def handleFinished(self):
        reply = self.reply.readAll()
        try:
            reply = json.loads(str(reply, "utf-8"))
            self.onRequestResponse(reply, self.service.api)
        except json.decoder.JSONDecodeError:
            self.onRequestError(reply, "bad-json")
        finally:
            self.clearRequest()

    def handleError(self):
        self.onRequestError(self.reply.errorString(), self.reply.error())

    def runRemoteTask(self, file, service):
        self.service = service
        self.uploadFile(file, self.service.resource())

    @abc.abstractmethod
    def onRequestResponse(self, reply, api):
        raise NotImplementedError

    @abc.abstractmethod
    def onRequestProgress(self, sent, total):
        raise NotImplementedError

    @abc.abstractmethod
    def onRequestError(self, message, error):
        raise NotImplementedError
