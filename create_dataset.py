import argparse
from src.simulator import evolve

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    evolve()
