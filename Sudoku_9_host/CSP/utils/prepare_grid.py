from itertools import zip_longest, chain

def cross_product(v1, v2):
    return[w1 + w2 for w1 in v1 for w2 in v2]
def chunk(iterable, n, fillvalue = None):
    args = [iter(iterable)] * 3
    return zip_longest(*args, fillvalue = fillvalue)

digits  = "123456789"
rows    = "ABCDEFGHI"
cols    = digits


#index of board
squares = cross_product(rows, cols)
# all rows, columns and blocks
all_units = ([cross_product(rows, c) for c in cols] + [cross_product(r, cols) for r in rows] + [cross_product(rs, cs) for rs in chunk(rows, 3) for cs in chunk(cols, 3)])

#square and all coressding rows, columns, block 
units = dict((square, [unit for unit in all_units if square in unit]) for square in squares)
#all neighbors
peers = dict((square, set(chain(*units[square])) - set([square])) for square in squares)