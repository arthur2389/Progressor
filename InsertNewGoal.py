import sys

from Core.Progressor import Progressor
from Interface.NewGoal.NewGoalFirstPhase import NewGoalFirstPhase
from Interface.NewGoal.NewGoalSecondPhase import NewGoalSecondPhase
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def _font():
    """
    Get font object with font properties
    """
    font = QFont()
    font.setPointSize(12)
    return font


if __name__ == '__main__':
    progressor = Progressor()
    app = QApplication(sys.argv)
    app.setFont(_font())
    new_goal_winI = NewGoalFirstPhase(progressor)
    if new_goal_winI.exec_():
        inp = new_goal_winI.goal_init_data
        new_goal_winII = NewGoalSecondPhase(goal_name=inp['name'],
                                            start_date=inp['start_date'],
                                            end_date=inp['end_date'],
                                            status=inp['status'],
                                            terms=inp['terms'])
        if new_goal_winII.exec_():
            progressor.add_goal(creation_data=new_goal_winII.goal_raw_data)
            pass
