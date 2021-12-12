from pathlib import Path
import os

if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2017", "day_01_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    answer = 0
    pi = puzzle_input[0]
    lookup = pi + pi
    for idx, c in enumerate(pi):
        if c == lookup[idx+1]:
            answer += int(c)

    print(f"Part 1: {answer}")

    answer = 0
    n_steps = len(pi)//2
    lookup = pi + pi
    for idx, c in enumerate(pi):
        if c == lookup[idx+n_steps]:
            answer += int(c)

    print(f"Part 2: {answer}")

