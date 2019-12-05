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
        command = self.int_code[self.command_pointer]
        if command % 10 == 1:
            self.process_add_command(
                command > 100 and command % 1000 > 100,
                command > 1000
            )
            self.command_pointer += 4
        elif command % 10 == 2:
            self.process_multiply_command(
                command > 100 and command % 1000 > 100,
                command > 1000
            )
            self.command_pointer += 4
        elif command % 10 == 3:
            self.process_input_command()
            self.command_pointer += 2
        elif command % 10 == 4:
            self.process_output_command(len(str(command)) == 3 and command > 100)
            self.command_pointer += 2
        elif command % 10 == 5:
            self.process_jump_if_true(
                command > 100 and command % 1000 > 100,
                command > 1000
            )
        elif command % 10 == 6:
            self.process_jump_if_false(
                command > 100 and command % 1000 > 100,
                command > 1000
            )
        elif command % 10 == 7:
            self.process_less_than(
                command > 100 and command % 1000 > 100,
                command > 1000
            )
        elif command % 10 == 8:
            self.process_equals(
                command > 100 and command % 1000 > 100,
                command > 1000
            )
        elif command % 10 == 9:
            self.halt = True
            print("HALT")
        else:
            self.halt = True
            print("UNRECOGNISED COMMAND: " + str(command))

    def process_add_command(self, is_arg1_immediate, is_arg2_immediate):
        arg1 = self.int_code[self.command_pointer + 1] if is_arg1_immediate else self.int_code[self.int_code[self.command_pointer + 1]]
        arg2 = self.int_code[self.command_pointer + 2] if is_arg2_immediate else self.int_code[self.int_code[self.command_pointer + 2]]
        output_pointer = self.int_code[self.command_pointer + 3]
        self.int_code[output_pointer] = arg1 + arg2

    def process_multiply_command(self, is_arg1_immediate, is_arg2_immediate):
        arg1 = self.int_code[self.command_pointer + 1] if is_arg1_immediate else self.int_code[self.int_code[self.command_pointer + 1]]
        arg2 = self.int_code[self.command_pointer + 2] if is_arg2_immediate else self.int_code[self.int_code[self.command_pointer + 2]]
        output_pointer = self.int_code[self.command_pointer + 3]
        self.int_code[output_pointer] = arg1 * arg2

    def process_input_command(self):
        # Opcode 3 takes a single integer as input and saves it to the
        # position given by its only parameter. For example, the
        # instruction 3,50 would take an input value and store it at
        # address 50.
        output_pointer = self.int_code[self.command_pointer + 1]
        self.int_code[output_pointer] = self.input

    def process_output_command(self, is_immediate_mode):
        # Opcode 4 outputs the value of its only parameter. For
        # example, the instruction 4,50 would output the value at
        # address 50.
        if is_immediate_mode:
            print(self.int_code[self.command_pointer + 1])
        else:
            print(self.int_code[self.int_code[self.command_pointer + 1]])

    def process_jump_if_true(self, is_arg1_immediate, is_arg2_immediate):
        arg1 = self.int_code[self.command_pointer + 1]
        arg1_value = arg1 if is_arg1_immediate else self.int_code[arg1]
        arg2 = self.int_code[self.command_pointer + 2]
        arg2_value = arg2 if is_arg2_immediate else self.int_code[arg2]
        if not arg1_value == 0:
            self.command_pointer = arg2_value
        else:
            self.command_pointer += 3

    def process_jump_if_false(self, is_arg1_immediate, is_arg2_immediate):
        arg1 = self.int_code[self.command_pointer + 1]
        arg1_value = arg1 if is_arg1_immediate else self.int_code[arg1]
        arg2 = self.int_code[self.command_pointer + 2]
        arg2_value = arg2 if is_arg2_immediate else self.int_code[arg2]
        if arg1_value == 0:
            self.command_pointer = arg2_value
        else:
            self.command_pointer += 3

    def process_less_than(self, is_arg1_immediate, is_arg2_immediate):
        arg1 = self.int_code[self.command_pointer + 1]
        arg1_value = arg1 if is_arg1_immediate else self.int_code[arg1]
        arg2 = self.int_code[self.command_pointer + 2]
        arg2_value = arg2 if is_arg2_immediate else self.int_code[arg2]
        output_location = self.int_code[self.command_pointer + 3]
        self.int_code[output_location] = 1 if arg1_value < arg2_value else 0
        self.command_pointer += 4

    def process_equals(self, is_arg1_immediate, is_arg2_immediate):
        arg1 = self.int_code[self.command_pointer + 1]
        arg1_value = arg1 if is_arg1_immediate else self.int_code[arg1]
        arg2 = self.int_code[self.command_pointer + 2]
        arg2_value = arg2 if is_arg2_immediate else self.int_code[arg2]
        output_location = self.int_code[self.command_pointer + 3]
        self.int_code[output_location] = 1 if arg1_value == arg2_value else 0
        self.command_pointer += 4

    def process_halt_command(self):
        self.halt = True


computer = IntCodeComputer('input.txt', 5)
computer.run_int_code()
