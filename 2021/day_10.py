import numpy as np
from pathlib import Path
import os

open_sides = {"{", "[", "(", "<"}
close_dict = {"}": "{", "]": "[", ")": "(", ">": "<"}

point_value = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def syntax_checker(line):
    opened_list = []
    for p in line:
        if p in close_dict.values():
            opened_list.append(p)
        if p in close_dict.keys():
            if close_dict[p] == opened_list.pop(-1):
                continue
            else:
                return point_value[p]
    return 0


ac_points = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}


def autocomplete(line):
    opened_list = []
    for p in line:
        if p in close_dict.values():
            opened_list.append(p)
        if p in close_dict.keys():
            if close_dict[p] == opened_list.pop(-1):
                continue
            else:
                return 0
    total_score = 0
    for b in opened_list[::-1]:
        total_score *= 5
        total_score += ac_points[b]
    return total_score


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2021", "day_10_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    print(f"Part 1: {sum([syntax_checker(l) for l in puzzle_input])}")

    # part 2
    autocomplete_scores = [autocomplete(l) for l in puzzle_input]
    autocomplete_scores = [s for s in autocomplete_scores if s > 0]
    autocomplete_scores.sort()
    print(f"Part 2: {autocomplete_scores[len(autocomplete_scores)//2]}")
