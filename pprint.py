from config import Config
from utils import position_to_str, state_to_str, action_to_str


def pprint_map(data=None):
    if data is None:
        data = {}

    def edge_weight(ij1, ij2):
        p1, p2 = position_to_str(ij1), position_to_str(ij2)
        w = Config.edges.get((p1, p2))
        if w:
            return w
        else:
            return Config.edges.get((p2, p1))

    s = '      a   b   c   d   e   f   g\n\n'
    for j in range(len(Config.numbers)):
        h = '    #'
        if j == 2:
            v = str(j + 1) + '--->'
        else:
            v = str(j + 1) + '    '
        for i in range(len(Config.letters)):
            w = edge_weight((i, j), (i, j - 1))
            if not w or w >= -1.:
                h += '   #'
            else:
                h += ' - #'
            if (i, j) in data:
                t = data[i, j]
            else:
                t = ' '
            if i == len(Config.letters) - 1:
                w = None
            else:
                w = edge_weight((i, j), (i + 1, j))
            if not w or w >= -1.:
                v += ' {}  '.format(t)
            else:
                v += ' {} |'.format(t)
        s += h + '\n'
        s += v + '\n'
    s += '    #'
    for _ in Config.letters:
        s += '   #'
    s += '\n'
    print(s)


def pformat_path(path, include_state=True):
    ppath = []
    for elem in path:
        if isinstance(elem, tuple):
            if include_state:
                ppath.append(state_to_str(elem))
        else:
            ppath.append(action_to_str(elem))

    return ppath


def pprint_transition(s1, a, s2, rew):
    tran_str = state_to_str(s1) + "-" + action_to_str(a) + "->" + state_to_str(s2) + " : " + str(rew)
    print(tran_str)


if __name__ == '__main__':
    pprint_map()
