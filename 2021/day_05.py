from pathlib import Path
import os
import numpy as np
import pandas as pd


def get_line_input(s):
    xyxy = s.strip().split(" -> ")
    return [[int(i) for i in xy.split(",")] for xy in xyxy]


def color_hv_line(line, grid):
    xy1, xy2 = line
    if xy1[0] == xy2[0] or xy1[1] == xy2[1]:
        x_start = min(xy1[0], xy2[0])
        x_end = max(xy1[0], xy2[0])
        y_start = min(xy1[1], xy2[1])
        y_end = max(xy1[1], xy2[1])
        grid[y_start : y_end + 1, x_start : x_end + 1] += 1
    elif abs(xy1[0] - xy2[0]) == abs(xy1[1] - xy2[1]):
        x = np.linspace(xy1[1], xy2[1], abs(xy1[1] - xy2[1]) + 1)
        y = np.linspace(xy1[0], xy2[0], abs(xy1[0] - xy2[0]) + 1)
        for xi, yi in zip(x, y):
            grid[int(xi), int(yi)] += 1
    else:
        print(line)


project_dir = Path(__file__).resolve().parents[1]
file = os.path.join(project_dir, "2021", "day_05_in.txt")
with open(file, "r") as f:
    puzzle_input = np.array([get_line_input(s) for s in f])

ocean_grid = np.zeros((puzzle_input.max() + 1, puzzle_input.max() + 1))

for line in puzzle_input:
    color_hv_line(line, ocean_grid)

print(np.where(ocean_grid >= 2)[0].shape[0])
print(ocean_grid)

if __name__ == "__main__":
    pass
