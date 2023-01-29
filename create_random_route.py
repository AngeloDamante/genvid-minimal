import logging
import random
import argparse

commands = ["const", "acc", "trap", "pause"]


def generate_number_with_sum(n: int, total: int, min_value: int = 1):
    """Generate random numbers with desired sum.

    Args:
        n: number of elements
        total: sum of elements
        min_value: min value for each element

    Returns:
        values(list) of n elements with total sum
    """
    if n == 0 or total == 0: return [total]
    if n == 1 or total == 1: return [total]

    if total < n * min_value:
        logging.error("desired sum must be greater than numbers")
        return [total]

    values = []
    for _ in range(n - 1):
        values.append(random.randint(min_value, total // n))
    values.append(total - sum(values))
    return values


def routes_generator(num_instructions: int, duration: int, frame_size: tuple) -> list:
    """Generate instruction list.

    Args:
        num_instructions(int):
        duration: [ms]
        frame_size: (w,h)

    Returns:
        list of instructions
    """
    instructions = []

    # make origin
    origin = [random.randint(0, frame_size[1]), random.randint(0, frame_size[0])]
    instructions.append(f'{origin[0]}, {origin[1]} \n')

    # times [ms]
    timeframe = generate_number_with_sum(num_instructions, duration, 100)

    # generate instructions
    cmd = "pause"
    for i in timeframe:
        # generate command
        if cmd == "pause":
            cmd = random.choice(tuple(set(commands) - {"pause"}))
        else:
            cmd = random.choice(commands)

        # generate destination
        dst = ()
        if cmd != "pause":
            dst = (random.randint(0, frame_size[1]), random.randint(0, frame_size[0]))
            instruction = f'{dst[0]}, {dst[1]}, {cmd}, {i} \n'
        else:
            instruction = f'{cmd}, {i} \n'
        instructions.append(instruction)
    return instructions


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, type=str, help="filename of random routes")
    parser.add_argument("-i", "--instructions", required=True, type=int, help="number of instructions")
    parser.add_argument("-d", "--duration", type=int, default=100, help="video duration in [ms]")
    parser.add_argument("-w", "--width", default=640, type=int, help="width of frame")
    parser.add_argument("-h", "--height", default=480, type=int, help="height of frame")

    # parsing
    args = parser.parse_args()
    generated_instructions = routes_generator(args.instructions, args.duration, (args.width, args.height))

    # save file
    DIR_ROUTES = "routes"
    with open(f"{DIR_ROUTES}/{args.name}.txt", 'w+') as outfile:
        outfile.writelines(generated_instructions)
