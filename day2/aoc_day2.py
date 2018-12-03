import collections
import itertools


def get_checksum(fn: str) -> int:
    """Opens file and counts number of lines that contain:
    - Exactly two of a character
    - Exactly three of a character

    returns 'checksum' by multiplying both counts
    """
    with open(fn) as f:
        two = 0
        three = 0
        for item in f:
            counts = set(collections.Counter(item).values())
            two += 2 in counts
            three += 3 in counts
        return two*three


def get_common_letters(fn: str) -> str:
    """Finds the two items in file that differ in just 1 character location;
    Returns their common letters as a joined string.
    """
    with open(fn) as f:
        for i, j in itertools.combinations(f, 2):
            if sum(c1 != c2 for c1, c2 in zip(i, j)) == 1:
                return "".join(c1 for c1, c2 in zip(i, j) if c1 == c2)


if __name__ == "__main__":
    checksum = get_checksum("day2-input.txt")
    print(f"The checksum is: {checksum}")

    common_letters = get_common_letters("day2-input.txt")
    print(f"The common letters are: {common_letters}")
