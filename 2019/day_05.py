from collections import deque

class OpCodeComputer:

    pointer_length = {
        1: 4,
        2: 4,
        3: 2,
        4: 2,
        5: 3,
        6: 3,
        7: 4,
        8: 4,
        99: 0
    }
    def __init__(self, instruction_list, debug_level=0, pause_on_output=False):
        self.instruction_list = instruction_list
        self.pause_on_output = pause_on_output
        self.position = 0
        self.debug_level = debug_level
        self.output = deque()


    def calculate(self, input):
        self.input = deque(input)
        if self.debug_level > 2:
            print("Input:" , input)
        while True:
            if self.debug_level > 2:
                print("Pointer:" , self.position)
            delta = self.read_instruction(self.instruction_list[self.position])
            if delta == -1:
                return False
            if delta == -2:
                self.position += 2
                return True
            self.position += delta
        return self.output


    def read_instruction(self, instruction):
        instruction_str = self.pad_instruction(instruction)
        if self.debug_level > 0:
            print("Instruction: ", instruction_str)
        opcode = int(instruction_str[-2:])
        if opcode == 99:
            return -1
        operation = ''
        params = self.parameters(opcode, instruction_str)
        if self.debug_level > 1:
            print("Values: ", params)

            pass
        if opcode == 1:
            self.add(params)
        if opcode == 2:
            self.multiply(params)
        if opcode == 3:
            inpt = self.input.popleft()
            if self.debug_level > 2:
                print("Saving input", inpt, "to position", self.instruction_list[self.position + 1])
            self.instruction_list[self.instruction_list[self.position + 1]] = inpt
        if opcode == 4:
            self.output.append(params[0])

            if self.pause_on_output:
                #print("Pausing on", self.position)
                return -2
        if opcode == 5:
            return self.jump(params, True)
        if opcode == 6:
            return self.jump(params, False)
        if opcode == 7:
            self.less_than(params)
        if opcode == 8:
            self.equals(params)

        return self.pointer_length[opcode]

    def parameters(self, opcode, instruction_str):
        length = self.pointer_length[opcode]
        start = self.position + 1
        params = self.instruction_list[start:start+length-1]
        values = self.get_values_by_mode(params, instruction_str[0:2])
        return values

    def get_values_by_mode(self, parameters, modes):
        values = []
        modes = modes[::-1]
        if self.debug_level > 2:
            print("Parameters: ", parameters)
            print("Modes:", modes)

        for i in range(0,len(parameters)):
            if(i >= len(modes)):
                values.append(parameters[i])
            else:
                if modes[i] == '0': # Position Mode
                    values.append(self.instruction_list[parameters[i]])
                else: #Immediate Mode
                    values.append(parameters[i])


        return values



    def pad_instruction(self, num):
        num_str = str(num)
        while len(num_str) != 4:
            num_str  = '0' + num_str
        return num_str

    def add(self, values):
        self.instruction_list[values[2]] = values[0] + values[1]
        if self.debug_level > 3:
            print("Saving value", values[1] + values[0], "to position", values[2])

    def multiply(self, values):
        self.instruction_list[values[2]] = values[0] * values[1]
        if self.debug_level > 3:
            print("Saving value", values[1] * values[0], "to position", values[2])

    def jump(self, values, jump_if_true):
        if (jump_if_true and values[0]!= 0) or (not jump_if_true and values[0] == 0):
            self.position = values[1]
            if self.debug_level > 2:
                print("Junping to position:", values[1])
            return 0
        return 3

    def less_than(self, values):
        v = 1 if values[0] < values[1] else 0
        self.instruction_list[values[2]] = v
        #print("Storing", v, "at pos", values[2])
    def equals(self, values):
        v = 1 if values[0] == values[1] else 0
        #print("storing", v, "at pos", values[2])
        self.instruction_list[values[2]] = v


def __main__():
    #Outputs 7988899 for input 1, 13758663 for input 5
    instr = [3,225,1,225,6,6,1100,1,238,225,104,0,1101,90,64,225,1101,15,56,225,1,14,153,224,101,-147,224,224,4,224,1002,223,8,223,1001,224,3,224,1,224,223,223,2,162,188,224,101,-2014,224,224,4,224,1002,223,8,223,101,6,224,224,1,223,224,223,1001,18,81,224,1001,224,-137,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1102,16,16,224,101,-256,224,224,4,224,1002,223,8,223,1001,224,6,224,1,223,224,223,101,48,217,224,1001,224,-125,224,4,224,1002,223,8,223,1001,224,3,224,1,224,223,223,1002,158,22,224,1001,224,-1540,224,4,224,1002,223,8,223,101,2,224,224,1,223,224,223,1101,83,31,225,1101,56,70,225,1101,13,38,225,102,36,192,224,1001,224,-3312,224,4,224,1002,223,8,223,1001,224,4,224,1,224,223,223,1102,75,53,225,1101,14,92,225,1101,7,66,224,101,-73,224,224,4,224,102,8,223,223,101,3,224,224,1,224,223,223,1101,77,60,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,7,226,677,224,1002,223,2,223,1005,224,329,1001,223,1,223,1007,226,677,224,1002,223,2,223,1005,224,344,101,1,223,223,108,226,226,224,1002,223,2,223,1006,224,359,101,1,223,223,7,226,226,224,102,2,223,223,1005,224,374,101,1,223,223,8,677,677,224,1002,223,2,223,1005,224,389,1001,223,1,223,107,677,677,224,102,2,223,223,1006,224,404,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,419,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,434,1001,223,1,223,7,677,226,224,102,2,223,223,1006,224,449,1001,223,1,223,1107,226,226,224,1002,223,2,223,1005,224,464,101,1,223,223,1108,226,677,224,102,2,223,223,1005,224,479,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,494,1001,223,1,223,1107,226,677,224,1002,223,2,223,1005,224,509,101,1,223,223,1007,226,226,224,1002,223,2,223,1006,224,524,101,1,223,223,107,226,226,224,1002,223,2,223,1005,224,539,1001,223,1,223,1108,677,677,224,1002,223,2,223,1005,224,554,101,1,223,223,1008,677,226,224,102,2,223,223,1006,224,569,1001,223,1,223,8,226,677,224,102,2,223,223,1005,224,584,1001,223,1,223,1008,677,677,224,1002,223,2,223,1006,224,599,1001,223,1,223,108,677,677,224,102,2,223,223,1006,224,614,1001,223,1,223,108,226,677,224,102,2,223,223,1005,224,629,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,644,101,1,223,223,107,677,226,224,1002,223,2,223,1005,224,659,101,1,223,223,1108,677,226,224,102,2,223,223,1005,224,674,1001,223,1,223,4,223,99,226]

    # Mode Tests
    # instr =  [1002,4,3,4,33]

    # Jump Tests
    #instr = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    #instr = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]

    # Outputs 999 if input < 8, 1000 input = 8, 1000 input > 8s
    #instr = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

    occ = OpCodeComputer(instr)
    occ.calculate(5)
    print(occ.output)
