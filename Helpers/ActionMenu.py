import qtawesome as qta

from Helpers.Action import Action


class ActionMenu(Action):

    def __init__(self, window, label, icon):
        super().__init__(window, label, visible_in_menu=True)
        icon = qta.icon(icon)
        super().setIcon(icon)

    def setIcon(self, image_icon):
        icon = qta.icon(image_icon)
        super().setIcon(icon)

    def onTriggered(self):
        self.callback()
