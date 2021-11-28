import pytest
from day_10 import AsteroidField
from pathlib import Path
import os


@pytest.fixture
def simple_map():
    # best is 8
    return ".#..#\n.....\n#####\n....#\n...##".split('\n')


@pytest.fixture
def map1():
    # best is 33
    return "......#.#.\n#..#.#....\n..#######.\n.#.#.###..\n.#..#.....\n..#....#.#\n#..#....#.\n.##.#..###\n##...#..#.\n.#....####".split('\n')


@pytest.fixture
def map2():
    # best is 35
    return "#.#...#.#.\n.###....#.\n.#....#...\n##.#.#.#.#\n....#.#.#.\n.##..###.#\n..#...##..\n..##....##\n......#...\n.####.###.".split('\n')


@pytest.fixture
def map3():
    # best is 41
    return ".#..#..###\n####.###.#\n....###.#.\n..###.##.#\n##.##.#.#.\n....###..#\n..#.#..#.#\n#..#.#.###\n.##...##.#\n.....#.#..".split('\n')


@pytest.fixture
def map4():
    # best is 210
    s = ".#..##.###...#######\n##.############..##.\n.#.######.########.#\n.###.#######.####.#.\n#####.##.#.##.###.##\n..#####..#.#########\n####################\n#.####....###.#.#.##\n##.#################\n#####.##.###..####..\n..######..##.#######\n####.##.####...##..#\n.#####..#.######.###\n##...#.##########...\n#.##########.#######\n.####.#.###.###.#.##\n....##.##.###..#####\n.#.#.###########.###\n#.#.#.#####.####.###\n###.##.####.##.#..##"
    return s.split('\n')


@pytest.fixture
def problem_data():
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2019", "day_10_input.txt")
    with open(file, "r") as f:
        map = f.readline().strip()
    return AsteroidField(map)


def test_example_maps(simple_map, map1, map2, map3, map4):
    f = AsteroidField(simple_map)
    assert f.find_best_asteroid_station() == 8
    f = AsteroidField(map1)
    assert f.find_best_asteroid_station() == 33
    f = AsteroidField(map2)
    assert f.find_best_asteroid_station() == 35
    f = AsteroidField(map3)
    assert f.find_best_asteroid_station() == 41
    f = AsteroidField(map4)
    assert f.find_best_asteroid_station() == 210


def test_laser(map4):
    f = AsteroidField(map4)
    zap_order = f.find_zap_order()
    assert f.find_best_asteroid_station() == 210
    assert len(f._calculate_asteroid_distances()) == 210
    assert (12, 11) in f.asteroids
    assert f.station == (13, 11)
    assert zap_order[0] == (11, 12)
    assert zap_order[1] == (12, 1)
    assert zap_order[2] == (12, 2)
    assert zap_order[9] == (12, 8)
    assert zap_order[19] == (16, 0)
    assert zap_order[49] == (16, 9)
    assert zap_order[99] == (10, 16)
    assert zap_order[199] == (8, 2)


