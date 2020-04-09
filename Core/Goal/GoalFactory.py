# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020

from Core.Goal.Goal import *
from Framework.ExpandWithFramework import ExpandWithFramework


class GoalFactory(metaclass=ExpandWithFramework):
    """
    Goal factory class holds all the logic about what goal class to create and how,
    by looking the the creation data object.
    """

    @classmethod
    def create_goal(cls, progressor, data):
        # first - check for the numeric types
        if data.type in [int, float]:
            return QuantifiedGoal(progressor, data)
        # second - check if the goal represents a time value
        if cls.fw.time_handler.is_time_format(data.start_value):
            return TimeBasedGoal(progressor, data)
        # now the input has to be string otherwise it is a bug - the string can be enumerated or not
        elif data.type is str:
            # in the input - a dictionary means that the terms are enumerated, a list is just list of terms
            if type(data.terms) is dict:
                return EnumeratedTermsGoal(progressor, data)
            return TermBasedGoal(progressor, data)
        # invalid state will lead to creation of Null goal. it was made to prevent immediate failure
        return NullGoal(progressor, data)


class NullGoal(Goal):
    """
    The None of the Goal. Invalid type.
    """

    def __init__(self, *args, **kwargs):
        """
        safe init without calling parent init
        """
        pass

    def __getattr__(self, item):
        raise NotImplementedError('working with invalid goal')

    def completion_rate(self):
        raise NotImplementedError('working with invalid goal')

    def completion_projection_at_end(self):
        raise NotImplementedError('working with invalid goal')

    def _data_process(self, v):
        pass
