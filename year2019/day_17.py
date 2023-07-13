from pathlib import Path
import os
from typing import List
import numpy as np

from computer import IntcodeComputer


# 35 = path
# 49 = .
# 10 = newline
def find_intersections(grid_out: List[int]):
    # turn the output list into a grid
    n_cols = grid_out.index(10) + 1
    n_rows = (len(grid_out) - 1) // n_cols
    grid = np.array(grid_out[:-1]).reshape(n_rows, n_cols)

    grid[np.where(grid == 35)] = 1
    grid[np.where(grid == 46)] = 0
    grid = grid[:, :-1]

    # find the intersections of the grid
    mask = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    np.convolve2d(grid, mask)


    # compute the sum of the products of the distances to the top and left edges of the intersections


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "year2019", "day_17_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    computer = IntcodeComputer(puzzle_input[0].split(","))

    outs = computer.run_to_input()

    find_intersections(outs)

    print("".join([chr(i) for i in outs]))
