from unittest import TestCase
import numpy as np
from src.simulator import aggregate_frames


class Test(TestCase):
    def test_aggregate_frames(self):
        h, w = 10, 10
        bg = np.zeros((h, w, 3))

        f1 = np.zeros((h, w, 3))
        f1[1, 1, 2] = 255
        f2 = np.zeros((h, w, 3))
        f2[2, 2, 2] = 255
        l1 = [f1, f2]

        f3 = np.zeros((h, w, 3))
        f3[9, 9, 2] = 255
        f4 = np.zeros((h, w, 3))
        f4[9, 8, 2] = 255
        f5 = np.zeros((h, w, 3))
        f5[9, 7, 2] = 255
        l2 = [f3, f4, f5]

        all_levels = [l1, l2]

        res = aggregate_frames(all_levels, bg)
        assert type(res) is list
        assert len(res) == 3
        assert type(res[0]) is np.ndarray

        assert res[0][5, 5, 2] == 0

        assert res[0][9, 9, 2] == 255
        assert res[0][1, 1, 2] == 255

        assert res[1][2, 2, 2] == 255
        assert res[1][9, 8, 2] == 255

        assert res[2][9, 7, 2] == 255
