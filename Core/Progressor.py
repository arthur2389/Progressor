# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020

from Core.Goal.GoalFactory import GoalFactory
from Core.DataTransferTypes.CreationData import CreationData
from Framework.ExpandWithFramework import ExpandWithFramework


class Progressor(metaclass=ExpandWithFramework):
    """
    Main class of the app core is also called by the app name - and is viewed as the main
    module of the system's source code. Controls and mediates all the actions
    of the core sub system
    """
    def __init__(self):
        self.factory = GoalFactory
        self._goals = self._load_goals()

    def _load_goals(self):
        goals = {}
        goal_data = self.fw.data_moderator.get_data()
        for name, goal in goal_data.items():
            data = CreationData.build_from_dict(name, goal)
            goals.update({name: self.factory.create_goal(self, data)})
        return goals

    def items(self):
        """
        return: iterator over the goals of the progressor
        """
        return self._goals.items()

    def add_goal(self, creation_data):
        g = self.factory.create_goal(self, creation_data)
        self._goals.update({creation_data.goal_name: g})
        self.dump_to_database(g)

    def get_goal(self, name):
        """
        param name: goal name
        return: goal object
        """
        try:
            return self._goals[name]
        except KeyError:
            raise KeyError('goal with name {0} does not exists'.format(name))

    def dump_to_database(self, goal):
        """
        param goal:
        return:
        """
        self.fw.data_moderator.write_data(parameter=goal.goal_name,
                                          new_data=goal.data.as_dict())
