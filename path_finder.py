from utils import parse_position, parse_state
from value_iterator import ValueIterator
from pprint import pprint_map, pformat_path


def find_path(initial_state: str, target_position: str, iterations=60, debug=False):

    target = parse_position(target_position)
    vi = ValueIterator(target)

    # вычислим Q-таблицу
    for _ in range(iterations):
        vi.update()

    # вычислим путь к цели из задонного состояния
    path = vi.path(parse_state(initial_state))

    pretty_path = pformat_path(path, include_state=False)

    if debug:
        # print map with path on it
        dat = {target: '$'}
        for s in path:
            if isinstance(s, tuple):
                dat[s[0], s[1]] = '*'
        pprint_map(data=dat)
        # print path with states
        print(pformat_path(path))

    return pretty_path


if __name__ == '__main__':
    path = find_path('a3l', 'a1', debug=False)
    print(path)

