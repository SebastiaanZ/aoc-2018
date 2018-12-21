from collections import namedtuple


Instruction = namedtuple("Instruction", ["operation", "a", "b", "c"])


class RegisterOperations:
    def __init__(self):
        self.functions = {
            'addr': (self.register_mathr, '+'),
            'mulr': (self.register_mathr, '*'),
            'banr': (self.register_mathr, '&'),
            'borr': (self.register_mathr, '|'),
            'setr': (self.register_mathr, '+ 0 *'),
            'addi': (self.register_mathi, '+'),
            'muli': (self.register_mathi, '*'),
            'bani': (self.register_mathi, '&'),
            'bori': (self.register_mathi, '|'),
            'seti': (self.register_mathi, '* 0 + a + 0 *'),
            'gtir': (self.register_testir, '>'),
            'eqir': (self.register_testir, '=='),
            'gtri': (self.register_testri, '>'),
            'eqri': (self.register_testri, '=='),
            'gtrr': (self.register_testrr, '>'),
            'eqrr': (self.register_testrr, '=='),
            }

    def __call__(self, instruction, register):
        f, a, b, c = instruction
        method, op = self.functions[f]
        return method(a, b, c, op, register)

    def register_mathr(self, a, b, c, op, register: dict):
        out = register.copy()
        out[c] = eval(f"out.get(a, 0) {op} out.get(b, 0)")
        return out

    def register_mathi(self, a, b, c, op, register: dict):
        out = register.copy()
        out[c] = eval(f"out.get(a, 0) {op} b")
        return out

    def register_testir(self, a, b, c, op, register: dict):
        out = register.copy()
        out[c] = 1 if eval(f"a {op} out[b]") else 0
        return out

    def register_testri(self, a, b, c, op, register: dict):
        out = register.copy()
        out[c] = 1 if eval(f"out[a] {op} b") else 0
        return out

    def register_testrr(self, a, b, c, op, register: dict):
        out = register.copy()
        out[c] = 1 if eval(f"out[a] {op} out[b]") else 0
        return out

    def load_program(self, fn):
        with open(fn) as f:
            self.pointer_location = int(f.readline().split(" ")[1])
            self.instructions = []
            for line in f:
                i, *regs = line.strip().split(" ")
                self.instructions.append(Instruction(i, *(int(n) for n in regs)))

    def run_program_one(self):
        register = {k: v for k, v in zip(range(6), [0]*6)}
        pointer = 0
        while 0 <= pointer < len(self.instructions):
            if pointer == 18:
                if register[4] < register[2]:
                    m = register[2] // 256
                    register[4] = 256 * m
                    register[1] = m
            elif pointer == 28:
                return register[3]
            register[self.pointer_location] = pointer
            instruction = self.instructions[pointer]
            register = self(instruction, register)
            pointer = register[self.pointer_location] + 1

    def run_program_two(self):
        register = {k: v for k, v in zip(range(6), [0]*6)}
        pointer = 0
        seen = set()
        last_seen = None
        while 0 <= pointer < len(self.instructions):
            if pointer == 18:
                if register[4] < register[2]:
                    m = register[2] // 256
                    register[4] = 256 * m
                    register[1] = m
            elif pointer == 28:
                    if register[3] in seen:
                        return last_seen
                    else:
                        seen.add(register[3])
                        last_seen = register[3]
            register[self.pointer_location] = pointer
            register = self(self.instructions[pointer], register)
            pointer = register[self.pointer_location] + 1
