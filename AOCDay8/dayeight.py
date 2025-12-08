# AOC Day 8 2025
# Suspended junction boxes to be connected with a string of lights
# When two boxes are connected, electricity can pass between them
# Input is one box per row with xyz coordinates in 3D space
# Trying to make connections as close as possible

import math

# Class used to store data on box's position and the size of its circuit
class Box:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
        self.key = -1

    def set_key(self, key: int):
        self.key = key
    
    def straight_line_distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        # print("Differences are %d, %d, and %d" % (dx, dy, dz))
        product = (dx*dx)+(dy*dy)+(dz*dz)
        # print("Product is %d" % (product))
        return math.sqrt((dx*dx)+(dy*dy)+(dz*dz))
    
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

# Process input, returns a grid layout
def process_input(input_name):
    boxes = []
    with open(input_name, "r") as file:
        for line in file:
            coords = line.strip().split(",")
            boxes.insert(len(boxes), Box(int(coords[0]), int(coords[1]), int(coords[2])))
    return boxes

# Part 1: Boxes connected according to straight-line distance
# Connect X pairs going from closest boxes ascending
# Connect together 1000 pairs, what's the product of the three largest circuits?

# Answer?
# Feels brute-forcey, but we may need to know every pair distance first in the first place.
# Then, sort those pairs by distance
# Apply those pairs, tracking the circuit size at each box
# From there, the biggest circuits can be determined and product found

def assemble_pair_list(boxes):
    box_pairs = []
    for x in range(len(boxes)):
        y = x + 1
        while y < len(boxes):
            box_pairs.insert(len(box_pairs), [boxes[x], boxes[y], boxes[x].straight_line_distance(boxes[y])])
            y += 1
    print("Box pairs assembled. Length: %d" % (len(box_pairs)))
    box_pairs.sort(key=box_pair_key)
    return box_pairs

def box_pair_key(box_pair):
    return box_pair[2]

# Part 1: Connect X circuits, find the product of the three largest circuits in terms of quanity of boxes
def connect_circuits(box_pairs, x, num_circuits=3):
    pair_num = 0
    circuits = {}
    print("Connecting %d circuits together" % (x))

    while pair_num < x:
        # print("Pair number %d" % (pair_num))
        # Connect the circuits and update the box circuit sizes
        box_one: Box = box_pairs[pair_num][0]
        box_two: Box = box_pairs[pair_num][1]
        if box_one.key == -1 and box_two.key == -1:
            # print("Two boxes aren't in pre-existing circuit")
            key = str(pair_num)
            circuits[key] = [box_one, box_two]
            box_one.set_key(key)
            box_two.set_key(key)
        elif box_one.key != -1 and box_two.key == -1:
            # print("Box one is in a circuit")
            c: list = circuits.get(box_one.key)
            c.insert(len(c), box_two)
            box_two.set_key(box_one.key)
        elif box_one.key == -1 and box_two.key != -1:
            # print("Box two is in a circuit")
            c: list = circuits.get(box_two.key)
            c.insert(len(c), box_one)
            box_one.set_key(box_two.key)
        elif box_one.key != box_two.key:
            # print("Both boxes are in two different circuits")
            c1: list = circuits.get(box_one.key)
            c2: list = circuits.pop(box_two.key)
            for box in c2:
                c1.insert(len(c1), box)
                box.set_key(box_one.key)
        pair_num += 1

    print("Number of circuits: %d" % (len(circuits.values())))

    # Find the three biggest circuits and get their product
    circuit_sizes = [len(circuit) for circuit in circuits.values()]
    circuit_sizes.sort()
    circuit_sizes.reverse()

    product = 1
    x = 0
    while x < 3 and x < len(circuit_sizes):
        product *= circuit_sizes[x]
        x += 1

    return product

def part_one():
    file = "Inputs/AOCday8.txt"
    boxes = process_input(file)
    box_pairs = assemble_pair_list(boxes)
    print("P1: Sorted pair list by distance")
    product = connect_circuits(box_pairs, 1000)
    print("P1: Circuit product is", product)


file = "AOCDay8/AOCday8example.txt"
boxes = process_input(file)
box_pairs = assemble_pair_list(boxes)
print("EX: Sorted pair list by distance")
product = connect_circuits(box_pairs, 10)

print("EX: Circuit product is", product)

part_one()