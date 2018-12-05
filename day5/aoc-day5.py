from string import ascii_lowercase as low
from string import ascii_uppercase as upp
from collections import deque


def get_reacting_couples():
    couples = []
    for l in low:
        couples.append(l + l.upper())
        couples.append(l.upper() + l)
    return couples


def part_one(chemicals):
    couples = get_reacting_couples()

    old_length = len(chemicals)
    while True:
        for c in couples:
            chemicals = chemicals.replace(c, "")
        new_length = len(chemicals)
        if old_length == new_length:
            break
        old_length = new_length
    return old_length


def part_one2(chemicals):
    d = deque()
    for chemical in chemicals:
        if not d:
            d.append(chemical)
        elif d[-1] == chemical.swapcase():
            d.pop()
        else:
            d.append(chemical)
    return len(d)


def part_two(c):
    return min(part_one(c.replace(a, "").replace(b, "")) for a, b in zip(low, upp))


def part_two2(c):
    return min(part_one2(c.replace(a, "").replace(b, "")) for a, b in zip(low, upp))


if __name__ == "__main__":
    with open('day5-input.txt') as f:
        chemicals = f.read().strip()

    answer1 = part_one2(chemicals)
    print(f"After the reaction, the length is: {answer1}")

    answer2 = part_two2(chemicals)
    print(f"Post-reaction length after removing offender: {answer2}")
