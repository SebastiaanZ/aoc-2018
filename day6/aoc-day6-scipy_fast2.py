import numpy as np
from scipy.spatial import distance
import itertools
from collections import Counter
from operator import itemgetter

with open("day6-input.txt") as f:
    lines = [tuple(int(c) for c in line.strip().split(", ")) for line in f]
    minx = min(lines, key=itemgetter(0))[0]
    miny = min(lines, key=itemgetter(1))[1]
    maxx = max(lines, key=itemgetter(0))[0] - minx
    maxy = max(lines, key=itemgetter(1))[1] - miny
    coor = np.array([(x-minx, y-miny) for x, y in lines])

items = (maxx+1) * (maxy+1)
edge_size = 2*maxx + 2*maxy

grid = np.zeros((items, 2), dtype="int")
edge = np.empty(items, dtype=bool)

for k, (i, j) in enumerate(itertools.product(range(maxx+1), range(maxy+1))):
    grid[k, ] = [i, j]
    if j in {0, maxy} or i in {0, maxx}:
        edge[k] = True
    else:
        edge[k] = False

dist = distance.cdist(grid, coor, "cityblock")
total_counter = Counter(dist.argmin(axis=1)[(dist == dist.min(axis=1).reshape((items, 1))).sum(axis=1)==1])
edge_counter = np.unique(dist[edge].argmin(axis=1)[(dist[edge] == dist[edge].min(axis=1).reshape((edge_size, 1))).sum(axis=1)==1])

largest_area = max(value for area, value in total_counter.items() if area not in edge_counter)
close_locations = np.where(dist.sum(axis=1) < 10_000)[0].size

print(f"The largest area is: {largest_area}")
print(f"The number of safe locations: {close_locations}")
