# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020

from Core.Goal.Goal import *
from Framework.ExpandWithFramework import ExpandWithFramework


class GoalFactory(metaclass=ExpandWithFramework):

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
        return NullGoal(progressor, data)


class NullGoal(Goal):
    """
    The None of the Goal. Invalid type
    """

    def completion_rate(self):
        """
        return: goal completion rate right to this day
        """
        raise NotImplementedError

    def completion_projection_at_end(self):
        """
        return: goal completion rate projected at the end day
        """
        raise NotImplementedError
