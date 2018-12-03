"""Solutions to the graph theory puzzle of day 12 of the Advent of Code 2017
I've implemented a recursive solution, although a derecursed version would
probably have been better. Since derecursing this function is straightforward
I may add such version in the future.
"""


def get_connections(fn: str) -> dict:
    """Open connections file and return dict with connections for each node"""
    pipes = {}
    with open(fn) as f:
        for line in f:
            node, connections = line.strip().split(" <-> ")
            pipes[node] = connections.split(", ")
    return pipes


def connected_nodes(node: str, pipes: dict, seen=None) -> set:
    """Recursive function that takes:
       - starting node; node: str
       - connected pipes; pipes: dict
       - working set; seen: set=None
       Returns set of connected nodes to starting node
    """
    if seen is None:
        seen = set()

    for cnode in pipes[node]:
        if cnode not in seen:
            seen.add(cnode)
            seen = seen | connected_nodes(cnode, pipes, seen)
    return seen


def get_clusters(pipes: dict) -> int:
    """Gets the number of clusters of connected nodes"""
    groups = 0
    nodes_left = set(pipes.keys())

    while len(nodes_left) > 0:
        groups += 1
        nodes_left = nodes_left - connected_nodes(nodes_left.pop(), pipes)
    return groups


pipes = get_connections("day12-input.txt")

zero_connections = len(connected_nodes("0", pipes))
groups = get_clusters(pipes)

print(f"Number of applications connected to zero: {zero_connections}")
print(f"Number of distinct application groups: {groups}")
