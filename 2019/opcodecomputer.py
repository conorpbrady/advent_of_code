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
