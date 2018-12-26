import numpy as np


def rolling_sum(a, n=3):
    box = np.cumsum(a, axis=1, dtype=int)
    box[:, n:] = box[:, n:] - box[:, :-n]
    return box[:, n-1:]


def square_sum(a, n=3):
    m = rolling_sum(rolling_sum(a, n).transpose(), n).transpose()
    return m


def next_minute2(land, state):
    state_c = state - land
    state100 = state_c % 100

    empty = land == 1
    trees = land == 10
    lumber = land == 100

    land[np.logical_and(empty, state100 >= 30)] = 10
    land[np.logical_and(trees, state_c >= 300)] = 100

    lumber_friendly = np.logical_and(state_c >= 100, state100 >= 10)
    land[np.logical_and(lumber, lumber_friendly)] = 100
    land[np.logical_and(lumber, np.logical_not(lumber_friendly))] = 1
    return land


def part_one(temp):
    cols = len(temp[0])
    rows = len(temp)

    # Create empty ndarrays
    land = np.zeros((cols+2, rows+2), dtype=int)
    state = np.zeros((cols+2, rows+2), dtype=int)

    # Initial configuration
    land[1:-1, 1:-1] = temp

    for _ in range(10):
        state[1:-1, 1:-1] = square_sum(land)
        land = next_minute2(land, state)

    value = (land == 10).sum() * (land == 100).sum()
    print(f"Answer: {value}")


def part_two(temp, max_iter=10_000):
    cols = len(temp[0])
    rows = len(temp)

    # Create empty ndarrays
    land = np.zeros((cols+2, rows+2), dtype=int)
    state = np.zeros((cols+2, rows+2), dtype=int)

    # Initial configuration
    land[1:-1, 1:-1] = temp

    # Set up the iterations
    iterations = max_iter
    answers = np.zeros(iterations, dtype=int)
    seen = set()

    for i in range(iterations):
        state[1:-1, 1:-1] = square_sum(land)
        land = next_minute2(land, state)
        value = (land == 10).sum() * (land == 100).sum()

        config_hash = hash(land.tostring())
        if config_hash in seen:
            found_at = int(np.argwhere(answers == value))
            length = i - found_at
            break
        else:
            answers[i] = value
            seen.add(config_hash)

    answer_at_index = found_at + (1_000_000_000 - found_at) % length - 1
    print(f"Answer: {answers[answer_at_index]}")


if __name__ == "__main__":
    m = {".": 1, "|": 10, "#": 100}

    with open("day18-input.txt") as f:
        temp = [[m[c] for c in row.strip()] for row in f]

    print("Start part  I:")
    part_one(temp)
    print("\nStart part II:")
    part_two(temp, max_iter=10_000)
