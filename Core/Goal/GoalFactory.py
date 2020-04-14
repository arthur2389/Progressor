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
    def create_goal(cls, progressor, skeleton):
        # first - check for the numeric types
        if skeleton.type in [int, float]:
            return QuantifiedGoal(progressor, skeleton)
        # second - check if the goal represents a time value
        if cls.fw.time_handler.is_time_format(skeleton.start_value):
            return TimeBasedGoal(progressor, skeleton)
        # now the input has to be string otherwise it is a bug - the string can be enumerated or not
        elif skeleton.type is str:
            # in the input - a dictionary means that the terms are enumerated, unless the values are all zeros
            if skeleton.terms and all(val == 0 for val in skeleton.terms.values()):
                return TermBasedGoal(progressor, skeleton)
            return EnumeratedTermsGoal(progressor, skeleton)
        # invalid state will lead to creation of Null goal. it was made to prevent immediate failure
        return NullGoal(progressor, skeleton)


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
