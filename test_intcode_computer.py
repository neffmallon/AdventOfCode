import pytest
from pytest import Pytester

from computer import IntcodeComputer
from intcode_computer import intcode_computer, instruction_reader
from intcode_test_fixtures import test_pairs, day_2_input, day_5_part_1_input
from programs import boost


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


def test_IntcodeComputer(test_pairs):
    for code, result in test_pairs:
        computer = IntcodeComputer(code)
        computer.run_to_halt()
        assert computer.code == {idx: v for idx, v in enumerate(result)}


def test_intcode_computer_day2(day_2_input):
    day_2_input[1] = 12
    day_2_input[2] = 2
    computer = IntcodeComputer(day_2_input)
    computer.run_to_halt()
    assert computer.code[0] == 3716293

    day_2_input[1] = 64
    day_2_input[2] = 29
    computer = IntcodeComputer(day_2_input)
    computer.run_to_halt()
    assert computer.code[0] == 19690720


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


def test_IntcodeComputer_day5(day_5_part_1_input):
    # part 1
    inputs = [1]
    computer = IntcodeComputer(day_5_part_1_input, inputs=inputs)
    computer.run_to_halt()
    for code in computer.outputs[:-1]:
        assert code == 0
    assert computer.outputs[-1] == 5346030

    # part 2
    inputs = [5]
    computer = IntcodeComputer(day_5_part_1_input, inputs=inputs)
    computer.run_to_halt()
    assert computer.outputs == [513116]


def test_IntcodeComputer_pretest_day9():
    code = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    computer = IntcodeComputer(code)
    computer.run_to_halt()
    assert computer.outputs == code

    code = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    computer = IntcodeComputer(code)
    computer.run_to_halt()
    assert computer.outputs[0] == 1219070632396864

    code = [104, 1125899906842624, 99]
    computer = IntcodeComputer(code)
    computer.run_to_halt()
    assert computer.outputs[0] == 1125899906842624

def test_IntcodeComputer_test_day9():
    computer = IntcodeComputer(boost, inputs=[1])
    computer.run_to_halt()
    assert len(computer.outputs) == 1
    assert computer.outputs[0] == 3429606717

    computer = IntcodeComputer(boost, inputs=[2])
    computer.run_to_halt()
    assert len(computer.outputs) == 1
    assert computer.outputs[0] == 33679
