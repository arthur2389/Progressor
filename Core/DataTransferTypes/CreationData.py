# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020


class CreationData(object):

    @classmethod
    def build_from_dict(cls, name, data_as_dict):
        """
        param data_as_dict:
        return:
        """
        return cls(goal_name=name, **data_as_dict)

    def __init__(self, goal_name, start_date, end_date, start_value, goal_value, curr_value=None):
        """
        param goal_name: name of the goal (str)
        param start_date: goal's start date
        param end_date: goal's end date - that's when you should reach the goal value
        param start_value: the value at the start date
        param goal_value: the goal value and the end date
        param curr_value: the value right now
        """
        # set the type of the input goal and check that all other values are aligned
        self.type = type(start_value)
        if (type(goal_value) is not self.type) or (curr_value and type(curr_value) is not self.type):
            raise TypeError

        if self.type not in [str, int, float]:
            raise TypeError

        self.goal_name = goal_name
        self.start_date = start_date
        self.end_date = end_date
        self.start_value = start_value
        self.goal_value = goal_value
        self.curr_value = start_value if curr_value is None else curr_value

    def __repr__(self):
        return self.__dict__.__repr__()
