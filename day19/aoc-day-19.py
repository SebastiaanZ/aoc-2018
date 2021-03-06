'''Part I of day 19, but it's very slow since I used the unoptimized class
of a couple of days ago. I did part II by hand/manually by adding a couple
of prints below and working out by hand what was going on.

The solution to Part I is also a hint, as the answers is the number that's
being analyzed from the first register: Since it's a prime number, the sum
of its divisors is itself + 1!
'''
import register


reg_op = register.RegisterOperations()

initial_state = [0]*6

register = {i: v for i, v in zip(range(6), initial_state)}
with open("day19-input.txt") as f:
    instructions = [line.strip() for line in f]


pointer_field = 5
pointer = 0
register[0] = 1
while 0 <= pointer < len(instructions):
    register[pointer_field] = pointer
    register = reg_op(instructions[pointer], register)
    pointer = register[pointer_field] + 1

print(register)
