from wargame import Board
from timeit import default_timer


start = default_timer()
print("Part one")
board = Board("day15-input.txt")
print(f"Answer = {board.play_game(preserve_elves=False)}")

print("\nPart two")
damage = 4
while True:
    board = Board("day15-input.txt", damage)
    result = board.play_game(preserve_elves=True)
    if result:
        break
    damage += 1
print(f"Answer = {result}")
print(f"[Time elapsed: {default_timer()-start}")
