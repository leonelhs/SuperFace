from remotetasks.remotetask import RemoteTask, openfile, decodeImage


class TaskSegmentation(RemoteTask):

    def __init__(self):
        super().__init__()
        self.resource = "segment"

    def runRemoteTask(self, image_path):
        image = openfile(image_path)
        overlay, colormap, mask = self.request(image)
        return decodeImage(overlay)
