import os
from pathlib import Path

import numpy as np

BASE_PATTERN = [0, 1, 0, -1]


def get_pattern_for_position(input: np.ndarray, position: int):
    pattern = np.zeros(input.shape)
    idx = 0
    pattern_idx = 0
    while idx < len(pattern):
        if idx == 0:
            pattern_idx = 1
            idx = position - 1
        for _ in range(position):
            pattern[idx] = BASE_PATTERN[pattern_idx % len(BASE_PATTERN)]
            idx += 1
            if idx == len(pattern):
                return pattern
        pattern_idx += 1
    return pattern


def process_phase(s: str):
    input = np.array([int(c) for c in s])
    output = []
    for i in range(len(input)):
        p = get_pattern_for_position(input, i + 1)
        n = np.abs(np.dot(p, input))
        output.append(str(int(n % 10)))
    return "".join(output)


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "year2019", "day_16_in.txt")
    with open(file, "r") as f:
        m = [s.strip("\n") for s in f]
    input = m[0]
    for _ in range(100):
        input = process_phase(input)

    print(input)
