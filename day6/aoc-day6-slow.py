import numpy as np
from scipy.spatial import distance
import itertools

with open("day6-input.txt") as f:
    lines = [tuple(int(c) - 40 - i
             for i, c in enumerate(line.strip().split(", ")))
             for line in f]
    coor = np.array(lines)

counts = {}
edge = set()
close_locations = 0

for i, j in itertools.product(range(314), range(314)):
    dist = distance.cdist(np.array([[i, j]]), coor, "cityblock")
    if np.sum(dist) < 10000:
        close_locations += 1
    if dist[dist == dist.min()].size == 1:
        k = dist.argmin()
        counts[k] = counts.setdefault(k, 0) + 1
        if j in {0, 363} or i in {0, 363}:
            edge.add(k)


largest_area = max(count for key, count in counts.items() if key not in edge)

print(f"The largest area is: {largest_area}")
print(f"The number of safe locations: {close_locations}")
