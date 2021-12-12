from pathlib import Path
import os

# solution goes here

if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2017", "day_05_in.txt")
    with open(file, "r") as f:
        puzzle_input = [int(s.strip()) for s in f]

    n_steps = 0
    new_idx = 0
    while 0 <= new_idx < len(puzzle_input):
        n_steps += 1
        current_idx = new_idx
        new_idx += puzzle_input[current_idx]
        puzzle_input[current_idx] += 1

    print(f"Part 1: {n_steps}")

    with open(file, "r") as f:
        puzzle_input = [int(s.strip()) for s in f]

    n_steps = 0
    new_idx = 0
    while 0 <= new_idx < len(puzzle_input):
        n_steps += 1
        current_idx = new_idx
        new_idx += puzzle_input[current_idx]
        if puzzle_input[current_idx] >= 3:
            puzzle_input[current_idx] -= 1
        else:
            puzzle_input[current_idx] += 1

    print(f"Part 2: {n_steps}")
