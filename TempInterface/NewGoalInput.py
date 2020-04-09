from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from TempInterface.ProgressorDialog import ProgressorDialog
from Core.DataTransferTypes.CreationData import CreationData
from EnumTypes import *


class NewGoalInputPartI(ProgressorDialog):

    def __init__(self, progressor):
        super(NewGoalInputPartI, self).__init__()

        self._progressor = progressor
        self._goal_init_data = {}
        self._name_entry = self._vs_entry = self._gv_entry = None
        self.dt_start_txt = self.dt_end_txt = None

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

        vlayout.addLayout(name_layout)
        vlayout.addLayout(dt_start_layout)
        vlayout.addLayout(dt_end_layout)

        self._get_dialog_buttons(vlayout)
        return vlayout

    def _open_calendar(self, stage):
        open_calendar = QPushButton()
        open_calendar.setIcon(QIcon(self.fw.data_moderator.get_icon_path(group="main", name="calendar")))
        open_calendar.clicked.connect(lambda: self._calendar(stage))

        return open_calendar

    def _calendar(self, stage):
        self.cal = ProgressorCalendar(self)
        if self.cal.exec_():
            if stage == EStage.START:
                ent = self.dt_start_txt
            else:
                ent = self.dt_end_txt
            ent.setText(self.cal.selected_date)

    def accept(self):
        name = self._name_entry.text()
        start_date = self.dt_start_txt.text()
        end_date = self.dt_end_txt.text()
        goal_status = self._progressor.check_dates_define_status(date_st=start_date, date_end=end_date)

        self._goal_init_data = {'name': name,
                                'start_date': start_date,
                                'end_date': end_date,
                                'status': goal_status}
        QDialog.accept(self)


class NewGoalInputPartII(ProgressorDialog):

    def __init__(self, goal_name, start_date, end_date, status):
        super(NewGoalInputPartII, self).__init__()

        self.goal_name = goal_name
        self.dt_start = start_date
        self.dt_end = end_date
        self.status = status

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
        status_layout = self._label("Goal's status: {}".format(self.status.value))

        vs_layout, self._vs_entry = self._entry(label="Value at the start: ")
        gv_layout, self._gv_entry = self._entry(label="Goal value: ")

        vlayout.addLayout(name_layout)
        vlayout.addLayout(dt_start_layout)
        vlayout.addLayout(dt_end_layout)
        vlayout.addLayout(status_layout)
        vlayout.addSpacing(25)
        vlayout.addLayout(vs_layout)
        vlayout.addLayout(gv_layout)

        if self.status == EGoalStatus.IN_PROGRESS:
            cv_layout, self._cv_entry = self._entry(label="The value today: ")
            vlayout.addLayout(cv_layout)

        vlayout.addSpacing(25)

        self._get_dialog_buttons(vlayout)
        return vlayout

    @property
    def goal_raw_data(self):
        return self._goal_raw_data

    def accept(self):
        name = self.goal_name
        vs = self._vs_entry.text()
        gv = self._gv_entry.text()
        start_date = self.dt_start
        end_date = self.dt_end

        self._goal_raw_data = CreationData(goal_name=name,
                                           start_date=start_date,
                                           end_date=end_date,
                                           start_value=vs,
                                           goal_value=gv,
                                           curr_value=self._cv_entry.text() if self._cv_entry else None)
        QDialog.accept(self)


class ProgressorCalendar(ProgressorDialog):

    def __init__(self, parent):
        super(ProgressorCalendar, self).__init__(parent=parent)
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
