import numpy as np
from pathlib import Path
import os


def decode_numbers(num_list: list):
    lengths = [len(s) for s in num_list]
    decoded_dict = {
        num_list[lengths.index(2)]: 1,
        num_list[lengths.index(3)]: 7,
        num_list[lengths.index(7)]: 8,
        num_list[lengths.index(4)]: 4,
    }
    encode_dict = {
        1: {c for c in num_list[lengths.index(2)]},
        4: {c for c in num_list[lengths.index(3)]},
        7: {c for c in num_list[lengths.index(4)]},
        8: {c for c in num_list[lengths.index(7)]},
    }
    # do the rest of the logic later
    return decoded_dict


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2021", "day_08_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    output_digits = [s.split(" | ")[1].split(" ") for s in puzzle_input]
    count_1478 = sum(
        [sum([1 for c in s if len(c) in (2, 3, 4, 7)]) for s in output_digits]
    )
    print(f"Part 1: {count_1478}")

    # Part 2: decode the values, then add them all up!
    # 0, 1, and 7 are missing d, 1 and 7 are id'd
    # 1 has 2 lights
    # 2 is the only one missing f
    # 3 is missing b, which is id'd from 2
    # 4 has only 4 lights up
    # 5 and 6 are the only two missing c, 5 has 5, 6 has 5
    # 7 has 3 lights
    # 8 has 7 lights
    # 9 is by process of elimination

    # ID 1, 4, 7, 8
    # ID d, 0
    # ID 6 vs 9 by comparing vs 1
    # ID 3 by comparing vs 1
    # ID 5 vs 2 by comparing to 8-9 or 8-6
