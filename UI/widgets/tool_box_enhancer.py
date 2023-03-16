from PySide6.QtWidgets import QToolBox, QWidget, QSizePolicy, QVBoxLayout, QLayout, QPushButton


class ToolBoxEnhancer(QToolBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.__pages = {}
        self.__items = {}

    def addPage(self, name, title):
        item = QWidget()
        self.addItem(item, title)
        page = QVBoxLayout(item)
        self.sizePolicy.setHeightForWidth(item.sizePolicy().hasHeightForWidth())
        item.setSizePolicy(self.sizePolicy)
        page.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.__items[name] = item
        self.__pages[name] = page

    def item(self, name):
        return self.__items[name]

    def page(self, name):
        return self.__pages[name]

    def addButton(self, page, label, action=None):
        button = QPushButton(self.item(page))
        button.setText(label)
        button.clicked.connect(action)
        self.page(page).addWidget(button)

    def createWidget(self, page, widget):
        new_widget = widget(self.item(page))
        self.page(page).addWidget(new_widget)
        return new_widget

    def createLayout(self, page, layout):
        new_layout = layout(self.item(page))
        self.page(page).addLayout(new_layout)
        return new_layout
