from enum import Enum


class EDateFormat(Enum):
    STR = 1
    VALUE = 2


class EGoalStatus(Enum):
    NOT_STARTED = 'Not started'
    IN_PROGRESS = 'In progress'
    FINISHED = 'Finished '


class EStage(Enum):
    START = 1
    CURRENT = 2
    END = 3
