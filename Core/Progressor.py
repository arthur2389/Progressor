# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020

from Core.Goal.GoalFactory import GoalFactory
from Core.Goal.GoalSketelon import GoalSkeleton
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

    def items(self):
        """
        return: iterator over the goals of the progressor
        """
        return self._goals.items()

    def add_goal(self, skeleton):
        """
        Add new goal
        param creation_data: gaol creation data
        """
        g = self.factory.create_goal(self, skeleton)
        self._goals.update({skeleton.goal_name: g})
        self.dump_to_database(g)

    def remove_goal(self, name):
        """
        Delete a goal
        param goal_name: name of the goal
        """
        try:
            del self._goals[name]
        except KeyError:
            raise KeyError('goal with name {0} does not exists'.format(name))
        self.fw.data_moderator.delete_data(parameter=name)

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
        Append goal data to the database
        param goal: goal to sump to database
        """
        self.fw.data_moderator.write_data(parameter=goal.goal_name,
                                          new_data=goal.skeleton.as_dict())

    def _load_goals(self):
        """
        Load goals from the database into 'Goal' type objects
        return: dict {str: Goal}
        """
        goals = {}
        goal_data = self.fw.data_moderator.get_data()
        for name, goal in goal_data.items():
            skeleton = GoalSkeleton.build_from_loaded_data(name, goal)
            goals.update({name: self.factory.create_goal(self, skeleton)})
        return goals
