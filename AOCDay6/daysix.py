# AOC Day 6 2025
# Solve a young cephalopod with her math homework
# Each problem has a group of numbers to add or multiply together
# Problems vertical separated by a vertical column of spaces
# Solve each problem, then get the grand total (sum)

import re

# Process input, for each line constructs lists for each problem
# Return the list of problems
def process_input_part_one(input_name):
    problems = []
    with open(input_name, "r") as file:
        for line in file:
            strip_line = re.sub(" +", " ", line).strip()
            problem_pieces = strip_line.split(" ")
            for i in range(len(problem_pieces)):
                    if len(problems) < len(problem_pieces):
                        problems.insert(len(problems), [problem_pieces[i]])
                    else:
                        problems[i].insert(len(problems), problem_pieces[i])
    return problems

# Part 1: Get grand total of problems
def problems_grand_total(problems):
    sum = 0
    for problem in problems:
        sign = problem[len(problem) - 1]
        answer = 0 if sign == "+" else 1
        for i in range(len(problem) - 1):
            answer = answer + int(problem[i]) if sign == "+" else answer * int(problem[i])
        # print("Problem %s: The answer is %d" % (problem, answer))
        sum += answer
    return sum

def part_one():
    file = "Inputs/AOCday6.txt"
    problems = process_input_part_one(file)
    print("Part one, grand total: %d" % (problems_grand_total(problems)))

# Process input, for each line constructs lists for each problem
# In this one, the input is rotated 90 degrees to make problem comprehension much easier
# Return the rotated input
def process_input_part_two(input_name):
    problems = []
    rotated_lines = []
    with open(input_name, "r") as file:
        first = True
        op_counter = 0
        for line in file:
            if first:
                first = False
                rotated_lines = [chr for chr in line]
            else:
                for i in range(len(line)):
                    if line[i] == "+" or line[i] == "*":
                        rotated_lines.insert(i + op_counter, line[i])
                        op_counter += 1
                    else:
                        rotated_lines[i] = rotated_lines[i] + line[i]

    return rotated_lines

# Part 2: Cephalopod math works differently.
# Now the numbers are vertical too!
def rotated_problems_grand_total(rotated_lines):
    sum = 0
    answer = 0
    operator = "+"
    
    for line in rotated_lines:
        input = line.strip()
        # print("|%s|" % (input))
        if input == "+":
            answer = 0
            operator = "+"
        elif input == "*":
            answer = 1
            operator = "*"
        elif input == "":
            sum += answer
        else:
            answer = answer + int(line) if operator == "+" else answer * int(line)
    return sum

def part_two():
    file = "Inputs/AOCday6.txt"
    rotated_lines = process_input_part_two(file)
    print("Part 2, grand total: %d" % (rotated_problems_grand_total(rotated_lines)))

part_one()
part_two()