from string import ascii_lowercase as low
from string import ascii_uppercase as upp
from collections import deque
from multiprocessing import Pool


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


def part_one2(chemicals, return_data=False):
    d = deque()
    for chemical in chemicals:
        if d and d[-1] == chemical.swapcase():
            d.pop()
        else:
            d.append(chemical)
    if return_data:
        return len(d), "".join(d)
    return len(d)


def part_two(c):
    return min(part_one(c.replace(a, "").replace(b, "")) for a, b in zip(low, upp))


def _part_two_mp(chemicals_letters):
    chemicals, letters = chemicals_letters
    return part_one2(chemicals.replace(letters[0], "").replace(letters[1], ""))


def part_two_mp(chemicals):
    chemicals_letters = [(chemicals, f"{a}{b}") for a, b in zip(low, upp)]

    pool = Pool(processes=7)
    return min(pool.map(_part_two_mp, chemicals_letters))


if __name__ == "__main__":
    with open('day5-input.txt') as f:
        chemicals = f.read().strip()

    answer1, chemicals2 = part_one2(chemicals, True)
    print(f"After the reaction, the length is: {answer1}")

    answer2 = part_two_mp(chemicals2)
    print(f"Post-reaction length after removing offender: {answer2}")
