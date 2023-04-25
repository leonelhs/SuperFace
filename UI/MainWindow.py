from UI.FrameWindow import FrameWindow
from remotetasks.service import Service
from UI.toolset.toolset_enhancer import ToolsetEnhancer
from UI.toolset.ToolsetFaceDrawer import ToolsetFaceDrawer
from UI.toolset.ToolsetFilters import ToolsetFilters
from UI.toolset.ToolsetParser import ToolsetParser
from utils import read_config


class MainWindow(FrameWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.toolsetEnhancer = ToolsetEnhancer(self)
        self.toolsetParser = ToolsetParser(self)
        self.toolsetFilters = ToolsetFilters(self)
        self.toolsetFaceDrawer = ToolsetFaceDrawer(self)
        self.setSpliterSize(1, 5)
        self.toolBox.setCurrentIndex(0)
        self.config = read_config()

    def service(self, api):
        service = self.config[api]
        address = service["address"]
        port = service["port"]
        return Service(address, port, api)
