from dataclasses import dataclass

@dataclass(frozen=True)
class Operator:
    signiture: int
    n_args: int
    call: callable
    writes: bool = True
    is_input: bool = False
    is_output: bool = False
    is_end: bool = False
    pointer_change: bool = False

class IntcodeComputer:

    def __init__(self, code):
        self.code = code.copy()
        self.operator = {
            1: self.add,
            2: self.mul,
            3: self.set_input,  # input operator
            4: self.make_output,  # output operator
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
            99: self.stop_code,  # end program operator
        }
        self.n_args = {1: 3,
                       2: 3,
                       3: 1,
                       4: 1,
                       5: 2,
                       6: 2,
                       7: 3,
                       8: 3,
                       99: 0
                       }
        self.pointer = 0  # pointer always starts at the first spot

    def instruction_reader(self, inst: int) -> tuple:
        """
        Takes
        :param inst:
        :return:
        """
        if inst == 103:
            raise ValueError("Write operations are never in immediate mode")
        opcode = inst % 100
        modes = [(inst // (10 ** (p + 2))) % 10 for p in range(self.n_args[opcode])]
        if opcode == 1 or opcode == 2:
            if modes[-1] == 1:
                raise ValueError("Write operations are never in immediate mode")
        return opcode, modes

    def get_arg(self, mode, value):
        if mode == 1:
            return value
        elif mode == 0:
            return self.code[value]
        else:
            raise ValueError("Invalid mode")

    def add(self, input1, input2, target_index):
        self.code[target_index] = input1 + input2

    def mul(self, input1, input2, target_index):
        self.code[target_index] = input1 * input2

    def set_input(self, target_index, input1):
        self.code[target_index] = input1

    def make_output(self, out_value):
        return out_value

    def jump_if_true(self, input1, target):
        if input1:
            return target

    def jump_if_false(self, input1, target):
        if not input1:
            return target

    def less_than(self, input1, input2, target):
        if input1 < input2:
            self.code[target] = 1
        else:
            self.code[target] = 0

    def equals(self, input1, input2, target):
        if input1 == input2:
            self.code[target] = 1
        else:
            self.code[target] = 0

    def stop_code(*_):
        raise StopIteration



    n_args = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 99: 0}

