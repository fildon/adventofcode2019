import math

class IntCodeComputer:
    def __init__(self, file_name, input_value):
        file = open(file_name, "r")
        self.int_code = list(map(
            lambda input_string: int(input_string),
            file.read().strip().split(',')
        ))
        self.input = input_value
        self.command_pointer = 0
        self.halt = False

    def run_int_code(self):
        while not self.halt and self.command_pointer < len(self.int_code):
            self.process_command_at_pointer()

    def process_command_at_pointer(self):
        command_switch = {
            1: [self.addition, [True, True, False]],
            2: [self.multiplication, [True, True, False]],
            3: [self.read_input, [False]],
            4: [self.write_output, [True]],
            5: [self.jump_if_true, [True, True]],
            6: [self.jump_if_false, [True, True]],
            7: [self.less_than, [True, True, False]],
            8: [self.equals, [True, True, False]],
            99: [self.set_halt, []]
        }
        int_code = self.int_code[self.command_pointer]
        if int_code % 100 not in command_switch:
            self.halt = True
            print("UNRECOGNISED COMMAND: ")
            print(str(self.int_code[self.command_pointer]))
            return   
        executable, n_args = command_switch[int_code % 100]
        args = self.get_args(n_args)
        executable(args)
    
    def get_args(self, n_args):
        param_modes = math.floor(self.int_code[self.command_pointer] / 100)
        args = []
        while param_modes > 0:
            args.append(param_modes % 10)
            param_modes = math.floor(param_modes / 10)
        for _ in range(len(n_args) - len(args)):
            args.append(0)
        for i in range(len(args)):
            is_immediate = args[i] == 1
            arg = self.int_code[self.command_pointer + 1 + i]
            if not is_immediate and n_args[i]:
                arg = self.int_code[arg]
            args[i] = arg
        return args

    def addition(self, args):
        self.int_code[args[2]] = args[0] + args[1]
        self.command_pointer += 4

    def multiplication(self, args):
        self.int_code[args[2]] = args[0] * args[1]
        self.command_pointer += 4

    def read_input(self, args):
        self.int_code[args[0]] = self.input
        self.command_pointer += 2

    def write_output(self, args):
        print(f'OUTPUT: {args[0]}')
        self.command_pointer += 2

    def jump_if_true(self, args):
        if not args[0] == 0:
            self.command_pointer = args[1]
        else:
            self.command_pointer += 3

    def jump_if_false(self, args):
        if args[0] == 0:
            self.command_pointer = args[1]
        else:
            self.command_pointer += 3

    def less_than(self, args):
        self.int_code[args[2]] = 1 if args[0] < args[1] else 0
        self.command_pointer += 4

    def equals(self, args):
        self.int_code[args[2]] = 1 if args[0] == args[1] else 0
        self.command_pointer += 4

    def set_halt(self, args):
        self.halt = True
        print('HALTING')


computer = IntCodeComputer('input.txt', 5)
computer.run_int_code()

# SOLVED: 2808771
