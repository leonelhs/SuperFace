from UI.widgets.mini_form import MiniForm
from remotetasks.remote_task import RemoteTask
from remotetasks.service import Service
from toolset.BaseToolset import BaseToolset

service = Service()
service.address = "http://127.0.0.1"
service.port = "5001"


class ToolsetEnhancer(BaseToolset):

    def __init__(self, parent):
        super().__init__(parent)
        self.include_faces = None
        self.taskImageColorizer = None
        self.taskMaskScratches = None
        self.taskEraseScratches = None
        self.taskSuperResolution = None
        self.maskIsReady = False
        self.remoteTask = None
        self.initTool()
        self.buildPage()

    def name(self):
        return "scratches"

    def buildPage(self):
        self.addPage("Enhancements")
        mini_form = self.createWidget(MiniForm)
        button = mini_form.addButton("Enhance resolution")
        self.include_faces = mini_form.addCheckbox("Include faces")
        button.clicked.connect(self.processSuperResolution)
        self.addButton("Erase scratches", self.processEraseScratches)
        self.addButton("Image colorization", self.processImageColorizer)

    def initTool(self):
        self.remoteTask = RemoteTask(self)

    def processSuperResolution(self):
        service.api = "super_resolution"
        if self.include_faces.isChecked():
            service.api = "super_face"
        self.remoteTask.setService(service)
        if self.parent.twinViewer.left.isEnabled():
            self.preInit("Super resolution")
            image = self.parent.twinViewer.left.bytes()
            files = {"image_a": image}
            self.original = image[:]
            self.remoteTask.runRemoteTask(files)
        else:
            raise TypeError("No image loaded")


    def processEraseScratches(self):
        service.api = "erase_scratches"
        self.remoteTask.setService(service)
        if self.parent.twinViewer.left.isEnabled():
            self.preInit("Erase scratches")
            image = self.parent.twinViewer.left.bytes()
            files = {"image_a": image}
            self.original = image[:]
            self.remoteTask.runRemoteTask(files)
        else:
            raise TypeError("No image loaded")

    def processImageColorizer(self):
        service.api = "colorize"
        self.remoteTask.setService(service)
        if self.parent.twinViewer.left.isEnabled():
            self.preInit("Face enhancement")
            image = self.parent.twinViewer.left.bytes()
            files = {"image_a": image}
            self.original = image[:]
            self.remoteTask.runRemoteTask(files)
        else:
            raise TypeError("No image loaded")

    def onRequestResponse(self, resource, reply):
        self.parent.showMessage(resource, ": done.")
        self.parent.twinViewer.right.display(reply)
        self.parent.twinViewer.swapImages()
        self.parent.progressBar.hide()
