from PyQt5.QtWidgets import *
from Framework.ExpandWithFramework import ExpandWithFramework
from EnumTypes import *
from Interface.ProgressorDialog import ProgressorDialog


class DateInput(metaclass=ExpandWithFramework):

    def __init__(self, parent):
        self.text_entries = {EStage.START: None,
                             EStage.END: None}
        self.calendars = {EStage.START: ProgressorCalendar(parent),
                          EStage.END: ProgressorCalendar(parent)}
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
        super(ProgressorCalendar, self).__init__(parent=parent)
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
