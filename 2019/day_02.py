# --- Day 2: 1202 Program Alarm ---
# https://adventofcode.com/2019/day/2
#
# An Intcode program is a list of integers separated by commas (like 1,0,0,3,99).
# To run one, start by looking at the first integer (called position 0).
# Here, you will find an opcode - either 1, 2, or 99.
#
# The opcode indicates what to do; for example, 99 means that the program
# is finished and should immediately halt. Encountering an unknown opcode
# means something went wrong.
#
# Opcode 1 adds together numbers read from two positions and stores the result
# in a third position. The three integers immediately after the opcode tell you
# these three positions - the first two indicate the positions from which you
# should read the input values, and the third indicates the position at which
# the output should be stored.
#
# Opcode 2 works exactly like opcode 1, except it multiplies the two inputs
# instead of adding them. Again, the three integers after the opcode indicate
# where the inputs and outputs are, not their values.
#
# Once you're done processing an opcode, move to the next one by stepping
# forward 4 positions.
#
# Once you have a working computer, the first step is to restore the gravity
# assist program (your puzzle input) to the "1202 program alarm" state it had
# just before the last computer caught fire. To do this, before running the
# program, replace position 1 with the value 12 and replace position 2 with
# the value 2.
#
# What value is left at position 0 after the program halts?


#opcode = [2,4,4,5,99,0]

def opcode_program(noun, verb):

    opcode = [1,12,2,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,5,19,23,1,23,5,
    27,1,27,13,31,1,31,5,35,1,9,35,39,2,13,39,43,1,43,10,47,1,47,13,51,2,
    10,51,55,1,55,5,59,1,59,5,63,1,63,13,67,1,13,67,71,1,71,10,75,1,6,75,
    79,1,6,79,83,2,10,83,87,1,87,5,91,1,5,91,95,2,95,10,99,1,9,99,103,1,
    103,13,107,2,10,107,111,2,13,111,115,1,6,115,119,1,119,10,123,2,9,123,
    127,2,127,9,131,1,131,10,135,1,135,2,139,1,10,139,0,99,2,0,14,0]

    opcode[1] = noun
    opcode[2] = verb
    #print opcode
    for cursor in xrange(0,len(opcode),4):
        if opcode[cursor] == 99:
            break
        op_one = opcode[opcode[cursor + 1]]
        op_two = opcode[opcode[cursor + 2]]
        store_position = cursor + 3

        if opcode[cursor] == 1:
            opcode[opcode[store_position]] = op_one + op_two
            #print("1: {} + {}".format(op_one, op_two))
        elif opcode[cursor] == 2:
            opcode[opcode[store_position]] = op_one * op_two
            #print("2: {} * {}".format(op_one, op_two))
        else:
            print("Something went wrong")
            return 0

    return opcode[0]

for i in range(0,100):
    for j in range(0,100):
        r = opcode_program(i,j)
        #print "{} {} {}".format(i, j, r)
        if r == 19690720:
            print 100 * i + j
            break
