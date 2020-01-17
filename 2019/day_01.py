# --- Day 1: The Tyranny of the Rocket Equation ---
# https://adventofcode.com/2019/day/1
#
# Fuel required to launch a given module is based on its mass.
# Specifically, to find the fuel required for a module, take its mass,
# divide by three, round down, and subtract 2.
#
# For example:
#
# For a mass of 12, divide by 3 and round down to get 4,
# then subtract 2 to get 2.
# For a mass of 14, dividing by 3 and rounding down still yields 4,
# so the fuel required is also 2.
# For a mass of 1969, the fuel required is 654.
# For a mass of 100756, the fuel required is 33583.
#
# The Fuel Counter-Upper needs to know the total fuel requirement.
# To find it, individually calculate the fuel needed for the mass of each
# module (your puzzle input), then add together all the fuel values.
#
# What is the sum of the fuel requirements for all of the modules on
# your spacecraft?

import math
testing = False

def fuel_counter_upper(mass):
    fuel = math.floor(mass / 3) - 2
    if fuel < 1:
        return 0
    fuel += fuel_counter_upper(fuel)
    return fuel

mass_of_modules = [
129561, 125433, 97919, 93037, 73254, 96511, 115676, 95032, 69369, 145385,
111145, 64368, 83462, 95765, 133284, 136563, 67439, 69311, 147720, 92632,
142940, 100610, 106538, 80025, 121672, 125386, 126601, 67943, 120022, 95914,
132721, 105831, 138493, 57649, 72843, 81754, 103116, 148993, 139042, 145929,
61039, 126034, 74187, 60750, 99048, 131776, 123137, 113098, 107571, 117050,
108649, 117455, 147443, 121863, 104952, 103465, 128718, 61795, 121049, 112010,
74403, 56153, 136161, 76872, 94156, 131477, 91769, 90744, 118647, 135791,
98914, 104988, 62070, 82308, 71964, 91477, 63733, 84412, 127000, 65449,
67976, 51400, 56045, 82951, 101119, 143015, 99388, 51796, 93467, 63220,
124459, 136330, 130535, 144270, 88616, 63626, 139954, 92191, 117618, 110422
]

if testing:
    num = input("Enter Module Mass: ")
    print fuel_counter_upper(int(num))
else:
    sum = 0
    for module in mass_of_modules:
        sum += fuel_counter_upper(module)
    print sum
