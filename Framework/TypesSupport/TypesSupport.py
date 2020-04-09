# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020


class TypesSupport(object):

    @staticmethod
    def try_int_cast(v):
        try:
            return int(v)
        except ValueError:
            return v
