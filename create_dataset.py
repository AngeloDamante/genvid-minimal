import argparse
import numpy as np
import json
import cv2
import os
import logging
from src.simulator import simulate, Instruction
from typing import Tuple


def parse_background(bg: str) -> np.ndarray:
    np_background = np.zeros((frame_height, frame_width, 3))
    if os.path.exists(args.background):
        np_background = cv2.imread(args.background, mode='RGB')
    if ',' in bg:
        parts = args.background.split(',')
        if len(parts) >= 3:
            try:
                r, g, b = int(parts[0]), int(parts[0]), int(parts[0])
                np_background = np.zeros((frame_height, frame_width, 3))
                r = np.ones((frame_height, frame_width)) * r
                g = np.ones((frame_height, frame_width)) * g
                b = np.ones((frame_height, frame_width)) * b
                np_background = np.dstack((r, g, b))
            except Exception as e:
                logging.error(
                    "Unable to convert 'R,G,B' format from {}".format(bg))
                exit(1)
    else:
        logging.error("Unable to parse background color '{}'".format(bg))
        exit(2)
    return np_background


def check_json_field(index: int, json_dict: dict, val: str, required: bool = True, default_val=None):
    if val not in json_dict:
        if required:
            logging.error(
                "Missing field {} from in json dict at object[{}]!".format(val, index))
            exit(4)
        else:
            json_dict[val] = default_val


def check_exists_with_default_dir(fn: str, default_dir: str):
    """
    Checks if given path exists in a default directory.
    Otherwise, it will check in current path.
    """
    # searching in his folder
    path = os.path.join(default_dir, fn)
    if not os.path.exists(path):
        # Trying as relative/abs path
        path = fn
        if not os.path.exists(path):
            logging.error(
                "File {} does not exist as path or in '{}' folder".format(fn, default_dir))
            exit(3)
    return path


def parse_instructions(istr_file: str) -> Tuple[int, int, list]:
    with open(istr_file, 'r') as file:
        route_readed = [l.strip() for l in file.readlines()]
    origin = route_readed[0].split(',')
    ox, oy = int(origin[0]), int(origin[1])
    route = []
    for i in range(1, len(route_readed), 1):
        instr = route_readed[i].split(',')
        if len(instr) == 0:
            logging.warning("Found istructions line empty, skipping")
            continue
        dw, dh, tp = int(instr[0]), int(instr[1]), str(instr[2])
        t0, t1, t2 = 0, 0, 0
        if tp == 'linear':
            t1 = int(instr[3])
        elif tp == 'acc':
            t0 = int(instr[3])
        elif tp == 'acc':
            t2 = int(instr[3])
        elif tp == 'trap':
            t0 = int(instr[3])
            t1 = int(instr[4])
            t2 = int(instr[5])
        else:
            logging.error(
                "Unable to parse step type '{}', use linear|acc,|dec|trap")
            exit(6)
        route.append({"dw": dw, "dh": dh, "t0": t0, "t1": t1, "t2": t2})
    return ox, oy, route


def parse_json(fn) -> list:
    path = check_exists_with_default_dir(fn, "sequences")
    with open(path, 'r') as file:
        json_file = json.load(file)
    # Parse instructions
    instructions = []
    for i, obj_info in enumerate(json_file):
        check_json_field(i, obj_info, "patch_label", required=True)
        check_json_field(i, obj_info, "patch_ratio",
                         required=False, default_val=1)
        check_json_field(i, obj_info, "route", required=True)
        route_path = check_exists_with_default_dir(obj_info["route"], "routes")
        check_json_field(i, obj_info, "patch", required=True)
        patch_path = check_exists_with_default_dir(
            obj_info["patch"], "patches")

        label = obj_info["patch_label"]
        if patch_path.endswith(".npy"):
            p = np.load(patch_path)
        else:
            cv2.imread(patch_path)
        ratio = obj_info["patch_ratio"]
        patch = cv2.resize(p, dsize=(
            int(p.shape[0] * ratio), int(p.shape[1] * ratio)), interpolation=cv2.INTER_AREA)
        ox, oy, route = parse_instructions(route_path)

        inst = Instruction(label=label, patch=patch,
                           origin_x=ox, origin_y=oy, route=route)
        instructions.append(inst)
    return instructions


def test_save_patches():
    """
    Create and save basic patches.
    """
    image_blank = np.zeros((101, 101, 3), np.uint8)
    image_blank[:0:50] = (0, 0, 255)  # Green in BGR format
    np.save("patches/square", image_blank)

    image_blank = np.zeros((101, 101, 3), np.uint8)
    cv2.circle(image_blank, (50, 50), 50, (0, 0, 255), -1)
    # np.save("patches/circle", image_blank)
    cv2.imwrite("patches/circle.png", image_blank)


if __name__ == '__main__':
    logging.basicConfig()
    parser = argparse.ArgumentParser()
    parser.add_argument("-W", "--width", type=int, default=1280,
                        help="Dataset frame height (e.g. 1280)")
    parser.add_argument("-H", "--height", type=int, default=720,
                        help="Dataset frame width (e.g. 720)")
    parser.add_argument("-B", "--background", type=str, default='0,0,0',
                        help="Background like color RGB or filename (e.g. '0,0,255', background_1.png)")
    parser.add_argument("-I", "--input-json", type=str,
                        required=True, help="json filename for sequence creation")
    parser.add_argument("-O", "--output-dir", type=str,
                        help="Output directory (e.g. 'datasets_out'")
    args = parser.parse_args()

    frame_width = args.width
    frame_height = args.height
    np_background = parse_background(args.background)
    instructions = parse_json(args.input_json)

    simulate(frame_width, frame_height, np_background, instructions)
