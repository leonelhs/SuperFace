from UI.widgets.drawing_box import DrawingBox
from UI.widgets.BaseGraphicsView import BaseGraphicsView


class ImageView(BaseGraphicsView):
    def __init__(self, parent=None):
        super(ImageView, self).__init__(parent)
        self.drawer = None

    def setDrawer(self, drawer: DrawingBox):
        if self.drawer is None:
            self.drawer = drawer
            self.drawer.setRect(self.rect())
            self.scene.addItem(self.drawer)

    def dropDrawer(self):
        if self.drawer is not None:
            self.scene.removeItem(self.drawer)
            self.drawer = None
