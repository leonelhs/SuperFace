import sys

from PySide6.QtWidgets import QApplication

from RemoteWindow import RemoteWindow
from remotetasks.tensorflow.tasksegmantation import TaskSegmentation

tasks = {
    "segment": TaskSegmentation
}

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = RemoteWindow()
    main.show()
    main.setTask(tasks["segment"])
    main.runTest()
    sys.exit(app.exec())
