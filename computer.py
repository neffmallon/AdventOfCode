from dataclasses import dataclass
import logging

from programs import boost

logging.basicConfig(filename="intcode.log", level=logging.INFO)


class EndOfCodeError(Exception):
    pass


class Code:
    def __init__(self, code):
        if type(code) == list:
            self._code = {idx: v for idx, v in enumerate(code)}
        elif type(code) == dict:
            self._code = code
        else:
            raise ValueError("code argument should either be a list or a dict")

    def __getitem__(self, x: int):
        if not type(x) == int:
            raise KeyError("key must be an integer")
        if x < 0:
            raise KeyError("key cannot be negative.")
        if x not in self._code.keys():
            self._code[x] = 0
        return self._code[x]

    def __setitem__(self, key, value):
        return self._code.__setitem__(key, value)

    def get(self, *args, **kwargs):
        return self._code.get(*args, **kwargs)

    def __len__(self):
        return len(self._code)

    def __str__(self):
        return str(self._code)


class IntcodeComputer:
    def __init__(self, code, inputs=None):
        self.code = Code(code)
        self.operator = {
            1: self.add,
            2: self.mul,
            3: self.set_input,  # input operator
            4: self.make_output,  # output operator
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
            9: self.modify_relative_base,
            99: self.stop_code,  # end program operator
        }
        self.n_args = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1, 99: 0}
        self.pointer = 0  # pointer always starts at the first spot
        if inputs is None:
            inputs = []
        self.inputs = inputs
        self.outputs = []
        self.relative_base = 0
        self.current_opcode = None

    def add_input(self, input_value):
        self.inputs.append(input_value)

    def do_next_instruction(self):
        """Executes the next instruction on the computer."""
        # TODO: Consider refactoring this to use a function to get all the args
        if len(self.code) < 20:
            logging.debug(f"code: {self.code}")

        if self.code[self.pointer] == 99 or self.pointer is None:
            raise EndOfCodeError(
                "The code has stopped, there are no more instructions to do"
            )

        opcode, modes = self.read_instruction(self.code[self.pointer])
        try:
            arg_idx = [
                i for i in range(self.pointer + 1, self.pointer + 1 + self.n_args[opcode])
            ]
        except KeyError as e:
            logging.debug("ouch")
            raise e
        raw_args = [self.code[idx] for idx in arg_idx]
        args = [self.get_arg(opcode, mode, raw_arg, arg_num+1) for mode, raw_arg, arg_num in zip(modes, raw_args, range(len(modes)))]
        # if opcode not in (4, 5, 6):
        #     # target index is the raw argument
        #     args[-1] = raw_args[-1]
        # End of to do section
        logging.debug(
            f"pointer {self.pointer}, Instruction: {opcode}, raw_args: {raw_args}, args: {args}, modes: {modes}"
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

    def get_arg(self, opcode, mode, value, n):
        if opcode not in (4, 5, 6, 9) and n == self.n_args[opcode]:
            if mode == 2:
                return self.relative_base + value
            else:
                return value
        if mode == 1:  # immeidate mode
            return value
        elif mode == 0:  # target mode
            return self.code[value]
        elif mode == 2:  # relative mode
            return self.code[self.relative_base + value]
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
        logging.debug(f"Input check: pointer: {self.pointer}  input: {input1}               raw target: {self.code[self.pointer+1]}")
        logging.debug(f"relative base: {self.relative_base}      target_index: {target_index}  target_index value: {self.code[target_index]}")
        sc = " ".join([str(self.code[i]) for i in range(max(self.pointer-5, 0), self.pointer+7)])
        logging.debug(f"Surrounding code: {sc}")
        self.code[target_index] = input1
        logging.debug(f"New target_index value: {self.code[target_index]}")
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

    def modify_relative_base(self, input1):

        logging.debug(f"Input check: pointer: {self.pointer}  \tinput: {input1}  \traw input: {self.code[self.pointer+1]}")
        arg1 = self.code[self.pointer]
        if str(arg1)[0] == "9":
            target_index = arg1
        elif str(arg1)[0] == "1":
            target_index = self.pointer + 1
        elif str(arg1)[0] == "2":
            target_index = self.relative_base + arg1
        else:
            logging.debug(f"Instruction: {arg1}")
            raise ValueError
        logging.debug(f"relative base: {self.relative_base}   \ttarget_index: {target_index}  \ttarget_index value: {self.code[target_index]}")
        sc = " ".join([str(self.code[i]) for i in range(max(self.pointer-5, 0), self.pointer+7)])
        logging.debug(f"Surrounding code: {sc}\n")
        self.relative_base += input1
        self.pointer += 2

    def stop_code(self):
        self.pointer = None
        raise EndOfCodeError(
            "The code has stopped, there are no more instructions to do"
        )

    # </editor-fold>

if __name__ == "__main__":
    computer = IntcodeComputer(boost, inputs=[2])
    computer.run_to_halt()
    print(computer.outputs)