import os
from pathlib import Path

project_dir = Path(__file__).resolve().parents[1]
file = os.path.join(project_dir, "2022", "../inputs/day_03_in.txt")
with open(file, "r") as f:
    puzzle_input = [s.strip() for s in f]

def priority(c: str):
    if c.isupper():
        return ord(c) - ord('A') + 27
    else:
        return ord(c) - ord('a') + 1

def process_sack(rucksack:str):
    t = 0
    pocket_a = set(rucksack[:len(rucksack)//2])
    pocket_b = set(rucksack[len(rucksack)//2:])
    for item in pocket_a.intersection(pocket_b):
        t += priority(item)
    return t

total = 0
for rucksack in puzzle_input:
    total += process_sack(rucksack)

print(f"Part 1: {total}")

def process_team(sack1:str, sack2:str, sack3:str):
    for item in set(sack1).intersection(set(sack2)).intersection(set(sack3)):
        return priority(item)

team_priorities = 0
for team_idx in range(len(puzzle_input)//3):
    sack_idx = team_idx * 3
    team_priorities += process_team(
        puzzle_input[sack_idx],
        puzzle_input[sack_idx+1],
        puzzle_input[sack_idx+2],
    )

print(f"Part 2: {team_priorities}")