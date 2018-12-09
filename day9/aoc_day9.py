from collections import deque


def play_marbles(players, last_marble):
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


if __name__ == "__main__":
    # do_test_cases_part_one("day9-test.txt")
    with open("day9-input.txt") as f:
        players, last_marble = (418, 71339)
        print(play_marbles(players, last_marble))
        print(play_marbles(players, last_marble*100))
