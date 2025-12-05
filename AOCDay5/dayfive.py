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

# Part 1
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

# Part 2 
# The list of id ranges should be sorted first by minimum value (followed by maximum value)
def total_num_fresh_ids(fresh_id_ranges: list):
    num_fresh_ids = 0
    merged_id_ranges = fresh_id_ranges.copy()

    # Sort by minimum id
    merged_id_ranges.sort(key=get_lower_range)

    # Process pairs.
    idx = 0
    while idx < len(merged_id_ranges) - 1:
        if merged_id_ranges[idx][1] >= merged_id_ranges[idx + 1][1]:
            # Second entry completely within first: discard it.
            merged_id_ranges.pop(idx + 1)
        elif merged_id_ranges[idx][1] >= merged_id_ranges[idx + 1][0]:
            # The two entries overlap with the largest id in entry i being largest than the smallest id in entry i + 1.
            merged_id_ranges[idx][1] = merged_id_ranges[idx + 1][1]
            merged_id_ranges.pop(idx + 1)
        else:
            # No merging occurred. Shift over one space.
            idx += 1

    print("Merged ranges by minimum value: %s" % (merged_id_ranges))

    i = 0
    for id_range in merged_id_ranges:
        total_range = id_range[1] - id_range[0] + 1
        num_fresh_ids += total_range
        print("%d: Added %d ids." % (i, total_range))
        i += 1

    return num_fresh_ids

def get_lower_range(range: list):
    return range[0]

# Part 2: Find total number of fresh ids
def part_two():
    file = "Inputs/AOCday5.txt"
    ids, fresh_id_ranges = process_input(file)
    print("Part 2, total number of fresh ids: %d" % (total_num_fresh_ids(fresh_id_ranges)))

part_one()
part_two()