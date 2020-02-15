from opcodecomputer import OpCodeComputer
from collections import deque
from random import randrange


def draw(map):
    for line in map:
        print(line)

def replace_char(s, p, r):
    return s[:p] + r + s[p+1:]

def update_map(map, c, x, y):
    map[y] = replace_char(map[y], x, c)
    return map
def count_known_spaces(map):
    sum = 0
    for line in map:
        sum += line.count('.')
        sum += line.count('#')
        sum += line.count('D')
        sum += line.count('D')
    return sum
def new_position(inp):
    x = 0
    y = 0
    #print("Input", inp)
    if inp == 1:
        y = -1
    elif inp == 2:
        y = 1
    elif inp == 3:
        x = -1
    elif inp == 4:
        x = 1
    return (x, y)

def movable_routes(x, y):
    global map
    block_chars = ['#','`']
    mr = []
    if map[y][x-1] not in block_chars:
        mr.append(3)
    if map[y][x+1] not in block_chars:
        mr.append(4)
    if map[y-1][x] not in block_chars:
        mr.append(1)
    if map[y+1][x] not in block_chars:
        mr.append(2)
    return mr

def expand(x, y):
    global map
    open_spaces = []
    block_chars = ['#','O']
    if map[y][x-1] not in block_chars:
        open_spaces.append((x-1, y))
    if map[y][x+1] not in block_chars:
        open_spaces.append((x+1, y))
    if map[y-1][x] not in block_chars:
        open_spaces.append((x, y-1))
    if map[y+1][x] not in block_chars:
        open_spaces.append((x, y+1))

    return open_spaces

with open('day_15.txt') as f:
    line = f.read().strip()
instr = line.split(',')
instr = [ int(x) for x in instr ]
with open('steps.txt') as s:
    steps = s.read().strip()
no_steps = len(steps)
repair_droid = OpCodeComputer(instr, 0, 1)

bounds = (50, 50)
map = []
for y in range(0, bounds[1]):
    line = ''
    for x in range(0, bounds[0]):
        line += ' '
    map.append(line)

movement = {
    'u': 1,
    'd': 2,
    'l': 3,
    'r': 4
}
rdx = 25
rdy = 25

#inputs = deque(steps)
#print(inputs)
inputs = deque()
running = True
while running:
    #print(rdx, rdy)
    draw(map)
    # valid_move = False
    # while not valid_move:
    #     move_input = input("Enter Direction: ")
    #     if move_input in movement:
    #         inputs.append(movement[move_input])
    #         valid_move = True
    #

    open_moves = movable_routes(rdx, rdy)

    if len(open_moves) == 0:
        break
    rand_index = randrange(len(open_moves))
    inputs.append(open_moves[rand_index])
    #inp = [movement[inputs.popleft()]]
    inp = [inputs.popleft()]

    running = repair_droid.calculate(inp)
    result = repair_droid.output.popleft()
    d = new_position(inp[0])
    # print("D:", d)
    # print("Result:", result)
    if result == 0:
        # print(no_steps - len(inputs))
        # break
        wx = rdx + d[0]
        wy = rdy + d[1]
        map = update_map(map, '#', wx, wy)

    if len(open_moves) == 1:
        floor_char = '`'
    else:
        floor_char = '.'
    if result == 1:
        map = update_map(map, floor_char, rdx, rdy)
        rdx += d[0]
        rdy += d[1]
        map = update_map(map, 'D', rdx, rdy)
    if result == 2:
        rdx += d[0]
        rdy += d[1]
        map = update_map(map, 'O', rdx, rdy)
        ox = rdx
        oy = rdy
    #map_counter = count_known_spaces(map)
    #if map_counter == 1660:
        #break


counter = 0
spaces_to_expand_into = 1
open_spaces = []
while spaces_to_expand_into > 0:
    next_round_open_spaces = []
    if len(open_spaces) == 0:
        update_map(map,'O',ox,oy)
        next_round_open_spaces = expand(ox, oy)
    else:
        for os in open_spaces:
            update_map(map, 'O', os[0], os[1])
            next_round_open_spaces += expand(os[0], os[1])

    open_spaces = next_round_open_spaces
    spaces_to_expand_into = len(open_spaces)
    if len(open_spaces) == 0:
        break
    draw(map)

    print(counter)
    input()
    counter += 1

print(counter)
