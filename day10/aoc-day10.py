'''Approach for this puzzle is a bit different from the rest and, at the
moment, the code does not reflect all the steps I took to solve it.

My approach was:
- Create two numpy arrays: coordinates and velocities
- Get an idea of the range with with min, max
- Use a binary search to find "close" cityblock configurations
- Plot these close configs one-by-one and watch the answer show up
'''
import numpy as np
# from scipy.spatial import distance
import matplotlib.pyplot as plt

coordinates = np.zeros((2, 322))

with open("day10-input.txt") as f:
    lines = list(f)
    coor = np.zeros((len(lines), 2), dtype=int)
    velo = np.zeros((len(lines), 2), dtype=int)
    for row, line in enumerate(lines):
        coor[row, :] = tuple(int(n) for n in line[10:24].split(", "))
        velo[row, :] = tuple(int(n) for n in line[-8:-2].split(", "))


print(coor.min(axis=0), coor.max(axis=0), sep="\t\t")
print(velo.min(axis=0), velo.max(axis=0), sep="\t\t")


coor2 = coor + 10630 * velo

# cityblocks = np.zeros(100, dtype=int)
# minx = miny = 1000
# maxx = maxy = 0
for i in range(1, 15):
    coor2 = coor2 + velo
    # mix, miy = coor2.min(axis=0)
    # mx, my = coor2.max(axis=0)
    # minx, miny = min(minx, mix), min(miny, miy)
    # maxx, maxy = max(maxx, mx), max(maxy, my)
    print(f"Nu: {10630+i}")
    plt.plot(coor2[:, 0], -1*coor2[:, 1], 'ro')
    plt.show()
    input(f"{10630+i}")
