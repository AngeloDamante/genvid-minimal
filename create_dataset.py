import argparse
import numpy as np
import json
import cv2
import os
import logging
from src.simulator import simulate


def parse_background(bg: str) -> np.ndarray:
    np_background = np.zeros((frame_height, frame_width, 3))
    if os.path.exists(args.background):
        np_background = cv2.imread(args.background, mode='RGB')
    if ',' in bg:
        parts = args.background.split(',')
        if len(parts) >= 3:
            try:
                r,g,b = int(parts[0]), int(parts[0]), int(parts[0])
                np_background = np.zeros((frame_height, frame_width, 3))
                r = np.ones((frame_height, frame_width)) * r
                g = np.ones((frame_height, frame_width)) * g
                b = np.ones((frame_height, frame_width)) * b
                np_background = np.dstack((r, g, b))
            except Exception as e:
                logging.error("Unable to convert 'R,G,B' format from {}".format(bg))
                exit(1)
    else:
        logging.error("Unable to parse background color '{}'".format(bg))
        exit(2)
    return np_background


def check_json_field(index: int, json_dict:dict, val:str, required:bool=True, default_val=None):
    if val not in json_dict:
        if required:
            logging.error("Missing field {} from in json dict at object[{}]!".format(val, index))
            exit(4)
        else:
            json_dict[val] = default_val


def parse_json(fn) -> list:
    if not os.path.exists(args.input_json):
        logging.error("input json file does not exist")
        exit(3)
    with open(fn, 'r') as file:
        json_file = json.load(file)
    # Check json instructions
    for i, obj_info in enumerate(json_file):
        check_json_field(i, obj_info, "patch_label", required=True)
        check_json_field(i, obj_info, "patch_ratio", required=False, default_val=1)
        check_json_field(i, obj_info, "route", required=True)
        check_json_field(i, obj_info, "patch", required=True)
    return json_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-W", "--width", type=int, default=1280, help="Dataset frame height (e.g. 1280)")
    parser.add_argument("-H", "--height", type=int, default=720, help="Dataset frame width (e.g. 720)")
    parser.add_argument("-B", "--background", type=str, default='0,0,0',
                        help="Background like color RGB or filename (e.g. '0,0,255', background_1.png)")
    parser.add_argument("-I", "--input-json", type=str, required=True, help="json filename for sequence creation")
    parser.add_argument("-O", "--output-dir", type=str, help="Output directory (e.g. 'datasets_out'")
    args = parser.parse_args()

    frame_width = args.width
    frame_height = args.height
    np_background = parse_background(args.background)
    json_info = parse_json(args.input_json)


    simulate(frame_width, frame_height, None)
