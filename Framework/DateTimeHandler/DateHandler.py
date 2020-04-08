# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020
from datetime import date
from EnumTypes import *


class DateHandler(object):

    def __init__(self):
        self._ref_date = date(1990, 1, 1)

    def today(self):
        return date.today()

    def day_diff(self, st_date, end_date):
        return self.date_from_str(end_date) - self.date_from_str(st_date)

    @staticmethod
    def date_from_str(_str):
        _split_vals = list(map(int, _str.split('-')))
        return date(year=_split_vals[0], month=_split_vals[1], day=_split_vals[2])
