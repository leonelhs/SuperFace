from UI.widgets.boundingBox import BoundingBox


class BoundingBoxRect(BoundingBox):
    def __init__(self):
        super().__init__()
        self.setSize(40, 40)
        self.boundingBoxEvent = None

    def setOnBoundingResizeEvent(self, callback):
        self.boundingBoxEvent = callback

    def mouseMoveEvent(self, e):
        self.boundingBoxEvent(self.mapRectToScene(self.boundingRect()))
        return super().mouseMoveEvent(e)

    def keyPressEvent(self, e):
        self.boundingBoxEvent(self.mapRectToScene(self.boundingRect()))
        return super().keyPressEvent(e)