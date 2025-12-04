# AOC Day 3 2025
# Banks of batteries with different voltages
# In each bank, turn on two batteries, voltage = digits of number formed
# Find largest possible joltage each bank can produce

def total_joltage(banks):
    sum = 0
    for bank in banks:
        sum += max_joltage(bank)
    return sum

def max_joltage(batteries):
    joltageTen = 0
    b2 = 0
    for b1 in range (len(batteries) - 1):
        if int(batteries[b1]) * 10 > joltageTen:
            joltageTen = int(batteries[b1]) * 10
            b2 = b1
    b2 += 1
    joltage = joltageTen
    while b2 < len(batteries):
        joltage = max(joltage, joltageTen + int(batteries[b2]))
        b2 += 1
    # print("Max joltage for a bank of %s was %d" % (batteries, joltage))
    return joltage

# Process input, returns a list of ranges
def process_input(input_name):
    with open(input_name, "r") as file:
        content = file.read()
        return content.split("\n")
    
# Part 1: Maximum total joltage
def part_one():
    file = "Inputs/AOCday3.txt"
    banks = process_input(file)
    print("Total joltage: %d" % (total_joltage(banks)))

part_one()

