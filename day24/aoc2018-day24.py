from reindeer import Disease


# Part I
disease = Disease("day24-input.txt")
found, result = disease.battle()
print(f"Answer part  I: {result}")

# Part II
for boost in range(10000):
    body = Disease("day24-input.txt", boost)
    found, result = body.battle()
    if found:
        break

print(f"Answer part II: {result} (with boost={boost})")
