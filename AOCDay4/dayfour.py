# AOC Day 4 2025
# Optimize work forklifts are doing in moving big rolls of paper
# Rolls of paper "@" are in a large grid
# Rolls with fewer than four adjacent can be accessed

# Process input, returns a grid layout
def process_input(input_name):
    with open(input_name, "r") as file:
        content = file.read()
        return content.split("\n")
    
# Given the grid and coords, check if this paper roll can be accessed
def can_access_roll(rows, x, y):
    num_adjacent = 0
    y_checks = [y-1, y, y+1, y+1, y+1, y, y-1, y-1]
    x_checks = [x-1, x-1, x-1, x, x+1, x+1, x+1, x]
    for i in range (len(y_checks)):
        if y_checks[i] >= 0 and y_checks[i] < len(rows) and x_checks[i] >= 0 and x_checks[i] < len(rows[0]) and rows[y_checks[i]][x_checks[i]] == "@":
            num_adjacent += 1
        if num_adjacent >= 4:
            return 0
    return 1

def num_rolls_accessible(rows):
    num_rolls = 0
    for y in range (len(rows)):
        for x in range (len(rows[0])):
            if rows[y][x] == "@":
                num_rolls += can_access_roll(rows, x, y)
    return num_rolls

# Part 1: Get total number of accessible rolls
def part_one():
    file = "Inputs/AOCday4.txt"
    rolls = process_input(file)
    print("Part 1, number of rolls accessible: %d" % (num_rolls_accessible(rolls)))

# Removes all currently accessible rows. Mutates the input.
# Return the number of rolls removed.
def remove_all_accessible_rolls(rows):
    num_removed = 0
    for y in range (len(rows)):
        for x in range (len(rows[0])):
            if rows[y][x] == "@" and can_access_roll(rows, x, y):
                rows[y] = rows[y][:x] + "." + rows[y][x+1:]
                num_removed += 1
    return num_removed

# Repeat the process until no more can be removed
def num_rolls_removable(rows):
    total_removed = 0
    num_removed = -1
    round = 1
    while (num_removed != 0):
        num_removed = remove_all_accessible_rolls(rows)
        total_removed += num_removed
        round += 1
    return total_removed

# Part 2: First input mutation!
# How many rolls can be removed?
def part_two():
    file = "Inputs/AOCday4.txt"
    rolls = process_input(file)
    print("Part 2, number of rolls removable: %d" % (num_rolls_removable(rolls)))

part_one()
part_two()