'''My approach was:
- Create two numpy arrays: coordinates and velocities
- Get an idea of the range with with min, max
- Minimize the sum of distances between points over time
- Plot the result
'''
import numpy as np
from scipy.spatial import distance
from scipy.optimize import minimize
import matplotlib.pyplot as plt


def distance_sum(t):
    return distance.pdist(coor + t * velo).sum()


if __name__ == "__main__":
    with open("day10-input.txt") as f:
        lines = list(f)
        coor = np.zeros((len(lines), 2), dtype=int)
        velo = np.zeros((len(lines), 2), dtype=int)
        for row, line in enumerate(lines):
            coor[row, :] = tuple(int(n) for n in line[10:24].split(", "))
            velo[row, :] = tuple(int(n) for n in line[-8:-2].split(", "))

    min_mean = (coor.min(axis=0) // velo.min(axis=0)).mean()
    max_mean = (coor.max(axis=0) // velo.max(axis=0)).mean()

    guess = (min_mean + max_mean)//2

    second = np.round(minimize(distance_sum, guess).x)

    print(f"Found minimal configurations after {second} seconds")

    coor2 = coor + second * velo

    plt.plot(coor2[:, 0], -1*coor2[:, 1], 'ro')
    plt.show()
