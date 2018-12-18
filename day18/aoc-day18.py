import numpy as np


def rolling_sum(a, n=3):
    box = np.cumsum(a, axis=1, dtype=int)
    box[:, n:] = box[:, n:] - box[:, :-n]
    return box[:, n-1:]


def square_sum(a, n=3):
    m = rolling_sum(rolling_sum(a, n).transpose(), n).transpose()
    return m


def next_minute(land, state):
    s = state - land
    if land == 0 and (s % 100) >= 30:
        return 10
    elif land == 10 and s >= 300:
        return 100
    elif land == 100:
        if s >= 100 and (s % 100) >= 10:
            return 100
        else:
            return 0
    return land


vnext_minute = np.vectorize(next_minute)

def part_one(temp):
    cols = len(temp[0])
    rows = len(temp)

    # Create empty ndarrays
    land = np.zeros((cols+2, rows+2))
    state = np.zeros((cols+2, rows+2))

    # Initial configuration
    land[1:-1, 1:-1] = temp

    for _ in range(10):
        state[1:-1, 1:-1] = square_sum(land)
        land = vnext_minute(land, state)

    value = (land == 10).sum() * (land == 100).sum()
    print(f"Answer: {value}")


def part_two(temp, max_iter=10_000):
    cols = len(temp[0])
    rows = len(temp)

    # Create empty ndarrays
    land = np.zeros((cols+2, rows+2))
    state = np.zeros((cols+2, rows+2))

    # Initial configuration
    land[1:-1, 1:-1] = temp

    # Set up the iterations
    iterations = max_iter
    answers = [0] * iterations
    seen = set()
    count = 0
    last_period = -1

    # Compute initial value
    pattern = False
    for i in range(iterations):
        state[1:-1, 1:-1] = square_sum(land)
        land = vnext_minute(land, state)
        value = (land == 10).sum() * (land == 100).sum()
        answers[i] = value

        if value in seen:
            if pattern:
                new_period = answers[(i-1)::-1].index(value) + 1
                if new_period == last_period:
                    count += 1
                    if count == last_period:
                        found_at = i-last_period+1
                        length = last_period
                        print(f"* Found repeating pattern at {found_at}")
                        print(f"* Pattern length = {length}")
                        break
                else:
                    count = 1
                    last_period = new_period
            else:
                last_period = answers[(i-1)::-1].index(value) + 1
                count = 1
                pattern = True
        else:
            pattern = False
            seen.add(value)

    answer_at_index = found_at + (1_000_000_000 - found_at) % length - 1
    print(f"Answer: {answers[answer_at_index]}")


if __name__ == "__main__":
    m = {".": 0, "|": 10, "#": 100}

    with open("day18-input.txt") as f:
        temp = [[m[c] for c in row.strip()] for row in f]

    print("Start part  I:")
    part_one(temp)
    print("\nStart part II:")
    part_two(temp, max_iter=10_000)
