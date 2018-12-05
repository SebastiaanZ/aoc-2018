"""Advent of Code 2017 - Day 18 - Part I only (for now)!"""


def set_func(args, register, pointer):
    a, b = args.split(" ")
    try:
        b = int(b)
    except ValueError:
        b = register.setdefault(b, 0)

    register[a] = b
    return register, pointer + 1


def add_func(args, register, pointer):
    a, b = args.split(" ")
    a_value = register.setdefault(a, 0)
    try:
        b = int(b)
    except ValueError:
        b = register.setdefault(b, 0)

    register[a] = a_value + b
    return register, pointer + 1


def mul_func(args, register, pointer):
    a, b = args.split(" ")
    a_value = register.setdefault(a, 0)
    try:
        b = int(b)
    except ValueError:
        b = register.setdefault(b, 0)

    register[a] = a_value * b
    return register, pointer + 1


def mod_func(args, register, pointer):
    a, b = args.split(" ")
    a_value = register.setdefault(a, 0)
    try:
        b = int(b)
    except ValueError:
        b = register.setdefault(b, 0)

    register[a] = a_value % b
    return register, pointer + 1


def jgz_func(args, register, pointer):
    a, b = args.split(" ")
    a_value = register.setdefault(a, 0)
    if a_value > 0:
        try:
            b = int(b)
        except ValueError:
            b = register.setdefault(b, 0)
        return register, pointer + b
    return register, pointer + 1


def rcv_func(args, register, pointer):
    a = register.setdefault(args, 0)
    if a != 0:
        print(a)
        return register, None
    return register, pointer + 1


def snd_func(args, register, pointer):
    a = register.setdefault(args, 0)
    register["last sound"] = a
    return register, pointer + 1


def part_one():
    functions = {
                "set": set_func,
                "mul": mul_func,
                "add": add_func,
                "jgz": jgz_func,
                "rcv": rcv_func,
                "mod": mod_func,
                "snd": snd_func,
                }

    with open("day17-input.txt") as f:
        instructions = []
        for line in f:
            f, _, args = line.strip().partition(" ")
            instructions.append((f, args))

    register = {}
    pointer = 0

    while pointer is not None:
        f, args = instructions[pointer]
        register, pointer = functions[f](args, register, pointer)

    print(register["last sound"])


part_one()
