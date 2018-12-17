from collections import deque
import numpy as np

import aoc_utils


ground, cursor, y_min = aoc_utils.create_array("day17-input.txt")

cursors = deque([cursor])
count = 0
seen = set()
while cursors:
    cursor = cursors.popleft()
    if cursor in seen:

        continue
    seen.add(cursor)

    cursor = aoc_utils.waterfall(cursor, ground)

    if cursor:
        cursor = aoc_utils.spread_water(cursor, ground)
        cursors.extend(cursor)
    count += 1

print(f"Part  I: {np.isin(ground[y_min:,:], ['|', '~']).sum()}")
print(f"Part II: {(ground[y_min:,:] == '~').sum()}")
