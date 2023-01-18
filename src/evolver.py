import numpy as np
from typing import Tuple
import cv2
import logging
import os
import sys
__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))
sys.path.insert(0, __location__)

from MovementType import MovementType


def evolve(frame_w: int, frame_h: int, origin_w: int, origin_h: int, patch: np.ndarray, route: list, fps: int) -> Tuple[list, list]:
    # q_i, q_f, t_f [s]
    origin = np.array([origin_h, origin_w], dtype=float)
    dest = np.array([route[0][0], route[0][1]], dtype=float)
    t_f = route[0][3] / 1000
    
    # compute num frames and step
    num_frames = int(fps * t_f)
    step = float(1 / fps)
    
    # extract commands    
    commands = [route[i][2] for i in range(len(route))]

    frames = []
    for command in commands:
        if command == MovementType.linear:
            # compute velocity
            v = (dest - origin) / t_f

            frames = []
            for i in range(num_frames + 1):
                frame = np.zeros((frame_h, frame_w))
                t = i * step

                # motion law
                x = origin + v*t

                # apply patch
                r_i = int(x[0] - patch.shape[0] / 2)
                r_f = int(x[0] + patch.shape[0] / 2)
                c_i = int(x[1] - patch.shape[1] / 2)
                c_f = int(x[1] + patch.shape[1] / 2)
                
                frame[r_i:r_f, c_i:c_f] = patch
                frames.append(frame)
                
        elif command == MovementType.acc:
            pass
        elif command == MovementType.dec:
            pass
        elif command == MovementType.trap:
            pass
        else:
            logging.error("Wrong type!")
            pass
    

def compute_linear(origin: np.ndarray, dest: np.ndarray, t_f:float, num_frames:int, step:float) -> list:
    pass