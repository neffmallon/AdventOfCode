import pytest
from day_06 import map_maker, count_orbits, orbit_transfer_distance


@pytest.fixture
def example_map():
    s = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L"
    return s.split("\n")


@pytest.fixture
def santa_map():
    s = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN"
    return s.split("\n")


def test_count_orbits(example_map):
    orbit_tree = map_maker(example_map)
    assert count_orbits(orbit_tree) == 42


def test_count_orbits_backwards(example_map):
    orbit_tree = map_maker(example_map[::-1])
    assert count_orbits(orbit_tree) == 42


def test_orbit_transfer_distance_backwards(santa_map):
    orbit_tree = map_maker(santa_map[::-1])
    assert orbit_transfer_distance(orbit_tree) == 4


if __name__ == "__main__":
    pass
