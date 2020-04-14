from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class PrListWidget(QListWidget):

    def __iter__(self):
        for i in range(self.count()):
            yield self.item(i)


class PrCheckBox(QCheckBox):

    def __init__(self, text, action):
        super(PrCheckBox, self).__init__(text)
        self.stateChanged.connect(action)


class ButtonWithIcon(QPushButton):

    def __init__(self, icon_path, action, btn_size=None, icon_size=None):
        super(ButtonWithIcon, self).__init__()
        self.setIcon(QIcon(icon_path))
        self.clicked.connect(action)
        if btn_size:
            self.setFixedSize(btn_size)
        if icon_size:
            self.setIconSize(icon_size)
