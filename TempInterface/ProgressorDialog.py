from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Framework.Framework import get_framework


class ProgressorDialog(QDialog):

    def __init__(self, parent=None, label_width=150, label_alone_width=300):
        super(ProgressorDialog, self).__init__(parent)
        self.fw = get_framework()
        self._label_width = label_width
        self._label_alone_width = label_alone_width
        self.setWindowIcon(QIcon(self.fw.data_moderator.get_icon_path(name="progressor_main")))

    def _entry(self, label, *args, **kwargs):
        layout = QHBoxLayout()
        label = QLabel(label)
        label.setFixedWidth(self._label_width)
        entry = QLineEdit()
        layout.addWidget(label)
        layout.addWidget(entry)
        return layout, entry

    def _entry_with_options(self, label, options):
        priority_layout = QHBoxLayout()
        names_label = QLabel(label)
        entry = QComboBox()
        entry.addItems(options)
        priority_layout.addWidget(names_label)
        priority_layout.addWidget(entry)
        return priority_layout, entry

    def _label(self, label):
        layout = QHBoxLayout()
        label = QLabel(label)
        label.setFixedWidth(self._label_alone_width)
        label.setAlignment(Qt.AlignLeft)
        layout.addWidget(label)
        return layout

    def _list(self):
        pass

    def _remove_layout(self, layout, layout_to_remove):
        import sip

        items = [layout_to_remove.itemAt(i) for i in range(layout_to_remove.count())]

        for item in items:
            w = item.widget()
            layout.removeWidget(w)
            sip.delete(w)

        for i in range(layout.count()):
            layout_item = layout.itemAt(i)
            if layout_item.layout() == layout_to_remove:
                layout.removeItem(layout_item)
                break

        self.adjustSize()

    def _get_dialog_buttons(self, _layout):
        button_box = QDialogButtonBox(QDialogButtonBox.Ok|
                                      QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        _layout.addWidget(button_box, alignment=Qt.AlignCenter)
        return button_box

    def accept(self):
        pass

    def _assert_inserted(self, fields):
        if any(field == "" for field in fields):
            raise ValueError('missing data in a mandatory field')
