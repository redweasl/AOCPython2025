# AOC Day 12 2025
# Presents have standard but very weird shapes and are measured in standard units
# Presents need to be placed in a 2D grid style (no stacking)
# Input has list of present shapes
# Followed by size of region under each tree and a list of number of presents of each shape that need to fit into region

# Part 1: This appears to be a gimmick problem.
# It's very difficult to solve with a program normally

# First gimmick answer I will try: Count trees if they have enough spaces for all present spaces
def process_input(input_name):
    present_sizes = []
    num_regions = 0
    with open(input_name, "r") as file:
        present_size = 0
        for line in file:
            # print(f"Line |{line.strip()}|")
            if "x" in line:
                input = line.strip().split(" ")
                tree_dimensions = input.pop(0).strip(":").split("x")
                space = int(tree_dimensions[0]) * int(tree_dimensions[1])
                # print(f"Area of the tree is {space}")
                for i in range (len(input)):
                    space -= int(input[i]) * present_sizes[i]
                print(f"Remaining area is {space}")
                if space >= 0:
                    num_regions += 1

            elif ":" in line and line[1] == ":":
                present_size = 0
            elif len(line.strip()) == 0:
                present_sizes.append(present_size)
            else:
                present_size += line.count("#")
    print(f"Present sizes: {present_sizes}")
    return num_regions

file = "Inputs/AOCday12.txt"
num_regions = process_input(file)
print(f"The number of regions that can fit all presents is {num_regions}")