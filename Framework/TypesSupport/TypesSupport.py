# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020


class TypesSupport(object):

    @staticmethod
    def try_float_cast(v):
        try:
            return float(v)
        except ValueError:
            return v
