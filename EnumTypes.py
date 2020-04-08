from enum import Enum


class EDateFormat(Enum):
    STR = 1
    VALUE = 2


class EGoalStatus(Enum):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    FINISHED = 3


class EStage(Enum):
    START = 1
    CURRENT = 2
    END = 3
