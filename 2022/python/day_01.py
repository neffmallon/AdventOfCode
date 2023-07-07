import os
from pathlib import Path

project_dir = Path(__file__).resolve().parents[1]
file = os.path.join(project_dir, "2022", "../inputs/day_01_in.txt")
with open(file, "r") as f:
    puzzle_input = [s.strip() for s in f]

elves = []
elf = 0
for snack in puzzle_input:
    if snack == '':
        elves.append(elf)
        elf = 0
    else:
        elf += int(snack)
elves.sort()
print(f"Part 1: {elves[-1]}")
print(f"Part 2: {sum(elves[-3:])}")
