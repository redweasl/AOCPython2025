# AOC Day 7 2025
# Need to calibrate a teleporter tachyon beam
# Moves down from "S" freely through "." but splits into two from a "^" on the sides
# In part 2, it instead splits timelines every time it hits a splitter

# Process input, returns a grid layout
def process_input(input_name):
    with open(input_name, "r") as file:
        content = file.read()
        return content.split("\n")

########################################################################    

# Given a map, find how many times beam is split
def count_splits(map):
    num_splits = 0
    for y in range(len(map)):
        if y == 0:
            continue
        for x in range(len(map[0])):
            map, split = beam_behavior(map, x, y)
            num_splits = num_splits + 1 if split else num_splits
    return num_splits

# Given the map and coords, determine the behavior at this tile (or neighboring it)
# Check top neighbor, then immediate tile
# May need to modify immediate tile or left/right neighbors
def beam_behavior(map: list, x: int, y: int):
    split = False
    if map[y - 1][x] == "S" or map[y - 1][x] == "|":
        # Splitter behavior
        if map[y][x] == "^":
            split = True
            if x - 1 >= 0:
                map[y] = map[y][:x-1] + "|" + map[y][x:]
            if x + 1 < len(map[0]):
                map[y] = map[y][:x+1] + "|" + map[y][x+2:]
        else:
            map[y] = map[y][:x] + "|" + map[y][x+1:]
    return map, split

# Part 1: Count total number of times beam is split
def part_one():
    file = "Inputs/AOCday7.txt"
    map = process_input(file)
    print("Part one, number of splits: %d" % (count_splits(map)))

part_one()

#################################################################################

# Begin counting. Find the "S" first, then begin tracing
def count_timelines_bf(map):
    if len(map) == 0:
        return 0
    else:
        return trace_timelines(map, map[0].index("S"), 0)

# Recursive function that, starting at the "S", recursively traces all timelines and returns the total number of possible timelines.
# This is the brute force solution, becomes too slow pretty quickly
def trace_timelines(map, x, y):
    if y + 1 == len(map):
        return 1 # Timeline reaches end
    elif x < 0 or x >= len(map[0]):
        return 0 # Timeline terminated by going off map
    elif map[y][x] == "^":
        return trace_timelines(map, x - 1, y + 1) + trace_timelines(map, x + 1, y + 1)
    else:
        return trace_timelines(map, x, y + 1)
    
# An alternate way of counting
def convert_map(map):
    converted_map = [[] for _ in map]
    for y in range(len(map)):
        row = [0 for _ in map[0]]
        for x in range(len(map[0])):
            if map[y][x] == "S":
                row[x] = 1
            elif map[y][x] == "^":
                row[x] = -1
        converted_map[y] = row
    return converted_map

# Given a map, find how many timelines are active from this particle
def count_timelines(map):
    num_timelines = 0
    for y in range(len(map)):
        if y == 0:
            continue
        for x in range(len(map[0])):
            map = particle_behavior(map, x, y)

    # At end, count timelines at bottom row
    for num in map[len(map) - 1]:
        num_timelines += num
    return num_timelines

# Given the map and coords, determine the behavior at this tile (or neighboring it)
# Check top neighbor, then immediate tile
# May need to modify immediate tile or left/right neighbors
def particle_behavior(map: list, x: int, y: int):
    if map[y - 1][x] > 0:
        num_timelines = map[y-1][x]
        # Splitter behavior
        if map[y][x] == -1:
            num_timelines = map[y-1][x]
            if x - 1 >= 0:
                map[y][x-1] += num_timelines

            num_timelines = map[y-1][x]
            if x + 1 < len(map[0]):
                map[y][x+1] += num_timelines
        else:
            map[y][x] += num_timelines
    return map
    
# Part 2: Count total number of active timelines
def part_two():
    file = "Inputs/AOCday7.txt"
    map = process_input(file)
    converted_map = convert_map(map)
    print("Part two, number of timelines: %d" % (count_timelines(converted_map)))

part_two()