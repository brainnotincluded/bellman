from utils import parse_position, parse_state
from value_iterator import ValueIterator
from pprint import pprint_map, pformat_path

"""
      a   b   c   d   e   f   g                    Orientations                       Actions
                                             
    #   #   #   #   #   #   #   #                        l (3)                          f (0)
1               |       | .   .                          ^                              ^
    # - #   #   #   #   #   #   #                        |                      (2) l <   > r (1)     
2       |           |     . | .                (2) b <--   --> f (0)                
    #   # - # - # - # - # - #   #                        |
3---> . | .   .   .   .   .   .                          v
    #   #   # - # - # - # - # - #                        r (1)
4     . | .   .   .   .   .   .  
    #   # - # - # - # - # - #   #
5     .   .   .   .   .   .   .  
    #   #   #   #   #   #   #   #
"""


def visualize_plan(path, target):
    """
    Распечатывает карту и путь на ней.
    :param path:
    :param target:
    :return:
    """
    # print map with path on it
    dat = {target: '+'}
    for s in path:
        if isinstance(s, tuple):
            dat[s[0], s[1]] = '.'
    pprint_map(data=dat)
    # print path with states
    print(pformat_path(path))


def find_path(initial_state: str, target_position: str, iterations=60, debug=False):
    """
    Вычисляет путь из начального состояния в конечное.
    :param initial_state:
        трёх-символьное сочетание -- буквенная координата, числовай координата, ориентация.
        Примеры: 'a3f', 'f2r', 'e4b', 'g1l'
    :param target_position:
        двух-символьное сочетание -- буквенная координата, числовай координата.
        Примеры: 'a3', 'f2', 'e4', 'g1'
    :param iterations:
        количество итераций достаточных для вычисления q-таблицы
    :param debug:
        если True то распечатается путь на карте и подробный план (с промежуточными состояниями)
    :return:
    """

    target = parse_position(target_position)
    vi = ValueIterator(target)

    # вычислим Q-таблицу
    for _ in range(iterations):
        vi.update()

    # вычислим путь к цели из задонного состояния
    path = vi.path(parse_state(initial_state))

    pretty_path = pformat_path(path, include_state=False)

    if debug:
        visualize_plan(path, target)

    return pretty_path


if __name__ == '__main__':
    path = find_path('a3f', 'f2', debug=True)
    print(path)

