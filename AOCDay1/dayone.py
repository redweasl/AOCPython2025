# AOC DAY 1 2025
# Need to unlock a safe with a password. Dials 0 through 99
# Puzzle input has a sequence of rotations for how to open the safe
# Each rotation has a direction (L or R) and a distance value (how many clicks to rotate)
# The dial is a circle (wrap from 0 to 99 and vice versa)
# Dial starts at 50
# Twist: The safe is a decoy!
# ANS: Number of times dial is on zero throughout the sequence

# Refreshers: Modulus wraps around negatives too
# The remainder will have the same sign as the modulus

# Part 1 code: Count how many times the dial goes to 0
def partOne(dialNum, numZeroes, fileName):
    with open(fileName + ".txt", "r") as file:
        for line in file:
            # Assuming that all lines have an instruction on them.
            direction = line[0:1]
            if direction == "R":
                dialNum = (dialNum + int(line[1:len(line)])) % 100
            else:
                dialNum = (dialNum - int(line[1:len(line)])) % 100
            numZeroes = numZeroes + 1 if dialNum == 0 else numZeroes
    print("The password is %d" % (numZeroes))

# Part 2 code: Count how many times the dial passes/points to 0
def partTwo(dialNum, numZeroes, fileName):
    with open(fileName + ".txt", "r") as file:
        for line in file:
            # Assuming that all lines have an instruction on them.
            direction = line[0:1]
            if direction == "R":
                dialNum = (dialNum + int(line[1:len(line)]))
                numZeroes += dialNum // 100 # This counts if we stop at 0
                dialNum = dialNum % 100
            else:
                passZero = 1 if dialNum == 0 else 0 # Handle edge case when we start at 0
                dialNum = (dialNum - int(line[1:len(line)]))
                numZeroes += (dialNum // 100 * -1) - passZero # This counts extra if we start at 0. Doesn't count if it stops at 0
                dialNum = dialNum % 100
                numZeroes = numZeroes + 1 if dialNum == 0 else numZeroes # Handle edge case when we end at 0
    print("The password is %d" % (numZeroes))

dialNum = 50
numZeroes = 0
fileName = "AOCday1"
partTwo(dialNum, numZeroes, fileName)

