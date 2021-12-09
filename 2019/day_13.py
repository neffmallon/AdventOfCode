from computer import IntcodeComputer
import numpy as np


def create_screen(d_inst: list) -> dict:
    d = {}
    for i in range(0, len(d_inst), 3):
        d[(d_inst[i], d_inst[1 + 1])] = d_inst[1 + 2]
    return d


def draw_screen(d):
    x_range = [0, 0]
    y_range = [0, 1]

    for key in d.keys():
        if key[0] > x_range[1]:
            x_range[1] = key[0]

        if key[1] > y_range[1]:
            y_range[1] = key[1]

    x = np.linspace(x_range[0], x_range[1], num=1 + x_range[1] - x_range[0])
    y = np.linspace(y_range[0], y_range[1], num=1 + y_range[1] - y_range[0])
    paint_job = np.zeros((1 + x_range[1] - x_range[0], 1 + y_range[1] - y_range[0]))

    for i, xi in enumerate(x):
        for j, yi in enumerate(y):
            paint_job[i, j] = d[(xi, yi)]
    return paint_job.T[::-1, :]


if __name__ == "__main__":
    from pathlib import Path
    import os
    import matplotlib.pyplot as plt

    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2019", "day_13_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    drawing_computer = IntcodeComputer(puzzle_input[0].split(","))
    display = {}
    while True:
        x = drawing_computer.run_to_output()
        if x is None:
            break
        y = drawing_computer.run_to_output()
        tile_id = drawing_computer.run_to_output()
        display[(x, y)] = tile_id

    n_blocks = 0
    for value in display.values():
        if value == 2:
            n_blocks += 1
    print(f"Day 13 part 1: {n_blocks}")
