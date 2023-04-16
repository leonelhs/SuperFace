from remotetasks.Restauration.taskerasescratches import TaskEraseScratches
from remotetasks.Restauration.taskmaskscratches import TaskMaskScratches
from toolset.BaseToolset import BaseToolset


class ToolsetScratches(BaseToolset):

    def __init__(self, parent):
        super().__init__(parent)
        self.taskMaskScratches = None
        self.taskEraseScratches = None
        self.maskIsReady = False
        self.initTool()
        self.buildPage()

    def name(self):
        return "scratches"

    def buildPage(self):
        self.addPage("Erase Scratches")
        self.addButton("Parse face", self.processParseFace)
        self.addButton("Erase scratches", self.processEraseScratches)

    def initTool(self):
        self.taskMaskScratches = TaskMaskScratches(self)
        self.taskEraseScratches = TaskEraseScratches(self)

    def processParseFace(self):
        if self.parent.twinViewer.left.isEnabled():
            self.preInit("Parsing face")
            image = self.parent.twinViewer.left.bytes()
            self.original = image[:]
            self.taskMaskScratches.runRemoteTask(image)
        else:
            raise TypeError("No image loaded")

    def processEraseScratches(self):
        if self.maskIsReady:
            self.preInit("Erasing scratches")
            image_transformed = self.parent.twinViewer.left.bytes()
            image_mask = self.parent.twinViewer.right.bytes()
            self.taskEraseScratches.runRemoteTask((image_transformed, image_mask))
        else:
            raise TypeError("Mask is not ready")

    def onRequestResponse(self, resource, reply):

        if resource == "mask_scratches":
            transformed_image, scratches_mask_image = reply
            self.parent.twinViewer.left.display(transformed_image)
            self.parent.twinViewer.right.display(scratches_mask_image)
            self.parent.progressBar.hide()
            self.maskIsReady = True

        if resource == "erase_scratches":
            image_restored, image_scratches = reply
            self.parent.twinViewer.left.display(image_restored)
            self.parent.twinViewer.right.display(image_scratches)
            self.parent.progressBar.hide()

