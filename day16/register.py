from ast import literal_eval
from itertools import zip_longest


class RegisterOperations:
    def __init__(self):
        self.a = "a"
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

    def __call__(self, operation, register):
        f, _, args = operation.partition(' ')
        a, b, c = tuple(int(n) for n in args.split(' '))
        method, op = self.functions[f]
        return method(a, b, c, op, register)

    def register_mathr(self, a, b, c, op, register: dict):
        out = register.copy()
        out[c] = eval(f"out[a] {op} out[b]")
        return out

    def register_mathi(self, a, b, c, op, register: dict):
        out = register.copy()
        out[c] = eval(f"out[a] {op} b")
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

    def test_sample(self, sample):
        before, instruction, after = sample
        i, a, b, c = (int(n) for n in instruction.split(" "))

        count = 0
        func_set = set()
        for key, (method, op) in self.functions.items():
            try:
                out = method(a, b, c, op, before)
                if all(a == b for a, b in zip(out.values(), after.values())):
                    count += 1
                    func_set.add(key)
            except Exception as e:
                print(e)
        return count, (i, func_set)

    def run_program(self, program_file, functions):
        function_mapping = {}
        for i in range(16):
            k, v = sorted(functions.items(), key=lambda x: len(x[1]))[0]
            v = v.pop()
            function_mapping[k] = v
            del functions[k]
            for s in functions.values():
                s.discard(v)

        self._function = self.functions.copy()
        self.functions = {str(k): self.functions[v] for k, v in function_mapping.items()}

        register = {i: 0 for i in range(4)}
        with open(program_file) as f:
            for instruction in f:
                register = self(instruction.strip(), register)
        return register


def parse_samples(samples_file):
    with open(samples_file) as f:
        for before, op, after, _ in zip_longest(*[iter(f)]*4, fillvalue=''):
            before = literal_eval(before[8:].strip())
            before = dict(zip(range(4), before))
            after = literal_eval(after[8:].strip())
            after = dict(zip(range(4), after))
            yield before, op.strip(), after
