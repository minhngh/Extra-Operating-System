import os
import sys
sys.path.append(os.path.abspath('./'))
sys.path.append(os.path.abspath('../'))

from utils import is_solved, place, valid_grid
from utils import  min_possible_values, max_possible_values
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed


def _solve(fringe, explored, lock):
    while fringe:
        # queue
        # grid = fringe.pop(0)

        # stack
        grid = fringe.pop()

        if grid in explored:
            continue
        if is_solved(grid):
            return grid
        _, square = min_possible_values(grid)
        with lock:
            explored.append(grid)
        for digit in grid[square]:
            new_grid = place(grid.copy(), square, digit)
            if new_grid and valid_grid(new_grid):
                fringe.append(new_grid)
    return False

def solve_1(grid, num_threads):
    explored = []
    lock = Lock()
    executors = ThreadPoolExecutor(max_workers = num_threads)
    futures = []
    _, square = max_possible_values(grid)
    for digit in grid[square]:
        new_grid = place(grid.copy(), square, digit)
        if new_grid and valid_grid(grid):
            futures.append(executors.submit(_solve, [new_grid], explored, lock))
    
    result = False
    for future in as_completed(futures):
        result = result or future.result()
        if result:
            return result
    return False


