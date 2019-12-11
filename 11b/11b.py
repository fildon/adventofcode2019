import math
import itertools


class IntCodeMemory:
    def __init__(self, int_code_list):
        self.int_code = int_code_list

    def read(self, memory_address):
        if memory_address < 0:
            raise IndexError(
                f'attempted to read negative index: {memory_address}')
        if memory_address >= len(self.int_code):
            return 0
        return self.int_code[memory_address]

    def write(self, memory_address, value):
        if memory_address < 0:
            raise IndexError(
                f'attempted to write to negative index: {memory_address}')
        if memory_address >= len(self.int_code):
            pad_length = memory_address - len(self.int_code) + 1
            self.int_code += [0 for _ in range(pad_length)]
        self.int_code[memory_address] = value
        # print(f'Wrote {value} to {memory_address}')


class IntCodeComputer:
    def __init__(self, file_name):
        file = open(file_name, "r")
        self.int_code = IntCodeMemory(list(map(
            lambda input_string: int(input_string),
            file.read().strip().split(',')
        )))
        self.input = []
        self.command_pointer = 0
        self.relative_base = 0
        self.halt = False
        self.output = []

    def run_int_code(self, input_value):
        self.input = [input_value] + self.input
        while not self.halt and len(self.output) < 2:
            self.process_command_at_pointer()

    def process_command_at_pointer(self):
        command_switch = {
            1: [self.addition, [False, False, True]],
            2: [self.multiplication, [False, False, True]],
            3: [self.read_input, [True]],
            4: [self.write_output, [False]],
            5: [self.jump_if_true, [False, False]],
            6: [self.jump_if_false, [False, False]],
            7: [self.less_than, [False, False, True]],
            8: [self.equals, [False, False, True]],
            9: [self.update_relative_base, [False]],
            99: [self.set_halt, []]
        }
        int_code = self.int_code.read(self.command_pointer)
        if int_code % 100 not in command_switch:
            raise KeyError(f'UNRECOGNISED COMMAND:\n{str(int_code)}')
        executable, write_args = command_switch[int_code % 100]
        # Used only for the debug statement below
        raw_args = [self.int_code.read(self.command_pointer + i + 1)
                    for i in range(len(write_args))]
        args = self.get_args(write_args)
        # print(f'{self.command_pointer}: {int_code} {executable.__name__}\n\twith args RAW: {raw_args} PARSED: {args} Relative_base: {self.relative_base} at 4297 is {self.int_code.read(4297)}')
        executable(args)

    def get_args(self, write_args):
        param_modes = math.floor(
            self.int_code.read(self.command_pointer) / 100)
        args = []
        while param_modes > 0:
            args.append(param_modes % 10)
            param_modes = math.floor(param_modes / 10)
        for _ in range(len(write_args) - len(args)):
            args.append(0)

        for i in range(len(args)):
            is_write = write_args[i]
            is_relative = args[i] == 2
            is_immediate = args[i] == 1
            if is_write:
                arg = self.int_code.read(
                    self.command_pointer + 1 + i
                ) + (self.relative_base if is_relative else 0)
            elif is_immediate:
                arg = self.int_code.read(self.command_pointer + 1 + i)
            else:
                arg = self.int_code.read(
                    self.int_code.read(
                        self.command_pointer + 1 + i
                    ) + (self.relative_base if is_relative else 0)
                )
            args[i] = arg
        return args

    def addition(self, args):
        self.int_code.write(args[2], args[0] + args[1])
        self.command_pointer += 4

    def multiplication(self, args):
        self.int_code.write(args[2], args[0] * args[1])
        self.command_pointer += 4

    def read_input(self, args):
        if len(self.input) == 0:
            raise RuntimeError('TRIED TO READ FROM EMPTY INPUT')
        input_value = self.input.pop()
        # print(f'\t\tRead input value: {input_value}. Writing to {args[0]}')
        self.int_code.write(args[0], input_value)
        self.command_pointer += 2

    def write_output(self, args):
        self.command_pointer += 2
        self.output.append(args[0])

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
        self.int_code.write(args[2], 1 if args[0] < args[1] else 0)
        self.command_pointer += 4

    def equals(self, args):
        self.int_code.write(args[2], 1 if args[0] == args[1] else 0)
        self.command_pointer += 4

    def update_relative_base(self, args):
        self.relative_base += args[0]
        self.command_pointer += 2

    def set_halt(self, args):
        print('HALTING')
        self.halt = True


class HullCanvas:
    def __init__(self):
        self.hull = {(0, 0): 1}

    def get_colour(self, xy):
        if xy in self.hull:
            return self.hull[xy]
        return 0

    def set_colour(self, xy, colour):
        self.hull[xy] = colour


class PaintingRobot:
    def __init__(self):
        self.canvas = HullCanvas()
        self.location = (0, 0)
        self.headings = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.heading_index = 0
        self.computer = IntCodeComputer('input.txt')

    def run(self):
        while True:
            self.computer.run_int_code(self.canvas.get_colour(self.location))
            if self.computer.halt:
                break
            colour_to_paint = self.computer.output[0]
            self.canvas.set_colour(self.location, colour_to_paint)
            should_turn_right = self.computer.output[1]
            self.computer.output = []
            if should_turn_right:
                self.heading_index = (self.heading_index + 1) % 4
            else:
                self.heading_index = (self.heading_index - 1) % 4
            heading = self.headings[self.heading_index]
            self.location = (
                self.location[0] + heading[0],
                self.location[1] + heading[1]
            )


robot = PaintingRobot()
robot.run()

xmin = min(map(lambda loc: loc[0], robot.canvas.hull.keys()))
ymin = min(map(lambda loc: loc[1], robot.canvas.hull.keys()))
xmax = max(map(lambda loc: loc[0], robot.canvas.hull.keys()))
ymax = max(map(lambda loc: loc[1], robot.canvas.hull.keys()))

for y in range(ymin, ymax + 1):
    paint_row = ''
    for x in range(xmin, xmax + 1):
        paint_row += '.' if robot.canvas.get_colour((x, y)) == 0 else '#'
    print(paint_row)

# SOLVED ZLEBKJRA
