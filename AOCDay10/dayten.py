# AOC Day 10 2025
# Factory machines offline, need to crack intialization procedure
# One machine per line w/light dragram [], button wiring schematics (), & joltage res {}
# Light diagram: What the final button layout should be
# Wiring schematic: For a button, what lights are toggled

import time

class Machine:
    def __init__(self, ld: list, bschems: list, jreqs: list):
        self.ld = ld
        self.bschems = bschems
        self.jreqs = jreqs
    
    def __str__(self):
        return f"({self.ld} | {self.bschems} | {self.jreqs})"

def process_input(input_name):
    machines = []
    with open(input_name, "r") as file:
        for line in file:
            vals = line.strip().split(" ")
            ld = vals[0]
            bschems = vals[1:len(vals)-1]
            jreqs = vals[len(vals)-1]
            jreqs =  list(int(num) for num in jreqs[1:len(jreqs)-1].split(","))
            for i in range(len(bschems)):
                bschems[i] = list(int(num) for num in bschems[i][1:len(bschems[i])-1].split(","))
            machines.insert(len(machines), Machine(ld[1:len(ld)-1],
                                                    bschems,
                                                      jreqs))
    return machines

# Part 1: Determine fewest total presses required
# Idea: Breadth-first checks
# Track what configs have already been seen, if a press results in an already seen config terminate that branch
# Go through checks in a queue-like process
# This works: If an existing layout is found in a different combo, that it took the same # or more button presses to get there
def fewest_button_presses(machine: Machine):
    cd = ''.join("." for i in range(len(machine.ld)))
    dict = set()
    dict.add(cd)
    queue = []
    queue.append([cd, 0])

    while len(queue) > 0:
        diagram, num_presses = queue.pop(0)
        for bschem in machine.bschems:
            new_diagram = diagram
            for num in bschem:
                new_diagram = new_diagram[:num] + ("#" if new_diagram[num] == "." else ".") + new_diagram[num+1:]
            if new_diagram == machine.ld:
                # print(f"Fewest button presses for machine {machine} is {num_presses + 1}")
                return num_presses + 1
            elif new_diagram not in dict:
                dict.add(new_diagram)
                queue.append([new_diagram, num_presses + 1])
    return -1

def presses_sum(machines: list[Machine]):
    sum = 0
    for machine in machines:
        sum += fewest_button_presses(machine)
    return sum

def part_one():
    file = "Inputs/AOCday10.txt"
    machines = process_input(file)
    sum = presses_sum(machines)
    print(f"Part 1 (390): The fewest sum of presses is {sum}")

before = time.perf_counter_ns()
part_one()
elapsed = time.perf_counter_ns() - before
print(f"Part 1 took {elapsed//1_000_000} ms")

# Part 2: Joltage requirements instead of light diagram
# Each button press increases it by a jolt
# Fewest total button presses to meet joltage reqs
def fewest_button_presses_jolts(machine: Machine):
    cv = list(0 for i in range(len(machine.ld)))
    str_cv = str(cv)
    dict = set()
    dict.add(str_cv[1:len(str_cv)-1])
    queue = []
    queue.append([cv, 0])
    print(f"Dictionary contains {dict}")

    while len(queue) > 0:
        diagram, num_presses = queue.pop(0)
        print(num_presses)
        for bschem in machine.bschems:
            new_diagram = diagram.copy()
            valid = True
            for num in bschem:
                new_diagram[num] += 1
                if new_diagram[num] > machine.jreqs[num]:
                    valid = False
            # print(f"Config after pressing a button: {new_diagram} is it valid? {valid}")
            if new_diagram == machine.jreqs:
                print(f"JOLT: Fewest button presses for machine {machine} is {num_presses + 1}")
                return num_presses + 1
            str_diagram = str(new_diagram)
            str_diagram = str_diagram[1:len(str_diagram)-1]
            if valid and str_diagram not in dict:
                dict.add(str_diagram)
                queue.append([new_diagram, num_presses + 1])
    print("Found no valid sequences")
    return -1

def presses_sum_jolts(machines: list[Machine]):
    sum = 0
    for machine in machines:
        sum += fewest_button_presses_jolts(machine)
    return sum

def part_two():
    file = "Inputs/AOCday10.txt"
    machines = process_input(file)
    sum = presses_sum_jolts(machines)
    print(f"Part 1 (UNKNOWN): The fewest sum of presses is {sum}")

before = time.perf_counter_ns()
part_two()
elapsed = time.perf_counter_ns() - before
print(f"Part 2 took {elapsed//1_000_000} ms")

file = "AOCDay10/AOCday10example.txt"
machines = process_input(file)
sum = presses_sum_jolts(machines)
print(f"Part 2 example: The fewest sum of presses is {sum}")