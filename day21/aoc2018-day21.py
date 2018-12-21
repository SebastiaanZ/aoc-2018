import register


reg_op = register.RegisterOperations()
reg_op.load_program("day21-input.txt")

print(f"Answer part  I: {reg_op.run_program_one()}")
print(f"Answer part II: {reg_op.run_program_two()}")
