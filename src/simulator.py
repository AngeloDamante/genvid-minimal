import numpy as np
import os
import sys
import cv2
import logging
from tqdm import tqdm

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
    zeros_ = np.array([0,0,0])
    logging.info("Aggregating frames...")
    for frame_index in tqdm(range(max([len(l) for l in levels]))):
        base_frame = background.copy()
        for i in range(len(levels)):
            if frame_index < len(levels[i]):
                frame = levels[i][frame_index]
                mask = frame == zeros_
                mask_inverse = (1 - mask) == zeros_
                base_frame = mask_inverse * frame + base_frame * mask
        frames_out.append(base_frame)
    return frames_out


def render_video(video_path:str, frames:list, fps:int):
    if not video_path.endswith('.mp4'): video_path = video_path + '.mp4'
    frameSize = frames[0].shape[1], frames[0].shape[0]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(video_path, fourcc, fps, frameSize)
    logging.info("Rendering frames...")
    for frame in frames:
        out.write(frame.astype('uint8'))
    out.release()


def build_datasets_dir(base_dir):
    if not os.path.exists(base_dir): os.makedirs(base_dir)
    i = 0
    def build(d, index): return os.path.join(d, "seq{}".format(index))
    while os.path.exists(build(base_dir, i)): i += 1
    dir = build(base_dir, i)
    os.makedirs(dir)
    return dir


def create_annotation(annotation_ul_dr, w:int, h:int):
    uh, uw, dh, dw = annotation_ul_dr
    # [cx, cy, w, h] relative to w, h
    return [((dw+uw)/2.0)/w, ((dh+uh)/2.0)/h, (dw-uw)/w, (dh-uh)/h]


def simulate(width: int, height: int, background: np.ndarray, instructions: list, dataset_dir: str, video_out: str=None, fps: int = 30):
    empty_back = np.array((0, 0, 0))
    dataset_dir = build_datasets_dir(dataset_dir)
    logging.info("Saving annotations in {}".format(dataset_dir))
    levels = []
    ann_out = []
    logging.info("Evolving objects...")
    for instruction in tqdm(instructions):
        evolver = Evolver(width, height, instruction.origin_x, instruction.origin_y, instruction.patch, fps)
        frames_out, annotations = evolver.compute_evolutions(instruction.route)
        levels.append(frames_out)
        ann_out.append([(instruction.label, ann) for ann in annotations])
    frames_out = aggregate_frames(levels, background)
    logging.info("Writing dataset in yolo annotations...")
    for i in tqdm(range(len(frames_out))):
        fn = os.path.join(dataset_dir, "{:010d}".format(i))
        cv2.imwrite(fn + ".png", frames_out[i])
        with open(fn + ".txt", 'w') as file:
            for j in range(len(ann_out)):
                if i < len(ann_out[j]):
                    label, ann = ann_out[j][i]
                    ann_yolo = create_annotation(ann, width, height)
                    file.write("{} {} {} {} {}\n".format(label, ann_yolo[0], ann_yolo[1], ann_yolo[2], ann_yolo[3]))
    if video_out is not None:
        render_video(video_out, frames_out, fps)
    return frames_out
