# Progressor application source code
# All rights reserved
# Author: Arthur Farber
# Date: April 2020

from Core.Goal.GoalFactory import GoalFactory
from Core.Goal.GoalSketelon import GoalSkeleton
from Framework.ExpandWithFramework import ExpandWithFramework
from EnumTypes import *


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

    def add_goal(self, creation_data):
        """
        Add new goal
        param creation_data: gaol creation data
        """
        g = self.factory.create_goal(self, creation_data)
        self._goals.update({creation_data.goal_name: g})
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

    def check_dates_define_status(self, date_st, date_end):
        """
        param date_st:
        param date_end:
        return:
        """
        today = self.fw.date_handler.today()
        date_st = self.fw.date_handler.date_from_str(date_st)
        date_end = self.fw.date_handler.date_from_str(date_end)

        if date_st >= date_end:
            raise NotImplemented('start date should be before the end date')

        if today <= date_st:
            return EGoalStatus.NOT_STARTED
        elif today > date_end:
            return EGoalStatus.FINISHED
        return EGoalStatus.IN_PROGRESS

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
            data = GoalSkeleton.build_from_dict(name, goal)
            goals.update({name: self.factory.create_goal(self, data)})
        return goals
