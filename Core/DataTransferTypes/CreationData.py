# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020
from Framework.ExpandWithFramework import ExpandWithFramework


class CreationData(metaclass=ExpandWithFramework):
    """
    Raw data of the goals. Generic to all goal types
    """

    @classmethod
    def build_from_dict(cls, name, data_as_dict):
        """
        Build CreationData object from dictionary. Useful when loading data of the database
        param name: goal name (str)
        param data_as_dict: goal data as dict (dict)
        return: CreationData loaded object
        """
        return cls(goal_name=name, **data_as_dict)

    def __init__(self, goal_name, start_date, end_date, start_value, goal_value, curr_value=None, terms=None):
        """
        param goal_name: name of the goal (str)
        param start_date: goal's start date
        param end_date: goal's end date - that's when you should reach the goal value
        param start_value: the value at the start date
        param goal_value: the goal value and the end date
        param curr_value: the value right now
        param terms: for term based goal - list of terms or dict of enumerated terms
        """
        # set the type of the input goal and check that all other values are aligned
        self.type = type(start_value)
        if (type(goal_value) is not self.type) or (curr_value and type(curr_value) is not self.type):
            raise TypeError('the types of the input for goal in inconsistent')

        if self.type not in [str, int, float, self.fw.time_handler.TimeExpansion]:
            raise TypeError('input type for goal is unexpected - {0}'.split(self.type))

        self.goal_name = goal_name
        self.start_date = start_date
        self.end_date = end_date
        self.start_value = start_value
        self.goal_value = goal_value
        self.curr_value = start_value if curr_value is None else curr_value

        self.type_of_date = type(start_date)

        if terms:
            # if terms are given check that the input values are aligned to them
            self.terms = terms
            if not all(v in terms for v in [self.start_value, self.goal_value, self.curr_value]):
                raise ValueError('start, end and current values should be in the determined terms')
        else:
            self.terms = None

    def as_dict(self):
        """
        return: dict representation - mainly for dump operations
        """
        all_fileds = {"start_date": self.start_date,
                      "end_date": self.end_date,
                      "start_value": self.start_value,
                      "goal_value": self.goal_value,
                      "curr_value": self.curr_value,
                      "terms": self.terms}
        return {k: v for k, v in all_fileds.items() if v is not None}

    def __repr__(self):
        return str(self.goal_name) + ": " + str(self.as_dict())
