import collections


def extract_coordinates(iterable):
    for label in iterable:
        number, _, specs = label.partition(" @ ")
        coor, _, size = specs.partition(": ")
        x, y = coor.split(",")
        width, height = size.strip().split("x")
        yield number[1:], (int(x), int(y)), (int(width), int(height))


def day3_part1(fn):
    with open(fn) as f:
        used = {}
        for _, (x, y), (width, height) in extract_coordinates(f):
            for x1 in range(x, x+width):
                for y1 in range(y, y+height):
                    used[(x1, y1)] = used.setdefault((x1, y1), 0) + 1
        squares = sum(1 for square in used.values() if square >= 2)
        print(squares)


def day3_part2(fn):
    with open(fn) as f:
        used = collections.defaultdict(list)
        labels = {}
        for number, (x, y), (width, height) in extract_coordinates(f):
            labels[number] = True
            for x1 in range(x, x+width):
                for y1 in range(y, y+height):
                    used[(x1, y1)].append(number)
                    if len(used[(x1, y1)]) > 1:
                        for item in used[(x1, y1)]:
                            labels[item] = False

        for key, value in labels.items():
            if value:
                print(key)


day3_part1("day3-input.txt")
day3_part2("day3-input.txt")
