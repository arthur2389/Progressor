from Framework.Framework import get_framework


class ExpandWithFramework(type):

    def __new__(cls, name, bases, dct):
        inst = super().__new__(cls, name, bases, dct)
        inst.fw = get_framework()
        return inst
