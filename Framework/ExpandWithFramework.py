# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020

from Framework.Framework import get_framework


class ExpandWithFramework(type):
    """
    Framework setter for progressor classes.
    """
    def __new__(cls, name, bases, dct):
        inst = super().__new__(cls, name, bases, dct)
        inst.fw = get_framework()
        return inst
