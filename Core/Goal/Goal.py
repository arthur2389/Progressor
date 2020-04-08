# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020
from EnumTypes import *
from Framework.ExpandWithFramework import ExpandWithFramework


class Goal(metaclass=ExpandWithFramework):
    """
    Class represents goals of the end user
    """
    class _Stages(object):

        def __init__(self, st, curr, end):
            self._stages = {EStage.START: st,
                            EStage.CURRENT: curr,
                            EStage.END: end}

        def __getitem__(self, item):
            return self._stages[item]

        def __setitem__(self, stage, value):
            self._stages[stage] = value

        def as_dict(self):
            return self._stages

        def completed_pct(self):
            return (abs(self._stages[EStage.CURRENT] - self._stages[EStage.START])
                    / abs(self._stages[EStage.END] - self._stages[EStage.START]))

    def __init__(self, data):
        """
        param data:
        """
        self._data = data
        self._values = None
        self._dates = self._Stages(st=self.fw.date_handler.date_from_str(data.start_date),
                                   curr=self.fw.date_handler.today(),
                                   end=self.fw.date_handler.date_from_str(data.end_date))
        self._status = self._define_status()

    def completion_rate(self):
        """
        return: goal completion rate right to this day
        """
        return round(self._values.completed_pct() * 100, 2)

    def completion_projection_at_end(self):
        """
        return: goal completion rate projected at the end day
        """
        if self._status == EGoalStatus.NOT_STARTED:
            return 0
        elif self._status == EGoalStatus.FINISHED:
            return self.completion_rate()
        return round(self.completion_rate() / self._dates.completed_pct(), 2)

    def _define_status(self):
        """
        return: goal current status right to this day (EGoalStatus)
        """
        if self._dates[EStage.CURRENT] < self._dates[EStage.START]:
            return EGoalStatus.NOT_STARTED
        elif self._dates[EStage.CURRENT] > self._dates[EStage.END]:
            return EGoalStatus.FINISHED
        return EGoalStatus.IN_PROGRESS

    def __repr__(self):
        return "(Goal of type : {0}, data: {1})".format(self.__class__.__name__, repr(self._data))


class QuantifiedGoal(Goal):

    def __init__(self, data):
        super(QuantifiedGoal, self).__init__(data)
        self._values = self._Stages(st=float(data.start_value),
                                    curr=float(data.curr_value),
                                    end=float(data.goal_value))


class TimeBasedGoal(Goal):

    def __init__(self, data):
        super(TimeBasedGoal, self).__init__(data)
        self._values = self._Stages(st=float(self.fw.time_handler.time_format_to_sec(data.start_value)),
                                    curr=float(self.fw.time_handler.time_format_to_sec(data.curr_value)),
                                    end=float(self.fw.time_handler.time_format_to_sec(data.goal_value)))


class TermBasedGoal(Goal):

    def __init__(self, data):
        super(TermBasedGoal, self).__init__(data)
        self._values = self._Stages(st=data.start_value,
                                    curr=data.curr_value,
                                    end=data.goal_value)

    def completion_rate(self):
        """
        return: non applicable for term based goal
        """
        return 'N\A'

    def completion_projection_at_end(self):
        """
        return: non applicable for term based goal
        """
        return 'N\A'

    def terms(self):
        """
        return: the terms used in this goal
        """
        return set(self._values.as_dict().values())
