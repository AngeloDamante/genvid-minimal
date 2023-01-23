import sys
import os
import logging
import numpy as np
from typing import Tuple
from src.MovementType import MovementType
from src.motion_law import urm, uarm, trapezoidal_profile

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
sys.path.insert(0, __location__)


class Evolver:
    """Evolver to implement custom video with patch applied.

    Attributes:
        frame_w(int)
        frame_h(int)
        origin(ndarray)
        patch(np.ndarray)
        fps(int)
    """

    def __init__(self, frame_w: int, frame_h: int, origin_w: int, origin_h: int, patch: np.ndarray, fps: int) -> None:
        # input
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.origin = np.array([origin_h, origin_w], dtype=float)
        self.patch = patch
        self.fps = fps

        # internal states
        self.v = 1
        self.step = float(1 / self.fps)

        # output
        self.frames = []
        self.gth = []

    def update_origin(self, origin_w: int, origin_h: int) -> None:
        self.origin = np.array([origin_h, origin_w], dtype=float)

    def update_patch(self, patch: np.ndarray) -> None:
        self.patch = patch

    def reset(self) -> None:
        self.v = 1
        self.frames.clear()
        self.gth.clear()

    def compute_evolutions(self, route: list) -> Tuple[list, list]:
        """Compute evolutions for each steps in route list.

        Args:
            route(list): list of steps for patch applied

        Returns:
            frames(list): list of frames to animate the path
            gth(list): list of path center coord in the frame
        """
        for (d_w, d_h, command, time_ms) in route:
            # compute kinematic data
            dest = np.array([d_h, d_w], dtype=float)
            t_f = time_ms / 1000
            num_frames = int(self.fps * t_f)

            # initializations
            x = np.zeros(2)
            empty_frame = np.zeros((self.frame_h, self.frame_w, 3))

            # velocity and acceleratione to compute motion laws
            vc = np.sign((dest - self.origin) / t_f)
            vc = vc * np.random.uniform(abs(dest - self.origin) / t_f + 0.001, 2 * abs(dest - self.origin) / t_f)
            self.v = (dest - self.origin) / t_f
            acc = 2 * (dest - self.origin - self.v * t_f) / (t_f ** 2)

            # compute new x-point with selected motion law for each frame
            for i in range(num_frames):
                t = i * self.step
                if command.value == MovementType.urm.value:
                    x[0] = urm(self.origin[0], self.v[0], t)
                    x[1] = urm(self.origin[1], self.v[1], t)
                elif command.value == MovementType.uarm.value:
                    x[0] = uarm(self.origin[0], self.v[0], acc[0], t)
                    x[1] = uarm(self.origin[1], self.v[1], acc[1], t)
                elif command.value == MovementType.trap.value:
                    _, x[0] = trapezoidal_profile(self.origin[0], dest[0], t_f, vc[0], t)
                    _, x[1] = trapezoidal_profile(self.origin[1], dest[1], t_f, vc[1], t)
                else:
                    logging.error("Wrong type!")
                frame, gth = self.apply_patch(empty_frame, self.patch, x)
                self.frames.append(frame)
                self.gth.append(gth)
            self.origin = dest
        return self.frames, self.gth

    @staticmethod
    def apply_patch(frame: np.ndarray, patch: np.ndarray, x: np.ndarray) -> Tuple[np.ndarray, list]:
        """To Apply patch in desired frame.

        Args:
            frame(ndarray)
            patch(ndarray)
            x(ndarray): center of patch in frame reference

        Returns:
            frame with applied patch and the coord where It is applied
            [top_left_x, top_left_y, bottom_right_x, bottom_right_y]
        """
        # compute coord
        x = np.floor(x)
        r_i = int(x[0] - int(patch.shape[0] / 2))
        r_f = int(x[0] + int(patch.shape[0] / 2) + 1)
        c_i = int(x[1] - int(patch.shape[1] / 2))
        c_f = int(x[1] + int(patch.shape[1] / 2) + 1)

        # check patch
        if patch.shape[0] % 2 == 0:
            r_f = int(x[0] + int(patch.shape[0] / 2))

        if patch.shape[1] % 2 == 0:
            c_f = int(x[1] + int(patch.shape[1] / 2))

        # out of border
        if r_i >= frame.shape[0] or r_f <= 0 or c_i >= frame.shape[1] or c_f <= 0:
            return frame, [-1, -1, -1, -1]

        # fix frame indices to handle edges
        fr_i = max(0, r_i)
        fr_f = min(frame.shape[0], r_f)
        fc_i = max(0, c_i)
        fc_f = min(frame.shape[1], c_f)

        # fix path indices to handle edges
        pc_f = patch.shape[1] - (c_f - fc_f)
        pc_i = fc_i - c_i
        pr_f = patch.shape[0] - (r_f - fr_f)
        pr_i = fr_i - r_i

        # patch
        frame = frame.copy()
        frame[fr_i:fr_f, fc_i:fc_f, :] = patch[pr_i:pr_f, pc_i:pc_f, :]
        return frame, [fr_i, fc_i, fr_f - 1, fc_f - 1]
