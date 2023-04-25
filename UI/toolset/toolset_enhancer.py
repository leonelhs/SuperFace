import utils
from UI.widgets.button_plus_check import ButtonPlusCheck
from remotetasks.remote_task import RemoteTask
from UI.toolset import make_transparent_foreground
from UI.toolset.Toolset import Toolset
from utils import uint8


def pasteForeground(foreground, background):
    foreground = utils.image_from_array(foreground).convert("RGBA")
    x = (background.size[0] - foreground.size[0]) / 2
    y = (background.size[1] - foreground.size[1]) / 2
    box = (x, y, foreground.size[0] + x, foreground.size[1] + y)
    crop = background.crop(box)
    final_image = crop.copy()
    # put the foreground in the centre of the background
    paste_box = (0, final_image.size[1] - foreground.size[1], final_image.size[0], final_image.size[1])
    final_image.paste(foreground, paste_box, mask=foreground)
    return final_image


class ToolsetEnhancer(Toolset):

    def __init__(self, main_window):
        Toolset.__init__(self, main_window)
        self.custom_background = None
        self.change_background = False
        self.buildPage()

    def name(self):
        return "scratches"

    def buildPage(self):
        self.addPage("Enhancements")
        form_hires = self.createWidget(ButtonPlusCheck)
        form_hires.setLabels("Enhance resolution", "Include faces")
        form_hires.setOnClickEvent(self.processSuperResolution)
        self.addButton("Erase scratches", self.processEraseScratches)
        self.addButton("Colorize photo", self.processImageColorizer)
        self.addButton("Enhance light", self.processEnhanceLight)
        form_back = self.createWidget(ButtonPlusCheck)
        form_back.setLabels("Clear background", "Add new")
        form_back.setOnClickEvent(self.processZeroBackground)

    def processEnhanceLight(self):
        process = self.process("enhance_light")
        self.requestImageProcess(process)

    def processZeroBackground(self, isChecked):
        process = self.process("zero_background")
        self.change_background = isChecked
        if isChecked:
            self.setCustomBackground()
        self.requestImageProcess(process)

    def setCustomBackground(self):
        image_path = self.main_window.launchDialogOpenFile()
        if image_path:
            self.custom_background = utils.load_image(image_path)

    def processSuperResolution(self, isChecked):
        process = self.process("super_resolution")
        if isChecked:
            process = self.process("super_face")
        self.requestImageProcess(process)

    def processEraseScratches(self):
        process = self.process("erase_scratches")
        self.requestImageProcess(process)

    def processImageColorizer(self):
        process = self.process("colorize")
        self.requestImageProcess(process)

    def onImageProcessDone(self, process, image):
        if process == "zero_background":
            bin_mask = uint8(image)
            image = self.viewer().left.ndarray()
            image = make_transparent_foreground(image, bin_mask)
            if self.change_background:
                image = pasteForeground(image, self.custom_background)

        self.main_window.showMessage(process, ": done.")
        self.viewer().right.display(image)
        self.viewer().swapImages()
        self.main_window.progressBar.hide()
