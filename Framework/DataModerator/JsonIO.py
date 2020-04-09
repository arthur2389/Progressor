# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020

import json
from os import path


def json_io_method(func):
    def add_json_suffix(*args, **kwargs):
        list_args = list(args)
        list_args[0] += ".json"
        return func(*list_args, **kwargs)
    return add_json_suffix


class JsonIO(object):
    """
    Json operations manager. Dumps data to json files, and reads data from json files while controlling
    the read data reference the avoid multiple access to the same json file.
    This class methods won't support keyword arguments !!!
    """

    parsed_data = {}

    @staticmethod
    @json_io_method
    def file_exists(file_path):
        return path.exists(file_path)

    @staticmethod
    @json_io_method
    def create_empty_file(file_path):
        """
        Method won't support keyword arguments !!!
        Create a new empty json file
        param filePath: json file full path  (str)
        """
        with open(file_path, "w") as file_to_write:
            json.dump({}, file_to_write)

    @staticmethod
    @json_io_method
    def read(file_path):
        """
        Method won't support keyword arguments !!!
        Read from json file. The read data is stoted in parsedData dictionary.
        If file is already read, return the stored data from parsedData dictionary.
        param: filePath: full path to json file (str)
        """
        # If the file is already read return the content, otherwise read the file, assign
        # the content the the dictionary and return the data.
        if file_path in JsonIO.parsed_data.keys():
            return JsonIO.parsed_data[file_path]
        JsonIO.parsed_data[file_path] = json.load(open(file_path))
        return JsonIO.parsed_data[file_path]

    @staticmethod
    @json_io_method
    def write_append(file_path, field, data):
        """
        Method won't support keyword arguments !!!
        Write data to json file
        param filePath: full path to data (str)
        param field: field to write (str)
        param data: data to write to the field  (str)
        """
        # Read file if it not already read
        if file_path not in JsonIO.parsed_data:
            JsonIO.parsed_data[file_path] = json.load(open(file_path))

        # Change the field in read reference and dump the content
        JsonIO.parsed_data[file_path][field] = data
        with open(file_path, 'w') as file_to_write:
            json.dump(JsonIO.parsed_data[file_path], file_to_write, indent=4)
        return JsonIO.parsed_data[file_path]

    @staticmethod
    @json_io_method
    def delete(file_path, field):
        """
        Delete a field from a file
        param file_path: file path
        param field: field name
        """
        if file_path not in JsonIO.parsed_data or field not in JsonIO.parsed_data[file_path]:
            raise NameError('file path or field name input to JsonIO are invalid')

        del JsonIO.parsed_data[file_path][field]

        with open(file_path, 'w') as file_to_write:
            json.dump(JsonIO.parsed_data[file_path], file_to_write, indent=4)

    @staticmethod
    @json_io_method
    def write(file_path, data):
        """
        Method won't support keyword arguments !!!
        Write data to json file
        param filePath: full path to data (str)
        param data: data to write to the field  (str)
        """
        # Change the field in read reference and dump the content
        JsonIO.parsed_data[file_path] = data
        with open(file_path, 'w') as file_to_write:
            json.dump(data, file_to_write, indent=4)
