from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QAction


def new_icon(icon_path):
    icon = QIcon()
    icon.addFile(icon_path, QSize(), QIcon.Normal, QIcon.Off)
    return icon


def new_action(window, icon_path, visible_in_menu=False):
    action = QAction(window)
    action.setIcon(new_icon(icon_path))
    action.setIconVisibleInMenu(visible_in_menu)
    return action



