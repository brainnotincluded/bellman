from config import Config


def position_to_str(ij):
    i, j = ij
    return Config.letters[i] + Config.numbers[j]


def orientation_to_str(o):
    assert isinstance(o, int)
    return Config.orientations[o]  # 0 - forward, 1 - right, 2 - backward, 3 - left


_orientation_index = {a: i for i, a in Config.orientations}


def parse_orientation(o_str):
    assert isinstance(o_str, str)

    return _orientation_index[o_str]


def action_to_str(a):
    import numpy as np

    assert isinstance(a, (int, np.integer))
    return Config.actions[a]  # 0 - move forward, 1 - rotate right, 2 - rotate left


_action_index = {a: i for i, a in Config.actions}


def parse_action(a):
    assert isinstance(a, str)

    return _action_index[a]


def parse_position(p):
    i = ord(p[0]) - ord(Config.letters[0])  # ord('a') = 97
    j = ord(p[1]) - ord(Config.numbers)  # ord('1') = 49
    assert 0 <= i < len(Config.letters)
    assert 0 <= j < len(Config.numbers)
    return i, j


def parse_state(s):
    i, j = parse_position(s)
    o = parse_orientation(s[-1])
    return i, j, o


def state_to_str(s):
    i, j, o = s
    return position_to_str((i, j)) + orientation_to_str(o)


def parse_edge(edge):
    s1_str, s2_str = edge
    assert s1_str != s2_str, "Positions " + s1_str + " and " + s2_str + " must be different."
    s1 = parse_position(s1_str)
    s2 = parse_position(s2_str)
    i1, j1 = s1
    i2, j2 = s2
    assert abs(i1 - i2) <= 1 and abs(j1 - j2) <= 1, "Positions " + s1_str + " and " + s2_str + " are not adjacent."
    return s1, s2
