import math
import itertools

class IntCodeComputer:
    def __init__(self, file_name, phase_setting):
        file = open(file_name, "r")
        self.int_code = list(map(
            lambda input_string: int(input_string),
            file.read().strip().split(',')
        ))
        self.input = [phase_setting]
        self.command_pointer = 0
        self.halt = False
        self.output_ready = False
        self.output = None

    def run_int_code(self, input_value):
        self.input = [input_value] + self.input
        while not self.halt and not self.output_ready and self.command_pointer < len(self.int_code):
            self.process_command_at_pointer()
        return self.output if self.output_ready else None

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
        if (self.input[-1] is None):
            print('READ NONE FROM INPUT')
        self.int_code[args[0]] = self.input.pop()
        self.command_pointer += 2

    def write_output(self, args):
        self.command_pointer += 2
        self.output_ready = True
        self.output = args[0]

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

def get_amplifier_output(config):
    computers = []
    for phase_setting in config:
        computers.append(IntCodeComputer('input.txt', phase_setting))

    previous_output_value = 0
    current_computer_id = 0
    while True:
        computer = computers[current_computer_id]
        output = computer.run_int_code(previous_output_value)
        if output is None:
            return previous_output_value
        previous_output_value = output
        computer.output_ready = False
        current_computer_id = (current_computer_id + 1) % 5

combinations = itertools.permutations([5, 6, 7, 8, 9])
max_thruster = 0
for combination in combinations:
    thruster_signal = get_amplifier_output(combination)
    if thruster_signal > max_thruster:
        max_thruster = thruster_signal

print(max_thruster)
# SOLVED 79846026
