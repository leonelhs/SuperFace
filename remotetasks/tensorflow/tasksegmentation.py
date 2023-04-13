from remotetasks.remotetask import RemoteTask


class TaskSegmentation(RemoteTask):

    def __init__(self, args):
        super().__init__(args)
        self.resource = "segment"

    def runRemoteTask(self, image: bytes):
        self.request(image)
