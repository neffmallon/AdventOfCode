from copy import copy
from pathlib import Path
import os


def one_day(f_c: dict):
    new_fc = {i: 0 for i in range(9)}
    for k, v in f_c.items():
        if k == 0:
            new_fc[8] = v
            new_fc[6] += v
        elif k == 7:
            new_fc[6] += v
        else:
            new_fc[k - 1] = v
    f_c = new_fc
    return f_c


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2021", "day_06_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    fishes = puzzle_input[0].split(",")

    fish_counts = {i: 0 for i in range(9)}
    for i in fishes:
        fish_counts[int(i)] += 1

    for _ in range(256):
        fish_counts = one_day(fish_counts)
        # day 80: 363101
        # day 256: 1644286074024

    print(f"{sum([v for v in fish_counts.values()])}")
