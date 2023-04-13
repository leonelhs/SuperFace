from PIL import ImageFilter

from Toolset import Toolset


class ToolsetFilters(Toolset):
    def __init__(self, args):
        super().__init__(args)

    def onSliderBlurChanged(self, radius):
        image = self.twinViewer.left.filter(ImageFilter.GaussianBlur, (radius,))
        self.twinViewer.right.display(image)
        self.showMessage("Filter Blur radius: ", radius)

    def onSliderBoxBlurChanged(self, radius):
        image = self.twinViewer.left.filter(ImageFilter.BoxBlur, (radius,))
        self.twinViewer.right.display(image)
        self.showMessage("Filter Box Blur radius: ", radius)

    def onSliderUnsharpMaskChanged(self, radius):
        image = self.twinViewer.left.filter(ImageFilter.UnsharpMask, (radius, 150, 3))
        self.twinViewer.right.display(image)
        self.showMessage("Filter Unsharp Mask radius:", radius)

    def applyFilter(self):
        image = self.twinViewer.right.pixmap()
        self.twinViewer.left.display(image)

    def onConvolutionFilter(self, gridKernel):
        scale = 1
        offset = 0
        size = gridKernel.getSize()
        kernel = gridKernel.getIntValues()
        image = self.twinViewer.left.filter(ImageFilter.Kernel, (size, kernel, scale, offset))
        self.twinViewer.right.display(image)
        self.showMessage("Convolution size :  ", size[0])

