from collections import deque
from bisect import insort_left
from itertools import count


class Train:
    trainid = count()

    def __init__(self, location, heading, track):
        self.location: tuple = location
        self.track = track
        self._id = next(self.trainid)

        self._direction = deque([(0, 1), (-1, 0), (0, -1), (1, 0)])
        self._direction.rotate(-self._direction.index(heading))
        self._nextturn = 0

    @property
    def direction(self):
        return self._direction[0]

    def intersection(self):
        self._direction.rotate(self._nextturn - 1)
        self._nextturn = (self._nextturn + 1) % 3

    def corner(self, corner_type):
        sign = 1 if corner_type == "\\" else -1
        x, y = self.direction
        self._direction.rotate(-self._direction.index((sign*y, sign*x)))

    def move(self):
        x, y = self.location
        h, v = self.direction
        self.location = (x+h, y+v)
        char = self.track.update_position((x, y), self.location, self)
        if char is None:
            return False
        if char == "+":
            self.intersection()
        elif char in ["\\", "/"]:
            self.corner(char)
        return True

    def __lt__(self, other):
        x1, y1 = self.location
        x2, y2 = other.location
        return (200 * x1 + y1) < (200 * x2 + y2)

    def __repr__(self):
        return f"Train(id=%r, location=%r, direction=%r)" % (self._id,
                                                             self.location,
                                                             self.direction,
                                                             )


class Track:
    def __init__(self, filename):
        self._trains = []

        self._positions = set()
        self._collision = False
        self._collisions = list()
        self._track: list
        self._next_iter: list
        self._build_track(filename)

    def _build_track(self, filename):
        with open(filename) as f:
            self._track = [list(line.rstrip("\n")) for line in f]

        direction = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
        for x, row in enumerate(self._track):
            for y, cell in enumerate(row):
                if cell in direction:
                    train = Train((x, y), direction[cell], self)
                    self._positions.add(train.location)
                    self._trains.append(train)

    def update_position(self, previous: tuple, current: tuple, train: Train):
        if train in self._collisions:
            return None

        self._positions.remove(previous)

        if current in self._positions:
            self._positions.remove(current)

            y, x = current
            print(f"Found collision at {x},{y}")

            self._collision = True
            self._collisions.extend((t for t in self._trains
                                     if t.location == current))
            return None

        self._positions.add(current)
        x, y = current
        return self._track[x][y]

    def tick(self):
        self._next_iter = []
        for train in self._trains:
            if train not in self._collisions:
                if train.move():
                    insort_left(self._next_iter, train)
        self._trains = self._next_iter
        for t in self._collisions:
            try:
                self._trains.remove(t)
            except ValueError:
                pass
        self._collisions = []


    def run_partone(self):
        print("===| Start of part one |===")
        while not self._collision:
            self.tick()
        print("="*27)

    def run_parttwo(self):
        print("===| Start of part Two |===")
        while len(self._trains) > 1:
            self.tick()

        y, x = self._trains[0].location
        print(f"Last train at {x},{y}")
        print("="*27)


if __name__ == "__main__":
    track = Track("day13-input.txt")
    track.run_partone()
    track2 = Track("day13-input.txt")
    track2.run_parttwo()
