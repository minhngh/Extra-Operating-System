import os
import sys
sys.path.append(os.path.abspath('./'))
sys.path.append(os.path.abspath('../'))

from utils import is_solved, place, valid_grid
from utils import  min_possible_values
from threading import Lock, Condition
from concurrent.futures import ThreadPoolExecutor, as_completed

waiting = 0
cv = Condition()
is_finished = False

def _solve(fringe, explored, lock, num_threads):
    global waiting, is_finished
    while waiting < num_threads and not is_finished:
        while not fringe:
            with lock:
                waiting += 1
            with cv:
                cv.wait()
            with lock:
                waiting -= 1
        # stack
        grid = fringe.pop()
        if grid in explored:
            continue
        if is_solved(grid):
            is_finished = True
            return grid
        with lock:
            explored.append(grid)

        _, square = min_possible_values(grid)
        for digit in grid[square]:
            new_grid = place(grid.copy(), square, digit)
            if new_grid and valid_grid(new_grid):
                with lock:
                    fringe.append(new_grid)
                with cv:
                    cv.notify()
    return False        

def solve_2(grid, num_threads):
    fringe = [grid]
    explored = []
    futures = []
    lock = Lock()
    executors = ThreadPoolExecutor(max_workers = num_threads)

    for _ in range(num_threads):
        futures.append(executors.submit(_solve, fringe, explored, lock, num_threads))
    
    result = False
    for future in as_completed(futures):
        result = result or future.result()
        if result:
            return result
    return False