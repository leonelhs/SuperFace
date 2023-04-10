from PySide6.QtWidgets import QComboBox

from UI.widgets.GridInputs import GridInputs
from UI.widgets.GridSliders import GridSliders
from UI.widgets.ToolBoxMaker import ToolBoxMaker


class ToolBoxEnhancer(ToolBoxMaker):

    def __init__(self, parent):
        super().__init__(parent)
        self.addPage("filters", u"Image filters")
        self.addPage("convolution", u"Convolution filter")
        self.addPage("face", u"Super Face")
        self.addPage("hires", u"Super Resolution")
        # self.addPage("zero", u"Zero Background")
        # self.addPage("makeup", u"Makeup Face")
        self.addPage("parser", u"Face Parser")
        self.addPage("scratch", u"Zero Scratches")
        self.addPage("light", u"Light Enhancement")
        self.addPage("style", u"Style transfer")
        self.addPage("vectors", u"Interpolate  vectors")
        self.addPage("retina", u"Retina Face")
        self.addPage("delf", u"Match images")
        self.addPage("pose", u"Human pose")
        self.addPage("color", u"Super Colorize")
        self.addPage("bald", u"Bald Face")
        self.setCurrentIndex(0)
        self.toolset_ai = None
        self.toolset_filters = None

    def buildPages(self):
        self.addButton("face", "Restore faces", self.toolset_ai.processSuperface)
        self.addButton("color", "Colorize", self.toolset_ai.processSuperColorize)
        self.addButton("light", "Shine picture", self.toolset_ai.processLowlight)
        self.addButton("bald", "Bald face", self.toolset_ai.processBaldFace)
        self.addButton("vectors", "Closest latent vector", self.toolset_ai.processInterpolateVectors)
        self.addButton("retina", "Draw face landmarks", self.toolset_ai.processRetinaFace)
        self.addButton("pose", " Estimate pose", self.toolset_ai.processEstimatePose)
        self.addButton("scratch", " Draw scratches mask", self.toolset_ai.processMaskScratches)
        self.addButton("scratch", " Erase scratches", self.toolset_ai.processEraseScratches)
        self.pageSuperResolution()
        self.pageStyleTransfer()
        self.pageDelf()
        self.pageFilters()
        self.pageConvolution()
        self.pageZeroBackground()

    def pageZeroBackground(self):
        self.addButton("parser", "Parse face", self.toolset_ai.processFaceParser)
        self.addButton("parser", "Segment image", self.toolset_ai.processSegmentation)
        self.addButton("parser", "Makeup face", self.toolset_ai.processFaceMakeup)
        self.addButton("parser", "Remove background", self.toolset_ai.processZeroBackground)
        self.addButton("parser", "Custom background", self.toolset_ai.setCustomBackground)

    def pageSuperResolution(self):
        scale = self.createWidget("hires", QComboBox)
        scale.addItems(["Scale 2X", "Scale 4X", "Scale 8X"])
        self.addButton("hires", "Pytorch code", self.toolset_ai.processHiresPytorch)
        self.addButton("hires", "Tensorflow code", self.toolset_ai.processHiresTensorflow)
        scale.currentIndexChanged.connect(self.toolset_ai.onHiresScaleChanged)

    def pageStyleTransfer(self):
        def appendStyleImage():
            image_path = self.launchDialogOpenFile()
            if image_path:
                self.toolset_ai.appendStyleImage(image_path)

        self.addButton("style", "Set style image", appendStyleImage)
        self.addButton("style", "Transfer style", self.toolset_ai.processStyleTransfer)

    def pageDelf(self):
        self.addButton("delf", "Set image match", self.toolset_ai.processDelf)
        self.addButton("delf", "Match images", self.toolset_ai.appendDelfImage)

    def pageFilters(self):
        controls = self.createLayout("filters", GridSliders)
        controls.addSlider("Blur", row=0, callback=self.toolset_filters.onSliderBlurChanged)
        controls.addSlider("Box blur", row=1, callback=self.toolset_filters.onSliderBoxBlurChanged)
        controls.addSlider("Unsharp", row=2, callback=self.toolset_filters.onSliderUnsharpMaskChanged)
        self.addButton("filters", "Apply filter", self.toolset_filters.applyFilter)

    def pageConvolution(self):
        gridKernel = None
        dataX3 = [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]
        dataX5 = [[1, 1, 1, 1, 1],
                  [1, 5, 5, 5, 1],
                  [1, 5, 44, 5, 1],
                  [1, 5, 5, 5, 1],
                  [1, 1, 1, 1, 1]]

        def onKernelSizeChanged(index):
            kernel = {0: {"size": 3, "data": dataX3}, 1: {"size": 5, "data": dataX5}}
            data = kernel[index]["data"]
            dim = kernel[index]["size"]
            gridKernel.build(matrix=data, size=(dim, dim))

        kernel_size = self.createWidget("convolution", QComboBox)
        kernel_size.addItems(["Size 3x3", "Size 5x5"])
        kernel_size.currentIndexChanged.connect(onKernelSizeChanged)

        gridKernel = self.createLayout("convolution", GridInputs)
        gridKernel.build(dataX3, size=(3, 3))
        self.addButton("convolution", "Convolution", self.toolset_filters.onConvolutionFilter, gridKernel)
