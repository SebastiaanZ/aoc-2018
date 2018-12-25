import numpy as np
import networkx as nx
from scipy.spatial import distance


with open("day25-input.txt") as f:
    points = [tuple(int(n) for n in line.strip().split(",")) for line in f]


points_array = np.array(points, dtype="int")
g = nx.Graph()

d = distance.cdist(points_array, points_array, metric="cityblock").astype(int)

for i in range(len(points)):
    dt = d[:, i] <= 3
    origin = points[i]
    for row in points_array[dt]:
        g.add_edge(origin, tuple(row))

print(nx.number_connected_components(g))
