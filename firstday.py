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

# Read the text file
dialNum = 50
numZeroes = 0
fileName = "AOCday1example"
with open(fileName + ".txt", "r") as file:
    for line in file:
        # Change for valid lines only
        if len(line) > 0:
            direction = line[0:1]
            if direction == "R":
                dialNum = (dialNum + int(line[1:len(line)])) % 100
            else:
                dialNum = (dialNum - int(line[1:len(line)])) % 100
            numZeroes = numZeroes + 1 if dialNum == 0 else numZeroes
            print("The dial number is %d. Current number of zeroes: %d" % (dialNum, numZeroes))
print("The password is %d" % (numZeroes))

