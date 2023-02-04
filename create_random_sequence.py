import json
import random
import os
import argparse


def json_generator(num_objects: int,
                   ratios: list = None,
                   routes: list = None,
                   patches: list = None) -> list:
    """Generator sequences for json file.

    Args:
        patches:
        ratios(list):
        routes:
        num_objects(int)

    Returns: list of dictionary for json file
    """
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    DIR_ROUTES = os.path.join(__location__, "routes")
    DIR_PATCHES = os.path.join(__location__, "patches")

    if routes is None or len(routes) == 0:
        routes = os.listdir(DIR_ROUTES)
    if patches is None or len(patches) == 0:
        patches = os.listdir(DIR_PATCHES)
    if ratios is None or len(ratios) == 0:
        ratios = [[0.01, 0.09] for _ in range(len(patches))]
    patches_indexed = [(i, p, ratio[0], ratio[1]) for i, (p, ratio) in enumerate(zip(patches, ratios))]

    seq = []
    routes_choosed = []
    for _ in range(num_objects):
        i, p, min_ratio, max_ratio = random.choice(patches_indexed)
        obj_path = {
            "patch_label": i,
            "patch_ratio": round(random.uniform(min_ratio, max_ratio), 2),
            "route": random.choice(list(set(routes) - set(routes_choosed))),
            "patch": p
        }
        seq.append(obj_path)
        routes_choosed.append(obj_path["route"])
    seq.sort(key=lambda x: x["patch_label"], reverse=False)
    return seq


if __name__ == '__main__':
    DIR_SEQUENCES = "sequences"

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", type=str, required=True, help="name of your random sequences")
    parser.add_argument("-o", "--number_objects", type=int, default=1, help="number of objects to be generated")
    args = parser.parse_args()

    data = json_generator(args.number_sequences)
    with open(f"{DIR_SEQUENCES}/{args.name}.json", 'w+') as outfile:
        json.dump(data, outfile)
    exit(0)
