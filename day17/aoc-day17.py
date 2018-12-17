import numpy as np
import aoc_utils


if __name__ == "__main__":
    ground, cursor, y_min = aoc_utils.create_array("day17-input.txt")

    cursors = set([cursor])
    while cursors:
        cursor = cursors.pop()

        cursor = aoc_utils.waterfall(cursor, ground)

        if cursor:
            cursor = aoc_utils.spread_water(cursor, ground)
            cursors.update(cursor)

    print(f"Part  I: {np.isin(ground[y_min:,:], ['|', '~']).sum()}")
    print(f"Part II: {(ground[y_min:,:] == '~').sum()}")
