import logging
from intcode_test_fixtures import day_5_part_1_input

logging.basicConfig(filename='intcode.log', level=logging.DEBUG)

# <editor-fold desc="Operation definitions">
# Arguments are organized to accept the code, the target index, then any additional arguments
# I might someday want to make the code a custom iterator?
def add(code, input1, input2, target_index):
    code[target_index] = input1 + input2


def mul(code, input1, input2, target_index):
    code[target_index] = input1 * input2


def set_input(code, target_index, input1):
    code[target_index] = input1


def make_output(code, out_value):
    return out_value


def jump_if_true(code, input1, target):
    if input1:
        return target


def jump_if_false(code, input1, target):
    if not input1:
        return target


def less_than(code, input1, input2, target):
    if input1 < input2:
        code[target] = 1
    else:
        code[target] = 0


def equals(code, input1, input2, target):
    if input1 == input2:
        code[target] = 1
    else:
        code[target] = 0


def stop_code(*_):
    raise StopIteration


operator = {
    1: add,
    2: mul,
    3: set_input,  # input operator
    4: make_output,  # output operator
    5: jump_if_true,
    6: jump_if_false,
    7: less_than,
    8: equals,
    99: stop_code,  # end program operator
}

n_args = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 99: 0}
# </editor-fold desc="Operation definitions">


def instruction_reader(inst: int) -> tuple:
    """
    Takes
    :param inst:
    :return:
    """
    if inst == 103:
        raise ValueError("Write operations are never in immediate mode")
    opcode = inst % 100
    modes = [(inst // (10 ** (p + 2))) % 10 for p in range(n_args[opcode])]
    if opcode == 1 or opcode == 2:
        if modes[-1] == 1:
            raise ValueError("Write operations are never in immediate mode")
    return opcode, modes


def get_arg(code, mode, value):
    if mode == 1:
        return value
    elif mode == 0:
        return code[value]
    else:
        raise ValueError("Invalid mode")


def intcode_computer(in_code: dict, inputs=None):
    code = in_code.copy()
    logging.debug(f"Start Code: {code}")
    command_idx = 0
    instruction, modes = instruction_reader(code[command_idx])
    input_idx = 0
    outputs = []
    while instruction != 99:
        # Get arguments
        raw_args = []
        for idx in range(1, 1 + n_args[instruction]):
            raw_args.append(code[idx + command_idx])
        args = [get_arg(code, mode, value) for mode, value in zip(modes, raw_args)]
        if instruction not in (4, 5, 6):
            # target index is the raw argument
            args[-1] = raw_args[-1]
        if instruction == 3:
            try:
                args += [inputs[input_idx]]
                input_idx += 1
            except IndexError as e:
                print(code)
                print(f"command_idx {command_idx}, Instruction: {instruction}, target: {args[-1]}, raw_args: {raw_args}, args: {args}")
                raise e

        logging.debug(
            f"command_idx {command_idx}, Instruction: {instruction}, target: {args[-1]}, raw_args: {raw_args}, args: {args}"
        )
        out = operator[instruction](code, *args)

        if instruction == 4:
            logging.debug("Code Output: {}".format(out))
            outputs.append(out)
            command_idx += 1 + n_args[instruction]
        elif instruction in (5, 6) and out is not None:
            command_idx = out
        else:
            command_idx += 1 + n_args[instruction]

        instruction, modes = instruction_reader(code[command_idx])

    if instruction == 99:
        logging.info("Code Completed with End Code")
        return code, outputs


if __name__ == "__main__":
    code = [3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 1101, 81, 30, 225, 1102, 9, 63, 225, 1001, 92, 45, 224, 101,-83, 224, 224, 4, 224, 102, 8, 223, 223, 101, 2, 224, 224, 1, 224, 223, 223, 1102, 41, 38, 225, 1002, 165, 73, 224, 101,-2920, 224, 224, 4, 224, 102, 8, 223, 223, 101, 4, 224, 224, 1, 223, 224, 223, 1101, 18, 14, 224, 1001, 224,-32, 224, 4, 224, 1002, 223, 8, 223, 101, 3, 224, 224, 1, 224, 223, 223, 1101, 67, 38, 225, 1102, 54, 62, 224, 1001, 224,-3348, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 1, 224, 1, 224, 223, 223, 1, 161, 169, 224, 101,-62, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 1, 224, 224, 1, 223, 224, 223, 2, 14, 18, 224, 1001, 224,-1890, 224, 4, 224, 1002, 223, 8, 223, 101, 3, 224, 224, 1, 223, 224, 223, 1101, 20, 25, 225, 1102, 40, 11, 225, 1102, 42, 58, 225, 101, 76, 217, 224, 101,-153, 224, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 5, 224, 1, 224, 223, 223, 102, 11, 43, 224, 1001, 224,-451, 224, 4, 224, 1002, 223, 8, 223, 101, 6, 224, 224, 1, 223, 224, 223, 1102, 77, 23, 225, 4, 223, 99, 0, 0, 0, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1105, 0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005, 227, 99999, 1005, 0, 256, 1105, 1, 99999, 1106, 227, 99999, 1106, 0, 265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227, 274, 1105, 1, 99999, 1105, 1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101, 294, 0, 0, 105, 1, 0, 1105, 1, 99999, 1106, 0, 300, 1105, 1, 99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105, 1, 99999, 8, 226, 677, 224, 1002, 223, 2, 223, 1006, 224, 329, 1001, 223, 1, 223, 7, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 344, 101, 1, 223, 223, 108, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 359, 101, 1, 223, 223, 1107, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 374, 101, 1, 223, 223, 1008, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 389, 101, 1, 223, 223, 1007, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 404, 1001, 223, 1, 223, 1107, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 419, 1001, 223, 1, 223, 108, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 434, 1001, 223, 1, 223, 7, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 449, 1001, 223, 1, 223, 107, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 464, 101, 1, 223, 223, 107, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 479, 101, 1, 223, 223, 1007, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 494, 1001, 223, 1, 223, 1008, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 509, 101, 1, 223, 223, 7, 677, 226, 224, 1002, 223, 2, 223, 1006, 224, 524, 1001, 223, 1, 223, 1007, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 539, 101, 1, 223, 223, 8, 677, 226, 224, 1002, 223, 2, 223, 1006, 224, 554, 101, 1, 223, 223, 1008, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 569, 101, 1, 223, 223, 1108, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 584, 101, 1, 223, 223, 107, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 599, 1001, 223, 1, 223, 1108, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 614, 1001, 223, 1, 223, 1107, 677, 677, 224, 1002, 223, 2, 223, 1005, 224, 629, 1001, 223, 1, 223, 108, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 644, 101, 1, 223, 223, 8, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 659, 101, 1, 223, 223, 1108, 226, 677, 224, 1002, 223, 2, 223, 1006, 224, 674, 101, 1, 223, 223, 4, 223, 99, 226]
    inputs = [5]
    out_code, outputs = intcode_computer(code, inputs)

