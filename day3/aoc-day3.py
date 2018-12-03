import collections


def extract_coordinates(iterable) -> tuple:
    """Takes iterable with claims in the form of:
            '#1 @ 906,735: 28x17\n'
       Extracts ID number, coordinates, size
       Returns it as tuple of tuples
    """
    for label in iterable:
        number, _, specs = label.partition(" @ ")
        coor, _, size = specs.partition(": ")
        x, y = coor.split(",")
        width, height = size.strip().split("x")
        yield number[1:], (int(x), int(y)), (int(width), int(height))


def day3_part1(fn: str) -> int:
    """Calculates the number of squares that have overlap from a claim file"""
    with open(fn) as f:
        used = {}
        for _, (x, y), (width, height) in extract_coordinates(f):
            for x1 in range(x, x+width):
                for y1 in range(y, y+height):
                    used[(x1, y1)] = used.setdefault((x1, y1), 0) + 1
        squares = sum(1 for square in used.values() if square >= 2)
        return squares


def day3_part2(fn: str) -> int:
    """Finds the claim that has no overlap with other claims in a claim file"""
    with open(fn) as f:
        claims_on_square = collections.defaultdict(list)
        labels = {}
        for number, (x, y), (width, height) in extract_coordinates(f):
            labels[number] = True
            for x1 in range(x, x+width):
                for y1 in range(y, y+height):
                    claims_on_square[(x1, y1)].append(number)

                    if len(claims_on_square[(x1, y1)]) > 1:
                        for claim in claims_on_square[(x1, y1)]:
                            labels[claim] = False

        for claim, no_overlap in labels.items():
            if no_overlap:
                return claim


if __name__ == "__main__":
    overlap_squares = day3_part1("day3-input.txt")
    claim_without_overlap = day3_part2("day3-input.txt")

    print(f"The number of squares with overlap: {overlap_squares}")
    print(f"Claim with no overlap: {claim_without_overlap}")
