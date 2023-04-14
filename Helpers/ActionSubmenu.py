from Helpers.Action import Action


class ActionSubmenu(Action):
    def __init__(self, window, label):
        super().__init__(window, label)

    def onTriggered(self):
        self.callback(self.label)
