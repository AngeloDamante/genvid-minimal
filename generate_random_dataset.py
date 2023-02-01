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
    parser.add_argument("-MinO", "--min-objects", type=int, default=1, help="Min number of objects per video.")
    parser.add_argument("-MaxO", "--max-objects", type=int, default=4, help="Max number of objects per video.")
    parser.add_argument("-IR", "--objects-ratio", type=str, default=None, help='Min,ax patch ratio for object scaling separated by comma (e.g. "0.01,0.09|0.4,0.9"')
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
    min_objects = args.min_objects
    max_objects = args.max_objects
    if min_objects > max_objects:
        logging.error("--min-objects can't be more than --max-objects")
        exit(2)
    ratios = args.objects_ratio
    if ratios is not None:
        try:
            ratios = [[float(r.split(',')[0]), float(r.split(',')[1])] for r in ratios.split('|')]
        except Exception as e:
            logging.error("Unable to parse --objects-ratio like min1,max1|min2,max2|...")
            exit(3)
    duration = args.duration * 1000
    if duration <= 100:
        logging.error("--duration must be more than 100 ms")
        exit(3)
    frame_width = args.width
    frame_height = args.height
    background = args.background
    objects = [os.path.join("patches", pa) for pa in os.listdir("patches")]
    if args.objects != '':
        objects = []
        for pa in args.objects.split(','):
            obj_path = os.path.join("patches", pa)
            if not os.path.exists(obj_path):
                obj_path = pa
                if not os.path.exists(obj_path):
                    logging.error("Unable to find patch " + pa)
                    exit(1)
            objects.append(obj_path)

    if ratios is not None:
        if len(ratios) != len(objects):
            logging.error("objects and ratios were given, but they are not same length")
            exit(5)
    save_video = args.save_video
    fps = args.fps

    logging.info("Starting dataset creation")

    BASE_DIR_ROUTES = "routes"
    logging.info("Creating random routes...")
    all_routes = []
    for i in range(max(number_videos, max_routes)):
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
        num_objs = random.randint(min_objects, max_objects)
        seq_new = json_generator(
            num_objects=num_objs,
            ratios=ratios,
            routes=all_routes,
            patches=objects
        )
        seq_fn = f"{BASE_DIR_SEQS}/seq_{name}_{i}.json"
        with open(seq_fn, 'w') as outfile:
            json.dump(seq_new, outfile, indent=2)
        all_sequences.append(seq_fn)

    logging.info("Building videos...")
    USE_OS = False
    out_dir = f"datasets_out"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    # create dataset_name_0, if exists dataset_name_1, ....
    i = 0
    dataset_dir = os.path.join(out_dir, f"dts_{name}_{i}")
    while os.path.exists(dataset_dir):
        i += 1
        dataset_dir = os.path.join(out_dir, f"dts_{name}_{i}")
    for i, seq in enumerate(all_sequences):
        video_path = None
        if save_video:
            video_path = os.path.join(dataset_dir, f"vid{i}.mp4")
        logging.info("")
        logging.info(f"Creating {dataset_dir}")
        if USE_OS:
            os.system(f"""
                python3 create_video.py \
                    --width={frame_width} \
                    --height={frame_height} \
                    --background={background} \
                    --input-json={seq} \
                    --output-dir={dataset_dir}\
                    --video={video_path} \
                    --fps={fps}
            """)
        else:
            from create_video import simulate, parse_background, parse_json
            np_background = parse_background(background, frame_width, frame_height)
            instructions = parse_json(seq)
            simulate(
                width=frame_width,
                height=frame_height,
                background=np_background,
                instructions=instructions,
                dataset_dir=dataset_dir,
                video_out=video_path,
                fps=fps)

    logging.info("Ended dataset creation")
