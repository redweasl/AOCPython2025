# AOC Day 3 2025
# Banks of batteries with different voltages
# In each bank, turn on two batteries, voltage = digits of number formed
# Find largest possible joltage each bank can produce

def total_joltage(banks, num_activate=2):
    sum = 0
    for bank in banks:
        sum += max_joltage(bank, num_activate)
    return sum

def max_joltage(batteries, num_activate):
    # joltageTen = 0
    # b2 = 0
    # for b1 in range (len(batteries) - 1):
    #     if int(batteries[b1]) * 10 > joltageTen:
    #         joltageTen = int(batteries[b1]) * 10
    #         b2 = b1
    # b2 += 1
    # joltage = joltageTen
    # while b2 < len(batteries):
    #     joltage = max(joltage, joltageTen + int(batteries[b2]))
    #     b2 += 1
    oldJoltage = 0
    joltage = 0
    leftEnd = 0
    max_idx = 0
    rightEnd = len(batteries) - num_activate + 1
    for _ in range (num_activate):
        b = leftEnd
        oldJoltage = joltage * 10
        while b < rightEnd:
            num = int(batteries[b])
            if oldJoltage + num > joltage:
                joltage = oldJoltage + num
                max_idx = b
                if num == 9:
                    break
            b += 1
        leftEnd = max_idx + 1
        rightEnd += 1

    # print("Max joltage for a bank of %s turning on %d batteries was %d" % (batteries, num_activate, joltage))
    return joltage

# Process input, returns a list of ranges
def process_input(input_name):
    with open(input_name, "r") as file:
        content = file.read()
        return content.split("\n")
    
# Part 1: Maximum total joltage (17316)
def part_one():
    file = "Inputs/AOCday3.txt"
    banks = process_input(file)
    print("Part 1 total joltage: %d" % (total_joltage(banks)))

# Part 2: Instead of two batteries, it is now twelve
def part_two():
    file = "Inputs/AOCday3.txt"
    banks = process_input(file)
    print("Part 2 total joltage: %d" % (total_joltage(banks, 12)))

part_one()
part_two()

