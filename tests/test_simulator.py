from unittest import TestCase
import numpy as np
from src.simulator import aggregate_frames


class Test(TestCase):
    def test_aggregate_frames(self):
        h, w = 3, 4
        bg = np.zeros((h, w, 3))

        f1 = np.zeros((h, w, 3))
        f2 = np.zeros((h, w, 3))
        l1 = [f1, f2]

        f3 = np.zeros((h, w, 3))
        f4 = np.zeros((h, w, 3))
        f5 = np.zeros((h, w, 3))
        l2 = [f3, f4, f5]

        all_levels = [l1, l2]

        res = aggregate_frames(all_levels, bg)
        assert type(res) is list
