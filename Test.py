import os
import sys

from PySide6 import QtWidgets

from AI.Pytorch.TaskFaceParser import TaskFaceParser
from AI.Pytorch.superface.TaskSuperFace import TaskSuperFace
from AI.Pytorch.superface.TaskSuperResolution import TaskSuperResolution
from AI.Tensorflow.TaskSegmentation import TaskSegmentation
from Test.TestWindow import TestWindow

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(ROOT_DIR)

tests = list()
tests.append(TaskFaceParser)
tests.append(TaskSegmentation)
tests.append(TaskSuperResolution)
tests.append(TaskSuperFace)

ACTIVE_TEST = 3

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = TestWindow()
    widget.resize(1200, 800)
    widget.show()
    widget.setTask(tests[ACTIVE_TEST])
    widget.runTest()
    sys.exit(app.exec())
