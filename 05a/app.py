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
            command_step_length = self.process_command_at_pointer()
            self.command_pointer += command_step_length

    def process_command_at_pointer(self):
        command = self.int_code[self.command_pointer]
        if command % 10 == 1:
            self.process_add_command(
                command > 100 and command % 1000 > 100,
                command > 1000
            )
            return 4
        elif command % 10 == 2:
            self.process_multiply_command(
                command > 100 and command % 1000 > 100,
                command > 1000
            )
            return 4
        elif command % 10 == 3:
            self.process_input_command()
            return 2
        elif command % 10 == 4:
            self.process_output_command(len(str(command)) == 3 and command > 100)
            return 2
        elif command % 10 == 9:
            self.halt = True
            print("HALT")
            return 0
        else:
            self.halt = True
            print("UNRECOGNISED COMMAND: " + str(command))
            return 0

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

    def process_halt_command(self):
        self.halt = True


computer = IntCodeComputer('input.txt', 1)
computer.run_int_code()
