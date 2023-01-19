import numpy as np
import os
import sys
import cv2
import logging

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
sys.path.insert(0, __location__)
from evolver import Evolver


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


def build_datasets_dir(base_dir):
    if not os.path.exists(base_dir): os.makedirs(base_dir)
    i = 0
    def build(d, index): return os.path.join(d, "seq{}".format(index))
    while os.path.exists(build(base_dir, i)): i += 1
    return build(base_dir, i)


def create_annotation(annotation_ul_dr, w:int, h:int):
    uw, uh, dw, dh = annotation_ul_dr
    # [cx, cy, w, h] relative to w, h
    return [((dw+uw)/2.0)/w, ((dh+uh)/2.0)/h, (dw-uw)/w, (dh-uh)/h]


def simulate(width: int, height: int, background: np.ndarray, instructions: list, dataset_dir: str, video_out: str=None, fps: int = 30):
    empty_back = np.array((0, 0, 0))
    dataset_dir = build_datasets_dir(dataset_dir)
    logging.info("Saving annotations in {}".format(dataset_dir))
    levels = []
    ann_out = []
    for instruction in instructions:
        evolver = Evolver(width, height, instruction.origin_x, instruction.origin_y, instruction.patch, fps)
        frames_out, annotations = evolver.compute_evolutions(instruction.route)
        levels.append(frames_out)
        ann_out.append([(instruction.label, ann) for ann in annotations])
    frames_out = aggregate_frames(levels, background)
    for i in range(len(frames_out)):
        fn = os.path.join(dataset_dir, "{:010d}".format(i))
        np.save(frames_out[i], fn + ".jpg")
        with open(fn + ".txt", 'w') as file:
            for j in range(len(ann_out)):
                label, ann = ann_out[j][i]
                ann_yolo = create_annotation(ann, width, height)
                file.write("{} {} {} {} {}".format(label, ann_yolo[0], ann_yolo[1], ann_yolo[2], ann_yolo[3]))
    if video_out is not None:
        render_video(video_out, frames_out, fps)
    return frames_out
