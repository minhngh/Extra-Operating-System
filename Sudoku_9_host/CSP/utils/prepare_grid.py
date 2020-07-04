from itertools import zip_longest, chain

def cross_product(v1, v2):
    if isinstance(v2, str):
        v2 = (v2, )
    return [w1 + w2 for w1 in v1 for w2 in v2]
def chunk(iterable, n, fillvalue = None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue = fillvalue)

# digits  = "123456789"
# rows    = "ABCDEFGHI"
# cols    = digits

SIZE = 16
BLOCK_SIZE = int(SIZE ** .5)
digits = [str(i) for i in range(1, SIZE + 1)]
rows = [chr(ord('A') + i) for i in range(SIZE)]
cols = digits
#index of board
squares = cross_product(rows, cols)
# all rows, columns and blocks
all_units = ([cross_product(rows, c) for c in cols] + [cross_product(r, cols) for r in rows] + [cross_product(rs, cs) for rs in chunk(rows, BLOCK_SIZE) for cs in chunk(cols, BLOCK_SIZE)])

#square and all coressding rows, columns, block 
units = dict((square, [unit for unit in all_units if square in unit]) for square in squares)
#all neighbors
peers = dict((square, set(chain(*units[square])) - set([square])) for square in squares)
