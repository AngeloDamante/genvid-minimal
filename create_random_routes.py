import logging
import random
import os
import argparse

commands = ["const", "acc", "trap", "pause"]


def routes_generator(num_instructions: int, duration: int, frame_size: tuple) -> list:
    return []


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, type=str, help="filename of random routes")
    parser.add_argument("-i", "--instructions", required=True, type=int, help="number of instructions")
    parser.add_argument("-d", "--duration", type=int, default=100, help="video duration in [ms]")
    parser.add_argument("-w", "--width", default=640, type=int, help="width of frame")
    parser.add_argument("-h", "--height", default=480, type=int, help="height of frame")

    # parsing
    args = parser.parse_args()
    instructions = routes_generator(args.instructions, args.duration, (args.width, args.height))

    # save file
    DIR_ROUTES = "routes"
    with open(f"{DIR_ROUTES}/{args.name}.txt", 'w+') as outfile:
        outfile.write(str(instructions))
