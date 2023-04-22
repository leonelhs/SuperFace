from abc import ABC
from remotetasks.remote_task import BaseRemoteTask
from toolset.BaseToolset import BaseToolset
from utils import uint8


class TaskSuperResolution(BaseRemoteTask, ABC):

    def __init__(self, parent: BaseToolset):
        super().__init__()
        self.files = dict()
        self.parent = parent

    def resource(self) -> str:
        return "super_resolution"

    def runRemoteTask(self, image):
        self.files["image_a"] = image
        self.request(self.files)

    def onRequestResponse(self, reply):
        imagen_hires = uint8(reply)
        self.parent.onRequestResponse(self.resource(), imagen_hires)

    def onRequestProgress(self, sent, total):
        self.parent.onRequestProgress(sent, total)

    def onRequestError(self, message, error):
        self.parent.onRequestError(message, error)
