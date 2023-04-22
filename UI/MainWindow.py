from UI.FrameWindow import FrameWindow
from toolset.ToolsetFaceDrawer import ToolsetFaceDrawer
from toolset.ToolsetFast import ToolsetFast
from toolset.ToolsetFilters import ToolsetFilters
from toolset.ToolsetEnhancer import ToolsetEnhancer


class MainWindow(FrameWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.toolsetEnhancer = ToolsetEnhancer(self)
        self.toolsetFast = ToolsetFast(self)
        self.toolsetFilters = ToolsetFilters(self)
        self.toolsetFaceDrawer = ToolsetFaceDrawer(self)
        self.setSpliterSize(0.5, 0.5)
        self.toolBox.setCurrentIndex(0)
