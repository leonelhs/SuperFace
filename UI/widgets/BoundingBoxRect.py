from UI.widgets.BoundingBox import BoundingBox


class BoundingBoxRect(BoundingBox):
    def __init__(self):
        super().__init__()
        self.setSize(400, 400)
        self.boundingBoxEvent = None

    def setOnBoundingResizeEvent(self, callback):
        self.boundingBoxEvent = callback

    def mouseMoveEvent(self, event):
        self.boundingBoxEvent(self.mapRectToScene(self.boundingRect()))
        return super().mouseMoveEvent(event)

    def keyPressEvent(self, e):
        self.boundingBoxEvent(self.mapRectToScene(self.boundingRect()))
        return super().keyPressEvent(e)
