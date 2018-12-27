from northpole import Lumberyard

collection_area = Lumberyard("day18-input.txt")
collection_area.run_until_cycle()
print(f"Answer  I: {collection_area.answer_one}")
print(f"Answer II: {collection_area.answer_two}")
print(f"Time elapsed: {collection_area.duration:0.5f}s")
