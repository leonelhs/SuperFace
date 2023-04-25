from PySide6.QtWidgets import QToolBox, QWidget, QSizePolicy, QVBoxLayout, QLayout, QPushButton, QFileDialog

from UI.widgets.Slider import Slider
from UI.widgets.left_aligin_button import LeftAlignButton


class ToolBoxMaker(QToolBox):
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

    def addButton(self, page, label, action=None, args=None):
        button = LeftAlignButton(self.item(page))
        button.setText(label)
        if action:
            def callback():
                if args:
                    action(args)
                else:
                    action()

            button.clicked.connect(callback)

        self.page(page).addWidget(button)
        return button

    def createWidget(self, page, custom_widget):
        new_widget = custom_widget(self.item(page))
        self.page(page).addWidget(new_widget)
        return new_widget

    def createLayout(self, page, layout):
        new_layout = layout(self.item(page))
        self.page(page).addLayout(new_layout)
        return new_layout

    def createSlider(self, page, title, row, callback=None):
        layout = self.createLayout(page, Slider)
        slider = layout.build(title, row, callback)
        return slider

    def launchDialogOpenFile(self, title="Open Image"):
        return QFileDialog.getOpenFileName(self, title)[0]

    def launchDialogSaveFile(self, title="Save Image"):
        return QFileDialog.getSaveFileName(self, title)[0]
