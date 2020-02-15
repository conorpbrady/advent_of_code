import math
class Reaction:

    def split_equation(self, s):
        i = s.find(" => ")
        l = s[:i]
        r = s[i+4:]
        return l, r

    def split_coeff(self, s):
        l = s.split()
        return (int(l[0]), l[1])


    def split_reactants(self, s):
        f_list = []
        r_list = s.split(', ')
        for r in r_list:
            f_list.append(self.split_coeff(r))
        return f_list

    def __init__(self, s):
        left, right = self.split_equation(s)
        self.reactants = self.split_reactants(left)
        full_product = self.split_coeff(right)
        self.product = full_product[1]
        self.pc = int(full_product[0])


def find_reaction(prd):
    for reaction in reactions:
        if reaction.product == prd:
            return reaction
    return 1

def tabs(level):
    s = ''
    for i in range(0,level):
        s += '  '
    return s

def find_reactants(coeff, rct, level=0):
    global ore_sum
    indent = tabs(level)
    reaction = find_reaction(rct)
    pc = reaction.pc
    if reaction.product in resource_store:# and reaction.reactants[0][1] != "ORE":
        #print("{}Using {} {}  from resource store".format(indent, resource_store[reaction.product], reaction.product))
        coeff -= resource_store[reaction.product]
        resource_store[reaction.product] = 0
    reactions_needed = math.ceil(coeff / pc)

    remainder = (reactions_needed * pc) - coeff
    if(remainder > 0):
        if reaction.product in resource_store:
            resource_store[reaction.product] += remainder
        else:
            resource_store[reaction.product] = remainder

    #print("{}To produce {} {}, we need:".format(indent, coeff, reaction.product))
    #print("{}Leaving {} {} as a remainder".format(indent, remainder, reaction.product))
    for reactant in reaction.reactants:

        ratio = reactions_needed * reactant[0]
        remainder -= ratio
        #print("{}{} {}".format(indent, ratio, reactant[1]))
        #print("{}{} {} left over".format(indent, remainder, reactant[1]))
        if reactant[1] == "ORE":
            ore_sum += ratio
            # if rct in raw_materials:
            #     raw_materials[rct] += coeff
            # else:
            #     raw_materials[rct] = coeff
        else:
            find_reactants(ratio, reactant[1], level+1)

    return


filename = 'day_14.txt'
#filename = 'd14test.txt'

ri = []
with open(filename) as f:
    for line in f:
        ri.append(line)
reactions = []
resource_store = {}
for line in ri:
    reactions.append(Reaction(line))
ore_sum = 0
fuel_count = -1
one_trillion = 1000000000000
while ore_sum < one_trillion:
    find_reactants(1, "FUEL")
    fuel_count += 1
    print(round(100 * ore_sum / one_trillion, 2))
    #print(resource_store)
print(fuel_count)
