from UI.widgets.ToolBoxMaker import ToolBoxMaker


class BaseToolBox(ToolBoxMaker):

    def __init__(self, parent):
        super().__init__(parent)
        self.setCurrentIndex(0)

