from collections import Counter
import numpy as np


def part_one(all_moves):
    """Takes all moves, counts steps in each directions,
    Combines directions to calculate x, y, z coordinates,
    Returns the distance in steps to the finish hexagon
    """
    c = Counter(all_moves)

    x = c["ne"] - c["sw"] + c["se"] - c["nw"]
    y = -c["s"] + c["n"] - c["se"] + c["nw"]
    z = c["s"] - c["n"] - c["ne"] + c["sw"]

    return max(abs(x), abs(y), abs(z))


def part_two(all_moves):
    """Uses the same x, y, z coordinate system as part one, but, since
    order is important for the furthest intermediate point, it adds all
    coordinate changes to np.array and uses cumsum to determine maximum
    offset from origin.
    """
    coordinates = {
                "n": [0, 1, -1],
                "ne": [1, 0, -1],
                "se": [1, -1, 0],
                "s": [0, -1, 1],
                "sw": [-1, 0, 1],
                "nw": [-1, 1, 0]
                }

    moves_array = np.zeros((len(all_moves), 3))
    for row, move in enumerate(all_moves):
        moves_array[row, :] = coordinates[move]

    return np.absolute(np.cumsum(moves_array, axis=0)).max()


if __name__ == "__main__":
    with open("day11-input.txt") as f:
        all_moves = f.readline().strip().split(",")

    part1 = part_one(all_moves)
    part2 = part_two(all_moves)

    print(f"Steps from origin: {part1}")
    print(f"Furthest we've ever been: {part2:0.0f}")
