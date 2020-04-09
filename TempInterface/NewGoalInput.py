from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from TempInterface.ProgressorDialog import ProgressorDialog
from Core.DataTransferTypes.CreationData import CreationData
from EnumTypes import *


class NewGoalInput(ProgressorDialog):

    def __init__(self):
        super(NewGoalInput, self).__init__()

        self._goal_raw_data = None
        self._name_entry = self._vs_entry = self._gv_entry = None
        self.dt_start_txt = self.dt_end_txt = None

        self.setLayout(self._build_layout())
        self.setWindowTitle("Insert new goal")
        self.setMinimumWidth(50)

    @property
    def goal_raw_data(self):
        return self._goal_raw_data

    def _build_layout(self):
        vlayout = QVBoxLayout()

        name_layout, self._name_entry = self._entry(label="Goal name: ")

        dt_start_layout, self.dt_start_txt = self._entry("Goal's start date: ")
        dt_start_layout.addWidget(self._open_calendar(EStage.START))
        dt_end_layout, self.dt_end_txt = self._entry("Goal's last date: ")
        dt_end_layout.addWidget(self._open_calendar(EStage.END))

        vs_layout, self._vs_entry = self._entry(label="Value as the start: ")
        gv_layout, self._gv_entry = self._entry(label="Goal value: ")

        vlayout.addLayout(name_layout)
        vlayout.addLayout(dt_start_layout)
        vlayout.addLayout(dt_end_layout)
        vlayout.addLayout(vs_layout)
        vlayout.addLayout(gv_layout)

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
        vs = self._vs_entry.text()
        gv = self._gv_entry.text()
        start_date = self.dt_start_txt.text()
        end_date = self.dt_end_txt.text()

        self._goal_raw_data = CreationData(goal_name=name,
                                           start_date=start_date,
                                           end_date=end_date,
                                           start_value=vs,
                                           goal_value=gv)
        QDialog.accept(self)

    # def _importance_items(self):
    #     importance_dict = self._data_moderator.get_data(group="event_properties",
    #                                                     parameter="importance_metrics")
    #     importance_names = list(importance_dict.keys())
    #     importance_names.sort(key=lambda i: importance_dict[i])
    #     return importance_names
    #
    # def _importance_entry(self):
    #     priority_layout = QHBoxLayout()
    #     names_label = QLabel("Event importance: ")
    #     self._priorities = QComboBox()
    #     self._priorities.addItems(self._importance_items())
    #     priority_layout.addWidget(names_label)
    #     priority_layout.addWidget(self._priorities)
    #     return priority_layout


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
