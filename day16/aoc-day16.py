from register import RegisterOperations, parse_samples
from collections import Counter


reg_op = RegisterOperations()

counts = []
functions = {i: set(reg_op.functions) for i in range(len(reg_op.functions))}
for sample in parse_samples("day16-samples.txt"):
    count, funcs = reg_op.test_sample(sample)
    counts.append(count)
    i, func_set = funcs
    functions[i] = functions[i] & func_set
print("Part I :", sum(v for k, v in Counter(counts).items() if k >= 3))

out = reg_op.run_program("day16-program.txt", functions)
print(f"Part II: {out[0]}")
