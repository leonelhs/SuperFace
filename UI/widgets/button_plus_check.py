from UI.widgets.mini_form import MiniForm


class ButtonPlusCheck(MiniForm):
    def __init__(self, parent):
        super().__init__(parent)
        self.callback = None
        self.button = self.addButton("button")
        self.check = self.addCheckbox("check")
        self.button.clicked.connect(self.onTriggered)

    def setLabels(self, button, check):
        self.button.setText(button)
        self.check.setText(check)

    def setOnClickEvent(self, callback):
        self.callback = callback

    def onTriggered(self):
        self.callback(self.check.isChecked())
