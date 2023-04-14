from abc import ABC

from PIL import ImageFilter
from PySide6.QtWidgets import QComboBox

from UI.widgets.GridInputs import GridInputs
from UI.widgets.GridSliders import GridSliders
from toolset import dataX3, dataX5
from toolset.Toolset import Toolset


class ToolsetFilters(Toolset, ABC):
    def __init__(self, parent):
        super().__init__(parent)
        self.buildPage()

    def name(self):
        return "filters"

    def buildPage(self):
        self.addPage("Image Filters")
        self.buildPageFilters()
        self.buildPageConvolution()
        self.addButton("Apply filter", self.applyFilter)

    def buildPageFilters(self):
        controls = self.createLayout(GridSliders)
        controls.addSlider("Blur", row=0, callback=self.onSliderBlurChanged)
        controls.addSlider("Box blur", row=1, callback=self.onSliderBoxBlurChanged)
        controls.addSlider("Unsharp", row=2, callback=self.onSliderUnsharpMaskChanged)

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

    def onSliderBlurChanged(self, radius):
        image = self.parent.twinViewer.left.filter(ImageFilter.GaussianBlur, (radius,))
        self.parent.twinViewer.right.display(image)
        self.parent.showMessage("Filter Blur radius: ", radius)

    def onSliderBoxBlurChanged(self, radius):
        image = self.parent.twinViewer.left.filter(ImageFilter.BoxBlur, (radius,))
        self.parent.twinViewer.right.display(image)
        self.parent.showMessage("Filter Box Blur radius: ", radius)

    def onSliderUnsharpMaskChanged(self, radius):
        if self.parent.twinViewer.left.isEnabled():
            image = self.parent.twinViewer.left.filter(ImageFilter.UnsharpMask, (radius, 150, 3))
            self.parent.twinViewer.right.display(image)
            self.parent.showMessage("Filter Unsharp Mask radius:", radius)
        else:
            raise TypeError("No image loaded")

    def applyFilter(self):
        image = self.parent.twinViewer.right.pixmap()
        self.parent.twinViewer.left.display(image)

    def onConvolutionFilter(self, gridKernel):
        scale = 1
        offset = 0
        size = gridKernel.getSize()
        kernel = gridKernel.getIntValues()
        image = self.parent.twinViewer.left.filter(ImageFilter.Kernel, (size, kernel, scale, offset))
        self.parent.twinViewer.right.display(image)
        self.parent.showMessage("Convolution size :  ", size[0])
