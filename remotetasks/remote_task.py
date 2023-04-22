from abc import ABC
from remotetasks.base_remote_task import BaseRemoteTask
from remotetasks.service import Service
from toolset.BaseToolset import BaseToolset
from utils import uint8


class WrongImageFormat(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'An image was expected'


class RemoteTask(BaseRemoteTask, ABC):

    def __init__(self, parent: BaseToolset):
        super().__init__()
        self.parent = parent
        self.service = None

    def setService(self, service: Service):
        self.service = service

    def runRemoteTask(self, files: dict):
        self.request(files, self.service.resource())

    def onRequestResponse(self, reply):
        try:
            reply = uint8(reply)
            self.parent.onRequestResponse(self.service.api, reply)
        except int() as error:
            print(reply)
            print(str(error))

    def onRequestProgress(self, sent, total):
        self.parent.onRequestProgress(sent, total)

    def onRequestError(self, message, error):
        self.parent.onRequestError(message, error)
