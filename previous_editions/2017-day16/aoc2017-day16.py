from string import ascii_lowercase


def spin(line, pivot):
    pivot = int(pivot)
    line[:pivot], line[pivot:] = line[-pivot:], line[:-pivot]


def exchange(line, indices):
    first, second = map(int, indices.split("/"))
    line[first], line[second] = line[second], line[first]


def partner(line, letters):
    first, second = letters.split("/")
    first, second = line.index(first), line.index(second)
    line[first], line[second] = line[second], line[first]


if __name__ == "__main__":
    with open("day16-input.txt") as f:
        moves = next(f).strip().split(",")

    line = list(ascii_lowercase[:16])

    dance = {"s": spin, "x": exchange, "p": partner}

    for move in moves:
        dance[move[0]](line, move[1:])

    print(f"After one dance:           {''.join(line)}")

    for i in range(1000000000 % 42 - 1):
        for move in moves:
            dance[move[0]](line, move[1:])

    print(f"After a billion dances:    {''.join(line)}")
