from dataclasses import dataclass
import logging


@dataclass(frozen=True)
class Operator:
    call: callable
    n_args: int
    writes: bool = True
    is_input: bool = False
    is_output: bool = False
    is_end: bool = False
    pointer_change: bool = False


class EndOfCodeError(Exception):
    pass


class IntcodeComputer:
    def __init__(self, code, inputs=None):
        if type(code) == list:
            self.code = {idx: v for idx, v in enumerate(code)}
        elif type(code) == dict:
            self.code = code
        else:
            raise ValueError("Code should either be a list or a dict")
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
        self.n_args = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 99: 0}
        self.pointer = 0  # pointer always starts at the first spot
        self.inputs = inputs
        self.outputs = []

    def add_input(self, input_value):
        self.inputs.append(input_value)

    def do_next_instruction(self):
        """Executes the next instruction on the computer."""
        # TODO: Consider refactoring this to use a function to get all the args
        if self.code[self.pointer] == 99 or self.pointer is None:
            raise EndOfCodeError(
                "The code has stopped, there are no more instructions to do"
            )

        opcode, modes = self.read_instruction(self.code[self.pointer])
        raw_args = [
            self.code[idx]
            for idx in range(self.pointer + 1, self.pointer + 1 + self.n_args[opcode])
        ]
        args = [self.get_arg(mode, raw_arg) for mode, raw_arg in zip(modes, raw_args)]
        if opcode not in (4, 5, 6):
            # target index is the raw argument
            args[-1] = raw_args[-1]
        # End of to do section
        logging.debug(
            f"pointer {self.pointer}, Instruction: {opcode}, target: {args[-1]}, raw_args: {raw_args}, args: {args}"
        )
        out = self.operator[opcode](*args)
        if out is not None:
            try:
                assert opcode == 4
            except AssertionError:
                raise RuntimeError(
                    "Operation other than make_output attempted to return a value"
                )
            return out

    def get_arg(self, mode, value):
        if mode == 1:
            return value
        elif mode == 0:
            return self.code[value]
        else:
            raise ValueError("Invalid mode")

    def peak_next_opcode(self):
        """Gets the opcode of the next operation."""
        if self.pointer is None:
            return None
        return self.read_instruction(self.code[self.pointer])[0]

    def read_instruction(self, inst: int) -> tuple:
        """
        Interprets an instruction, returning the opcode and modes
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

    def run_to_halt(self):
        """Runs the computer until it halts."""
        while self.peak_next_opcode() != 99:
            out = self.do_next_instruction()
            if out is not None:
                self.outputs.append(out)

    def run_to_output(self):
        """Runs the computer until it produces output or halts."""
        out = None
        while self.peak_next_opcode() != 99 and out is None:
            out = self.do_next_instruction()
            if out is not None:
                self.outputs.append(out)
        return out

    # <editor-fold desc="operators">
    # Operators must:
    # 1) Collect external input if necessary
    # 2) Modify the code as required
    # 3) Set the new pointer as required
    # 4) Return output if necessary
    def add(self, input1, input2, target_index):
        """Adds the first and second argument and stores the answer in the target index"""
        self.code[target_index] = input1 + input2
        self.pointer += 4

    def mul(self, input1, input2, target_index):
        self.code[target_index] = input1 * input2
        self.pointer += 4

    def set_input(self, target_index):
        input1 = self.inputs.pop(0)
        self.code[target_index] = input1
        self.pointer += 2

    def make_output(self, out_value):
        self.pointer += 2
        return out_value

    def jump_if_true(self, input1, target):
        if input1:
            self.pointer = target
        else:
            self.pointer += 3

    def jump_if_false(self, input1, target):
        if not input1:
            self.pointer = target
        else:
            self.pointer += 3

    def less_than(self, input1, input2, target):
        if input1 < input2:
            self.code[target] = 1
        else:
            self.code[target] = 0
        self.pointer += 4

    def equals(self, input1, input2, target):
        if input1 == input2:
            self.code[target] = 1
        else:
            self.code[target] = 0
        self.pointer += 4

    def stop_code(self):
        self.pointer = None
        raise EndOfCodeError(
            "The code has stopped, there are no more instructions to do"
        )

    # </editor-fold>
