import argparse
from src.simulator import simulate

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-W", "--width", type=int, default=1280, help="Dataset frame height (e.g. 1280)")
    parser.add_argument("-H", "--height", type=int, default=720, help="Dataset frame width (e.g. 720)")
    args = parser.parse_args()

    simulate(None, None, None)
