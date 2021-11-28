import pytest
from day_03 import wire_cross_finder, wire_cross_finder_wire_distance


@pytest.fixture()
def easy_test():
    """answer is 6"""
    return "R8,U5,L5,D3\nU7,R6,D4,L4", 6


@pytest.fixture()
def med_test():
    """answer is 159"""
    return "R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83", 159


@pytest.fixture()
def hard_test():
    """answer is 135"""
    return (
        "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
        135,
    )


def test_easy_wire_cross_finder(easy_test):
    assert wire_cross_finder(easy_test[0].split("\n")) == easy_test[1]


def test_med_wire_cross_finder(med_test):
    assert wire_cross_finder(med_test[0].split("\n")) == med_test[1]


def test_hard_wire_cross_finder(hard_test):
    assert wire_cross_finder(hard_test[0].split("\n")) == hard_test[1]


def test_easy_wire_cross_finder_wire_distance(easy_test):
    assert wire_cross_finder_wire_distance(easy_test[0].split("\n")) == 30


def test_med_wire_cross_finder_wire_distance(med_test):
    assert wire_cross_finder_wire_distance(med_test[0].split("\n")) == 610


def test_hard_wire_cross_finder_wire_distance(hard_test):
    assert wire_cross_finder_wire_distance(hard_test[0].split("\n")) == 410


if __name__ == "__main__":
    pass
