# AOC Day 2 2025
# Identify invalid product IDs in a gift shop database
# Comma-separated ID ranges with the min and max separated by a "-"
# If a sequence of digits repeats twice in a value, it is invalid.
# NOTE: The two digits need to make up the whole number.

# Add up all invalid id sums based on if a number's digits make up two repeating numbers
def invalid_id_sum(ranges):
    id_sum = 0
    for range in ranges:
        min_max = range.split("-")
        min = min_max[0]
        max = min_max[1]
        num = int(min)
        while num <= int(max):
            str_num = str(num)
            if (len(str_num) % 2 == 0) and (int(str_num[:(len(str_num)//2)]) == int(str_num[(len(str_num)//2):])):
                id_sum += num
            num += 1
    return id_sum

# Add up invalid id sums based on any sequence of repeating numbers in all digits

# Process input, returns a list of ranges
def process_input(input_name):
    with open(input_name, "r") as file:
        content = file.read()
        return content.split(",")

# Part 1: Find all invalid ids, then add them all up.
def part_one():
    ranges = process_input("AOCDay2/AOCday2example.txt")
    id_sum = invalid_id_sum(ranges)
    print("Example test. Expecting 1227775532. Got %d" % (id_sum))

    ranges = process_input("Inputs/AOCday2.txt")
    id_sum = invalid_id_sum(ranges)
    print("Part one answer: %d" % (id_sum))

part_one()