# AOC Day 7 2025
# Need to calibrate a teleporter tachyon beam
# Moves down from "S" freely through "." but splits into two from a "^" on the sides

# Process input, returns a grid layout
def process_input(input_name):
    with open(input_name, "r") as file:
        content = file.read()
        return content.split("\n")
    
# Given a map, find how many times beam is split
def count_splits(map):
    num_splits = 0
    for y in range(len(map)):
        if y == 0:
            continue
        for x in range(len(map[0])):
            map, split = beam_behavior(map, x, y)
            num_splits = num_splits + 1 if split else num_splits
    # print("FINAL MAP")
    # for line in map:
    #     print(line)
    return num_splits

# Given the map and coords, determine the behavior at this tile (or neighboring it)
# Check top neighbor, then immediate tile
# May need to modify immediate tile or left/right neighbors
def beam_behavior(map: list, x: int, y: int):
    # print("Calculating beam behavior at position %d, %d" % (x, y))
    split = False
    if map[y - 1][x] == "S" or map[y - 1][x] == "|":
        # Splitter behavior
        # print("Beam continues onto tile %s" % (map[y][x]))
        if map[y][x] == "^":
            split = True
            # print("Split happened!")
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