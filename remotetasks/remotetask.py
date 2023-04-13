import json
from abc import abstractmethod
from PySide6 import QtNetwork
from uploader import Uploader

endpoint = 'http://127.0.0.1:{0}/{1}'
port = 5000


class RemoteTask(Uploader):
    def __init__(self, args):
        super().__init__()
        self.onRequestResponse = args[0]
        self.onRequestProgress = args[1]
        self.onRequestError = args[2]
        self.netaccess = QtNetwork.QNetworkAccessManager()
        self.resource = None

    def endpoint(self):
        return endpoint.format(port, self.resource)

    def request(self, data):
        self.upload(data, self.endpoint())

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

    @abstractmethod
    def runRemoteTask(self, image_path):
        pass
