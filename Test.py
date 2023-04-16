import sys

from PySide6 import QtWidgets

from AI.TaskFaceParser import TaskFaceParser
from AI.Tensorflow.TaskSegmentation import TaskSegmentation
from Test.TestWindow import TestWindow

tests = list()
tests.append(TaskFaceParser)
tests.append(TaskSegmentation)

ACTIVE_TEST = 0

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = TestWindow()
    widget.resize(1200, 800)
    widget.show()
    widget.setTask(tests[ACTIVE_TEST])
    widget.runTest()
    sys.exit(app.exec())
