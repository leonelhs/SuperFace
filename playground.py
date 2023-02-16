#####################################################################
#
# Forked from https://rk.edu.pl/en/qgraphicsview-and-qgraphicsscene/
#
######################################################################

import sys

from PySide6 import Qt
from PySide6.QtCore import QMetaObject
from PySide6.QtGui import *
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene


class ImageGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(ImageGraphicsView, self).__init__(parent)
        QMetaObject.connectSlotsByName(self)

    def resizeEvent(self, event):
        self.fitInView(self.items()[0], Qt.AspectRatioMode.KeepAspectRatio)
        return super().resizeEvent(event)


app = QApplication(sys.argv)

picture = QPixmap('/home/leonel/images/pechocha/20220101_220046.jpg')
graphics_view = ImageGraphicsView()

scene = QGraphicsScene()
scene.addPixmap(picture)

graphics_view.setScene(scene)
graphics_view.show()

sys.exit(app.exec())
