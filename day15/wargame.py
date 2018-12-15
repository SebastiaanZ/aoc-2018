from bisect import insort_left
from operator import attrgetter


class Board:
    def __init__(self, fn, damage=3):
        with open(fn) as f:
            self.board = [list(line.strip()) for line in f]

        self.units: list = []

        self.cols = len(self.board[0])

        self.race_counts = {"G": 0, "E": 0}

        for y, row in enumerate(self.board[1:-1], start=1):
            for x, cell in enumerate(row[1:-1], start=1):
                if cell in ["G", "E"]:
                    self.race_counts[cell] += 1
                    unit = Unit(cell, (x, y), self, damage)
                    self.units.append(unit)
                    self.board[y][x] = unit

        self.starting_elfs = self.race_counts["E"]

    def __str__(self):
        return "\n".join("".join(str(sq) for sq in row) for row in self.board)

    def __getitem__(self, i):
        x, y = i
        return self.board[y][x]

    def __setitem__(self, i, item):
        x, y = i
        self.board[y][x] = item

    def game_turn(self):
        next_turn = []
        for i, unit in enumerate(self.units, start=1):
            if 0 in self.race_counts.values():
                return False
            if unit.dead:
                continue
            unit = unit.turn()
            insort_left(next_turn, unit)
        self.units = next_turn
        return True

    def play_game(self, preserve_elves=False):
        turn = 0
        while True:
            turn += 1
            result = self.game_turn()
            if preserve_elves and self.starting_elfs > self.race_counts["E"]:
                return False
            if not result:
                turn -= 1
                hp_sum = sum(unit.hp for unit in self.units if unit.hp > 0)
                return turn * hp_sum


class Unit:
    steps = [(0, -1), (-1, 0), (1, 0), (0, 1)]

    def __init__(self, race, position, board, damage):
        self.race = race
        self.enemy = "E" if race == "G" else "G"
        self.position = position
        self.hp = 200
        self.board = board
        self.damage = 3 if race == "E" else damage

    @property
    def dead(self):
        return self.hp < 1

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    def adjacent_squares(self, location=None):
        location = self.position if location is None else location
        x, y = location
        return [(x+dx, y+dy) for dx, dy in self.steps]

    def is_enemy(self, location):
        return (isinstance(self.board[location], Unit) and self.board[location].race == self.enemy)

    def adjacent_enemy(self, location=None):
        """Determines if location adjacent to enemy"""
        location = self.position if location is None else location

        for square in self.adjacent_squares(location):
            if self.is_enemy(square):
                return self.board[square]
        return None

    def attack(self):
        enemies = (self.board[s] for s in self.adjacent_squares() if self.is_enemy(s))
        enemy = min(enemies, key=attrgetter("hp"))
        enemy.take_damage()
        return self

    def move(self):
        seen = {self.position}
        viable_moves = [Move(s) for s in self.adjacent_squares() if self.board[s] == "."]
        if not viable_moves:
            return self

        while any(not move.exhausted for move in viable_moves):
            for move in viable_moves:
                if move.exhausted:
                    continue
                for square in move.open_squares:
                    enemy = self.adjacent_enemy(square)
                    if enemy:
                        self.board[self.position] = "."
                        self.position = move.destination
                        self.board[self.position] = self
                        if square == move.destination:
                            self.attack()
                        return self
                    for s in self.adjacent_squares(square):
                        if s in seen:
                            continue
                        seen.add(s)
                        if self.board[s] == ".":
                            move.next_step.append(s)
                move.open_squares = move.next_step
                move.next_step = []
                if not move.open_squares:
                    move.exhausted = True
        return self

    def turn(self):
        """Starts the turn for this unit"""
        adjacent_enemy = self.adjacent_enemy()
        if adjacent_enemy:
            return self.attack()
        else:
            return self.move()

    def take_damage(self):
        self.hp -= self.damage
        if self.hp < 1:
            self.board[self.position] = "."
            self.board.race_counts[self.race] -= 1

    def __str__(self):
        return self.race

    def __repr__(self):
        return "{!s}(race={!r}, position={!r}, hp={!r:>3})".format(
                    self.__class__.__name__,
                    self.race,
                    self.position,
                    self.hp
                    )

    def __lt__(self, other):
        return self.board.cols * self.y + self.x < other.board.cols * other.y + other.x


class Move:
    def __init__(self, destination):
        self.exhausted = False
        self.steps = 1
        self.destination = destination
        self.open_squares = [destination]
        self.next_step = []

    def __repr__(self):
        return "%s(destination=%r)" % (self.__class__.__name__, self.destination)


if __name__ == "__main__":
    print("Part one")
    board = Board("testcases-1.txt")
    print(f"Answer = {board.play_game(preserve_elves=False)}")

    print("Part two")
    damage = 4
    while True:
        board = Board("day15-input.txt", damage)
        result = board.play_game(preserve_elves=True)
        if result:
            break
        damage += 1
    print(f"Answer = {result}")
