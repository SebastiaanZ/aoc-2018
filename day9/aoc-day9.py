from collections import deque
from timeit import default_timer


def do_test_cases_part_one(fn):
    with open(fn) as f:
        test_cases = [[int(n) for n in line.strip().split(",")] for line in f]

        for case in test_cases:
            players, last_marble, winning_score = case
            result = part_one(players, last_marble)
            print(result, winning_score)
            assert(result == winning_score)


def part_one(players, last_marble):
    circle = deque([0])
    scores = [0]*players

    for i in range(1, last_marble+1):
        if i % 23:
            circle.rotate(-2)
            circle.appendleft(i)
        else:
            circle.rotate(7)
            scores[i % players] += i + circle.popleft()

    return max(scores)


# print(part_one(7, 25))


with open("day9-input.txt") as f:
    start = default_timer()
    players, last_marble = (418, 71339)
    print(part_one(players, last_marble))
    print(part_one(players, last_marble*100))
    print(default_timer() - start)


#do_test_cases_part_one("day9-test.txt")
