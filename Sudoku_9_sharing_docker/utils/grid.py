from .prepare_grid import *

def parse_puzzle(puzzle):
    assert set(puzzle) <= set(".0123456789")
    assert len(puzzle) == 81

    grid = dict((square, digits) for square in squares)

    for square, value in zip(squares, puzzle):
        if value in digits and not place(grid, square, value):
            return False
    return grid

def print_grid(grid):
    print('*' * 55)
    print("*" + ' ' * 22 + ' SOLUTION ' + ' ' * 21 + '*')
    print('*' * 55 + '\n')
    print('-' * 55)
    for row in rows:
        for digit in digits:
            print(f'|  {grid[row + digit]}  ', end = '')
        print('|\n' + '-' * 55)

def min_possible_values(grid):
    return min((len(grid[square]), square) for square in squares if len(grid[square]) > 1)

def max_possible_values(grid):
    return max((len(grid[square]), square) for square in squares if len(grid[square]) > 1)

def valid_grid(grid):
    for col in cols:
        v = []
        for row in rows:
            if len(grid[f'{row}{col}']) == 1:
                v.append(grid[f'{row}{col}'])
        if len(v) != len(set(v)):
            return False
    for row in rows:
        v = []
        for col in cols:
            if len(grid[f'{row}{col}']) == 1:
                v.append(grid[f'{row}{col}'])
        if len(v) != len(set(v)):
            return False
    subgrids = [cross_product(rs, cs) for rs in chunk(rows, 3) for cs in chunk(cols, 3)]
    for subgrid in subgrids:
        v = []
        for square in subgrid:
            if len(grid[square]) == 1:
                v.append(grid[square])
        if len(v) != len(set(v)):
            return False
    return True

def is_solved(grid):
    return all([len(grid[square]) == 1 for square in squares])

def place(grid, square, digit):
    #get rest numbers
    other_values = grid[square].replace(digit, '')
    #remove rest numbers
    if all(eliminate(grid, square, val) for val in other_values):
        return grid
    return False

def eliminate(grid, square, digit):
    if digit not in grid[square]:
        return grid
    #remove digit
    grid[square] = grid[square].replace(digit, '')
    #if square has no number, fail
    if len(grid[square]) == 0:
        return False
    elif len(grid[square]) == 1:
        #square has only number, remove it from peers
        value = grid[square]
        if not all(eliminate(grid, peer, value) for peer in peers[square]):
            return False
    for unit in units[square]:
        places = [sqr for sqr in unit if digit in grid[sqr]]
        if len(places) == 0: #if no places where number is placed, fail
            return False
        elif len(places) == 1: #if only one place for number
            if not place(grid, places[0], digit):
                return False
    return grid