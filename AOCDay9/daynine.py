# AOC Day 9 2025
# Elves want to find largest rectangle that uses red tiles for two opposite corners
# List of red tile locations (input)
# You can choose two red tiles as opposite corners of the rectangle

import math, time, cProfile

# Point class that stores coordinates, orientation, and inside direction
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.is_ccw = None
        self.inside_direction = "NA"
    
    def get_area(self, other):
        return (abs(self.x-other.x)+1)*(abs(self.y-other.y)+1)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", is CCW? " + str(self.is_ccw) + ", Direction " + self.inside_direction + ")"

# Process input, returns a list of coordinates
def process_input(input_name):
    points = []
    with open(input_name, "r") as file:
        for line in file:
            point = line.strip().split(",")
            points.insert(len(points), Point(int(point[0]), int(point[1])))
    return points

# Get all rectangles and sort them by area
def sort_rectangles(points: list[Point]):
    rectangles = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            area = points[i].get_area(points[j])
            rectangles.insert(len(rectangles), [points[i], points[j], area])
    rectangles.sort(key=get_area)
    rectangles.reverse()
    return rectangles

def get_area(rectangle):
    return rectangle[2]

# Returns whether the orientation of a vector pair from the three points is clockwise or counterclockwise
# True = ccw, False = cw
def ccw(p1, p2, p3):
    return (p3.y-p1.y)*(p2.x-p1.x) > (p2.y-p1.y)*(p3.x-p1.x)

# Get orientations at each point, using that to determine the direction of the inside face of the polygon.
def get_inside_directions(points: list[Point]):
    for i in range (len(points)):
        point = points[i]
        lpoint = points[(i-1)%len(points)]
        rpoint = points[(i+1)%len(points)]

        # 2D Vector from lpoint to point
        v1 = [point.x-lpoint.x, point.y-lpoint.y]
        # 2D Vector from point to rpoint
        v2 = [rpoint.x-point.x, rpoint.y-point.y]

        # Calculate the orientation at this point.
        # Counter-clockwise = inside edge is filled
        # Clockwise = outside edge is filled
        point.is_ccw = ccw(lpoint, point, rpoint)

        if (v1[1] < 0 and v2[0] > 0) or (v1[0] < 0 and v2[1] > 0):
            # top left corner
            point.inside_direction = "SE" if point.is_ccw else "NW"
        elif (v1[0] > 0 and v2[1] > 0) or (v1[1] < 0 and v2[0] < 0):
            # top right corner
            point.inside_direction = "SW" if point.is_ccw else "NE"
        elif (v1[1] > 0 and v2[0] < 0) or (v1[0] > 0 and v2[1] < 0):
            # bottom right corner
            point.inside_direction = "NW" if point.is_ccw else "SE"
        elif (v1[0] < 0 and v2[1] < 0) or (v1[1] > 0 and v2[0] > 0):
            # bottom left corner
            point.inside_direction = "NE" if point.is_ccw else "SW"

# Checks if the outlined rectangle, broadly speaking, is sitting inside of the polygon.
def corners_inside_polygon(p1: Point, p2: Point):
    # This logic doesn't need to be applied to single points or lines
    if p1.x == p2.x or p1.y == p2.y:
        return True
    
    # Depending on the position of the first point, determine whether the inside face directions align with one another for both points.
    if p1.x < p2.x and p1.y < p2.y:
        # p1 on top left
        return ((p1.inside_direction == "SE" or (not p1.is_ccw and p1.inside_direction == "SW"))
            and (p2.inside_direction == "NW" or (not p2.is_ccw and p2.inside_direction == "NE")))
    elif p1.x < p2.x and p1.y > p2.y:
        # p1 on bottom left
        return ((p1.inside_direction == "NE" or (not p1.is_ccw and p1.inside_direction == "NW")) 
            and (p2.inside_direction == "SW" or (not p2.is_ccw and p2.inside_direction == "SE")))
    elif p1.x > p2.x and p1.y > p2.y:
        # p1 on bottom right
        return ((p1.inside_direction == "NW" or (not p1.is_ccw and p1.inside_direction == "NE"))
            and (p2.inside_direction == "SE" or (not p2.is_ccw and p2.inside_direction == "SW")))
    else:
        # p1 on top right
        return ((p1.inside_direction == "SW" or (not p1.is_ccw and p1.inside_direction == "SE"))
            and (p2.inside_direction == "NE" or (not p2.is_ccw and p2.inside_direction == "NW")))

# This method is NAIVE in that it assumes any line intersection with the rectangle results in a not full rectangle.
# Excludes mean cases of adjacent lines and assumes the rectangle is big enough that a rectangle can be fitted inside of the original one.
# Returns True if no intersections were found on this rectangle, False otherwise.
# This also will ensure no points are inside the rectangle.
def rectangle_intersects(points: list[Point], p1: Point, p2: Point):
    min_x, max_x = sorted((p1.x, p2.x))
    min_y, max_y = sorted((p1.y, p2.y))

    # Create a small rectangle within the original one that will be checked for intersections
    small_rect = ((Point(min_x + 1, min_y + 1)), 
                  (Point(min_x + 1, max_y - 1)), 
                  (Point(max_x - 1, max_y - 1)), 
                  (Point(max_x - 1, min_y + 1)))

    # Iterate through all points, checking every line for intersection
    for i in range(len(points)):
        point = points[i]
        rpoint = points[(i+1)%len(points)]
        # Check for intersections
        for j in range (len(small_rect)):
            intersect = lines_intersect(small_rect[j], small_rect[(j+1)%len(small_rect)], point, rpoint)
            if intersect:
                return False
    return True

# Check if line going from p1 to p2 intersects line going from p3 to p4
def lines_intersect(p1: Point, p2: Point, p3: Point, p4: Point):
    # Whether two lines intersect can be determined by the orientation for four vector pairs.
    # The orientations of the vectors sharing (p1, p2) and the vectors sharing (p3, p4) must be different for it to be an intersection.
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

# Given two points and the set of points, determine if this rectangle is valid.
def is_a_valid_rectangle(points, p1, p2):
    # NAIVE: Rectangles with width or height less than two are valid rectangles
    width = abs(p1.x - p2.x)
    height = abs(p1.y - p2.y)
    if width < 2 or height < 2:
        return True
    
    # Case 3: Rectangle
    is_in_polygon = corners_inside_polygon(p1, p2)
    avoids_intersections = rectangle_intersects(points, p1, p2)
    return is_in_polygon and avoids_intersections

# Given a list of rectangles and points, find the largest valid rectangle.
# This list should be sorted starting with the largest area
def find_largest_valid_rectangle(points, rectangles):
    rect_counter = 0
    print(f"There are a total of {len(rectangles)} rectangles to check.")
    for rectangle in rectangles:
        rect_counter += 1
        if is_a_valid_rectangle(points, rectangle[0], rectangle[1]):
            print(f"Rectangle {rect_counter} was selected.")
            return rectangle[2]
    return 0

##########################################################################

# Part 1: Find largest area of any rectangle that can be made
def part_one():
    file = "Inputs/AOCday9.txt"
    points = process_input(file)
    rectangles = sort_rectangles(points)
    largest_area = rectangles[0][2]
    print("P1 (4777816465): Largest rectangle area is", largest_area)

before = time.perf_counter_ns()
part_one()
elapsed = time.perf_counter_ns() - before
print(f"Part 1 took {elapsed//1_000_000} ms")

###########################################################################

# Part 2: Adjacent red tiles connected by green tiles, inside is also green tiles
# Attempt 1 (4509295292): Too high
# Attempt 2 (1597246662): Too high
# Attempt 3 (1325340522): Too low
# Attempt 4 (1339784604 current): Incorrect
def part_two():
    file = "AOCday9/AOCday9example.txt"
    file = "Inputs/AOCday9.txt"
    points = process_input(file)

    get_inside_directions(points)
    rectangles = sort_rectangles(points)
    area = find_largest_valid_rectangle(points, rectangles)
    print("Part 2 (1325340522<x<1597246662): Largest valid rectangle area is", area)

before = time.perf_counter_ns()
part_two()
elapsed = time.perf_counter_ns() - before
print(f"Part 2 took {elapsed//1_000_000} ms")

# cProfile.run("part_two()", sort = "cumtime")