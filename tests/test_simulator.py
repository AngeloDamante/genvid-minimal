import os.path
from unittest import TestCase
import numpy as np
from src.simulator import aggregate_frames
from src.simulator import render_video


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

    def test_render_video(self):
        out_path = "out_test_video.mp4"
        if os.path.exists(out_path): os.remove(out_path)
        h, w = 10,10
        f1 = np.ones((h, w, 3)) * 255
        f1[8, 8, 1] = 10
        f2 = np.ones((h, w, 3)) * 255
        f2[7, 7, 1] = 10
        f3 = np.ones((h, w, 3)) * 255
        f3[6, 6, 1] = 10
        f4 = np.ones((h, w, 3)) * 255
        f4[5, 5, 1] = 10
        f5 = np.ones((h, w, 3)) * 255
        f5[4, 4, 1] = 10
        frames = [f1, f2, f3, f4, f5]

        render_video(out_path, frames, 3)
        assert os.path.exists(out_path)
