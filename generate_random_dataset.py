import argparse
import numpy as np
import json
import cv2
import os
import logging
from src.LoggingManager import configure_logging
from create_random_route import routes_generator
from create_random_sequence import json_generator
import random


if __name__ == '__main__':
    configure_logging(log_lvl=logging.DEBUG, log_console=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, type=str, help="filename of random routes")
    parser.add_argument("-NV", "--number-videos", type=int, default=5, help="Number of sequences to create.")
    parser.add_argument("-MinR", "--min-routes", type=int, default=5, help="Min number of routes per video.")
    parser.add_argument("-MaxR", "--max-routes", type=int, default=10, help="Max number of routes per video.")
    parser.add_argument("-D", "--duration", type=float, default=10, help="Duration of each sequence (seconds).")
    parser.add_argument("-W", "--width", type=int, default=1280, help="Dataset frame height (e.g. 1280)")
    parser.add_argument("-H", "--height", type=int, default=720, help="Dataset frame width (e.g. 720)")
    parser.add_argument("-B", "--background", type=str, default='0,0,0', help='Background like color RGB or filename (e.g. "0,0,255", background_1.png)')
    parser.add_argument("-I", "--objects", type=str, default='', help='A subset of objets in patch dir instead of all objects (e.g. "circle.png,square.npy")')
    parser.add_argument("-SV", "--save-video", action="store_true",  help="If needed, also saves *.mp4 video file in output")
    parser.add_argument("-F", "--fps", type=int, default=30, help="Output sequence fps (e.g. 30)")
    args = parser.parse_args()

    name = args.name
    number_videos = args.number_videos
    if number_videos < 1:
        logging.error("--number-videos must be positive")
        exit(1)
    min_routes = args.min_routes
    max_routes = args.max_routes
    if min_routes > max_routes:
        logging.error("--min-routes can't be more than --max-routes")
        exit(2)
    duration = args.duration * 1000
    if number_videos <= 100:
        logging.error("--duration must be more than 100 ms")
        exit(3)
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

    BASE_DIR_ROUTES = "routes"
    logging.info("Creating random routes...")
    all_routes = []
    for i in range(number_videos):
        instr = random.randint(min_routes, max_routes)
        route_new = routes_generator(
            num_instructions=instr,
            duration=duration,
            frame_size=(frame_width, frame_height)
        )
        route_fn = f"{BASE_DIR_ROUTES}/route_{name}_{i}.txt"
        with open(route_fn, 'w') as outfile:
            outfile.writelines(route_new)
        all_routes.append(route_fn)

    BASE_DIR_SEQS = "sequences"
    logging.info("Creating random sequences...")
    all_sequences = []
    for i in range(number_videos):
        num_objs = random.randint(1, len(objects))
        seq_new = json_generator(
            num_objects=num_objs,
            routes=all_routes,
            patches=objects
        )
        seq_fn = f"{BASE_DIR_SEQS}/seq_{name}_{i}.json"
        with open(seq_fn, 'w') as outfile:
            json.dump(seq_new, outfile, indent=2)
        all_sequences.append(seq_fn)

    logging.info("Building videos...")
    for seq in all_sequences:
        # simulate( ... )
        pass

    logging.info("Ended dataset creation")
