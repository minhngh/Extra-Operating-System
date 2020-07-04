from time import time
from contextlib import contextmanager

@contextmanager
def timer():
    start_t = time()
    yield
    end_t = time()
    elapsed_time = end_t - start_t
    print(f'Elapsed time: {elapsed_time: .4f}s')
