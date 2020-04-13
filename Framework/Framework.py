# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020
import importlib

from Framework.DataModerator.DataModerator import DataModerator
from Framework.DateHandler.DateHandler import DateHandler
from Framework.TimeHandler.TimeHandler import TimeHandler
from Framework.TypesSupport.TypesSupport import TypesSupport


class Framework(object):
    """
    Progressor Framework is a python extension for the benefit of progressor app. It is global, and it consists
    of multiple tools that extend python functionality (E.g. data moderator extends storage IO, or date handler
    that extends python's datetime.date numeric operations) and those tools cannot use onr another by design.
    Each tool has a property of it's name - and any class in the app source code can use (unless it is another tool).
    To get Framework tools a class should mention ExtendWithFramework as it's metaclass.
    """

    def __init__(self):
        self._time_keeper_ops = []
        self._data_moderator = DataModerator()
        self._date_handler = DateHandler()
        self._time_handler = TimeHandler()
        self._types = TypesSupport()
        self._widgets = importlib.import_module(name='Framework.Widgets.Widgets')

    @property
    def time_handler(self):
        return self._time_handler

    @property
    def date_handler(self):
        return self._date_handler

    @property
    def data_moderator(self):
        return self._data_moderator

    @property
    def types(self):
        return self._types

    @property
    def widgets(self):
        return self._widgets

    def register_for_time_keeper(self, func):
        self._time_keeper_ops.append(func)


# framework is static type
framework = Framework()


def get_framework():
    global framework
    return framework
