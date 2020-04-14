from PyQt5.QtWidgets import *

from Interface.ProgressorDialog import ProgressorDialog
from Core.Goal.GoalSketelon import GoalSkeleton
from EnumTypes import *


class NewGoalSecondPhase(ProgressorDialog):

    def __init__(self, goal_name, start_date, end_date, status, terms):
        super(NewGoalSecondPhase, self).__init__()

        self.goal_name = goal_name
        self.dt_start = start_date
        self.dt_end = end_date
        self.status = status
        self.terms = terms

        if terms:
            self.create_value_entries = self._entry_with_options
        else:
            self.create_value_entries = self._entry

        self._goal_raw_data = None

        self._vs_entry = self._gv_entry = self._cv_entry = None

        self.setLayout(self._build_layout())
        self.setWindowTitle("Insert new goal - set your goal !")
        self.setMinimumWidth(50)

    def _build_layout(self):
        vlayout = QVBoxLayout()

        name_layout = self._label("Goal name: {}".format(self.goal_name))
        dt_start_layout = self._label("Goal's start date: {}".format(self.dt_start))
        dt_end_layout = self._label("Goal's last date: {}".format(self.dt_end))
        status_layout = self._label("Goal status: {}".format(self.status.value))

        vs_layout, self._vs_entry = self.create_value_entries(label="Value at the start: ",
                                                              options=self._keys_for_entry())
        gv_layout, self._gv_entry = self.create_value_entries(label="Goal value: ",
                                                              options=self._keys_for_entry())

        vlayout.addLayout(name_layout)
        vlayout.addLayout(dt_start_layout)
        vlayout.addLayout(dt_end_layout)
        vlayout.addLayout(status_layout)
        vlayout.addSpacing(25)
        vlayout.addLayout(vs_layout)
        vlayout.addLayout(gv_layout)

        if self.status == EGoalStatus.IN_PROGRESS:
            cv_layout, self._cv_entry = self.create_value_entries(label="The value today: ",
                                                                  options=self._keys_for_entry())
            vlayout.addLayout(cv_layout)

        vlayout.addSpacing(25)

        self._get_dialog_buttons(vlayout)
        return vlayout

    @property
    def goal_raw_data(self):
        return self._goal_raw_data

    def accept(self):
        name = self.goal_name
        vs = self._extract_value(self._vs_entry)
        gv = self._extract_value(self._gv_entry)
        start_date = self.dt_start
        end_date = self.dt_end

        self._goal_raw_data = GoalSkeleton(goal_name=name,
                                           start_date=start_date,
                                           end_date=end_date,
                                           start_value=vs,
                                           goal_value=gv,
                                           curr_value=self._extract_value(self._cv_entry) if self._cv_entry else None,
                                           terms=self.terms)
        QDialog.accept(self)

    def _extract_value(self, entry):
        try:
            return entry.text()
        except AttributeError:
            return entry.currentText()

    def _keys_for_entry(self):
        return [''] + list(self.terms.keys())
