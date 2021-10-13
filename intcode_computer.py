# <editor-fold desc="Operation definitions">
# Arguments are organized to accept the code, the target index, then any additional arguments
# I might someday want to make the code a custom iterator?
def add(code, target_index, input1, input2):
    code[target_index] = input1 + input2


def mul(code, target_index, input1, input2):
    code[target_index] = input1 * input2


def set_input(code, target_index, input1):
    code[target_index] = input1


def make_output(code, target_index):
    return code[target_index]


def stop_code(*_):
    raise StopIteration


operator = {
    1: add,
    2: mul,
    3: set_input,  # input operator
    4: make_output,  # output operator
    99: stop_code,  # end program operator
}

n_args = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    99: 0
}
# </editor-fold desc="Operation definitions">


def instruction_reader(inst: int) -> tuple:
    """
    Takes
    :param inst:
    :return:
    """
    opcode = inst % 100
    modes = [(inst//(10**(p+2))) % 10 for p in range(n_args[opcode])]
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
    command_idx = 0
    max_steps = (len(code) // 2) + 1
    instruction, modes = instruction_reader(code[command_idx])
    input_idx = 0
    while instruction != 99 and max_steps > 0:
        # Get arguments
        raw_args = [code[v] for v in range(command_idx+1, command_idx+n_args[instruction])]
        args = [get_arg(code, mode, value) for mode, value in zip(modes, raw_args)]
        target = code[command_idx+n_args[instruction]]
        if instruction == 3:
            args += [inputs[input_idx]]
            input_idx += 1
        out = operator[instruction](code, target, *args)
        if out:
            print("Code Output: {}".format(out))

        max_steps -= 1
        command_idx += 1 + n_args[instruction]
        instruction, modes = instruction_reader(code[command_idx])

    if instruction == 99:
        # print("Code Completed with End Code")
        return code
    if max_steps <= 0:
        print("Warning! Ran out of steps!")
        return code

if __name__ == "__main__":
    pass