from abc import ABC

from remotetasks.remotetask import RemoteTask


class TaskSegmentation(RemoteTask, ABC):

    def __init__(self, args):
        super().__init__(args)

    def resource(self) -> str:
        return "segment"

    def runRemoteTask(self, image: bytes):
        self.request(image)
