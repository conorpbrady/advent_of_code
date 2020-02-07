class Moon:

    def __init__(self, p):
        self.position = p
        self.velocity = [0, 0, 0]

    def set_velocity(self, v):
        for d in range(0,3):
            if v[d] is None:
                continue
            self.velocity[d] += v[d]

    def move(self, axes):
        for a in axes:
            self.position[a] += self.velocity[a]


    def pe(self):
        return abs(self.position[0]) + abs(self.position[1]) + abs(self.position[2])

    def ke(self):
        return abs(self.velocity[0]) + abs(self.velocity[1]) + abs(self.velocity[2])

class OrbitSystem:

    def __init__(self, starting_positions):
        self.moons = []
        coords = ['x','y','z']
        for line in starting_positions:
            position = []
            for c in coords:
                s = line.find(c + '=') + 2
                e = line.find(',', line.find(c))
                position.append(int(line[s:e]))
            self.moons.append(Moon(position))

    def accel(self, moon, axes):
        deltas = [0, 0, 0]
        for j in range(0,3):
            if j not in axes:
                deltas[j] = None


        for m in self.moons:
            for i in range(0,3):
                if deltas[i] is None:
                    continue
                if m.position[i] > moon.position[i]:
                    deltas[i] += 1
                if m.position[i] < moon.position[i]:
                    deltas[i] += -1
        moon.set_velocity(deltas)


    def step(self, axes):

        for m in self.moons:
            self.accel(m, axes)
        for m in self.moons:
            m.move(axes)


    def calc_energy(self):
        sum = 0
        for m in self.moons:
            #print(m.pe(), m.ke(), m.pe() * m.ke())
            sum += m.pe() * m.ke()
        return sum

    def __str__(self):
        str = ''
        for m in self.moons:
            str += "<{}, {}, {}>".format(m.position[0], m.position[1], m.position[2])
            str += " | "
            str += "<{}, {}, {}>".format(m.velocity[0], m.velocity[1], m.velocity[2])
            str += "\n"
        return str

    def is_equals(self, os, axes):
        for i in range(0,4):
            for j in axes:
                if os.moons[i].position[j] != self.moons[i].position[j] or os.moons[i].velocity[j] != self.moons[i].velocity[j]:
                    return False
        return True


scan = [
"<x=-1, y=0, z=2>",
"<x=2, y=-10, z=-7>",
"<x=4, y=-8, z=8>",
"<x=3, y=5, z=-1>"
]
# scan = [
# "<x=-8, y=-10, z=0>",
# "<x=5, y=5, z=10>",
# "<x=2, y=-7, z=3>",
# "<x=9, y=-8, z=-3>"
# ]
# #
scan = [
"<x=-7, y=17, z=-11>",
"<x=9, y=12, z=5>",
"<x=-9, y=0, z=-4>",
"<x=4, y=6, z=0>"
]

os = OrbitSystem(scan)
init_os = OrbitSystem(scan)
axes = [[0],[1],[2]]
multiples = []

for a in axes:
    for i in range(1,100000000):
        os.step(a)
        if os.is_equals(init_os, a):
            #print(os)
            multiples.append(i)
            print(i)
            break
product = 1
for m in multiples:
    #Should find lcm
    product *= m
print(product)
#print(os.calc_energy())
