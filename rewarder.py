from bellman.pprint import pprint_map

from bellman.config import Config
from bellman.utils import parse_edge, parse_position, transition_to_str


class Rewarder:
    """
    Ревардер знает какое вознаграждение/наказание дать переходу из одного состояния в другое.

    Если мы хотим сказать роботу что между какимито позициями есть препятствие или затруднение,
    то мы должны задать накзание за переход между этими позициями, т.е. задать отрицательный ревард.

    И наоборот, если мы хотим сообщить роботу что в какойто позиции его цель, то мы должны задать поощрение,
    т.е. положительный ревард за переход в такую позицию.
    """
    def __init__(self, target_position=None):
        # запоминаем целевую позицию
        self.target_position = target_position
        # создаем пустой словарь для хранения вознаграждений: (p1, p2) -> reward
        self._reward = {}
        # подготавливаем вознаграждения переходов соглассно конфигурации
        for edge, weight in Config.edges.items():
            # преобразуем строковые представления в численные, например (a3, b3) в ((0, 2), (1, 2)).
            p1, p2 = parse_edge(edge)
            # прямой переход
            self._reward[p1, p2] = weight
            # обратный переход
            self._reward[p2, p1] = weight

    def __getitem__(self, transition):
        _s1, s2 = transition
        # Если целевое состояние None, т.е. запрещенное, то наказываем переход в него
        if s2 is None:
            return -1000.

        # преобразуем переход между состояниями в переход между позициями, т.е. убираем ориентацию
        edge = self._to_positions(transition)

        # ищем ревард по таблице (по словарю)
        reward = self._reward.get(edge)
        if not reward:  # если ревард НЕ найден то возвращаем значение по умолчанию
            reward = Config.edge_default_reward

        # тут вознаграждается переход в целевую позицию, если она заданна (т.е. не None)
        if self.target_position and edge[1] == self.target_position:
            reward += Config.target_transition_reward

        return reward

    @staticmethod
    def _to_positions(transition):
        s1, s2 = transition  # переход между состояниями

        i1, j1, _o1 = s1
        i2, j2, _o2 = s2

        p1 = (i1, j1)  # ориентация _o1 "выкинута"
        p2 = (i2, j2)  # ориентация _o2 "выкинута"

        edge = (p1, p2)  # переход между позициями
        return edge


if __name__ == '__main__':
    pprint_map(data={parse_position('e4'): '$'})
