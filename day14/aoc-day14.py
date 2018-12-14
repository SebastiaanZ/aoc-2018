import numpy as np
from collections import deque

if __name__ == "__main__":

    # recipes[0] = 3
    # recipes[1] = 7
    # a = 0
    # b = 1
    # length = 2
    # while length < (stop+10):
    #     a_num = recipes[a]
    #     b_num = recipes[b]
    #     to_add = str(a_num+b_num)
    #     length += len(to_add)
    #     recipes[length-len(to_add):length] = [int(n) for n in to_add]
    #     a = (a + a_num + 1) % length
    #     b = (b + b_num + 1) % length
    # print("".join(str(n) for n in recipes[stop:stop+10]))

    block_size = 1_000_000

    recipes = np.zeros(block_size, dtype=int)

    recipes[0] = 3
    recipes[1] = 7
    a = 0
    b = 1
    length = 2
    to_find = "190221"
    last_recipes = deque("37", maxlen=7)
    blocks = 1
    while True:
        a_num = recipes[a]
        b_num = recipes[b]
        to_add = str(a_num+b_num)
        length += len(to_add)
        recipes[length-len(to_add):length] = [int(n) for n in to_add]
        a = (a + a_num + 1) % length
        b = (b + b_num + 1) % length
        last_recipes.extend(to_add)
        if length >= 7:
            to_check = "".join(last_recipes)
            if to_find in to_check:
                print(length - 7 + to_check.find(to_find))
                break
        if length > (blocks * block_size - 10):
            print("Added block to array")
            recipes = np.concatenate((recipes, np.zeros(block_size, dtype=int)))
            blocks += 1
    print("Done")
