import numpy as np
import networkx as nx


with open("day22-input.txt") as f:
    depth = int(f.readline().split(" ")[1])
    x, y = (int(n) for n in f.readline().split(" ")[1].split(','))


xdim, ydim = int(x*3), int(y*3)

cave = np.empty((xdim, ydim), dtype=int)

xx, yy = np.meshgrid(np.arange(xdim), np.arange(ydim), indexing="ij")

cave[xx == 0] = (yy[xx == 0] * 48271 + depth) % 20183
cave[yy == 0] = (xx[yy == 0] * 16807 + depth) % 20183

for i in range(1, xdim):
    for j in range(1, ydim):
        cave[i, j] = ((cave[i-1, j] % 20183) * (cave[i, j-1] % 20183) + depth) % 20183

cave[x, y] = depth

cave_type = cave % 3

print(f"Answer part  I: {cave_type[:x+1, :y+1].sum()}")

grid = nx.Graph()

common_states = {
    2: [0, 1],
    3: [1],
    4: [1, 2],
    5: [0],
    6: [2],
    8: [0, 2]
    }

for (r, c), t in np.ndenumerate(cave_type):
    layers = [(r, c, s) for s in common_states[2 * 2**t]]
    grid.add_edge(*layers, weight=7)
    if r < (xdim - 1):
        t2 = cave_type[r+1, c]
        for s in common_states[2**t + 2**t2]:
            grid.add_edge((r, c, s), (r+1, c, s), weight=1)
    if c < (ydim - 1):
        t2 = cave_type[r, c+1]
        for s in common_states[2**t + 2**t2]:
            grid.add_edge((r, c, s), (r, c+1, s), weight=1)


print(f"Answer part II: {nx.shortest_path_length(grid, (0, 0, 0), (x, y, 0), weight='weight')}")
