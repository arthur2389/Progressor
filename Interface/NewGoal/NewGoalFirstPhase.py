from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Interface.ProgressorDialog import ProgressorDialog
from Interface.NewGoal.DateInput import DateInput
from Interface.NewGoal.TermsInput import TermsInput
from EnumTypes import *


class NewGoalFirstPhase(ProgressorDialog):

    def __init__(self):
        super(NewGoalFirstPhase, self).__init__()

        self._goal_init_data = {}
        self._name_entry = None

        self._dates = DateInput(self)
        self._terms = TermsInput(self)

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

    def _if_user_enumerates_terms(self, state):
        if state == 2:
            self._new_term.clicked.disconnect(self._add_term)
            self._new_term.clicked.connect(self._add_enum_term)
        else:
            self._new_term.clicked.disconnect(self._add_enum_term)
            self._new_term.clicked.connect(self._add_term)

    def _terms_layout(self):
        layout = QVBoxLayout()

        layout.addWidget(self.fw.widgets.PrCheckBox("Enumerate the goal terms (optional)",
                                                    self._if_user_enumerates_terms))
        layout.addWidget(self._terms.term_list_create())
        self._new_term = self.fw.widgets.ButtonWithIcon(icon_path=self.fw.data_moderator.get_icon_path(name="add_line"),
                                                        action=self._add_term,
                                                        btn_size=QSize(70, 40),
                                                        icon_size=QSize(35, 35))
        layout.addWidget(self._new_term)

        return layout

    def _add_term(self):
        self._terms.exec(ETermType.REGULAR)

    def _add_enum_term(self):
        self._terms.exec(ETermType.ENUMERATED)

    def accept(self):
        name = self._name_entry.text()

        self._dates.process_results()
        self._terms.process_results()
        goal_status = self._dates.status

        self._goal_init_data = {'name': name,
                                'date_input': self._dates,
                                'status': goal_status,
                                'terms': self._terms.terms}
        QDialog.accept(self)
