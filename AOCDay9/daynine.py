# AOC Day 9 2025
# Elves want to find largest rectangle that uses red tiles for two opposite corners
# List of red tile locations (input)
# You can choose two red tiles as opposite corners of the rectangle

import math, time
import numpy as np

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.cp = 0
        self.inside_direction = "NA"
    
    def get_area(self, other):
        return int((math.fabs(self.x-other.x)+1)*(math.fabs(self.x-other.x)+1))
    
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", CP " + str(self.cp) + ", Direction " + self.inside_direction + ")"

# Process input, returns a list of coordinates
def process_input(input_name):
    points = []
    with open(input_name, "r") as file:
        for line in file:
            point = line.strip().split(",")
            points.insert(len(points), Point(int(point[0]), int(point[1])))
    return points

##########################################################################

# Part 1: Find largest area of any rectangle that can be made
def largest_rectangle_area(points):
    largest_area = 0
    for i in range(len(points)):
        x1 = points[i].x
        y1 = points[i].y
        j = i + 1
        while j < len(points):
            x2 = points[j].x
            y2 = points[j].y
            area = (math.fabs(x2-x1)+1)*(math.fabs(y2-y1)+1)
            if area > largest_area:
                largest_area = area
                # print(f"New largest rectangle: Area of {area} from points ({x1}, {y1}) and ({x2}, {y2})")
            j += 1
    return int(largest_area)

def part_one():
    file = "Inputs/AOCday9.txt"
    points = process_input(file)
    area = largest_rectangle_area(points)
    print("P1: Largest rectangle area is", area)

part_one()

###########################################################################

# Part 2: Adjacent red tiles connected by green tiles, inside is also green tiles
# Rectangles must have red AND green tiles (no black tiles)
# The challenge: How to verify only red and green tiles without a map strat? Map strat is too slow.
# STRATEGY
# Start by getting C.P. of all vectors of the polygon clockwise. 
# This can be used to determine if the inner corner of two vectors is the inside or outside of the polygon.
# Get all rectangle areas from point pairs, sort them by area (with their points too) from largest to smallest.
# For each rectangle:
# Single point: Valid
# Line: Do a line check for validity
# 1. Check if corners indicate the rectangle being inside the polygon
# 2. Scan the edges (line check per edge). If a single line crosses the line perpendicularly, the rectangle is false.
# If there's a line following the line check, when it ends the C.P tells if we're inside or outside. If outside, the rectangle is false.
# 3. Check all inside points of the rectangle. For each point:
# A. If its neighbors form a straight line, it is clear if a line is adjacent to it (edge does not count).
# Multiple lines case: If there are several lines adjacent in a sequence, that sequence must be even in length.
# B. If its neighbors form a right angle, C.P. should indicate the outside side. If that side is filled by another right angle vector, it is clear.
# If all checks are passed, then we have a valid rectangle!

# Get all rectangles and sort them by area
def sort_rectangles(points):
    print(f"Point one is {points[0]}")
    rectangles = []
    for i in range(len(points)):
        x1 = points[i].x
        y1 = points[i].y
        j = i
        while j < len(points):
            x2 = points[j].x
            y2 = points[j].y
            area = (math.fabs(x2-x1)+1)*(math.fabs(y2-y1)+1)
            rectangles.insert(len(rectangles), [points[i], points[j], area])
            j += 1
    rectangles.sort(key=get_area)
    rectangles.reverse()
    return rectangles

def get_area(rectangle):
    return rectangle[2]

# Get cross products of two vectors, one going into the point and one going out.
# Mutates the points to give their cross product.
# Positive cross product values indicate in inside inner corner.
# Negative cross product values indicate an outside inner corner.
# Zero indicates a straight edge.
# Also gets the direction of the inside face of the polygon for each pair of vectors formed at that point.
def get_inside_directions(points: list[Point]):
    for i in range (len(points)):
        point = points[i]
        lpoint = points[(i-1)%len(points)]
        rpoint = points[(i+1)%len(points)]

        print(f"Calculating cross product for point {point}")

        # Vector from lpoint to point
        v1 = np.array([point.x-lpoint.x, point.y-lpoint.y, 0])
        # Vector from point to rpoint
        v2 = np.array([rpoint.x-point.x, rpoint.y-point.y, 0])
        print(f"Incoming vector: {v1}\nOutgoing vector: {v2}")

        cp = np.cross(v1, v2)
        point.cp = cp[2]
        print(f"Their cross product is {point.cp}")

        if (v1[1] < 0 and v2[0] > 0) or (v1[0] < 0 and v2[1] > 0):
            # top left corner
            print("Top left corner")
            point.inside_direction = "SE" if point.cp > 0 else "NW"
        elif (v1[0] > 0 and v2[1] > 0) or (v1[1] < 0 and v2[0] < 0):
            # top right corner
            print("Top right corner")
            point.inside_direction = "SW" if point.cp > 0 else "NE"
        elif (v1[1] > 0 and v2[0] < 0) or (v1[0] > 0 and v2[1] < 0):
            # bottom right corner
            print("Bottom right corner")
            point.inside_direction = "NW" if point.cp > 0 else "SE"
        elif (v1[0] < 0 and v2[1] < 0) or (v1[1] > 0 and v2[0] > 0):
            # bottom left corner
            print("Bottom left corner")
            point.inside_direction = "NE" if point.cp > 0 else "SW"

        # Either horizontal or vertical line
        if point.cp == 0:
            if v1[0] == 0 and v2[0] == 0:
                # vertical line
                if lpoint.inside_direction == "NW" or lpoint.inside_direction == "W" or lpoint.inside_direction == "SW":
                    print("Left side")
                    point.inside_direction = "W"
                else:
                    print("Right side")
                    point.inside_direction = "E"
            else:
                # horizontal line
                if lpoint.inside_direction == "NW" or lpoint.inside_direction == "N" or lpoint.inside_direction == "NE":
                    print("Top side")
                    point.inside_direction = "N"
                else:
                    print("Bottom side")
                    point.inside_direction = "S"
        print(f"The direction of the inside face from this point is {point.inside_direction}")

# Checks if the outlined rectangle, broadly speaking, is sitting inside of the polygon.
def corners_inside_polygon(p1: Point, p2: Point):
    return p1.cp 

# Checks the edge if it's fulled filled in.
def edge_check(p1, p2):
    return

# Given two points and the set of points, determine if this rectangle is valid.
def is_a_rectangle(points, p1, p2):
    return False

# Given a list of rectangles and points, find the largest valid rectangle.
def find_largest_valid_rectangle(points, rectangles):
    return 0

def part_two():
    file = "AOCday9/AOCday9example.txt"
    # file = "Inputs/AOCday9.txt"
    points = process_input(file)
    get_inside_directions(points)
    rectangles = sort_rectangles(points)
    area = find_largest_valid_rectangle(points, rectangles)
    print("Example: Largest valid rectangle area is", area)

before = time.perf_counter_ns()
part_two()
elapsed = time.perf_counter_ns() - before
print(f"Part 2 took {elapsed//1_000_000} ms")