import itertools


def get_frequency(fn: str, start: int = 0) -> int:
    """Takes frequency modulation file and returns final frequency"""
    with open(fn) as f:
        return start + sum(int(item) for item in f)


def first_repeat(fn: str, start: int = 0) -> int:
    """Finds the first repeating frequency when cycling the modulation file

    Note: Updating a dict item-by-item seems faster than set; using dummy dict
    """
    seen = {start: 0}
    frequency = start
    with open(fn) as f:
        for modulation in itertools.cycle(f):
            frequency += int(modulation)
            if frequency in seen:
                return frequency

            seen[frequency] = 0


if __name__ == "__main__":
    frequency = get_frequency("day1-input.txt")
    print(f"After one modulation cycle, the frequency is: {frequency}")

    repeating_frequency = first_repeat("day1-input.txt")
    print(f"The first repeating frequency is: {repeating_frequency}")
