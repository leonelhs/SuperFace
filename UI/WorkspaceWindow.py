from PySide6.QtCore import QThreadPool

from AI.TaskLowLight import TaskLowLight
from AI.TaskSuperFace import TaskSuperFace
from AI.TaskZeroBackground import TaskZeroBackground
from Actions import Action
from UI.MainWindow import MainWindow, tr


class WorkspaceWindow(MainWindow):
    def __init__(self, parent=None):
        super(WorkspaceWindow, self).__init__(parent)
        self.action_background = None
        self.action_low_light = None
        self.action_zero_background = None
        self.action_super_resolution = None
        self.taskLowLight = None
        self.taskZeroBackground = None
        self.taskSuperFace = None
        self.threadpool = None
        self.createActions()
        self.setupCallbacks()
        self.setupInstances()

    def createActions(self):
        self.action_super_resolution = Action(self, "Super Resolution", "mdi.face")
        self.action_zero_background = Action(self, "Zero Background", "mdi.eraser")
        self.action_low_light = Action(self, "Light Enhancement", "ei.adjust")
        self.action_background = Action(self, "Custom Background", "ph.selection-background")

        self.toolBar.addAction(self.action_super_resolution)
        self.toolBar.addAction(self.action_zero_background)
        self.toolBar.addAction(self.action_low_light)
        self.toolBar.addAction(self.action_background)

        self.action_super_resolution.setToolTip(tr("Super Resolution"))
        self.action_zero_background.setToolTip(tr("Zero Background"))
        self.action_low_light.setToolTip(tr("Low Light"))

    def setupCallbacks(self):
        self.action_super_resolution.setOnClickEvent(self.processSuperResolution)
        self.action_zero_background.setOnClickEvent(self.processZeroBackground)
        self.action_low_light.setOnClickEvent(self.processLowlight)
        self.action_background.setOnClickEvent(self.setCustomBackground)

    def setupInstances(self):
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        args = (self.threadpool, self.enhanceDone, self.enhanceComplete, self.trackEnhanceProgress)
        self.taskSuperFace = TaskSuperFace(*args)
        self.taskZeroBackground = TaskZeroBackground(*args)
        self.taskLowLight = TaskLowLight(*args)

    def processSuperResolution(self):
        self.show_message("Super resolution at: ", self.imagePath())
        self.progressBar.show()
        self.taskSuperFace.startEnhanceThread(self.workingImage())

    def processZeroBackground(self):
        self.show_message("Zeo background at: ", self.imagePath())
        self.progressBar.show()
        self.taskZeroBackground.startEnhanceThread(self.workingImage())

    def setCustomBackground(self):
        image_path = self.launchDialogOpenFile()
        if image_path:
            background = self.readImageFile(image_path)
            self.pasteForeground(background)

    def pasteForeground(self, background):
        foreground = self.workingImage()
        x = (background.size[0] - foreground.size[0]) / 2
        y = (background.size[1] - foreground.size[1]) / 2
        box = (x, y, foreground.size[0] + x, foreground.size[1] + y)
        crop = background.crop(box)
        final_image = crop.copy()
        # put the foreground in the centre of the background
        paste_box = (0, final_image.size[1] - foreground.size[1], final_image.size[0], final_image.size[1])
        final_image.paste(foreground, paste_box, mask=foreground)
        self.displayImageOutput(final_image)

    def processLowlight(self):
        self.show_message("Light enhancement at: ", self.imagePath())
        self.progressBar.show()
        self.taskLowLight.startEnhanceThread(self.workingImage())

    def trackEnhanceProgress(self, progress):
        self.progressBar.setValue(progress)
        self.show_message("Scanning gallery completed: ", progress)

    def enhanceDone(self, image_result):
        self.show_message("finish ", " done")
        self.displayImageOutput(image_result)

    def enhanceComplete(self):
        self.progressBar.hide()
        self.show_message("Scanning complete ", "Done")

    def imageZoom(self):
        pass

    def imageFlip(self):
        pass