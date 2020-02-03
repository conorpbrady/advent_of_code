from opcodecomputer import OpCodeComputer

class HullSpace:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = 0
        self.painted = False

    def paint(self, color):
        self.color = color
        self.painted = True

class Hull:

    moves = {
        'up': {
            'x': 0,
            'y': -1,
            'turn_left': 'left',
            'turn_right': 'right'
        },
        'right': {
            'x': 1,
            'y': 0,
            'turn_left': 'up',
            'turn_right': 'down'
        },
        'down': {
            'x': 0,
            'y': 1,
            'turn_left': 'right',
            'turn_right': 'left'
        },
        'left': {
            'x': -1,
            'y': 0,
            'turn_left': 'down',
            'turn_right': 'up'
        }
    }
    def __init__(self, color):
        self.robot_x = 0
        self.robot_y = 0
        hull_space = HullSpace(0, 0)
        hull_space.color = color
        self.hull_spaces = [];
        self.hull_spaces.append(hull_space)
        self.direction = 'up'

    def add_space(self, hull_space):
        self.hull_spaces.append(hull_space)

    def find_space(self, x, y):
        for hs in self.hull_spaces:
            if hs.x == x and hs.y == y:
                return hs
        return None

    def count_painted_spaces(self):
        counter = 0
        for hs in self.hull_spaces:
            if hs.painted:
                counter += 1
        return counter

    def turn(self, turn_direction):
        if turn_direction == 1:
            #print("turning right")
            self.direction = self.moves[self.direction]['turn_right']
        else:
            #print("turning left")
            self.direction = self.moves[self.direction]['turn_left']
        #print("now pointing", self.direction)

    def move(self):
        self.robot_x += self.moves[self.direction]['x']
        self.robot_y += self.moves[self.direction]['y']
        #print("moving to", self.robot_x, self.robot_y)
        new_hull_space = self.find_space(self.robot_x, self.robot_y)
        if new_hull_space is None:
            #print("creating at", self.robot_x, self.robot_y)
            new_hull_space = HullSpace(self.robot_x, self.robot_y)
            self.hull_spaces.append(new_hull_space)

        return new_hull_space.color

    def paint_space(self, color):
        hull_space = self.find_space(self.robot_x, self.robot_y)
        hull_space.paint(color)

    def read_color(self):
        hull_space = self.find_space(self.robot_x, self.robot_y)
        return hull_space.color

    def get_bounds(self):
        min_x = None
        min_y = None
        max_x = None
        max_y = None

        for hs in self.hull_spaces:

            if min_x == None:
                min_x = hs.x
            if max_x == None:
                max_x = hs.x
            if min_y == None:
                min_y = hs.y
            if max_y == None:
                max_y = hs.y

            if hs.x < min_x:
                min_x = hs.x
            if hs.x > max_x:
                max_x = hs.x
            if hs.y < min_y:
                min_y = hs.y
            if hs.y > max_y:
                max_y = hs.y

        return (min_x,max_x), (min_y,max_y)

    def get_color_at(self, x, y):
        hull_space = self.find_space(x, y)
        if hull_space is None:
            return 0
        return hull_space.color

    def draw(self):

        bounds_x , bounds_y = self.get_bounds()
        print(bounds_x, bounds_y)
        for y in range(bounds_y[0]-2, bounds_y[1]+2):
            line = ''
            for x in range(bounds_x[0], bounds_x[1]):
                char = '#' if self.get_color_at(x,y) == 1 else '.'
                line += char
            print(line)


instr = [3,8,1005,8,310,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,29,1,2,11,10,1,1101,2,10,2,1008,18,10,2,106,3,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,67,2,105,15,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,93,2,1001,16,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,119,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,141,2,7,17,10,1,1103,16,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,170,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1002,8,1,193,1,7,15,10,2,105,13,10,1006,0,92,1006,0,99,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,101,0,8,228,1,3,11,10,1006,0,14,1006,0,71,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,101,0,8,261,2,2,2,10,1006,0,4,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,289,101,1,9,9,1007,9,1049,10,1005,10,15,99,109,632,104,0,104,1,21101,0,387240009756,1,21101,327,0,0,1105,1,431,21101,0,387239486208,1,21102,1,338,0,1106,0,431,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,3224472579,1,1,21101,0,385,0,1106,0,431,21101,0,206253952003,1,21102,396,1,0,1105,1,431,3,10,104,0,104,0,3,10,104,0,104,0,21102,709052072296,1,1,21102,419,1,0,1105,1,431,21102,1,709051962212,1,21102,430,1,0,1106,0,431,99,109,2,21202,-1,1,1,21102,1,40,2,21102,462,1,3,21102,452,1,0,1105,1,495,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,457,458,473,4,0,1001,457,1,457,108,4,457,10,1006,10,489,1101,0,0,457,109,-2,2105,1,0,0,109,4,2102,1,-1,494,1207,-3,0,10,1006,10,512,21101,0,0,-3,22101,0,-3,1,21202,-2,1,2,21102,1,1,3,21101,531,0,0,1105,1,536,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,559,2207,-4,-2,10,1006,10,559,21202,-4,1,-4,1105,1,627,22102,1,-4,1,21201,-3,-1,2,21202,-2,2,3,21102,1,578,0,1105,1,536,21202,1,1,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,597,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,619,21201,-1,0,1,21102,1,619,0,106,0,494,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]


hull = Hull(1)
hull_painter = OpCodeComputer(instr, 0, 2)

color_read = []
running = True
#while running:
while running:

    color_read.append(hull.read_color())
    #print(color_read)
    running = hull_painter.calculate(color_read)

    color_read.pop()
    if not running:
        break
    #print(hull_painter.output)
    color = hull_painter.output.popleft()
    turn_dir = hull_painter.output.popleft()

    hull.paint_space(color)
    hull.turn(turn_dir)
    hull.move()

hull.draw()
