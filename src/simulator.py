import numpy as np
import os
import sys
import cv2

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


def render_video(video_path:str, frames:list, fps:int):
    if not video_path.endswith('.mp4'): video_path = video_path + '.mp4'
    frameSize = frames[0].shape[1], frames[0].shape[0]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(video_path, fourcc, fps, frameSize)
    for frame in frames:
        out.write(frame.astype('uint8'))
    out.release()


def simulate(width: int, height: int, background: np.ndarray, instructions: list, video_out: str=None, fps: int = 30):
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
    if video_out is not None:
        render_video(video_out, frames_out, fps)
    return frames_out
