from Core.Progressor import Progressor


if __name__ == '__main__':
    progressor = Progressor()
    goal_name = input('Enter a goal name to edit current value: ')
    g = progressor.get_goal(goal_name)
    new_value = input('Enter a new value for the goal: ')
    g.set_curr_value(new_value)
