'''My approach was:
- Create two numpy arrays: coordinates and velocities
- Get an idea of the range with with min, max
- Minimize the sum of distances between points over time
- Plot the result
'''
import numpy as np
from scipy.spatial import distance
# from scipy.optimize import minimize
import matplotlib.pyplot as plt


def distance_sum(t):
    return distance.pdist(coor + t * velo).sum()


def find_minimum(t):
    stress1 = distance_sum(t)
    dt = 1 if distance_sum(t+1) < stress1 else -1

    while True:
        t += dt
        stress2 = distance_sum(t)
        if stress2 > stress1:
            return t - dt
        stress1 = stress2


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

    # second = np.round(minimize(distance_sum, guess).x)

    second = find_minimum(guess)

    print(f"Found minimal configurations after {second} seconds")

    coor2 = coor + second * velo

    plt.plot(coor2[:, 0], -1*coor2[:, 1], 'ro')
    plt.show()
