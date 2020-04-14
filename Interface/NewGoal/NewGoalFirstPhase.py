from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Interface.ProgressorDialog import ProgressorDialog
from Framework.ExpandWithFramework import ExpandWithFramework
from EnumTypes import *


class NewGoalFirstPhase(ProgressorDialog):

    class AddTerm(ProgressorDialog):

        def __init__(self, parent):
            super(NewGoalFirstPhase.AddTerm, self).__init__(parent=parent)
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
            super(NewGoalFirstPhase.AddEnumeratedTerm, self).__init__(parent=parent)
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

    class DateInput(metaclass=ExpandWithFramework):

        def __init__(self, parent):
            self.text_entries = {EStage.START: None,
                                 EStage.END: None}
            self.calendars = {EStage.START: NewGoalFirstPhase.ProgressorCalendar(parent),
                              EStage.END: NewGoalFirstPhase.ProgressorCalendar(parent)}
            self.status = EGoalStatus.NOT_STARTED

        @property
        def start_date(self):
            return self.calendars[EStage.START].selected_date

        @property
        def end_date(self):
            return self.calendars[EStage.END].selected_date

        def exec(self, stage):
            if self.calendars[stage].exec_():
                self.text_entries[stage].setText(str(self.calendars[stage].selected_date))

        def process_results(self):
            today = self.fw.date_handler.today()
            if not self.start_date or not self.end_date:
                raise ValueError('missing date input')

            if self.start_date >= self.end_date:
                raise NotImplemented('start date should be before the end date')

            if today <= self.start_date:
                self.status = EGoalStatus.NOT_STARTED
            elif today > self.end_date:
                self.status = EGoalStatus.FINISHED
            else:
                self.status = EGoalStatus.IN_PROGRESS

    class ProgressorCalendar(ProgressorDialog):

        def __init__(self, parent):
            super(NewGoalFirstPhase.ProgressorCalendar, self).__init__(parent=parent)
            self.calendar = None
            self._date = None
            self.setLayout(self._build_layout())

        @property
        def selected_date(self):
            return self._date

        @selected_date.setter
        def selected_date(self, date):
            self._date = date

        def _build_layout(self):
            vlayout = QVBoxLayout()
            self.calendar = QCalendarWidget()

            vlayout.addWidget(self.calendar)
            self._get_dialog_buttons(vlayout)

            return vlayout

        def accept(self):
            self._date = self.calendar.selectedDate().toPyDate()
            QDialog.accept(self)

    def __init__(self):
        super(NewGoalFirstPhase, self).__init__()

        self._goal_init_data = {}
        self._name_entry = None

        self._term_list = self.fw.widgets.PrListWidget()
        self._dates = self.DateInput(self)

        self.setLayout(self._build_layout())
        self.setWindowTitle("Insert new goal")
        self.setMinimumWidth(50)

    @property
    def goal_init_data(self):
        return self._goal_init_data

    def _build_layout(self):
        vlayout = QVBoxLayout()

        name_layout, self._name_entry = self._entry(label="Goal name: ")

        dt_start_layout, self._dates.text_entries[EStage.START] = self._entry("Goal's start date: ")
        dt_start_layout.addWidget(self.fw.widgets.ButtonWithIcon(icon_path=self.fw.data_moderator.get_icon_path(name="calendar"),
                                                                 action=lambda: self._dates.exec(EStage.START)))

        dt_end_layout, self._dates.text_entries[EStage.END] = self._entry("Goal's last date: ")
        dt_end_layout.addWidget(self.fw.widgets.ButtonWithIcon(icon_path=self.fw.data_moderator.get_icon_path(name="calendar"),
                                                               action=lambda: self._dates.exec(EStage.END)))
        add_terms = self.fw.widgets.PrCheckBox("Define terms for the goal (optional)",
                                               self._if_user_defines_terms)

        vlayout.addLayout(name_layout)
        vlayout.addLayout(dt_start_layout)
        vlayout.addLayout(dt_end_layout)
        vlayout.addSpacing(25)

        vlayout.addWidget(add_terms)
        vlayout.addSpacing(15)
        self._buttons = self._get_dialog_buttons(vlayout)
        return vlayout

    def _if_user_defines_terms(self, state):
        if state == 2:
            layout = self.layout()
            layout.removeWidget(self._buttons)

            self._sub_terms_layout = self._terms_layout()
            layout.addLayout(self._sub_terms_layout)
            layout.addWidget(self._buttons, alignment=Qt.AlignCenter)
        else:
            self._remove_layout(layout=self.layout(),
                                layout_to_remove=self._sub_terms_layout)

    def _terms_layout(self):
        layout = QVBoxLayout()

        layout.addWidget(self.fw.widgets.PrCheckBox("Enumerate the goal terms (optional)",
                                                    self._if_user_enumerates_terms))
        self._term_list = self.fw.widgets.PrListWidget()
        layout.addWidget(self._term_list)
        self._new_term = self.fw.widgets.ButtonWithIcon(icon_path=self.fw.data_moderator.get_icon_path(name="add_line"),
                                                        action=self._add_term,
                                                        btn_size=QSize(70, 40),
                                                        icon_size=QSize(35, 35))
        layout.addWidget(self._new_term)

        return layout

    def _add_term(self):
        add_term_window = self.AddTerm(self)
        if add_term_window.exec_():
            self._term_list.addItem(self._term_item(is_enum=False, text=add_term_window.new_term))

    def _add_enum_term(self):
        add_term_window = self.AddEnumeratedTerm(self)
        if add_term_window.exec_():
            self._term_list.addItem(self._term_item(is_enum=True, text=add_term_window.new_term))

    def _term_item(self, is_enum, text):
        item = QListWidgetItem(text)
        if is_enum:
            icon_name = 'blue_arrow'
        else:
            icon_name = 'blank_arrow'
        item.setIcon(QIcon(self.fw.data_moderator.get_icon_path(name=icon_name)))
        return item

    def _if_user_enumerates_terms(self, state):
        if state == 2:
            self._new_term.clicked.disconnect(self._add_term)
            self._new_term.clicked.connect(self._add_enum_term)
        else:
            self._new_term.clicked.disconnect(self._add_enum_term)
            self._new_term.clicked.connect(self._add_term)

    def accept(self):
        name = self._name_entry.text()
        self._dates.process_results()
        goal_status = self._dates.status

        terms = {}
        for item in self._term_list:
            txt = item.text()
            if ':' in txt:
                vals = txt.split(':')
                terms.update({vals[0]: vals[1].strip()})
            else:
                terms.update({txt: 0})
        self._goal_init_data = {'name': name,
                                'date_input': self._dates,
                                'status': goal_status,
                                'terms': terms}
        QDialog.accept(self)
