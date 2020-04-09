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
            """
            The values types in _Stages has to have __sub__ [operator '-'] functionality, as that's
            what's needed to calculate delta.
            It can be int, as well as datetime.date.
            param st: start value (any type with __sub__ functionality)
            param curr: start value (any type with __sub__ functionality)
            param end: start value (any type with __sub__ functionality)
            """
            self._stages = {EStage.START: st,
                            EStage.CURRENT: curr,
                            EStage.END: end}

        def __getitem__(self, item):
            """
            get item from stages
            param item: stage (EStage)
            return: item value
            """
            return self._stages[item]

        def __setitem__(self, stage, value):
            """
            set stage value
            param item: stage (EStage)
            param value: new value (any type with __sub__ functionality)
            """
            self._stages[stage] = value

        def delta(self):
            """
            Main method and the reason _Stages type was designed. having start, end and current values,
            calculate the delta of the progression made.
            return: delta value (X - X0)/(Xend - X0)
            """
            return (self._stages[EStage.CURRENT] - self._stages[EStage.START]) \
                       / (self._stages[EStage.END] - self._stages[EStage.START])

    def __init__(self, progressor, data):
        """
        param progressor: progressor object that built the goal - for mediation purposes (Progressor)
        param data: creation data object (CreationData)
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
        """
        return: goals raw data (CreationData)
        """
        return self._data

    @property
    def status(self):
        """
        return: goals status (EGoalStatus)
        """
        return self._status

    @property
    def goal_name(self):
        """
        return: goal name (str)
        """
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
        during the goal's life.
        param val: new value for current value
        """
        # only goal that is in progress can have it's current value changed
        if self._status != EGoalStatus.IN_PROGRESS:
            raise NotImplementedError('Cannot set value to finished or not started goal')
        # try cast to int - mainly for QuantifiedGoal representation
        val = self.fw.types.try_int_cast(val)
        # update both in the stages object and in raw data
        self._values[EStage.CURRENT] = self._data_process(val)
        self._data.curr_value = val
        # use progressor to update the database
        self._progressor.dump_to_database(self)

    def completion_rate(self):
        """
        return: goal completion rate right to this day
        """
        return round(self._values.delta() * 100, 2)

    def completion_projection_at_end(self):
        """
        return: goal completion rate projected at the end day
        """
        if self._status == EGoalStatus.NOT_STARTED:
            return 0
        elif self._status == EGoalStatus.FINISHED:
            return self.completion_rate()
        # projection is really only relevant to goal that is in progress
        return round(self.completion_rate() / self._dates.delta(), 2)

    @abc.abstractmethod
    def _data_process(self, v):
        """
        method for derived types to implement. define how to process the raw data in a way it will
        be ready to be calculated in _Stages object.
        param v: value to process
        return: processed value
        """
        pass

    def _define_status(self):
        """
        return: goal current status right to this day (EGoalStatus)
        """
        if self._dates[EStage.CURRENT] <= self._dates[EStage.START]:
            return EGoalStatus.NOT_STARTED
        elif self._dates[EStage.CURRENT] > self._dates[EStage.END]:
            return EGoalStatus.FINISHED
        return EGoalStatus.IN_PROGRESS

    def __repr__(self):
        return "(Goal of type : {0}, name: {1})".format(self.__class__.__name__, self.goal_name)


class QuantifiedGoal(Goal):
    """
    A Goal that its values are based on numbers. E.g. start value is 75 Kg body weight, goal is 95 Kg
    """

    def _data_process(self, v):
        return float(v)


class TimeBasedGoal(Goal):
    """
    A Goal that its values represent time - a time it takes to finish certain action.
    E.g. start value is 00:03:00 (4 minutes) to run 800 meters, goal is 00:02:05
    """

    def _data_process(self, v):
        return self.fw.time_handler.time_obj_from_str(v)


class TermBasedGoal(Goal):
    """
    A goal that it's values are terms. E.g like start value is "Beginner" in spanish, end value is "Expert", while
    In the middle, there is also the term "Advanced" and "Average" - and all the possible terms will
    lay under "terms" key. Calculation about goal completion are irrelevant for this type.
    """

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
    """
    Like TermBasedGoal - this class' values are also based on terms - but those terms are enumerated - which
    enables the completion states calculation. The terms field here is a map with {term: term value} fields -
    all initialized by end user - and the values are used for the completion calculations.
    """

    def _data_process(self, v):
        return float(self._data.terms[v])
