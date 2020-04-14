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
    new_goal_winI = NewGoalFirstPhase()
    if new_goal_winI.exec_():
        inp = new_goal_winI.goal_init_data
        new_goal_winII = NewGoalSecondPhase(goal_name=inp['name'],
                                            date_input=inp['date_input'],
                                            status=inp['status'],
                                            terms=inp['terms'])
        if new_goal_winII.exec_():
            progressor.add_goal(skeleton=new_goal_winII.goal_raw_data)
            pass
