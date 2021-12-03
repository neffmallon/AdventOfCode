from pathlib import Path
import os

project_dir = Path(__file__).resolve().parents[1]
file = os.path.join(project_dir, "2021", "day_02_in.txt")
with open(file, "r") as f:
    puzzle_input = [s.strip() for s in f]

depth = 0
x_pos = 0

instructions = [s.split(" ") for s in puzzle_input]

for i in instructions:
    if i[0] == "forward":
        x_pos += int(i[1])
    elif i[0] == "down":
        depth += int(i[1])
    elif i[0] == "up":
        depth -= int(i[1])
print(f"Part 1: {depth*x_pos}")

depth = 0
x_pos = 0
aim = 0

for i in instructions:
    if i[0] == "forward":
        x_pos += int(i[1])
        depth += aim * int(i[1])
    elif i[0] == "down":
        aim += int(i[1])
    elif i[0] == "up":
        aim -= int(i[1])
print(f"Part 2: {depth*x_pos}")

if __name__ == "__main__":
    pass