# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020
import abc

from EnumTypes import *
from Framework.ExpandWithFramework import ExpandWithFramework


class Goal(metaclass=ExpandWithFramework):
    """
    Class represents goals of the end user
    """
    class _Stages(object):
        """
        Stages private object is made for storing values for calculation of certain
        properties of the goal
        """

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

    def __init__(self, progressor, data):
        """
        param data:
        """
        self._progressor = progressor
        self._name = data.goal_name
        self._values = None
        self._data = data
        self._dates = self._Stages(st=self.fw.date_handler.date_from_str(data.start_date),
                                   curr=self.fw.date_handler.today(),
                                   end=self.fw.date_handler.date_from_str(data.end_date))
        self._values = self._Stages(st=self._data_process(data.start_value),
                                    curr=self._data_process(data.curr_value),
                                    end=self._data_process(data.goal_value))

        self._status = self._define_status()

    @property
    def data(self):
        return self._data

    @property
    def goal_name(self):
        return self._name

    def __getattr__(self, item):
        """
        param item: attribute to get
        return: attribute value
        """
        return getattr(self._data, item)

    def set_curr_value(self, val):
        """
        current value setter. current value is the only field that can be set in the goal
        during the goal's life
        param val: new value for current value
        """
        if self._status != EGoalStatus.IN_PROGRESS:
            raise NotImplementedError('Cannot set value to finished or not started goal')
        val = self.fw.types.try_int_cast(val)
        self._values[EStage.CURRENT] = self._data_process(val)
        self._data.curr_value = val
        self._progressor.dump_to_database(self)

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

    @abc.abstractmethod
    def _data_process(self, v):
        pass

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

    def _data_process(self, v):
        return float(v)


class TimeBasedGoal(Goal):

    def _data_process(self, v):
        return float(self.fw.time_handler.time_format_to_sec(v))


class TermBasedGoal(Goal):

    def __init__(self, progressor, data):
        super(TermBasedGoal, self).__init__(progressor, data)
        self._terms = data.terms

    def _data_process(self, v):
        return v

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


class EnumeratedTermsGoal(Goal):

    def __init__(self, progressor, data):
        self._terms = data.terms
        self._value_to_term_map = {v: k for k, v in data.terms.items()}
        super(EnumeratedTermsGoal, self).__init__(progressor, data)

    def _data_process(self, v):
        return float(self._terms[v])
