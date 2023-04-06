from PIL import ImageFilter

from Toolset import Toolset


class ToolsetFilters(Toolset):
    def __init__(self, args):
        super().__init__(args)

    def onSliderBlurChanged(self, radius):
        self.twinViewer.imageFilter(ImageFilter.GaussianBlur, (radius,))
        self.showMessage("Filter Blur radius: ", radius)

    def onSliderBoxBlurChanged(self, radius):
        self.twinViewer.imageFilter(ImageFilter.BoxBlur, (radius,))
        self.showMessage("Filter Box Blur radius: ", radius)

    def onSliderUnsharpMaskChanged(self, radius):
        self.twinViewer.imageFilter(ImageFilter.UnsharpMask, (radius, 150, 3))
        self.showMessage("Filter Unsharp Mask radius:", radius)

    def applyFilter(self):
        self.twinViewer.applyFilter()

    def onConvolutionFilter(self, gridKernel):
        scale = 1
        offset = 0
        size = gridKernel.getSize()
        kernel = gridKernel.getIntValues()
        image_working = self.twinViewer.imageInput().filter(ImageFilter.Kernel(size, kernel, scale, offset))
        self.twinViewer.displayOutput(image_working)
        self.showMessage("Convolution size :  ", size[0])

