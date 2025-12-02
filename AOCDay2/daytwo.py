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
def invalid_id_sum_all_digits(ranges):
    id_sum = 0
    for range in ranges:
        min_max = range.split("-")
        min = min_max[0]
        max = min_max[1]
        num = int(min)
        while num <= int(max):
            str_num = str(num)
            if contains_value_sequence(str_num):
                id_sum += num
            num += 1
    return id_sum

# Does this number contain a repeating value sequence? (Helper function for part 2)
def contains_value_sequence(str_num):
    seq_max = len(str_num) // 2
    for seq_len in range(seq_max + 1):
        if seq_len > 0 and len(str_num) % seq_len == 0:
            chunk_val = int(str_num[0:seq_len])
            is_repeating = True
            for chunk_num in range(len(str_num) // seq_len):
                cur_chunk_val = int(str_num[seq_len * chunk_num:seq_len * (chunk_num + 1)])
                if cur_chunk_val != chunk_val:
                    is_repeating = False
                    break
            if is_repeating:
                return True
    return False

# Process input, returns a list of ranges
def process_input(input_name):
    with open(input_name, "r") as file:
        content = file.read()
        return content.split(",")

# Part 1: Find all invalid ids (numbers with all digits making a two-sequence), then add them all up.
def part_one():
    ranges = process_input("AOCDay2/AOCday2example.txt")
    id_sum = invalid_id_sum(ranges)
    print("Example test. Expecting 1227775532. Got %d" % (id_sum))

    ranges = process_input("Inputs/AOCday2.txt")
    id_sum = invalid_id_sum(ranges)
    print("Part one answer: %d" % (id_sum))

# Part 2: Same thing, but any length of sequence applies.
def part_two():
    ranges = process_input("AOCDay2/AOCday2exampletwo.txt")
    id_sum = invalid_id_sum_all_digits(ranges)
    print("Example test. Expecting 4174379265. Got %d" % (id_sum))

    ranges = process_input("Inputs/AOCday2.txt")
    id_sum = invalid_id_sum_all_digits(ranges)
    print("Part two answer: %d" % (id_sum))

part_one()
part_two()