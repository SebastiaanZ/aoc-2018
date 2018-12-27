import numpy as np
from timeit import default_timer


class NoCycleFound(Exception):
    pass


class Lumberyard:
    """Elves are collecting lumber for the North Pole base construction
    project. This class holds the current state of their lumber collection
    area, calculates the next state of the area and detects when/if the
    collection area gets stuck in a cycle so we can fastforward the changes.

    The individiaul cells have convenient values to represent their state:
       1: Open land
      10: Trees
     100: Lumberyard

    The convience lies in the fact we can now easily get an idea of the state
    of the neighbors by summing the values of the neighbors. For example, the
    following sums indicate:

     008: Cell is surrounded by eight open areas
     332: Cells is surrouned by 3 lumberyards, 3 trees, and 2 open areas.

    So, by using powers of 10, we've created a human-readable sum format,
    namely [LTO], where L represents the number of lumberyards, T the number
    of tree areas, and O the number of open areas surrounding the cell.
    """

    def __init__(self, file_name: str, max_iter: int=10_000) -> None:
        if max_iter < 10:
            raise ValueError("The iteration limit needs to be at least 10")

        self.start_time = default_timer()

        self.max_iter: int = max_iter
        self.iterations_needed: int

        self.land: np.array = Lumberyard.file_to_array(file_name)
        self.neighbors: np.array = np.zeros(self.land.shape, dtype=int)

        self.land_hashes = set()
        self.land_values = [0] * max_iter

    @staticmethod
    def file_to_array(fn: str) -> np.array:
        """Opens the input file and converts it to a numpy array with padding"""
        m = {".": 1, "|": 10, "#": 100}

        with open(fn) as raw_data:
            data = [[m[c] for c in row.strip()] for row in raw_data]

        cols = len(data[0])
        rows = len(data)

        land = np.zeros((cols+2, rows+2), dtype=int)
        land[1:-1, 1:-1] = data
        return land

    def calculate_neighbors(self) -> None:
        """For each cell, compute the sum of the eight neighbors"""
        box = np.cumsum(self.land, axis=1, dtype=int)
        box[:, 3:] = box[:, 3:] - box[:, :-3]
        box = np.cumsum(box, axis=0, dtype=int)
        box[3:, :] = box[3:, :] - box[:-3, :]
        self.neighbors[1:-1, 1:-1] = box[2:, 2:] - self.land[1:-1, 1:-1]

    def advance_minute(self) -> None:
        """Advance the land state to the next minute"""
        self.calculate_neighbors()

        neighbors_100 = self.neighbors % 100

        empty = self.land == 1
        trees = self.land == 10
        lumber = self.land == 100

        self.land[np.logical_and(empty, neighbors_100 >= 30)] = 10
        self.land[np.logical_and(trees, self.neighbors >= 300)] = 100

        lumber_friendly = np.logical_and(self.neighbors >= 100, neighbors_100 >= 10)
        self.land[np.logical_and(lumber, lumber_friendly)] = 100
        self.land[np.logical_and(lumber, np.logical_not(lumber_friendly))] = 1

    def run_until_cycle(self) -> None:
        """Advances the collection area in time until it finds a cycle or it reaches
        the maximum number of iterations. It detects cycles by comparing the hash of
        the current iteration to a hashtable of old land hashes. Assuming we don't
        have to worry about hash collisions, finding a duplicate hash means we have
        started a cycle.
        """
        for current_iter in range(self.max_iter):
            self.advance_minute()
            value = (self.land == 10).sum() * (self.land == 100).sum()

            land_hash = hash(self.land.tostring())
            if land_hash in self.land_hashes:
                self.cycle_start = self.land_values.index(value)
                self.cycle_length = current_iter - self.cycle_start
                break
            else:
                self.land_values[current_iter] = value
                self.land_hashes.add(land_hash)
        else:
            raise NoCycleFound("No cycle found within the specified number of iterations")

        self.iterations_needed = current_iter

        self.answer_one = self.land_values[9]

        self.location_in_cycle = (1_000_000_000 - self.cycle_start) % self.cycle_length
        answer_index = self.cycle_start + self.location_in_cycle - 1
        self.answer_two = self.land_values[answer_index]

        self.end_time = default_timer()
        self.duration = self.end_time - self.start_time


if __name__ == "__main__":
    collection_area = Lumberyard("day18-input.txt")
    collection_area.run_until_cycle()
    assert(collection_area.answer_one == 589931)
    assert(collection_area.answer_two == 222332)

