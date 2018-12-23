import numpy as np
import re
from scipy.spatial import distance
from operator import itemgetter


def drones_in_range(coordinate, drones):
    d = distance.cdist(coor, drones[:, :3], metric="cityblock")
    return (d <= drones[:, 3]).sum()


with open("day23-input.txt") as f:
    lines = list(f)

drones = np.empty((len(lines), 4), dtype=int)
for i, line in enumerate(lines):
    drones[i, ] = tuple(int(n) for n in re.findall(r'-?\d\d*', line))


# Code for part I
strongest_drone = drones[drones[:, 3].argmax(axis=0), :][np.newaxis, :]
cityblocks = distance.cdist(strongest_drone[:, 0:3], drones[:, 0:3], metric="cityblock")
print(f"Answer part  I: {(cityblocks <= strongest_drone[:, 3]).sum()}")

# Code for part II
minima = drones.min(axis=0)
maxima = drones.max(axis=0)
ranges = maxima - minima

# Set-up span to be smaller than smallest drone range // 3 for first search
# to hopefully not let the answer disappear between the latice
span = minima[3] // 3
start = minima[:3] + span // 2
steps = ranges[:3] // span

x_min, x_max = start[0], maxima[0]
y_min, y_max = start[1], maxima[1]
z_min, z_max = start[2], maxima[2]

while True:
    results = []
    for i in range(x_min, x_max, span):
        for j in range(y_min, y_max, span):
            for k in range(z_min, z_max, span):
                coor = np.array([[i, j, k]])
                dist_origin = int(distance.cdist(coor, np.array([[0, 0, 0]]), metric="cityblock"))
                results.append((coor, (drones_in_range(coor, drones), -dist_origin)))
    candidate = max(results, key=itemgetter(1))
    if span == 1:
        break

    # Once we've found the candidate box, continue searching it with a binary search
    span = int(np.ceil(span / 2))
    x, y, z = candidate[0][0]
    x_min, x_max = x - span, x + span
    y_min, y_max = y - span, y + span
    z_min, z_max = z - span, z + span


print(f"Answer part II: {-candidate[1][1]}")
