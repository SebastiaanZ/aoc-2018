from aoc_day9 import play_marbles


def do_test_cases_part_one(fn):
    with open(fn) as f:
        test_cases = [[int(n) for n in line.strip().split(",")] for line in f]

        for case in test_cases:
            players, last_marble, winning_score = case
            result = play_marbles(players, last_marble)
            print(result, winning_score)
            assert(result == winning_score)


if __name__ == "__main__":
    do_test_cases_part_one("day9-test.txt")
