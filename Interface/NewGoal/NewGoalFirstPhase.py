from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Interface.ProgressorDialog import ProgressorDialog
from EnumTypes import *


class NewGoalFirstPhase(ProgressorDialog):

    class ProgressorCalendar(ProgressorDialog):

        def __init__(self, parent):
            super(NewGoalFirstPhase.ProgressorCalendar, self).__init__(parent=parent)
            self.calendar = None
            self._date = ''
            self.setLayout(self._build_layout())

        @property
        def selected_date(self):
            return self._date

        def _build_layout(self):
            vlayout = QVBoxLayout()
            self.calendar = QCalendarWidget()

            vlayout.addWidget(self.calendar)
            self._get_dialog_buttons(vlayout)

            return vlayout

        def accept(self):
            self._date = str(self.calendar.selectedDate().toPyDate())
            QDialog.accept(self)

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

    def __init__(self, progressor):
        super(NewGoalFirstPhase, self).__init__()

        self._progressor = progressor
        self._goal_init_data = {}
        self._name_entry = self._vs_entry = self._gv_entry = None
        self.dt_start_txt = self.dt_end_txt = None
        self._term_list = self.fw.widgets.PrListWidget()

        self.setLayout(self._build_layout())
        self.setWindowTitle("Insert new goal")
        self.setMinimumWidth(50)

    @property
    def goal_init_data(self):
        return self._goal_init_data

    def _build_layout(self):
        vlayout = QVBoxLayout()

        name_layout, self._name_entry = self._entry(label="Goal name: ")

        dt_start_layout, self.dt_start_txt = self._entry("Goal's start date: ")
        dt_start_layout.addWidget(self._open_calendar(EStage.START))

        dt_end_layout, self.dt_end_txt = self._entry("Goal's last date: ")
        dt_end_layout.addWidget(self._open_calendar(EStage.END))

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
        self._new_term = self._new_term_button()
        layout.addWidget(self._new_term)

        return layout

    def _new_term_button(self):
        button = QPushButton()
        button.setIcon(QIcon(self.fw.data_moderator.get_icon_path(name="add_line")))
        button.setFixedWidth(70)
        button.setFixedHeight(40)
        button.setIconSize(QSize(35, 35))
        button.clicked.connect(self._add_term)
        return button

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

    def _build_layout_for_terms(self):
        pass

    def _open_calendar(self, stage):
        open_calendar = QPushButton()
        open_calendar.setIcon(QIcon(self.fw.data_moderator.get_icon_path(name="calendar")))
        open_calendar.clicked.connect(lambda: self._calendar(stage))

        return open_calendar

    def _calendar(self, stage):
        self.cal = self.ProgressorCalendar(self)
        if self.cal.exec_():
            if stage == EStage.START:
                ent = self.dt_start_txt
            else:
                ent = self.dt_end_txt
            ent.setText(str(self.cal.selected_date))

    def accept(self):
        name = self._name_entry.text()
        start_date = self.dt_start_txt.text()
        end_date = self.dt_end_txt.text()
        goal_status = self._progressor.check_dates_define_status(date_st=start_date, date_end=end_date)

        self._goal_init_data = {'name': name,
                                'start_date': start_date,
                                'end_date': end_date,
                                'status': goal_status}
        terms = {}
        for item in self._term_list:
            txt = item.text()
            if ':' in txt:
                vals = txt.split(':')
                terms.update({vals[0]: vals[1].strip()})
            else:
                terms.update({txt: 0})
        self._goal_init_data = {'name': name,
                                'start_date': start_date,
                                'end_date': end_date,
                                'status': goal_status,
                                'terms': terms}
        QDialog.accept(self)
