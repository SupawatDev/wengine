import numpy as np

def Distance(position_1, position_2):
    pos1 = np.array(position_1)
    pos2 = np.array(position_2)
    assert pos1.shape == pos2.shape

    return np.sum((pos1-pos2)**2)

def Direction(start_position, end_position):
    pos1 = np.array(start_position)
    pos2 = np.array(end_position)
    assert pos1.shape == pos2.shape

    direct = pos2 - pos1;
    norm = np.sqrt(np.sum(np.power(direct,2)))
    return direct/norm