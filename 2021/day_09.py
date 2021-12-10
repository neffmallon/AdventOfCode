import numpy as np
from pathlib import Path
import os


def check_neighbors(grid, basin_set: set, r, c):
    max_row = grid.shape[0] - 1
    max_col = grid.shape[1] - 1
    to_check = []
    if r > 0:
        to_check.append((r - 1, c))
    if r < max_row:
        to_check.append((r + 1, c))
    if c > 0:
        to_check.append((r, c - 1))
    if c < max_col:
        to_check.append((r, c + 1))

    for site in to_check:
        if site not in basin_set and grid[site[0], site[1]] != 9:
            basin_set.add(site)
            check_neighbors(grid, basin_set, site[0], site[1])


def find_basin_size(grid, x, y):
    basin_set = {(x, y)}
    check_neighbors(grid, basin_set, x, y)
    return len(basin_set)


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2021", "day_09_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    grid_array = np.array([[int(c) for c in line] for line in puzzle_input])
    max_row = grid_array.shape[0] - 1
    max_col = grid_array.shape[1] - 1
    # print(grid_array)
    total_risk = 0

    basin_sizes = []
    for r in range(grid_array.shape[0]):
        for c in range(grid_array.shape[1]):
            v = grid_array[r, c]
            if r > 0:
                if v >= grid_array[r - 1, c]:
                    continue
            if r < max_row:
                if v >= grid_array[r + 1, c]:
                    continue
            if c > 0:
                if v >= grid_array[r, c - 1]:
                    continue
            if c < max_col:
                if v >= grid_array[r, c + 1]:
                    continue
            total_risk += 1 + v
            # print(f"row {r}\tcol {c}\tvalue {v}")
            basin_sizes.append(find_basin_size(grid_array, r, c))
    print(f"Part 1: {total_risk}")

    basin_sizes.sort()
    product = 1
    for p in basin_sizes[-3:]:
        product *= p
    print(f"Part 2: {product}")
