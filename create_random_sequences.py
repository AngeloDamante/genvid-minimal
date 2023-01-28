import json
import logging
import random
import os
import argparse

DIR_SEQUENCES = "sequences"
DIR_PATCHES = "patches"
DIR_ROUTES = "routes"


def json_generator(num_instrunction: int) -> list:
    """Generator sequences for json file.

    Args:
        num_instrunction(int)

    Returns: list of dictionary for json file
    """
    seq = []
    for i in range(num_instrunction):
        my_dict = {
            "patch_label": i,
            "patch_ratio": round(random.uniform(0.1, 1), 2),
            "route": random.choice(os.listdir(DIR_ROUTES)),
            "patch": random.choice(os.listdir(DIR_PATCHES))
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
    configure_logging("log_json_gen.log", True, log_lvl=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", type=str, help="name of your random sequences")
    parser.add_argument("-ns", "--number_sequences", type=int, help="number of sequences to be generated")
    args = parser.parse_args()

    if args.name is None or args.number_sequences is None:
        logging.error("Invalid Argument")
        exit(1)

    data = json_generator(args.number_sequences)
    with open(f"{DIR_SEQUENCES}/{args.name}.json", 'w+') as outfile:
        json.dump(data, outfile)
    exit(0)
