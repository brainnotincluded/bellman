import numpy as np

from config import Config


class VTable:
    def __init__(self):
        letters = len(Config.letters)
        numbers = len(Config.numbers)
        orientations = len(Config.orientations)
        self._v = np.zeros((letters, numbers, orientations), dtype=np.float32) - 1000

    def __setitem__(self, key, value):
        i, j, o = key
        self._v[i, j, o] = value

    def __getitem__(self, key):
        i, j, o = key
        return self._v[i, j, o]
