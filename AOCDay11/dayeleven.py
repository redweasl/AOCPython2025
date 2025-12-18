# AOC Day 11 2025
# Each line in input gives device name followed by list of devices which its outputs are attached to
# Data flows via outputs (cannot go backwards)
# Device with "you" is where you start
# End with devices with label "out"

import time

class Device:
    def __init__(self, label):
        self.label = label
        self.devices = []

    def addConnection(self, other):
        self.devices.append(other)

    def numPathsToOut(self, devicedict: dict):
        # print(f"Looking at device {self}")
        if self.label == "out":
            return 1
        else:
            sum = 0
            for device in self.devices:
                sum += devicedict.get(device).numPathsToOut(devicedict)
            # print(f"Done with machine {self.label}")
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

def numPathsYouToOut(devicedict: dict[Device]):
    if devicedict.get("you") is None:
        return -1
    return devicedict.get("you").numPathsToOut(devicedict)

# PART 1: How many different paths lead you to out?
def part_one():
    file = "Inputs/AOCday11.txt"
    devices = process_input(file)
    numPaths = numPathsYouToOut(devices)
    print(f"Part 1 (UNKNOWN): Number of paths from device you to out: {numPaths}")

file = "AOCDay11/AOCday11example.txt"
devices = process_input(file)
numPaths = numPathsYouToOut(devices)
print(f"Part 1 example (5): Number of paths from device you to out: {numPaths}")

before = time.perf_counter_ns()
part_one()
elapsed = time.perf_counter_ns() - before
print(f"Part 1 took {elapsed//1_000_000} ms")