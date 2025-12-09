# AOC Day 9 2025
# Elves want to find largest rectangle that uses red tiles for two opposite corners
# List of red tile locations (input)
# You can choose two red tiles as opposite corners of the rectangle

import math

# Part 1: Find largest area of any rectangle that can be made
def largest_rectangle_area(coord_pairs):
    largest_area = 0
    for i in range(len(coord_pairs)):
        x1 = coord_pairs[i][0]
        y1 = coord_pairs[i][1]
        j = i + 1
        while j < len(coord_pairs):
            x2 = coord_pairs[j][0]
            y2 = coord_pairs[j][1]
            area = (math.fabs(x2-x1)+1)*(math.fabs(y2-y1)+1)
            if area > largest_area:
                largest_area = area
                # print(f"New largest rectangle: Area of {area} from points ({x1}, {y1}) and ({x2}, {y2})")
            j += 1
    return int(largest_area)

# Process input, returns a list of coordinates
def process_input(input_name):
    coord_pairs = []
    with open(input_name, "r") as file:
        for line in file:
            coords = line.strip().split(",")
            coord_pairs.insert(len(coord_pairs), [int(coords[0]), int(coords[1])])
    return coord_pairs

def part_one():
    file = "Inputs/AOCday9.txt"
    coord_pairs = process_input(file)
    area = largest_rectangle_area(coord_pairs)
    print("P1: Largest rectangle area is", area)

part_one()

# file = "AOCDay9/AOCday9example.txt"
# coord_pairs = process_input(file)
# area = largest_rectangle_area(coord_pairs)
# print("Example: Largest rectangle area is", area)