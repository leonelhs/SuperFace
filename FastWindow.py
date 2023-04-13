from PySide6 import QtNetwork

from ToolsetFast import ToolsetFast
from ToolsetFilters import ToolsetFilters
from UI.FrameWindow import FrameWindow


class FastWindow(FrameWindow):
    def __init__(self, parent=None):
        super(FastWindow, self).__init__(parent)
        controls = (self.progressBar, self.showMessage, self.twinViewer)

        self.toolset_fast = ToolsetFast(None)
        self.toolBox.toolset_fast = self.toolset_fast
        self.toolset_fast.setControls(controls)
        self.toolBox.buildFastPage()

        self.toolset_filters = ToolsetFilters(None)
        self.toolset_filters.setControls(controls)
        self.toolBox.toolset_filters = self.toolset_filters
        self.toolBox.buildPageFilters()

    def happyPath(self):
        self.image_path = "./Test/makeup.png"
        self.displayPhoto(self.image_path)
        self.twinViewer.inputViewRedraw()
