from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
def find_empty_location(arr):
    for row in range(9):
        for col in range(9):
            if arr[row][col] == 0:
                return (row, col)
    return None
def used_in_row(arr, row, num):
    return not all([num != arr[row][col] for col in range(9)])
def used_in_col(arr, col, num):
    return not all([num != arr[row][col] for row in range(9)])
def used_in_box(arr, row, col, num):
    for i in range(row, row + 3):
        for j in range(col, col + 3):
            if arr[row][col] == num:
                return True
    return False
def is_location_safe(arr, row, col, num):
    return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) and not used_in_box(arr, row, col, num)
def solve_sudoku(arr):
    location = find_empty_location(arr)
    if location is None:
        return True
    for i in range(1, 10):
        if is_location_safe(arr, *location, i):
            arr[location[0]][location[1]] = i
            if solve_sudoku(arr):
                return True
            arr[location[0]][location[1]] = 0
    return False
def solve(arr):
    return solve_sudoku(arr)

if __name__ == "__main__":
    grid =[[3, 0, 6, 5, 0, 8, 4, 0, 0], 
          [5, 2, 0, 0, 0, 0, 0, 0, 0], 
          [0, 8, 7, 0, 0, 0, 0, 3, 1], 
          [0, 0, 3, 0, 1, 0, 0, 8, 0], 
          [9, 0, 0, 8, 6, 3, 0, 0, 5], 
          [0, 5, 0, 0, 9, 0, 6, 0, 0], 
          [1, 3, 0, 0, 0, 0, 2, 5, 0], 
          [0, 0, 0, 0, 0, 0, 0, 7, 4], 
          [0, 0, 5, 2, 0, 6, 3, 0, 0]] 
    if solve(grid):
        print('Solution found')
    else:
        print('No solution')
