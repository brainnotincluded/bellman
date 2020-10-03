from q_table import QTable
from transitions import Transitions
from v_table import VTable


class ValueIterator:
    def __init__(self, target_position):
        self.target_position = target_position
        self._tran = Transitions()
        self._rewards = Rewarder(target_position)
        self._q_tab = QTable()
        self._v_tab = VTable()

    def update(self):
        for s in self.all_states():
            for a in range(3):
                s1 = self._tran.run(s, a)
                if s1:
                    rew = self._rewards[s, s1]
                    self._q_tab[s, a] = rew + 0.7 * self._v_tab[s1]
                else:  # punish impossible transition
                    self._q_tab[s, a] = -1000.

        for s in self.all_states():
            for a in range(3):
                _, q = self._q_tab.get_best_action(s)
                self._v_tab[s] = q

    def all_states(self):
        for i in range(len(Config.letters)):
            for j in range(len(Config.numbers)):
                # if (i, j) == self.target_position:
                #     continue
                for o in range(4):
                    yield i, j, o

    def path(self, s0):
        a, _ = self._q_tab.get_best_action(s0)
        s1 = self._tran.run(s0, a)
        if not s1:
            raise ValueError("Forbidden transition: " + s0 + " " + a)
        elif (s1[0], s1[1]) == self.target_position:
            return [s0, a, s1]
        return [s0, a] + self.path(s1)


if __name__ == '__main__':
    from rewarder import Rewarder
    from config import parse_position, Config, parse_state
    from pprint import pprint_map, pformat_path

    target = parse_position('e4')
    vi = ValueIterator(target)

    # вычислим Q-таблицу
    for _ in range(15):
        vi.update()
    # вычислим путь к цели из задонного состояния
    path = vi.path(parse_state('a3f'))

    print(pformat_path(path))
    print(pformat_path(path, include_state=False))

    dat = {target: '$'}
    for s in path:
        if isinstance(s, tuple):
            dat[s[0], s[1]] = '*'
    pprint_map(data=dat)
    print(path)
    # print(vi._v_tab._v.max(axis=2).T)
    print("done")
