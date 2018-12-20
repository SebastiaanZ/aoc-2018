"""Reworked solution to day 20, heavily inspired by the solution provided
by eivl (https://github.com/eivl/Advent-of-code/blob/2018/day20.py). This
was more a practice in using networkx than it is an independent solution.

While the logic is mostly the same as in my own solution, my own solution
did something awkward with building custom nodes and keeping track of the
junction node objects. It was a mess and really slow, so after glancing
at eivl's code, I tried to replicate it by taking similar steps.

The result ended up as the near plagiarism you see below. His version is
much better and cleaner, though.

"""
import networkx
from collections import deque
from collections import Counter


with open("day20-input.txt") as f:
    directions = f.readline().strip()


compound = networkx.Graph()

move = {
    'N': (0, 1),
    'E': (1, 0),
    'S': (0, -1),
    'W': (-1, 0),
    }

junctions = deque()
junction = (0, 0)
location = (0, 0)

for direction in directions:
    if direction in 'NEWS':
        x, y = location
        dx, dy = move[direction]
        new_location = (x + dx, y + dy)
        compound.add_edge(location, new_location)
        location = new_location
    elif direction == '(':
        # Branch off, save junction and add to junction deque
        junctions.append(junction)
        junction = location
    elif direction == ')':
        # Go back to junction of last branching
        # Wait, this should work for nested branchings
        # Use deque to keep track of branching order
        junction = junctions.pop()
    elif direction == '|':
        # Go back to last branch point/junction
        # Don't pop it! Could have multiple pipes
        location = junction


doors = networkx.shortest_path_length(compound, (0, 0)).values()
print(max(doors))
c = Counter(doors)
print(sum(v for k, v in c.items() if k >= 1000))
