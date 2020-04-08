# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020
from datetime import time


class TimeHandler(object):

    class TimeExpansion(time):

        MIN_FACTOR = 60
        HOUR_FACTOR = 3600

        def __int__(self):
            return self.hour * self.HOUR_FACTOR + self.minute * self.MIN_FACTOR + self.second

        def __float__(self):
            return float(self.__int__())

    @classmethod
    def time_obj(cls, hour, min, sec):
        return cls.TimeExpansion(hour, min, sec)

    def time_format_to_sec(self, _time):
        """
        param _str: time
        return:
        """
        if isinstance(_time, self.TimeExpansion):
            return int(_time)

        time_obj = self.TimeExpansion(*map(int, _time.split(':')))
        return int(time_obj)

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
