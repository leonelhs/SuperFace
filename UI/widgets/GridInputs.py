from PySide6.QtWidgets import QGridLayout, QLineEdit


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


class GridInputs(QGridLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.size = None
        self.parent = parent

    def build(self, matrix, size=(3, 3)):
        self.size = size
        clearLayout(self)
        for i in range(size[0]):
            for j in range(size[1]):
                edit = QLineEdit(self.parent)
                edit.setText(str(matrix[i][j]))
                self.addWidget(edit, i, j, 1, 1)

    def getSize(self):
        return self.size

    def getValues(self):
        input_list = list()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                item = self.itemAtPosition(i, j)
                input_list.append(item.widget().text())
        return input_list

    def getIntValues(self):
        input_list = list()
        for value in self.getValues():
            input_list.append(int(value))
        return input_list
