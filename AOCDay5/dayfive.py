# AOC Day 5 2025
# Need to figure out which ingredients are fresh and which are spoiled
# Input is a database with ingredient IDs
# List of fresh ID ranges and a list of available IDs
# Find how many ingredients are fresh

# Process input, returns a list of ids and a list of fresh id ranges
def process_input(input_name):
    with open(input_name, "r") as file:
        content = file.read()
        input = content.split("\n")
        split_idx = input.index("")
        fresh_id_ranges = input[:split_idx]
        ids = input[split_idx + 1:]
        for i in range (len(fresh_id_ranges)):
            fresh_id_ranges[i] = fresh_id_ranges[i].split("-")
        for i in range (len(ids)):
            ids[i] = int(ids[i])
        for i in range (len(fresh_id_ranges)):
            for j in range (len(fresh_id_ranges[i])):
                fresh_id_ranges[i][j] = int(fresh_id_ranges[i][j])
    return ids, fresh_id_ranges

def num_ingredients_fresh(ids, fresh_id_ranges):
    num_fresh = 0
    for id in ids:
        if is_ingredient_fresh(id, fresh_id_ranges):
            num_fresh += 1
    return num_fresh

def is_ingredient_fresh(id, fresh_id_ranges):
    for i in range (len(fresh_id_ranges)):
        if id >= fresh_id_ranges[i][0] and id <= fresh_id_ranges[i][1]:
            return True
    return False

# Part 1: Find number of ids that are fresh
def part_one():
    file = "Inputs/AOCday5.txt"
    ids, fresh_id_ranges = process_input(file)
    print("Part 1, number of fresh ids: %d" % (num_ingredients_fresh(ids, fresh_id_ranges)))

part_one()

# file = "AOCDay5/AOCday5example.txt"
# ids, fresh_id_ranges = process_input(file)
# print("Available ids: %s\nFresh id ranges: %s" % (ids, fresh_id_ranges))
# print("Example, number of fresh ids: %d" % (num_ingredients_fresh(ids, fresh_id_ranges)))