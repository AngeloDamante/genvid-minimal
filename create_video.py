import argparse
import numpy as np
import json
import cv2
import os
import logging
from src.simulator import simulate, Instruction
from src.MovementType import MovementType
from src.LoggingManager import configure_logging
from typing import Tuple


def parse_background(bg: str, frame_width:int, frame_height:int) -> np.ndarray:
    np_background = np.zeros((frame_height, frame_width, 3))
    bg_path = check_exists_with_default_dir_noexc(bg, "backgrounds")
    if bg_path is not None and os.path.exists(bg_path):
        new_img = cv2.imread(bg_path)
        np_background = cv2.resize(new_img, dsize=(frame_width, frame_height), interpolation=cv2.INTER_AREA)
    elif ',' in bg:
        parts = bg.split(',')
        if len(parts) >= 3:
            try:
                r, g, b = int(parts[0]), int(parts[0]), int(parts[0])
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


def check_exists_with_default_dir_noexc(fn: str, default_dir: str):
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
            return None
    return path


def check_exists_with_default_dir(fn: str, default_dir: str):
    """
    Checks if given path exists in a default directory.
    Otherwise, it will check in current path.
    Otherwise it will exit
    """
    path = check_exists_with_default_dir_noexc(fn, default_dir)
    if path is None:
        logging.error("File {} does not exist as path or in '{}' folder".format(fn, default_dir))
        exit(3)
    return path


def txt_to_MovementType(_type: str) -> MovementType:
    if _type == 'const':
        return MovementType.urm
    elif _type == 'acc':
        return MovementType.uarm
    elif _type == 'trap':
        return MovementType.trap
    else:
        logging.error("Unable to parse movement type {}".format(_type))
        exit(7)


def parse_instructions(istr_file: str) -> Tuple[int, int, list]:
    allowed_types = ['const', 'acc', 'dec', 'trap']
    with open(istr_file, 'r') as file:
        route_readed = [l.strip() for l in file.readlines()]
    origin = route_readed[0].split(',')
    ox, oy = int(origin[0]), int(origin[1])
    last_dw, last_dh = ox, oy
    route = []
    for i in range(1, len(route_readed), 1):
        instr = route_readed[i].split(',')
        if len(instr) == 0:
            logging.warning("Found istructions line empty, skipping")
            continue
        if len(instr) >=4:
            dw, dh, _type, _time = int(instr[0]), int(instr[1]), str(instr[2]).strip(), str(instr[3])
        elif len(instr) < 4 and instr[0].strip() == "pause":
            dw, dh, _type, _time = last_dw, last_dh, "const", str(instr[1])
        else:
            logging.error("Unable to parse line {}".format(route_readed[i]))
            exit(7)
        if _type not in allowed_types:
            logging.error(
                "Unable to parse step type '{}', use {}".format(_type, allowed_types))
            exit(6)
        tp = txt_to_MovementType(_type)
        route.append([dw, dh, tp, int(_time)])
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
            p = cv2.imread(patch_path)
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
    image_blank[:,:,:] = (0, 0, 255)  # Green in BGR format
    np.save("patches/square", image_blank)

    image_blank = np.zeros((101, 101, 3), np.uint8)
    cv2.circle(image_blank, (50, 50), 50, (0, 0, 255), -1)
    # np.save("patches/circle", image_blank)
    cv2.imwrite("patches/circle.png", image_blank)


if __name__ == '__main__':
    configure_logging(log_lvl=logging.DEBUG, log_console=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("-W", "--width", type=int, default=1280,
                        help="Dataset frame height (e.g. 1280)")
    parser.add_argument("-H", "--height", type=int, default=720,
                        help="Dataset frame width (e.g. 720)")
    parser.add_argument("-B", "--background", type=str, default='0,0,0',
                        help="Background like color RGB or filename (e.g. '0,0,255', background_1.png)")
    parser.add_argument("-I", "--input-json", type=str,
                        required=True, help="json filename for sequence creation")
    parser.add_argument("-O", "--output-dir", type=str, default="datasets_out",
                        help="Output directory (e.g. 'datasets_out'")
    parser.add_argument("-V", "--video", type=str, default=None,
                        help="Output video file if wanted (e.g. 'out.mp4'")
    parser.add_argument("-F", "--fps", type=int, default=30,
                        help="Output sequence fps (e.g. 30)")
    args = parser.parse_args()

    frame_width = args.width
    frame_height = args.height
    np_background = parse_background(args.background, frame_width, frame_height)
    instructions = parse_json(args.input_json)
    fps = args.fps
    video_out = args.video
    annotations_dir = args.output_dir

    simulate(frame_width, frame_height, np_background, instructions, annotations_dir, video_out, fps)
