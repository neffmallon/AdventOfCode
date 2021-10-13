import pytest
from pytest import Pytester
from intcode_computer import intcode_computer
from intcode_test_fixtures import test_pairs, day_2_part_1_input


def test_intcode_computer_simple(test_pairs):
    for code, result in test_pairs:
        assert intcode_computer(code) == result

#currently failing with latest change
def test_intcode_computer_day2(day_2_part_1_input):
    assert intcode_computer(day_2_part_1_input)[0] == 3716293
    # day_2_part_1_input[1] = 64
    # day_2_part_1_input[2] = 29
    # assert intcode_computer(day_2_part_1_input)[0][0] == 19690720

