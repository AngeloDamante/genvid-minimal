import json
import logging
import random
import os
import argparse


def json_generator(num_objects: int, routes: list = None, patches: list = None) -> list:
    """Generator sequences for json file.

    Args:
        patches:
        routes:
        num_objects(int)

    Returns: list of dictionary for json file
    """
    DIR_ROUTES = "routes"
    DIR_PATCHES = "patches"

    if routes is None:
        routes = os.listdir(DIR_ROUTES)
    if patches is None:
        patches = os.listdir(DIR_PATCHES)

    seq = []
    for i in range(num_objects):
        my_dict = {
            "patch_label": i,
            "patch_ratio": round(random.uniform(0.1, 1), 2),
            "route": random.choice(routes),
            "patch": random.choice(patches)
        }
        seq.append(my_dict)
    return seq


def configure_logging(log_filename: str, log_console=False, log_lvl=logging.DEBUG):
    """Cofnigure logging

    Args:
        log_filename:
        log_console:
        log_lvl:
    """
    if log_console:
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=log_lvl)
    else:
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                            filename=log_filename, level=log_lvl)


if __name__ == '__main__':
    DIR_SEQUENCES = "sequences"

    configure_logging("log_json_gen.log", True, log_lvl=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", type=str, required=True, help="name of your random sequences")
    parser.add_argument("-o", "--number_objects", type=int, default=1, help="number of objects to be generated")
    args = parser.parse_args()

    data = json_generator(args.number_sequences)
    with open(f"{DIR_SEQUENCES}/{args.name}.json", 'w+') as outfile:
        json.dump(data, outfile)
    exit(0)
