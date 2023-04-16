from UI.FrameWindow import FrameWindow
from toolset.ToolsetFast import ToolsetFast
from toolset.ToolsetFilters import ToolsetFilters
from toolset.ToolsetScratches import ToolsetScratches


class FastWindow(FrameWindow):
    def __init__(self, parent=None):
        super(FastWindow, self).__init__(parent)

        self.toolsetFast = ToolsetFast(self)
        self.toolsetFilters = ToolsetFilters(self)
        self.toolsetScratches = ToolsetScratches(self)
        self.setSpliterSize(0.5, 0.5)
