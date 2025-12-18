# AOC Day 11 2025
# Each line in input gives device name followed by list of devices which its outputs are attached to
# Data flows via outputs (cannot go backwards)
# Device with "you" is where you start
# End with devices with label "out"

import time

pathsDict: dict = dict()

class Device:
    def __init__(self, label):
        self.label = label
        self.devices = []

    def addConnection(self, other):
        self.devices.append(other)

    def numPathsToOut(self, devicedict: dict, endlabel: str):
        if self.label == endlabel:
            return 1
        else:
            sum = 0
            for deviceLabel in self.devices:
                devicePaths = 0
                if pathsDict.get(deviceLabel) is None:
                    devicePaths = devicedict.get(deviceLabel).numPathsToOut(devicedict, endlabel)
                    pathsDict[deviceLabel] = devicePaths
                else:
                    devicePaths = pathsDict.get(deviceLabel)
                sum += devicePaths
            return sum
    
    def __str__(self):
        return f"Device w/label {self.label} and connected to {self.devices} devices"

def process_input(input_name):
    devices = dict()
    with open(input_name, "r") as file:
        for line in file:
            dv = line.strip().split(" ")
            label = dv.pop(0).strip(":")
            devices[label] = Device(label)
            for d in dv:
                if devices.get(d) is None:
                    devices[d] = Device(d)
                devices[label].addConnection(d)
    return devices

def numPathsToOut(startlabel: str, endlabel: str, devicedict: dict[Device]):
    if devicedict.get(startlabel) is None or devicedict.get(endlabel) is None :
        return -1
    pathsDict.clear()
    return devicedict.get(startlabel).numPathsToOut(devicedict, endlabel)

# PART 1: How many different paths lead you to out?
def part_one():
    file = "Inputs/AOCday11.txt"
    devices = process_input(file)
    numPaths = numPathsToOut("you", "out", devices)
    print(f"Part 1 (658): Number of paths from device you to out: {numPaths}")

before = time.perf_counter_ns()
part_one()
elapsed = time.perf_counter_ns() - before
print(f"Part 1 took {elapsed//1_000_000} ms")

# PART 2: How many different paths lead svr to out that also pass through fft and dac?
def part_two():
    file = "Inputs/AOCday11.txt"
    devices = process_input(file)
    n1 = numPathsToOut("svr", "fft", devices)
    n2 = numPathsToOut("fft", "dac", devices)
    n3 = numPathsToOut("dac", "out", devices)
    numPaths = n1 * n2 * n3
    totalPaths = numPathsToOut("svr", "out", devices)
    print(f"Part 2 (371113003846800): Number of paths from device svr to out passing through fft and dac: {numPaths}\nCompare to total paths from svr to out: {totalPaths}")

before = time.perf_counter_ns()
part_two()
elapsed = time.perf_counter_ns() - before
print(f"Part 2 took {elapsed//1_000_000} ms")