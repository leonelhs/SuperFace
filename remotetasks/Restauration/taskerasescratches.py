from abc import ABC
from remotetasks.remote_task import BaseRemoteTask
from toolset.BaseToolset import BaseToolset
from utils import uint8


class TaskEraseScratches(BaseRemoteTask, ABC):

    def __init__(self, parent: BaseToolset):
        super().__init__()
        self.files = dict()
        self.parent = parent

    def resource(self) -> str:
        return "erase_scratches"

    def runRemoteTask(self, images):
        self.files["image_a"], self.files["image_b"] = images
        self.request(self.files)

    def onRequestResponse(self, reply):
        transformed_image, scratches_mask_image = reply
        reply = uint8(transformed_image), uint8(scratches_mask_image)
        self.parent.onRequestResponse(self.resource(), reply)

    def onRequestProgress(self, sent, total):
        self.parent.onRequestProgress(sent, total)

    def onRequestError(self, message, error):
        self.parent.onRequestError(message, error)
