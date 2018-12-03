def number_generator(start: int, factor: int, mod: int, skip: bool) -> int:
    """Generator that yields the last 16 bits of the next number"""
    number = start
    while True:
        number = number * factor % 2147483647
        if skip or not number % mod:
            yield number & 65535


if __name__ == "__main__":
    a1 = number_generator(722, 16807, 1, True)
    b1 = number_generator(354, 48271, 1, True)

    part1 = sum(next(a1) == next(b1) for i in range(4*10**7))
    print(f"In part 1, the judge counts: {part1}")

    a2 = number_generator(722, 16807, 4, skip_mod=False)
    b2 = number_generator(354, 48271, 8, skip_mod=False)

    part2 = sum(next(a2) == next(b2) for i in range(5*10**6))
    print(f"In part 2, the judge counts: {part2}")
