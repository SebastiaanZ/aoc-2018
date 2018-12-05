from string import ascii_lowercase, ascii_uppercase


with open('day5-input.txt') as f:
    chemicals = f.read().strip()


def get_reacting_couples():
    couples = []
    for l in ascii_lowercase:
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


def part_two(c):
    low = ascii_lowercase
    upp = ascii_uppercase
    return min(part_one(c.replace(a, "").replace(b, "")) for a, b in zip(low, upp))


print(part_one(chemicals))
print(part_two(chemicals))
