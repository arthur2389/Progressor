from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Framework.ExpandWithFramework import ExpandWithFramework
from EnumTypes import *
from Interface.ProgressorDialog import ProgressorDialog


class TermsInput(metaclass=ExpandWithFramework):

    def __init__(self, parent):
        super(TermsInput, self).__init__()
        self.term_list_create()
        self.parent = parent
        self.term_dialogs = {ETermType.REGULAR: AddTerm,
                             ETermType.ENUMERATED: AddEnumeratedTerm}
        self.term_processing = {ETermType.REGULAR: self._fill_terms,
                                ETermType.ENUMERATED: self._fill_enum_terms}
        self.terms = {}

    def term_list_create(self):
        self.term_list = self.fw.widgets.PrListWidget(action_double_click=self.list_item_double_clicked,
                                                      action_right_click=self.list_item_right_clicked)
        return self.term_list

    def exec(self, term_type):
        add_term = self.term_dialogs[term_type](self.parent)
        if add_term.exec_():
            self.term_list.addItem(TermItem(term_type=term_type,
                                            dialog_box=add_term,
                                            icon_func=self.fw.data_moderator.get_icon_path))

    def list_item_double_clicked(self, item):
        add = item.dialog_box
        if add.exec_():
            item.setText(add.new_term)

    def list_item_right_clicked(self, item):
        self.rc_menu = self._drop_menu(item)
        self.rc_menu.popup(QCursor.pos() + QPoint(15, 0))

    def _drop_menu(self, item):
        rc_menu = QMenu(self.term_list)

        delete_term = QAction("Delete {}".format(item.text()), rc_menu)
        delete_term.triggered.connect(lambda: self.term_list.remove_item(item))

        rc_menu.addAction(delete_term)
        font = QFont()
        font.setPointSize(10)
        rc_menu.setFont(font)
        return rc_menu

    def process_results(self):
        terms = [i.text() for i in self.term_list]
        term_type = set(map(lambda t: self._term_type(t), terms))
        if len(term_type) > 1:
            raise TypeError
        term_type = list(term_type)[0]
        self.terms = self.term_processing[term_type](terms)

    def _fill_enum_terms(self, term_list):
        vals = {}
        for t in term_list:
            fields = t.split(':')
            vals.update({fields[0]: fields[1].strip()})
        return vals

    def _fill_terms(self, term_list):
        return {t: 0 for t in term_list}

    def _term_type(self, term):
        if ':' in term and len(term.split(':')) == 2:
            return ETermType.ENUMERATED
        return ETermType.REGULAR


class AddTerm(ProgressorDialog):

    def __init__(self, parent):
        super(AddTerm, self).__init__(parent=parent)
        self._term_entry = None
        self._new_term = None
        self.setLayout(self._build_layout())

    @property
    def new_term(self):
        return self._new_term

    def _build_layout(self):
        vlayout = QVBoxLayout()
        term_layout, self._term_entry = self._entry(label="New term: ")
        vlayout.addLayout(term_layout)
        self._get_dialog_buttons(vlayout)
        return vlayout

    def accept(self):
        self._new_term = self._term_entry.text()
        QDialog.accept(self)


class AddEnumeratedTerm(ProgressorDialog):

    def __init__(self, parent):
        super(AddEnumeratedTerm, self).__init__(parent=parent)
        self._term_entry = None
        self._value_entry = None
        self._new_term = None
        self.setLayout(self._build_layout())

    @property
    def new_term(self):
        return self._new_term

    def _build_layout(self):
        vlayout = QVBoxLayout()
        term_layout, self._term_entry = self._entry(label="New term: ")
        value_layout, self._value_entry = self._entry(label="Value for the term: ")
        vlayout.addLayout(term_layout)
        vlayout.addLayout(value_layout)
        self._get_dialog_buttons(vlayout)
        return vlayout

    def accept(self):
        self._new_term = '{0}: {1}'.format(self._term_entry.text(), self._value_entry.text())
        QDialog.accept(self)


class TermItem(QListWidgetItem):

    def __init__(self, dialog_box, term_type, icon_func):
        super(TermItem, self).__init__(dialog_box.new_term)
        if term_type == ETermType.ENUMERATED:
            icon_name = 'blue_arrow'
        else:
            icon_name = 'blank_arrow'
        self.setIcon(QIcon(icon_func(name=icon_name)))
        self.dialog_box = dialog_box
