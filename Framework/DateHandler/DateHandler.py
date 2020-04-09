# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020

from datetime import date


class DateHandler(object):

    def __init__(self):
        self._ref_date = date(1990, 1, 1)

    def today(self):
        """
        return: today's date (datetime.date)
        """
        return date.today()

    @staticmethod
    def date_from_str(_str):
        """
        date object from string
        param _str: string value
        return: date (datetime.date)
        """
        _split_vals = list(map(int, _str.split('-')))
        return date(year=_split_vals[0], month=_split_vals[1], day=_split_vals[2])
