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
        self._name = data.goal_name
        self._values = None
        self._dates = self._Stages(st=self.fw.date_handler.date_from_str(data.start_date),
                                   curr=self.fw.date_handler.today(),
                                   end=self.fw.date_handler.date_from_str(data.end_date))

        self._status = self._define_status()

    @property
    def goal_name(self):
        return self._name

    @property
    def start_date(self):
        return self._dates[EStage.START]

    @property
    def end_date(self):
        return self._dates[EStage.END]

    def start_value(self):
        return self._values[EStage.START]

    def end_value(self):
        return self._values[EStage.END]

    def curr_value(self):
        return self._values[EStage.CURRENT]

    def set_curr_value(self, val):
        self._values[EStage.CURRENT] = val

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
        return "(Goal of type : {0}, name: {1})".format(self.__class__.__name__, self.goal_name)


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
        self._terms = data.terms

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
        return self._terms


class EnumeratedTermsGoal(Goal):

    def __init__(self, data):
        super(EnumeratedTermsGoal, self).__init__(data)
        self._terms = data.terms
        self._value_to_term_map = {v: k for k, v in data.terms.items()}
        self._values = self._Stages(st=self.enum_value(data.start_value),
                                    curr=self.enum_value(data.curr_value),
                                    end=self.enum_value(data.goal_value))

    def enum_value(self, k):
        return float(self._terms[k])

    def start_value(self):
        sv = self._values[EStage.START]
        return sv, self._value_to_term_map[sv]

    def end_value(self):
        ev = self._values[EStage.END]
        return ev, self._value_to_term_map[ev]

    def curr_value(self):
        cv = self._values[EStage.CURRENT]
        return cv, self._value_to_term_map[cv]

    def set_curr_value(self, val):
        self._values[EStage.CURRENT] = self.enum_value(val)

    def terms(self):
        """
        return: the terms used in this goal
        """
        return self._terms
