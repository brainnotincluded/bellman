from bellman.q_table import QTable
from bellman.transitions import Transitions
from bellman.utils import state_to_str, action_to_str
from bellman.v_table import VTable
from bellman.rewarder import Rewarder
from bellman.config import Config
from bellman.pprint import pprint_transition


class ValueIterator:
    def __init__(self, target_position):
        self.target_position = target_position
        self._tran = Transitions()
        self._rewards = Rewarder(target_position)
        self._q_tab = QTable()
        self._v_tab = VTable()

    def update(self, debug=False):
        for s1 in self.all_states():
            for a in range(len(Config.actions)):
                s2 = self._tran.run(s1, a)
                rew = self._rewards[s1, s2]
                if s2:
                    q = rew + Config.gamma * self._v_tab[s2]
                else:
                    q = rew
                self._q_tab[s1, a] = q

                if debug:
                    pprint_transition(s1, a, s2, rew)

        self._v_tab.update_from_q_table(self._q_tab)

    # noinspection PyMethodMayBeStatic
    def all_states(self):
        for i in range(len(Config.letters)):
            for j in range(len(Config.numbers)):
                if (i, j) == self.target_position:
                    continue
                for o in range(len(Config.orientations)):
                    yield i, j, o

    def path(self, s0):
        a, _ = self._q_tab.get_best_action(s0)
        s1 = self._tran.run(s0, a)
        if not s1:
            raise ValueError("Переход в запрещенное состояние: " + state_to_str(s0) + "-" + action_to_str(a) + "-> None")
        elif (s1[0], s1[1]) == self.target_position:
            return [s0, a, s1]
        return [s0, a] + self.path(s1)


if __name__ == '__main__':
    from rewarder import Rewarder
    from config import parse_position, Config, parse_state
    from pprint import pprint_map, pformat_path, pprint_transition

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
