import numpy as np
from PIL import ImageEnhance
from PIL import ImageFilter
from PySide6.QtWidgets import QComboBox

from UI.toolset import dataX3, dataX5
from UI.toolset.Toolset import Toolset
from UI.widgets.GridInputs import GridInputs


class ToolsetFilters(Toolset):

    def __init__(self, parent):
        super().__init__(parent)
        self.buildPage()

    def name(self):
        return "filters"

    def buildPage(self):
        self.addPage("Image Filters")
        self.buildPageEnhancers()
        # self.buildPageConvolution()
        # self.addButton("Apply filter", self.applyFilter)

    def buildPageEnhancers(self):
        color = self.addSlider("Color", row=0, callback=self.onSliderColorChanged)
        contrast = self.addSlider("Contrast", row=1, callback=self.onSliderContrastChanged)
        sharpness = self.addSlider("Sharpness", row=2, callback=self.onSliderSharpnessChanged)
        sharpness.setInterval(scale=1, data_min=10, data_max=1000.0)
        brightness = self.addSlider("Brightness", row=3, callback=self.onSliderBrightnessChanged)
        brightness.setInterval(scale=1, data_min=10, data_max=100.0)
        unsharp = self.addSlider("Unsharp", row=4, callback=self.onSliderUnsharpMaskChanged)
        unsharp.setInterval(scale=1, data_min=10, data_max=1000.0)

    def buildPageConvolution(self):
        gridKernel = None

        def onKernelSizeChanged(index):
            kernel = {0: {"size": 3, "data": dataX3}, 1: {"size": 5, "data": dataX5}}
            data = kernel[index]["data"]
            dim = kernel[index]["size"]
            gridKernel.build(matrix=data, size=(dim, dim))

        kernel_size = self.createWidget(QComboBox)
        kernel_size.addItems(["Size 3x3", "Size 5x5"])
        kernel_size.currentIndexChanged.connect(onKernelSizeChanged)

        gridKernel = self.createLayout(GridInputs)
        gridKernel.build(dataX3, size=(3, 3))
        self.addButton("Convolution", self.onConvolutionFilter, gridKernel)

    def onSliderSharpnessChanged(self, factor):
        image = self.viewer().left.enhance(ImageEnhance.Sharpness, factor)
        self.viewer().right.display(image)
        self.showMessage("Enhance Sharpen image factor: ", factor)

    def onSliderColorChanged(self, factor):
        image = self.viewer().left.enhance(ImageEnhance.Color, factor)
        self.viewer().right.display(image)
        self.showMessage("Enhance color image factor: ", factor)

    def onSliderContrastChanged(self, factor):
        image = self.viewer().left.enhance(ImageEnhance.Contrast, factor)
        self.viewer().right.display(image)
        self.showMessage("Enhance contrast image factor: ", factor)

    def onSliderBrightnessChanged(self, factor):
        image = self.viewer().left.enhance(ImageEnhance.Brightness, factor)
        self.viewer().right.display(image)
        self.showMessage("Enhance brightness image factor: ", factor)

    def onSliderUnsharpMaskChanged(self, radius):
        if self.viewer().left.isEnabled():
            image = self.viewer().left.filter(ImageFilter.UnsharpMask, (radius, 150, 3))
            self.viewer().right.display(image)
            self.showMessage("Filter Unsharp Mask radius:", radius)
        else:
            raise TypeError("No image loaded")

    def applyFilter(self):
        image = self.viewer().right.pixmap()
        self.viewer().left.display(image)

    def onConvolutionFilter(self, gridKernel):
        scale = 1
        offset = 0
        size = gridKernel.getSize()
        kernel = gridKernel.getIntValues()
        image = self.viewer().left.filter(ImageFilter.Kernel, (size, kernel, scale, offset))
        self.viewer().right.display(image)
        self.showMessage("Convolution size :  ", size[0])

    def onImageProcessDone(self, process: str, image: np.ndarray):
        pass
