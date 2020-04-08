# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020

from Framework.DataModerator.DataModerator import DataModerator
from Framework.DateTimeHandler.DateHandler import DateHandler
from Framework.DateTimeHandler.TimeHandler import TimeHandler


class Framework(object):

    def __init__(self):
        self._time_keeper_ops = []
        self._data_moderator = DataModerator()
        self._date_handler = DateHandler()
        self._time_handler = TimeHandler()

    @property
    def time_handler(self):
        return self._time_handler

    @property
    def date_handler(self):
        return self._date_handler

    @property
    def data_moderator(self):
        return self._data_moderator

    def register_for_time_keeper(self, func):
        self._time_keeper_ops.append(func)


framework = Framework()


def get_framework():
    global framework
    return framework
