# AOC Day 9 2025
# Elves want to find largest rectangle that uses red tiles for two opposite corners
# List of red tile locations (input)
# You can choose two red tiles as opposite corners of the rectangle

# Based on my input, notable observations:
# 1. All points make up vertices
# 2. The largest rectangle that can fit should be larger than 3x3
# 3. All vectors are not directly adjacent to one another
# 4. The polygon is generally being drawn "counterclockwise", so CCW should be inside direction and CW outside direction

import time

# Point class that stores coordinates, orientation, and inside direction
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.is_ccw = 0
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

def sort_rectangles(points):
    rects = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            rects.insert(len(rects), [points[i], points[j], points[i].get_area(points[j])])        
    rects.sort(key=get_area, reverse=True)
    return rects

def get_area(rect):
    return rect[2]

def draw_polygon(points):
    for i in range(len(points)):
        lp = points[(i-1)%len(points)]
        cp = points[i]
        rp = points[(i+1)%len(points)]
        cp.is_ccw = ccw(lp, cp, rp)
        cp.inside_direction = get_inside_direction(lp, cp, rp)

def get_inside_direction(lp: Point, cp: Point, rp: Point):
    v1 = [(cp.x-lp.x), (cp.y-lp.y)]
    v2 = [(rp.x-cp.x), (rp.y-cp.y)]

    if v1[0] < 0:
        # Incoming vertex from left
        if v2[1] > 0:
            return "NE" if cp.is_ccw else "SW" # Bottom left
        else:
            return "SE" if cp.is_ccw else "NW" # Top left
    elif v1[0] > 0:
        # Incoming vertex from right
        if v2[1] > 0:
            return "NW" if cp.is_ccw else "SE" # Bottom right
        else:
            return "SW" if cp.is_ccw else "NE" # Top right
    elif v1[1] > 0:
        # Incoming vertex from below
        if v2[0] > 0:
            return "SE" if cp.is_ccw else "NW" # Top left
        else:
            return "SW" if cp.is_ccw else "NE" # Top right
    else:
        # Incoming vertex from above
        if v2[0] > 0:
            return "NW" if cp.is_ccw else "SE" # Bottom right
        else:
            return "NE" if cp.is_ccw else "SW" # Bottom left

# Using partial cross product to determine the orientation of a vertex (Using Z axis)
def ccw(p1, p2, p3):
    return (p3.y-p1.y)*(p2.x-p1.x) > (p2.y-p1.y)*(p3.x-p1.x)

def find_largest_inside_rect(points, rects):
    for rect in rects:
        area = rect[2]
        if (abs(rect[0].x-rect[1].x)+1) <= 2 or (abs(rect[0].y-rect[1].y)+1) <= 2:
            return area
        elif is_inside_polygon(rect[0], rect[1]) and rect_no_intersects(rect[0], rect[1], points):
            return area
    return -1

def is_inside_polygon(p1: Point, p2: Point):
    lp, rp = None, None
    vv = p2.y - p1.y
    hv = p2.x - p1.x
    area = p1.get_area(p2)
    lp = p1 if hv > 0 else p2
    rp = p2 if hv > 0 else p1

    if area == 1410501884:
        print(f"Investigating this rectangle with area {area}.\nLeft point: {lp}\nRight point: {rp}")

    if vv * hv > 0: # Bottom left & top right corner
        return (((lp.inside_direction == "NE" and lp.is_ccw) or (not lp.is_ccw and lp.inside_direction != "SW")) and
                ((rp.inside_direction == "SW" and rp.is_ccw) or (not rp.is_ccw and rp.inside_direction != "NE")))
    else: # Bottom right & top left corner
        return (((lp.inside_direction == "SE" and lp.is_ccw) or (not lp.is_ccw and lp.inside_direction != "NW")) and
                ((rp.inside_direction == "NW" and rp.is_ccw) or (not rp.is_ccw and rp.inside_direction != "SE")))
    
def rect_no_intersects(p1: Point, p2: Point, points: list[Point]):
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

def lines_intersect(p1: Point, p2: Point, p3: Point, p4: Point):
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

# Part 1: Find largest rectangle
def part_one():
    file = "Inputs/AOCday9.txt"
    points = process_input(file)
    rects = sort_rectangles(points)
    largest_area = rects[0][2]
    print("P1 (4777816465): Largest rectangle area is", largest_area)

before = time.perf_counter_ns()
part_one()
elapsed = time.perf_counter_ns() - before
print(f"Part 1 took {elapsed//1_000_000} ms")

# Part 2: Find largest rectangle in bounding polygon
def part_two():
    file = "Inputs/AOCday9.txt"
    points = process_input(file)
    draw_polygon(points)
    rects = sort_rectangles(points)
    largest_area = find_largest_inside_rect(points, rects)
    print("P2 (1410501884): Largest rectangle area within polygon is", largest_area)

before = time.perf_counter_ns()
part_two()
elapsed = time.perf_counter_ns() - before
print(f"Part 2 took {elapsed//1_000_000} ms")