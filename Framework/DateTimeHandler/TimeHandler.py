# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020

from datetime import time


class TimeHandler(object):

    class TimeExpansion(time):
        """
        Expansion of python's datetime.time for arithmetic operations
        """
        MIN_FACTOR = 60
        HOUR_FACTOR = 3600

        def __int__(self):
            return self.hour * self.HOUR_FACTOR + self.minute * self.MIN_FACTOR + self.second

        def __sub__(self, other):
            return int(self) - int(other)

    @classmethod
    def time_obj_from_str(cls, _time_repr):
        """
        Create time obejct from string
        param _time_repr: string 'YYYY-MM-DD'
        return: time object (TimeHandler.TimeExpansion)
        """
        return cls.TimeExpansion(*map(int, _time_repr.split(':')))

    def is_time_format(self, p):
        """
        time format is HH:MM:SS or MM:SS
        param _str: string to be evaluated is it in time format
        return: is representing time (bool)
        """
        if isinstance(p, self.TimeExpansion):
            return True
        try:
            self.TimeExpansion(*map(int, p.split(':')))
            return True
        except Exception as e:
            return False
