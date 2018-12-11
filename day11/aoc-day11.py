import numpy as np
from itertools import product
from operator import itemgetter


def rolling_sum_row(a, n=3):
    box = np.cumsum(a, axis=1, dtype=int)
    box[:, n:] = box[:, n:] - box[:, :-n]
    return box[:, n-1:]


def rolling_sum_col(a, n=3):
    box = np.cumsum(a, axis=0, dtype=int)
    box[n:, :] = box[n:, :] - box[:-n, :]
    return box[n-1:, :]


serial_number = 3999
grid = np.zeros((300, 300), dtype=int)

for (x, y) in product(range(1, 301), range(1, 301)):
    rack_id = x + 10
    fuel = str((y*rack_id + serial_number) * rack_id)
    fuel = int(fuel[-3]) if len(fuel) >= 3 else 0
    fuel -= 5
    grid[x-1, y-1] = fuel


sums = rolling_sum_col(rolling_sum_row(grid))
x, y = np.unravel_index(sums.argmax(), sums.shape)

print(f"Answer part  I: {x+1},{y+1}")

powers = []
for i in range(1, 301):
    sums = rolling_sum_col(rolling_sum_row(grid, n=i), n=i)
    x, y = np.unravel_index(sums.argmax(), sums.shape)
    powers.append((sums[x, y], (x+1, y+1), i))

maximum = max(powers, key=itemgetter(0))
x, y = maximum[1]
size = maximum[2]

print(f"Answer part II: {x},{y},{size}")
