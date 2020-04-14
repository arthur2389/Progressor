from Core.Progressor import Progressor
from Framework.DataModerator.JsonIO import JsonIO


def goal_data(goal):
    d = goal.skeleton.as_dict()
    d.update({'status': goal.status.value,
              'completion %': goal.completion_rate(),
              'completion % projection at end date ': goal.completion_projection_at_end()})
    return d

if __name__ == '__main__':
    _path_to_plot = "C://Users//USER//Documents//My goals//my_goals"
    progressor = Progressor()
    data = {name: goal_data(goal) for name, goal in progressor.items()}
    JsonIO.write(_path_to_plot, data)
