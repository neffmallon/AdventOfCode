import logging

input = [
    1,
    0,
    0,
    3,
    1,
    1,
    2,
    3,
    1,
    3,
    4,
    3,
    1,
    5,
    0,
    3,
    2,
    10,
    1,
    19,
    2,
    19,
    6,
    23,
    2,
    13,
    23,
    27,
    1,
    9,
    27,
    31,
    2,
    31,
    9,
    35,
    1,
    6,
    35,
    39,
    2,
    10,
    39,
    43,
    1,
    5,
    43,
    47,
    1,
    5,
    47,
    51,
    2,
    51,
    6,
    55,
    2,
    10,
    55,
    59,
    1,
    59,
    9,
    63,
    2,
    13,
    63,
    67,
    1,
    10,
    67,
    71,
    1,
    71,
    5,
    75,
    1,
    75,
    6,
    79,
    1,
    10,
    79,
    83,
    1,
    5,
    83,
    87,
    1,
    5,
    87,
    91,
    2,
    91,
    6,
    95,
    2,
    6,
    95,
    99,
    2,
    10,
    99,
    103,
    1,
    103,
    5,
    107,
    1,
    2,
    107,
    111,
    1,
    6,
    111,
    0,
    99,
    2,
    14,
    0,
    0,
]


def opcode_reader(code: list):
    out_code = code.copy()
    command_idx = 0
    max_steps = (len(out_code) // 4) + 1
    while out_code[command_idx] != 99 and max_steps > 0:
        if out_code[command_idx] == 1:
            logging.debug(
                f"command_idx {command_idx}, Instruction: 1, target: {out_code[command_idx + 3]}, args: {[out_code[out_code[command_idx + 1]], out_code[out_code[command_idx + 2]]]}"
            )
            out_code[out_code[command_idx + 3]] = (
                out_code[out_code[command_idx + 1]]
                + out_code[out_code[command_idx + 2]]
            )
        elif out_code[command_idx] == 2:
            logging.debug(
                f"command_idx {command_idx}, Instruction: 2, target: {out_code[command_idx + 3]}, args: {[out_code[out_code[command_idx + 1]], out_code[out_code[command_idx + 2]]]}"
            )
            out_code[out_code[command_idx + 3]] = (
                out_code[out_code[command_idx + 1]]
                * out_code[out_code[command_idx + 2]]
            )
        else:
            raise ValueError("That code is not valid")
        max_steps -= 1
        command_idx += 4

    if out_code[command_idx] == 99:
        logging.info("Code Completed with End Code")
        return out_code
    if max_steps <= 0:
        logging.error("Warning! Ran out of steps!")
        return out_code


def test_opcode_reader():
    assert opcode_reader([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]) == \
           [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    assert opcode_reader([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99]
    assert opcode_reader([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
    assert opcode_reader([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801]
    assert opcode_reader([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99]


def solution_searcher(code: list) -> list:
    for noun in range(100):
        for verb in range(100):
            run_code = code.copy()
            run_code[1] = noun
            run_code[2] = verb
            if opcode_reader(run_code)[0] == 19690720:
                print(noun, verb)
                return 100 * noun + verb
    raise RuntimeError("No solution found")
