import math
import collections

def map_asteroids(m):
    asteroids = []
    for i in range(0,len(m)):
        for j in range(0,len(m[i])):
            if map[i][j] != '.':
                asteroids.append((j,i))

    return asteroids

def find_sign(c):
    if c > 0:
        return -1
    if c < 0:
        return 1
    if c == 0:
        return 0

def clear_line_of_sight(asteroids, x, y, dx, dy):
    if dx != 0:
        slope = dy / dx
        #print(slope)
    x_step = find_sign(dx)
    y_step = find_sign(dy)
    #print(x_step, y_step)
    pos_ast = []
    for a in asteroids:
        pos_ast.append((a[0],a[1]))

    while dx != 0 or dy != 0:

        if dx == 0:
            dy = dy + y_step

        else:
            dx = dx + x_step
            dy = dx * slope

            if dy % 1 == 0:
                dy = int(dy)
                #print(dy)
            else:

                continue
        #print("checking position",(x+dx,y+dy))


        if (x+dx, y+dy) in pos_ast and (dx, dy) != (0,0):
            #print("found blocker at",(x+dx,y+dy))
            return False

    return True

def determine_location_monitoring_station(asteroids):
    max_num = 0
    max_ast = 'a'
    for start_ast in asteroids:
        num = 0
        for end_ast in asteroids:
            #print("start", start_ast,"ending", end_ast)

            if start_ast[0] == end_ast[0] and start_ast[1] == end_ast[1]:
                continue
            dx = (end_ast[0] - start_ast[0])
            dy = (end_ast[1] - start_ast[1])
            #print((dx,dy))
            if clear_line_of_sight(asteroids, start_ast[0], start_ast[1], dx, dy):
                #print("LOS from", start_ast, "to", end_ast)
                num = num + 1

        if num > max_num:
            max_num = num
            max_ast = start_ast

    #print("Max num", max_num)
    return max_ast

def next_quadrant(q):
    if q == '1':
        return '2'
    if q == '2':
        return '3'
    if q == '3':
        return '4'
    if q == '4':
        return '1'

def theta(dx, dy):
    if dx == 0:
        if dy > 0:
            return 0
        else:
            return 180
    elif dy == 0:
        if dx > 0:
            return 270
        else:
            return 90
    else:

        if dy > 0 and dx > 0:
            return 270 + abs(math.degrees(math.atan(dy / dx)))
        if dy > 0 and dx < 0:
            return 0 + abs(math.degrees(math.atan(dx / dy)))
        if dy < 0 and dx > 0:
            return 180 + abs(math.degrees(math.atan(dx / dy)))
        if dy < 0 and dx < 0:
            return 90 + abs(math.degrees(math.atan(dy / dx)))

def calculate_thetas(asteroids, station):
    aa = []
    for a in asteroids:
        dx = station[0] - a[0]
        dy = station[1] - a[1]
        t_key = round(theta(dx,dy),2)
        aa.append((a[0],a[1],t_key))
    return aa


def fire_the_laser(station, ast_angles, last_angle):

    min_angle = None
    min_ast = None
    incr_angle = 0
    visible_ast = []
    for ast in ast_angles:
        dx = station[0] - ast[0]
        dy = station[1] - ast[1]
        clear_los = clear_line_of_sight(ast_angles, station[0], station[1], dx * -1, dy * -1)
        if clear_los:
            visible_ast.append(ast)

    while min_angle is None:

        for ast in visible_ast:
            incr_angle = ast[2] - last_angle
            #print(ast)
            if min_angle is None or (ast[2] < min_angle and incr_angle > 0):
                #print(min_angle)
                min_angle = ast[2]
                min_ast = ast

        if min_angle is None:
            last_angle -= 360

    return min_ast, min_angle

# map = [
# ".#....###.....#..",
# "##...##...#.....#",
# "##...#......1234.",
# "..#.....X...5##..",
# "..#.9.....8....76"
# ]
#
# map = [
# ".#....###24...#..",
# "##...##.13#67..9#",
# "##...#...5.8####.",
# "..#.....X...###..",
# "..#.#.....#....##"
# ]
map = []
with open('asteroid_map.txt') as f:
    for line in f:
        map.append(line.strip())

#print(map)
asteroids = map_asteroids(map)
#print(asteroids)
station = determine_location_monitoring_station(asteroids)
#station = (8, 3)
asteroids.remove(station)
print("Station:", station)
ast_angles = calculate_thetas(asteroids, station)
last_angle = -0.1
counter = 1
while len(ast_angles) > 0:
    destroyed, last_angle = fire_the_laser(station, ast_angles, last_angle)
    ast_angles.remove(destroyed)
    print(counter, destroyed)
    if counter == 200:
        break
    counter += 1
