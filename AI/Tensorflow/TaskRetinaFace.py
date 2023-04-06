#############################################################################
#
#   Source from:
#   https://github.com/serengil/retinaface
#   Forked from:
#   https://github.com/serengil/retinaface
#   Reimplemented by: Leonel Hernández
#
##############################################################################
import test as np
import face_recognition
from PySide6.QtGui import QPainter, QColor
from face_recognition import face_landmarks

from Helpers.TaskPhotoEnhancer import TaskPhotoEnhancer


def get_line(array):
    for i in range(0, len(array), 2):
        yield array[i:i + 2]


def drawFaceLandmarks(pixmap, landmarks):
    painter = QPainter(pixmap)
    painter.setPen(QColor(255, 255, 0))
    for marks in landmarks:
        for positions in marks:
            for position in get_line(marks[positions]):
                if len(position) > 1:
                    painter.drawLine(*position[0], *position[1])


class TaskRetinaFace(TaskPhotoEnhancer):

    def __init__(self, args):
        super().__init__(args)

    def executeEnhanceWork(self, image, progress_callback):
        np_array = np.array(image)
        locations = face_recognition.face_locations(np_array)
        landmarks = face_landmarks(np_array, locations)
        pixmap = image.toqpixmap()
        drawFaceLandmarks(pixmap, landmarks)
        return pixmap
