from utils import timer, print_grid
from utils import parse_puzzle
from solvers import *

import os
import json
import psutil
from itertools import chain
import argparse
from time import time

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
    process = psutil.Process(os.getpid())
    puzzle = load_puzzles()
    puzzle = list(chain.from_iterable(puzzle))

    total_times = []
    total_memories = []
    for i in range(1000):
        grid = parse_puzzle(puzzle.copy())
        if not grid:
            return
        start_time = time()
        grid = solve_2(grid.copy(), num_threads)
        elapsed_time = time() - start_time
        total_times.append(elapsed_time)
        if grid:
            print('[INFO] A solution is found', i + 1)
            # print_grid(grid)
        else:
            print("[ERROR] Can't find any solution")
        total_memories.append(process.memory_info().rss / 1024 ** 2)
    print(f'["INFO"] Average time: {sum(total_times)/ len(total_times): .4f}')
    print(f'["INFO"] Average usage memory: {sum(total_memories)/ len(total_memories): .4f} MB')

        

if __name__ == "__main__":
    main(parse_args())
