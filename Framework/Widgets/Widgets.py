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
