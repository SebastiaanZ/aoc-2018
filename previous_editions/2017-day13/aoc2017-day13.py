def split_lines(f: str) -> tuple:
    """Simple generator to yield splitted tuples for building the firewall"""
    for line in f:
        layer, depth = line.split(": ")
        yield int(layer), int(depth)


def calculate_penalty(firewall: dict, start: int=0) -> int:
    """Calculate the penalty of starting the firewall with delay start"""
    penalty = sum(layer*depth for layer, depth in firewall.items()
                  if not (layer+start) % (2*depth-2))
    return penalty


def calculate_safe_offset(firewall: dict) -> int:
    """Calculate the delay for making it through without getting caught"""
    i = 0
    while True:
        s = any(True for layer, depth in firewall.items()
                if not (layer+i) % (2*depth-2))
        if not s:
            return i
        i += 1


if __name__ == "__main__":
    with open("day13-input.txt") as f:
        firewall = {layer: depth for layer, depth in split_lines(f)}

    penalty = calculate_penalty(firewall)
    print(f"The penalty is: {penalty}")

    offset = calculate_safe_offset(firewall)
    print(f"The minimal safe offset: {offset}")
