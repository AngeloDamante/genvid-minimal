import numpy as np
import os
import sys

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
sys.path.insert(0, __location__)
from evolver import evolve


class Instruction:
    label: int = 0
    origin_x: int = 0
    origin_y: int = 0
    patch: np.ndarray = None
    route: list = None

    def __init__(self, label: int, patch: np.ndarray, origin_x: int, origin_y: int, route: list):
        self.label = label
        self.patch = patch
        self.route = route
        self.origin_x = origin_x
        self.origin_y = origin_y


def aggregate_frames(levels: list, background: np.ndarray) -> list:
    frames_out = []
    for frame_index in range(max([len(l) for l in levels])):
        for level in levels:
            for i, frame in enumerate(level):
                if i >= len(frames_out):
                    frames_out.append(background.copy())
                mask = frame == (0, 0, 0)
                frames_out[i] = (1 - mask) * frame + frames_out[i] * mask
    return frames_out


def simulate(width: int, height: int, background: np.ndarray, instructions: list, fps: int = 30):
    empty_back = np.array((0, 0, 0))
    levels = []
    for instruction in instructions:
        frames_out = evolve(frame_w=width,
                            frame_h=height,
                            origin_w=instruction.origin_x,
                            origin_h=instruction.origin_y,
                            patch=instruction.patch,
                            route=instruction.route,
                            fps=fps)
        levels.append(frames_out)
    frames_out = aggregate_frames(levels, background)
    return frames_out
