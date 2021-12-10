import numpy as np
from pathlib import Path
import os


def fuel_cost_nonlinear(c, x):
    n = abs(c - x)
    return n * (n + 1) / 2


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2021", "day_07_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    crabs = [int(s) for s in puzzle_input[0].split(",")]

    fuels = [sum([abs(i - c) for c in crabs]) for i in range(300, 350)]
    positions = [i for i in range(300, 350)]
    min_fuel = 400000
    for i in range(100, 500):
        fuel = sum([abs(i - c) for c in crabs])
        if fuel < min_fuel:
            min_fuel = fuel
    print(f"Part 1: {min_fuel}")

    fuels = [sum([fuel_cost_nonlinear(i, c) for c in crabs]) for i in range(100, 600)]
    positions = [i for i in range(100, 600)]
    print(f"Part 2: {min(fuels)}")
