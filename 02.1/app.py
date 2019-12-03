class IntCodeComputer:
    def __init__(self, file_name):
        file = open(file_name, "r")
        self.int_code = list(map(
            lambda input_string: int(input_string),
            file.read().strip().split(',')
        ))
        self.command_pointer = 0
        self.halt = False

    def run_int_code(self):
        while not self.halt and self.command_pointer < len(self.int_code):
            self.process_command_at_pointer()
            self.command_pointer += 4

    def process_command_at_pointer(self):
        commands = {
            1: self.process_add_command,
            2: self.process_multiply_command,
            99: self.process_halt_command
        }
        commands[self.int_code[self.command_pointer]]()

    def process_add_command(self):
        arg1 = self.int_code[self.int_code[self.command_pointer + 1]]
        arg2 = self.int_code[self.int_code[self.command_pointer + 2]]
        output_pointer = self.int_code[self.command_pointer + 3]
        self.int_code[output_pointer] = arg1 + arg2

    def process_multiply_command(self):
        arg1 = self.int_code[self.int_code[self.command_pointer + 1]]
        arg2 = self.int_code[self.int_code[self.command_pointer + 2]]
        output_pointer = self.int_code[self.command_pointer + 3]
        self.int_code[output_pointer] = arg1 * arg2

    def process_halt_command(self):
        self.halt = True


computer = IntCodeComputer('input.txt')
computer.int_code[1] = 12
computer.int_code[2] = 2
computer.run_int_code()
print(computer.int_code)
