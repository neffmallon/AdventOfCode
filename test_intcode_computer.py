import pytest
from pytest import Pytester
from intcode_computer import intcode_computer, instruction_reader
from intcode_test_fixtures import test_pairs, day_2_input, day_5_part_1_input


def test_instruction_reader():
    assert instruction_reader(1) == (1, [0, 0, 0])
    assert instruction_reader(2) == (2, [0, 0, 0])

    assert instruction_reader(101) == (1, [1, 0, 0])
    assert instruction_reader(1101) == (1, [1, 1, 0])
    assert instruction_reader(1001) == (1, [0, 1, 0])

    assert instruction_reader(102) == (2, [1, 0, 0])
    assert instruction_reader(1102) == (2, [1, 1, 0])
    assert instruction_reader(1002) == (2, [0, 1, 0])

    assert instruction_reader(3) == (3, [0])

    assert instruction_reader(4) == (4, [0])
    assert instruction_reader(104) == (4, [1])


def test_intcode_computer_simple(test_pairs):
    for code, result in test_pairs:
        assert intcode_computer(code)[0] == result


def test_intcode_computer_day2(day_2_input):
    day_2_input[1] = 12
    day_2_input[2] = 2
    assert intcode_computer(day_2_input)[0][0] == 3716293
    day_2_input[1] = 64
    day_2_input[2] = 29
    assert intcode_computer(day_2_input)[0][0] == 19690720


def test_intcode_computer_day5(day_5_part_1_input):
    # part 1
    inputs = [1]
    out_code, outputs = intcode_computer(day_5_part_1_input, inputs)
    for code in outputs[:-1]:
        assert code == 0
    assert outputs[-1] == 5346030

    # part 2
    inputs = [5]
    out_code, outputs = intcode_computer(day_5_part_1_input, inputs)
    assert outputs == [513116]
