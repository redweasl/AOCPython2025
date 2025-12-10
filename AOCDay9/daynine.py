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
# HINT: The input does not include any points in the middle of lines, only corners!!!

# Attempt 1 (4509295292): TOO HIGH
# Attempt 2 (1597246662): TOO HIGH

# Get all rectangles and sort them by area
def sort_rectangles(points):
    rectangles = []
    for i in range(len(points)):
        x1 = points[i].x
        y1 = points[i].y
        j = i + 1
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

        # Vector from lpoint to point
        v1 = np.array([point.x-lpoint.x, point.y-lpoint.y, 0])
        # Vector from point to rpoint
        v2 = np.array([rpoint.x-point.x, rpoint.y-point.y, 0])

        cp = np.cross(v1, v2)
        point.cp = cp[2]

        if (v1[1] < 0 and v2[0] > 0) or (v1[0] < 0 and v2[1] > 0):
            # top left corner
            point.inside_direction = "SE" if point.cp > 0 else "NW"
        elif (v1[0] > 0 and v2[1] > 0) or (v1[1] < 0 and v2[0] < 0):
            # top right corner
            point.inside_direction = "SW" if point.cp > 0 else "NE"
        elif (v1[1] > 0 and v2[0] < 0) or (v1[0] > 0 and v2[1] < 0):
            # bottom right corner
            point.inside_direction = "NW" if point.cp > 0 else "SE"
        elif (v1[0] < 0 and v2[1] < 0) or (v1[1] > 0 and v2[0] > 0):
            # bottom left corner
            point.inside_direction = "NE" if point.cp > 0 else "SW"

# Checks if the outlined rectangle, broadly speaking, is sitting inside of the polygon.
def corners_inside_polygon(p1: Point, p2: Point):
    # This logic doesn't need to be applied to single points or lines
    if p1.x == p2.x or p1.y == p2.y:
        return True
    # Four cases
    if p1.x < p2.x and p1.y < p2.y:
        # p1 on top left
        # print("p1 top left")
        return ((p1.inside_direction == "SE" or (p1.cp < 0 and p1.inside_direction == "SW"))
            and (p2.inside_direction == "NW" or (p2.cp < 0 and p2.inside_direction == "NE")))
    elif p1.x < p2.x and p1.y > p2.y:
        # p1 on bottom left
        # print("p1 bottom left")
        return ((p1.inside_direction == "NW" or (p1.cp < 0 and p1.inside_direction == "NE")) 
            and (p2.inside_direction == "SE" or (p2.cp < 0 and p2.inside_direction == "SW")))
    elif p1.x > p2.x and p1.y > p2.y:
        # p1 on bottom right
        # print("p1 bottom right")
        return ((p1.inside_direction == "NW" or (p1.cp < 0 and p1.inside_direction == "NE"))
            and (p2.inside_direction == "SE" or (p2.cp < 0 and p2.inside_direction == "SW")))
    else:
        # p1 on top right
        # print("p1 top right")
        return ((p1.inside_direction == "SE" or (p1.cp < 0 and p1.inside_direction == "SW"))
            and (p2.inside_direction == "NW" or (p2.cp < 0 and p2.inside_direction == "NE")))

# This method is NAIVE in that it assumes any line intersection with the rectangle results in a not full rectangle.
# Excludes mean cases of adjacent lines.
# Also assumes the rectangle is big enough that a rectangle can be fitted inside of the original one and strictly cannot have any intersections.
# Returns True if no intersections were found on this rectangle, False otherwise.
def edge_check(points: list[Point], p1: Point, p2: Point):
    # Create four lines corresponding to the edges of the rectangle.
    # Check all lines of the polygon for full intersections (line completely crosses rectangle).
    # If any are found, this isn't a full rectangle.
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    if p1.x < p2.x:
        min_x = p1.x
        max_x = p2.x
    else:
        min_x = p2.x
        max_x = p1.x
    if p1.y < p2.y:
        min_y = p1.y
        max_y = p2.y
    else:
        min_y = p2.y
        max_y = p1.y

    s1 = Point(min_x + 1, min_y + 1)
    s2 = Point(min_x + 1, max_y - 1)
    s3 = Point(max_x - 1, max_y - 1)
    s4 = Point(max_x - 1, min_y + 1)

    # print(f"For rectangle with points {p1} and {p2}, created points at {s1}, {s2}, {s3}, and {s4} for intersection check")

    # Iterate through all points, checking every line for intersection
    for i in range(len(points)):
        point = points[i]
        rpoint = points[(i+1)%len(points)]
        # Check for intersections
        intersect_1 = lines_intersect(s1, s2, point, rpoint)
        intersect_2 = lines_intersect(s2, s3, point, rpoint)
        intersect_3 = lines_intersect(s3, s4, point, rpoint)
        intersect_4 = lines_intersect(s4, s1, point, rpoint)
        if intersect_1 or intersect_2 or intersect_3 or intersect_4:
            return False
    return True

# Check if line going from p1 to p2 intersects line going from p3 to p4
def lines_intersect(p1: Point, p2: Point, p3: Point, p4: Point):
    # No parallel or identical lines
    if (p1.x == p2.x and p3.x == p4.x) or (p1.y == p2.y and p3.y == p4.y):
        return False
    
    # Some annoying checks here because I need to know what points correspond to the left, top, right, and bottom points
    lp = None
    rp = None
    tp = None
    bp = None
    if p1.x == p2.x:
        if p1.y < p2.y:
            tp = p1
            bp = p2
        else:
            tp = p2
            bp = p1
        if p3.x < p4.x:
            lp = p3
            rp = p4
        else:
            lp = p4
            rp = p3
    else:
        if p1.x < p2.x:
            lp = p1
            rp = p2
        else:
            lp = p2
            rp = p1
        if p3.y < p4.y:
            tp = p3
            bp = p4
        else:
            tp = p4
            bp = p3

    # Since we know these are horizontal and vertical lines, makes the intersection checks here easier
    # Edge case to add: The second line stops on top of the first line. In this case, the intersection is counted if the second line comes from the inside edge.
    return tp.x >= lp.x and tp.x <= rp.x and tp.y >= lp.y and bp.y <= lp.y

# Under the NAIVE assumption of no adjacent lines, inside hollow polygons aren't possible without intersecting lines at the edges.
# Therefore, any point inside of a rectangle means that the rectangle isn't completely whole.
def has_no_inside_points(points: list[Point], p1: Point, p2: Point):
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    if p1.x < p2.x:
        min_x = p1.x
        max_x = p2.x
    else:
        min_x = p2.x
        max_x = p1.x
    if p1.y < p2.y:
        min_y = p1.y
        max_y = p2.y
    else:
        min_y = p2.y
        max_y = p1.y
    
    for point in points:
        if point.x > min_x and point.x < max_x and point.y > min_y and point.y < max_y:
            return False
    return True

# Given two points and the set of points, determine if this rectangle is valid.
def is_a_rectangle(points, p1, p2):
    # NAIVE: Rectangles with width or height or two are valid rectangles
    width = math.fabs(p1.x - p2.x)
    height = math.fabs(p1.y - p2.y)
    if width < 2 or height < 2:
        # print("This is a line, tough luck")
        return True
    # Case 3: Rectangle
    # print("This is a rectangle")
    is_in_polygon = corners_inside_polygon(p1, p2)
    avoids_intersections = edge_check(points, p1, p2)
    no_inside_points = has_no_inside_points(points, p1, p2)
    print(f"Is this rectangle with points ({p1}, {p2}) within the polygon? {is_in_polygon}")
    # print(f"Does this rectangle avoid intersections? {avoids_intersections}")
    # print(f"Does this rectangle have no inside points? {no_inside_points}")
    if is_in_polygon and avoids_intersections and no_inside_points:
        return True
    else:
        return False

# Given a list of rectangles and points, find the largest valid rectangle.
# This list should be sorted starting with the largest area
def find_largest_valid_rectangle(points, rectangles):
    rect_counter = 0
    for rectangle in rectangles:
        rect_counter += 1
        # print(f"Looking at rectangle from point {rectangle[0]} to point {rectangle[1]} with area of {rectangle[2]}")
        if is_a_rectangle(points, rectangle[0], rectangle[1]):
            print(f"Rectangle {rect_counter} was selected.")
            return rectangle[2]
    return 0

def part_two():
    file = "AOCday9/AOCday9example.txt"
    file = "Inputs/AOCday9.txt"
    points = process_input(file)
    
    filtered_points = filter(within_x_range, points)

    print("Check all points overlapping impostor rectangle along x axis")
    for point in list(filtered_points):
        print(point)

    # print("Obtained points")
    # get_inside_directions(points)
    # print("Obtained cross products and inside directions.")
    # rectangles = sort_rectangles(points)
    # print("Sorted the rectangles by area.")
    # area = find_largest_valid_rectangle(points, rectangles)
    # print("Part 2: Largest valid rectangle area is", area)

def within_x_range(point, min_x=17217, max_x=82570):
    return point.x > min_x and point.x < max_x

before = time.perf_counter_ns()
part_two()
elapsed = time.perf_counter_ns() - before
print(f"Part 2 took {elapsed//1_000_000} ms")