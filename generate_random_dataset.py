import argparse
import numpy as np
import json
import cv2
import os
import logging
from src.LoggingManager import configure_logging
from create_random_routes import routes_generator
from create_random_sequence import json_generator
from typing import Tuple


if __name__ == '__main__':
    configure_logging(log_lvl=logging.DEBUG, log_console=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("-N", "--number-videos", type=int, default=5, help="Number of sequences to create.")
    parser.add_argument("-D", "--duration", type=int, default=10, help="Duration of each sequence.")
    parser.add_argument("-W", "--width", type=int, default=1280, help="Dataset frame height (e.g. 1280)")
    parser.add_argument("-H", "--height", type=int, default=720, help="Dataset frame width (e.g. 720)")
    parser.add_argument("-B", "--background", type=str, default='0,0,0', help='Background like color RGB or filename (e.g. "0,0,255", background_1.png)')
    parser.add_argument("-I", "--objects", type=str, default='', help='A subset of objets in patch dir instead of all objects (e.g. "circle.png,square.npy")')
    parser.add_argument("-SV", "--save-video", action="store_true",  help="If needed, also saves *.mp4 video file in output")
    parser.add_argument("-F", "--fps", type=int, default=30, help="Output sequence fps (e.g. 30)")
    args = parser.parse_args()

    frame_width = args.width
    frame_height = args.height
    background = args.background
    objects = [os.path.join(pa, "patches") for pa in os.listdir("patches")]
    if args.objects != '':
        objects = []
        for pa in args.objects.split(','):
            obj_path = os.path.join("patches", pa)
            if not os.path.exists(obj_path):
                obj_path = pa
                if not os.path.exists(obj_path):
                    logging.error("Unable to find patch " + pa)
                    exit(1)
    save_video = args.save_video
    fps = args.fps

    logging.info("Starting dataset creation")
    pass
    logging.info("Ended dataset creation")
