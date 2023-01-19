import sys
import os
import logging
import cv2
import numpy as np
from typing import Tuple
from MovementType import MovementType
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
sys.path.insert(0, __location__)


class Evolver:
    """ Evolver to implement custom video with patch applied.

        Attributes:
            frame_w(int) 
            frame_h(int)
            origin_w(int): origin along y-axis
            origin_h(int): origin along x-axis
            patch(np.ndarray): to apply to the frame
            fps(int)
    """

    def __init__(self,
                 frame_w: int,
                 frame_h: int,
                 origin_w: int,
                 origin_h: int,
                 patch: np.ndarray,
                 fps: int) -> None:

        # input
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.origin = np.array([origin_h, origin_w], dtype=float)
        self.patch = patch
        self.fps = fps

        # internal states
        self.v = 0
        self.step = float(1 / self.fps)

        # output
        self.frames = []
        self.gth = []

    def compute_evolutions(self, route: list) -> Tuple[list, list]:
        """ Compute evolutions for each steps in route list.

            Args:
                route(list): list of steps for patch applied

            Returns:
                frames(list): list of frames to animate the path
                gth(list): list of path center coord in the frame
        """
        for (d_w, d_h, command, time_ms) in route:

            # compute dest and final time [s]
            dest = np.array([d_h, d_w], dtype=float)
            t_f = time_ms / 1000

            # compute velocity
            num_frames = int(self.fps * t_f)
            self.v = (dest - self.origin) / t_f

            if command == "linear":
                self._compute_linear(num_frames)

            elif command == "acc":
                # TODO
                pass

            elif command == "dec":
                # TODO
                pass

            elif command == MovementType.trap:
                # TODO
                pass
            else:
                logging.error("Wrong type!")
                pass

            # update origin for next command
            self.origin = dest

        return self.frames, self.gth

    def _compute_linear(self, num_frames: int) -> None:
        """ Compute frames with uniformly rectilinear motion for patch.
        
            Args:
                num_frames(int): number of desired frames 
        """
        for i in range(num_frames + 1):
            frame = np.zeros((self.frame_h, self.frame_w, 3))

            # motion law
            t = i * self.step
            x = self.origin + self.v * t

            frame = self.apply_patch(frame, self.patch, x)

            # save
            self.frames.append(frame)
            self.gth.append(x)
            
            
    def apply_patch(self, frame: np.ndarray, patch: np.ndarray, x: np.ndarray) -> np.ndarray:
        """ To Apply patch in desired frame.

            Args: 
                frame(ndarray)
                patch(ndarray)
                x(ndarray): center of patch in frame reference
            
            Return:
                frame with apllied patch
        """
        # compute coord
        r_i = int(x[0] - patch.shape[0] / 2)
        r_f = int(x[0] + patch.shape[0] / 2)
        c_i = int(x[1] - patch.shape[1] / 2)
        c_f = int(x[1] + patch.shape[1] / 2)

        # TODO: fix path indices to handle edges
        # patch
        frame[r_i:r_f, c_i:c_f, :] = patch
        return frame