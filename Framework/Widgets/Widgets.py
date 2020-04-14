from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class PrListWidget(QListWidget):

    def __init__(self, action_double_click=None, action_right_click=None):
        super(PrListWidget, self).__init__()
        if action_double_click:
            self.itemDoubleClicked.connect(action_double_click)
        self.action_right_click = action_right_click

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.RightButton and self.action_right_click:
            try:
                self.action_right_click(self.itemAt(QMouseEvent.pos().y(), QMouseEvent.pos().y()))
            # Catch exception in case user right clicked the tree in place with no item
            except Exception as e:
                print(e)
        super(PrListWidget, self).mousePressEvent(QMouseEvent)

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
