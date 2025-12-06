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
    print("Final problems: %s" % (problems))
    return problems

# Process input, for each line constructs lists for each problem
# In this one, problems are assembled a little differently
# Return the list of problems
def process_input_part_two(input_name):
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
    print("Final problems: %s" % (problems))
    return problems

# Part 1: Get grand total of problems
def problems_grand_total(problems):
    sum = 0
    for problem in problems:
        sign = problem[len(problem) - 1]
        answer = 0 if sign == "+" else 1
        for i in range(len(problem) - 1):
            answer = answer + int(problem[i]) if sign == "+" else answer * int(problem[i])
        print("Problem %s: The answer is %d" % (problem, answer))
        sum += answer
    return sum

def part_one():
    file = "Inputs/AOCday6.txt"
    problems = process_input_part_one(file)
    print("Part one, grand total: %d" % (problems_grand_total(problems)))

# Part 2: Cephalopod math works differently.
# Now the numbers are vertical too!

part_one()