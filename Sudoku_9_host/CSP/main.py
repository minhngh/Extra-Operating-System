from utils import timer
from utils import parse_puzzle
from solvers import *

import json
import argparse

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--num-threads", type = int, default = 5, help = "# of threads run parallel")
    return vars(ap.parse_args())
def load_puzzles():
    with open("config.json", 'r') as f:
        data = json.loads(f.read())
    return data['puzzles']
def main(args):
    num_threads = args["num_threads"]
    puzzles = load_puzzles()
    for puzzle in puzzles:
        grid = parse_puzzle(puzzle)
        if not grid:
            print("Invalid puzzle")
        with timer():
            solve_1(grid.copy(), num_threads)
        

if __name__ == "__main__":
    main(parse_args())
