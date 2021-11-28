import pytest
from day_08 import SpaceImage
from pathlib import Path
import os


@pytest.fixture
def example_image():
    return SpaceImage(3, 2, "123456789012")


@pytest.fixture()
def problem_image():
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2019", "day_08_input.txt")
    with open(file, "r") as f:
        image_data = f.readline().strip()
    return SpaceImage(25, 6, image_data)


def test_simple_example(example_image):
    assert example_image.image_check() == 1


def test_problem(problem_image):
    assert problem_image.image_check() == 1690


if __name__ == "__main__":
    pass
