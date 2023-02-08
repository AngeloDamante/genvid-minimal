import argparse
import numpy as np
import json
import cv2
import os
import logging
from src.LoggingManager import configure_logging
from create_random_route import routes_generator
from create_random_sequence import json_generator
from create_video import simulate, parse_background, parse_json
import random


def log_and_exit(message: str, exit_code: int):
    logging.error(message)
    exit(exit_code)


def parse_ratios(ratios_arg: str) -> list:
    ratios = []
    if ratios_arg is not None:
        try:
            ratios = [[float(r.split(',')[0]), float(r.split(',')[1])] for r in ratios_arg.split('|')]
        except Exception as e:
            log_and_exit("Unable to parse --objects-ratio like min1,max1|min2,max2|...", 4)
    return ratios


def parse_list_filenames(objects_args: str, base_dir: str):
    objects = []
    for fn in objects_args.split(','):
        filename = os.path.join(base_dir, fn)
        if not os.path.exists(filename):
            filename = fn
            if not os.path.exists(filename):
                log_and_exit(f"Unable to find {fn}", 10)
        objects.append(filename)
    return objects


def create_random_routes(min_routes:int, max_routes:int, min_instructions:int, max_instructions:int, duration:int, allowed_commands: list = None):
    commands = ["const", "acc", "trap", "pause"] if allowed_commands is None or len(allowed_commands) == 0 else allowed_commands
    all_routes = []
    routes_num = random.randint(min_routes, max_routes)
    for i in range(routes_num):
        logging.debug(f"Creating random route {i}")
        instr = random.randint(min_instructions, max_instructions)
        route_new = routes_generator(
            num_instructions=instr,
            duration=duration,
            frame_size=(frame_width, frame_height),
            min_pause=int((float(duration)/instr)/1.2),
            commands=commands
        )
        route_fn = f"routes/route_{name}_{i}.txt"
        with open(route_fn, 'w') as outfile:
            outfile.writelines(route_new)
        all_routes.append(route_fn)
    return all_routes


def build_next_dataset_dir(out_dir:str):
    # create dataset_name_0, if exists dataset_name_1, ....
    i = 0
    dataset_dir = os.path.join(out_dir, f"dts_{name}_{i}")
    while os.path.exists(dataset_dir):
        i += 1
        dataset_dir = os.path.join(out_dir, f"dts_{name}_{i}")
    return dataset_dir


def generate_random_sequences(num_sequences: int, min_objects: int, max_objects: int, name:str, ratios, all_routes, objects):
    all_sequences = []
    for i in range(num_sequences):
        num_objs = random.randint(min_objects, max_objects)
        seq_new = json_generator(
            num_objects=num_objs,
            ratios=ratios,
            routes=all_routes,
            patches=objects
        )
        seq_fn = f"sequences/seq_{name}_{i}.json"
        with open(seq_fn, 'w') as outfile:
            json.dump(seq_new, outfile, indent=2)
        all_sequences.append(seq_fn)
    return all_sequences


def generate_videos(dta_dir, sequences, w, h, bgs, fps, also_save_video):
    for i, seq in enumerate(sequences):
        video_path = os.path.join(dta_dir, f"vid{i}.mp4") if also_save_video else None
        logging.info(f"\nCreating new sequence #{i}")
        bg_path = random.choice(bgs)
        bachground_iterator = parse_background(bg_path, w, h)
        instructions = parse_json(seq)
        simulate(
            width=w,
            height=h,
            background=bachground_iterator,
            instructions=instructions,
            dataset_dir=dta_dir,
            video_out=video_path,
            fps=fps)


if __name__ == '__main__':
    configure_logging(log_lvl=logging.DEBUG, log_console=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, type=str, help="filename of random routes")
    parser.add_argument("-NV", "--number-videos", type=int, default=5, help="Number of sequences to create.")
    parser.add_argument("-MinR", "--min-routes", type=int, default=10, help="Min number of routes per video.")
    parser.add_argument("-MaxR", "--max-routes", type=int, default=20, help="Max number of routes per video.")
    parser.add_argument("-MinI", "--min-instructions", type=int, default=7, help="Min number of instructions per route.")
    parser.add_argument("-MaxI", "--max-instructions", type=int, default=10, help="Max number of instructions per route.")
    parser.add_argument("-MinO", "--min-objects", type=int, default=1, help="Min number of objects per video.")
    parser.add_argument("-MaxO", "--max-objects", type=int, default=4, help="Max number of objects per video.")
    parser.add_argument("-IR", "--objects-ratio", type=str, default=None, help='Min,ax patch ratio for object scaling separated by comma (e.g. "0.01,0.09|0.4,0.9"')
    parser.add_argument("-D", "--duration", type=float, default=10, help="Duration of each sequence (seconds).")
    parser.add_argument("-W", "--width", type=int, default=1280, help="Dataset frame height (e.g. 1280)")
    parser.add_argument("-H", "--height", type=int, default=720, help="Dataset frame width (e.g. 720)")
    parser.add_argument("-B", "--backgrounds", type=str, default='', help='A subset of backgrounds in backgrounds dir instead of all backgrounds (e.g. "vid1.mp4,vid2.mp4")')
    parser.add_argument("-I", "--objects", type=str, default='', help='A subset of objets in patch dir instead of all objects (e.g. "circle.png,square.npy")')
    parser.add_argument("-R", "--routes", type=str, default='', help='A subset of routes in routes dir instead of all routes (e.g. "pentagon.txt,boxed.txt")')
    parser.add_argument("-AC", "--allowed-commands", type=str, default='const,acc,trap,pause', help='A list of available commands to random create routes in ["const", "acc", "trap", "pause"]')
    parser.add_argument("-SV", "--save-video", action="store_true",  help="If needed, also saves *.mp4 video file in output")
    parser.add_argument("-OC", "--only-create", action="store_true",  help="Just create the random routes/sequences without creating the dataset")
    parser.add_argument("-F", "--fps", type=int, default=30, help="Output sequence fps (e.g. 30)")
    parser.add_argument("-SD", "--seed", type=int, default=-1, help="Use a seed for each random")
    args = parser.parse_args()

    logging.info("parsing arguments")
    if args.seed >= 0: random.seed(args.seed)
    name = args.name
    number_videos = args.number_videos
    if number_videos < 1: log_and_exit("--number-videos must be positive", 1)
    min_routes_files = args.min_routes
    max_routes_files = args.max_routes
    if min_routes_files > max_routes_files: log_and_exit("--min-routes can't be more than --max-routes", 2)
    min_instructions_per_route = args.min_instructions
    max_instructions_per_route = args.max_instructions
    if min_instructions_per_route > max_instructions_per_route: log_and_exit("--min-instructions can't be more than --max-instructions", 2)
    min_objects = args.min_objects
    max_objects = args.max_objects
    if min_objects > max_objects: log_and_exit("--min-objects can't be more than --max-objects", 3)
    ratios = parse_ratios(args.objects_ratio)
    allowed_commands = args.allowed_commands.split(',')
    if len(allowed_commands) == 0 or args.allowed_commands.rstrip() == "": log_and_exit("--allowed-commands must contain at least one command", 5)
    duration = args.duration * 1000
    if duration <= 100: log_and_exit("--duration must be more than 100 ms", 5)
    frame_width = args.width
    frame_height = args.height
    backgrounds = [os.path.join("backgrounds", pa) for pa in os.listdir("backgrounds")]
    if args.backgrounds != '':
        backgrounds = parse_list_filenames(args.backgrounds, "backgrounds")
    objects = [os.path.join("patches", pa) for pa in os.listdir("patches")]
    if args.objects != '':
        objects = parse_list_filenames(args.objects, "patches")
    if len(ratios) != 0 and len(ratios) != len(objects):
        log_and_exit("objects and ratios were given, but they are not same length", 6)
    save_video = args.save_video
    framerate = args.fps
    only_create = args.only_create

    all_routes = []
    if args.routes != '':
        all_routes = parse_list_filenames(args.routes, "routes")
    else:
        all_routes = create_random_routes(min_routes_files, max_routes_files, min_instructions_per_route, max_instructions_per_route, duration, allowed_commands)

    logging.info("Creating random sequences...")
    all_sequences = generate_random_sequences(number_videos, min_objects, max_objects, name, ratios, all_routes, objects)

    if only_create:
        logging.info("Random routes/sequences created.")
        exit(0)

    logging.info("Building datasets...")
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    out_dir = os.path.join(__location__, "datasets_out")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    dataset_dir = build_next_dataset_dir(out_dir)
    generate_videos(dataset_dir, all_sequences, frame_width, frame_height, backgrounds, framerate, save_video)

    logging.info("Ended dataset creation")
