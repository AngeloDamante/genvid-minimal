import unittest
import numpy as np
from src.evolver import Evolver
import cv2

frame_w = 1280
frame_h = 720
frame = np.zeros((frame_h, frame_w, 3))
patch = np.ones((3, 3, 3))

class Test_evolver(unittest.TestCase):
    def test_apply_patch(self):
        x = np.array([200, 400], dtype=int)
        modified_frame = Evolver.apply_patch(frame, patch, x)
        self.assertEqual(np.all(modified_frame[199:202, 399:401] == 1), True)
        self.assertEqual(np.all(modified_frame == 1), False)
        self.assertEqual(np.count_nonzero(modified_frame) / 3, 9)

        x = np.array([0, 0], dtype=int)
        modified_frame = Evolver.apply_patch(frame, patch, x)
        self.assertEqual(np.count_nonzero(modified_frame) / 3, 4)

    def test_apply_patch_failure(self):
        x = np.array([-2, -2], dtype=int)
        modified_frame = Evolver.apply_patch(frame, patch, x)
        self.assertEqual(np.count_nonzero(modified_frame) / 3, 0)

        x = np.array([-1, -1], dtype=int)
        modified_frame = Evolver.apply_patch(frame, patch, x)
        self.assertEqual(np.count_nonzero(modified_frame) / 3, 1)

    def test_computing_evolve(self):
        pass


if __name__ == '__main__':
    unittest.main()
