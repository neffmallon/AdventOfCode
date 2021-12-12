import itertools

import numpy as np
from pathlib import Path
import os


def add_one(grid: np.ndarray):
    grid += 1


def flash_and_reset(grid: np.array):
    flashed = set()
    while True:
        tf = np.where(grid > 9)
        to_flash = [(x, y) for x, y in zip(tf[0], tf[1]) if (x, y) not in flashed]
        if len(to_flash) == 0:
            break
        flashed.update({x for x in to_flash})
        for x, y in to_flash:
            for dx, dy in itertools.product([-1, 0, 1], [-1, 0, 1]):
                if 0 <= x + dx < grid.shape[0] and 0 <= y + dy < grid.shape[1]:
                    grid[x + dx, y + dy] += 1
    for x, y in flashed:
        grid[x, y] = 0

    return len(flashed)


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2021", "day_11_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    octopus_grid = np.array([[int(c) for c in line] for line in puzzle_input])

    n_flashed = 0
    for i in range(100):
        add_one(octopus_grid)
        n_flashed += flash_and_reset(octopus_grid)

    print(octopus_grid)
    print(f"Part 1: {n_flashed}")

    # calculate the first time they all flash together
    n_flashed = 0
    while n_flashed < 100:
        i += 1
        add_one(octopus_grid)
        n_flashed = flash_and_reset(octopus_grid)

    print(f"Part 2: round {i+1}")
