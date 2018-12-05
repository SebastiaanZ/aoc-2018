PERIOD = 328


def part_one(n=2017):
    buf = [0]
    pos = 0
    for i in range(1, n+1):
        pos = (pos + PERIOD) % i + 1
        buf.insert(pos, i)
    return(buf[buf.index(2017)+1])


def part_two(n=50_000_000):
    second_item = None
    pos = 0
    for i in range(1, n+1):
        pos = (pos + PERIOD) % i + 1
        if pos == 1:
            second_item = i
        if not i % 1_000_000:
            print(f"Done: {i:>8}")
    return second_item


print(part_one())
print(part_two())
