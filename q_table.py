import numpy as np

from bellman.config import Config


class QTable:
    """
    Q-таблица, или Q-функция, содержит оценку "хорошести" действий в зависимости от состояний.
    Каждая запись в Q-таблицэ задаёт соответствие между парой (состояние, действие) и оценкой:
        |State|Action|Value|
        |  s0 |  a0  |  0.5|
        |  s0 |  a1  |  1.3|
        |  s1 |  a0  | -1.0|
                ...
    В нашем случае состояние есть трёх-позиционный тупль (i, j, o), а действие просто целое число.
    """
    def __init__(self):
        letters = len(Config.letters)
        numbers = len(Config.numbers)
        orientations = len(Config.orientations)
        actions = len(Config.actions)
        self._q = np.zeros((letters, numbers, orientations, actions), dtype=np.float16) + Config.q0

    def __setitem__(self, key, value):
        """
        Данная функция дает возможность устанавливать значения в Q-таблицу как:
            q[(состояние, действие)] = value
        :param key:
            тупль (состояние, действие)
        :param value:
            вещетвенное число (т.е. float)
        """
        assert isinstance(value, float)
        s, a = key
        i, j, o = s
        self._q[i, j, o, a] = value

    def __getitem__(self, key):
        """
        Данная функция дает возможность считывать значения из Q-таблицы как:
            value = q[(состояние, действие)]
        :param key:
            тупль (состояние, действие)
        :return value:
            вещетвенное число (т.е. float)
        """
        s, a = key
        i, j, o = s
        return self._q[i, j, o, a]

    def get_best_action(self, s):
        """
        Для заданного состояния возвращает наилучшее действие и его q-вэлью
        :param s:
            состояние -- тупль (i, j, o)
        :return:
            тупль (action, q-value)
        """
        assert isinstance(s, tuple)

        i, j, o = s
        a = self._q[i, j, o].argmax()
        q = self._q[i, j, o, a]
        return a, q

