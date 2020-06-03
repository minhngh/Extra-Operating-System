from utils import timer, print_grid
from utils import parse_puzzle
from solvers import *

import os
import json
import argparse
import psutil

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
            grid = solve_1(grid.copy(), num_threads)
            if grid:
                print_grid(grid)
        process = psutil.Process(os.getpid())
        print(f'Memory usage: {process.memory_info().rss / 1024 : .2f} KB = {process.memory_info().rss / 1024 ** 2 : .2f} MB')
        

if __name__ == "__main__":
    main(parse_args())
