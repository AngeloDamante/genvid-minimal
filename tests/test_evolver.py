import unittest
import numpy as np
from src.evolver import Evolver
from src.MovementType import MovementType
import cv2

frame_w = 1280
frame_h = 720
frame = np.zeros((frame_h, frame_w, 3))
patch = np.ones((3, 3, 3))


class Test_evolver(unittest.TestCase):
    def test_apply_patch(self):
        x = np.array([200, 400], dtype=int)
        modified_frame, gth = Evolver.apply_patch(frame, patch, x)
        self.assertEqual(np.all(modified_frame[199:202, 399:402] == 1), True)
        self.assertEqual(np.all(modified_frame == 1), False)
        self.assertEqual(np.count_nonzero(modified_frame) / 3, 9)
        self.assertEqual((gth[0], gth[1], gth[2], gth[3]), (199, 399, 201, 401))

        x = np.array([0, 0], dtype=int)
        modified_frame, gth = Evolver.apply_patch(frame, patch, x)
        self.assertEqual(np.count_nonzero(modified_frame) / 3, 4)
        self.assertEqual((gth[0], gth[1], gth[2], gth[3]), (0, 0, 1, 1))

    def test_apply_patch_failure(self):
        x = np.array([-2, -2], dtype=int)
        modified_frame, gth = Evolver.apply_patch(frame, patch, x)
        self.assertEqual(np.count_nonzero(modified_frame) / 3, 0)
        self.assertEqual((gth[0], gth[1], gth[2], gth[3]), (-1, -1, -1, -1))

        x = np.array([-1, -1], dtype=int)
        modified_frame, gth = Evolver.apply_patch(frame, patch, x)
        self.assertEqual(np.count_nonzero(modified_frame) / 3, 1)
        self.assertEqual((gth[0], gth[1], gth[2], gth[3]), (0, 0, 0, 0))

    def test_compute_evolutions(self):
        circle = cv2.imread('../patches/circle.png')
        origin_w = 200
        origin_h = 300
        fps = 30
        route = [[300, 500, MovementType.urm, 1000],
                 [400, 500, MovementType.urm, 3000],
                 [600, 700, MovementType.uarm, 5000],
                 [800, 750, MovementType.uarm, 2000],
                 [300, 500, MovementType.trap, 2500],
                 [500, 650, MovementType.trap, 2500]]

        # compute evolutions
        evolver = Evolver(frame_w, frame_h, origin_w, origin_h, circle, fps)
        frames, gth = evolver.compute_evolutions(route)
        self.assertEqual(len(frames), len(gth))

        # create video
        frameSize = frames[0].shape[1], frames[0].shape[0]
        codec = cv2.VideoWriter_fourcc(*"mp4v")
        video = cv2.VideoWriter("test_video_output.mp4", codec, fps, frameSize)

        for frm in frames:
            video.write(frm.astype('uint8'))
        video.release()


if __name__ == '__main__':
    unittest.main()
