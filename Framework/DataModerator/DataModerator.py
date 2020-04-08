# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020

from os import path
import root
from Framework.DataModerator.JsonIO import JsonIO


class DataModerator(object):

    def __init__(self):
        self._main_path = root.get_root()
        self._path_database = path.join(self._main_path, "Data//Database")
        self._path_metadata = path.join(self._main_path, "Data//Metadata")

    def get_metadata(self, group, parameter=None):
        file_data = JsonIO.read(path.join(self._path_metadata, group))
        if not parameter:
            return file_data
        return file_data[parameter]

    def write_metadata(self, group, parameter, new_data):
        full_path = path.join(self._path_metadata, group)
        JsonIO.write(full_path, parameter, new_data)

    def get_data(self, parameter=None, group='GoalList'):
        file_data = JsonIO.read(path.join(self._path_database, group))
        if not parameter:
            return file_data
        return file_data[parameter]

    def write_data(self, parameter, new_data, group='GoalList'):
        full_path = path.join(self._path_database, group)
        JsonIO.write_append(full_path, parameter, new_data)
