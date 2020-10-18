import numpy as np

from bellman.config import Config


class VTable:
    def __init__(self, initial_value=Config.v0):
        letters = len(Config.letters)
        numbers = len(Config.numbers)
        orientations = len(Config.orientations)
        self._v = np.zeros((letters, numbers, orientations), dtype=np.float16) + initial_value

    def __setitem__(self, key, value):
        i, j, o = key
        self._v[i, j, o] = value

    def __getitem__(self, key):
        i, j, o = key
        return self._v[i, j, o]

    def update_from_q_table(self, q_tab):
        self._v = q_tab._q.max(axis=3)
