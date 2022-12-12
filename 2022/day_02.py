import os
from pathlib import Path

project_dir = Path(__file__).resolve().parents[1]
file = os.path.join(project_dir, "2022", "day_02_in.txt")
with open(file, "r") as f:
    puzzle_input = [s.strip() for s in f]

score_dict = {
    "A X": 3 + 1,
    "A Y": 6 + 2,
    "A Z": 0 + 3,
    "B X": 0 + 1,
    "B Y": 3 + 2,
    "B Z": 6 + 3,
    "C X": 6 + 1,
    "C Y": 0 + 2,
    "C Z": 3 + 3,

}
score = 0
for round in puzzle_input:
    score += score_dict[round]
print(f"Part 1: {score}")

new_score_dict = {
    "A X": 0 + 3,
    "A Y": 3 + 1,
    "A Z": 6 + 2,
    "B X": 0 + 1,
    "B Y": 3 + 2,
    "B Z": 6 + 3,
    "C X": 0 + 2,
    "C Y": 3 + 3,
    "C Z": 6 + 1,

}
score = 0
for round in puzzle_input:
    score += new_score_dict[round]
print(f"Part 2: {score}")
