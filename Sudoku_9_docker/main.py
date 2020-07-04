from utils import timer, print_grid
from utils import parse_puzzle
from solvers import *

import os
import json
import argparse
import psutil
from time import time

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--num-threads", type = int, default = 7, help = "# of threads run parallel")
    return vars(ap.parse_args())
def load_puzzles():
    with open("config.json", 'r') as f:
        data = json.loads(f.read())
    return data['puzzles']
def main(args):
    num_threads = args["num_threads"]
    puzzles = load_puzzles()
    total_times = []
    total_memories = []
    process = psutil.Process(os.getpid())

    for puzzle in puzzles:

        for i in range(1000):
            grid = parse_puzzle(puzzle)
            if not grid:
                print("Invalid puzzle")
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
    print(f'["INFO"] Average time: {sum(total_times)/ len(total_times): .6f}')
    print(f'["INFO"] Average usage memory: {sum(total_memories)/ len(total_memories): .4f} MB')
        

if __name__ == "__main__":
    main(parse_args())
