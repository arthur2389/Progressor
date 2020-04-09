# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020

from os import path
import root
from Framework.DataModerator.JsonIO import JsonIO


class DataModerator(object):
    """
    The data moderator is the common interface of the progressor app claases for accessing
    the data - either the database or the app metadata. Encapsulates the technique of reading
    and writing to data.
    """

    def __init__(self):
        self._main_path = root.get_root()
        self._path_database = path.join(self._main_path, "Data//Database")
        self._path_metadata = path.join(self._main_path, "Data//Metadata")

    def get_metadata(self, group, parameter=None):
        """
        Get metadata parameter
        param group: group name (str)
        param parameter: parameter name (str)
        return: parameter value
        """
        file_data = JsonIO.read(path.join(self._path_metadata, group))
        if not parameter:
            return file_data
        return file_data[parameter]

    def get_data(self, parameter=None, group='GoalList'):
        """
        Get parameter from database
        param parameter: parameter name (str)
        param group: group name (str)
        return: parameter value
        """
        file_data = JsonIO.read(path.join(self._path_database, group))
        if not parameter:
            return file_data
        return file_data[parameter]

    def write_data(self, parameter, new_data, group='GoalList'):
        """
        Write parameter to database
        param new_data: data to write
        param parameter: parameter name (str)
        param group: group name (str)
        """
        full_path = path.join(self._path_database, group)
        JsonIO.write_append(full_path, parameter, new_data)

    def delete_data(self, parameter, group='GoalList'):
        """
        Delete parameter from database
        param parameter: parameter name (str)
        param group: group name (str)
        """
        full_path = path.join(self._path_database, group)
        JsonIO.delete(file_path=full_path, field=parameter)
