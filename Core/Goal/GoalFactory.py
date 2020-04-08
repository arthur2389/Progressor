# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020

from Core.Goal.Goal import *
from Framework.ExpandWithFramework import ExpandWithFramework


class GoalFactory(metaclass=ExpandWithFramework):

    @classmethod
    def create_goal(cls, data):
        if data.type in [int, float]:
            return QuantifiedGoal(data)
        elif data.type is str:
            if cls.fw.time_handler.is_time_format(data.start_value):
                return TimeBasedGoal(data)
            return TermBasedGoal(data)
