# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020

from Core.Goal.GoalFactory import GoalFactory
from Core.DataTransferTypes.CreationData import CreationData
from Framework.ExpandWithFramework import ExpandWithFramework


class Progressor(metaclass=ExpandWithFramework):
    """
    Main utility of the app core is also called by the app name - and is viewed as the main
    module of the system's source code. Controls and mediates all the actions
    of the core sub system
    """
    def __init__(self):
        self._goals = self._load_goals()

    def _load_goals(self):
        goals = {}
        goal_data = self.fw.data_moderator.get_data()
        for name, goal in goal_data.items():
            data = CreationData.build_from_dict(name, goal)
            goals.update({name: GoalFactory.create_goal(data)})
        return goals

    def add_goal(self, creation_data):
        self._goals.update({creation_data.goal_name: GoalFactory.create_goal(creation_data)})
