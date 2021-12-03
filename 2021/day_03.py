from pathlib import Path
import os
import numpy as np
import pandas as pd

project_dir = Path(__file__).resolve().parents[1]
file = os.path.join(project_dir, "2021", "day_03_in.txt")
with open(file, "r") as f:
    puzzle_input = [s.strip() for s in f]

puzzle_input = [[int(c) for c in n] for n in puzzle_input]
puzzle_df = pd.DataFrame(puzzle_input)
# gamma rate: most common bit in each column
# epsilon is the least common bit
# multiply the two together


gamma = [puzzle_df[c].value_counts().index[0] for c in puzzle_df.columns]
gamma = sum([np.round(v) * (2 ** i) for i, v in enumerate(gamma[::-1])])

epsilon = [puzzle_df[c].value_counts().index[1] for c in puzzle_df.columns]
epsilon = sum([np.round(v) * (2 ** i) for i, v in enumerate(epsilon[::-1])])
print(f"Part 1: {gamma * epsilon}")
# 111100100011 # 3875
# 000011011100 # 220

# part 2
# oxygen

ox_df = pd.DataFrame(puzzle_input)
for c in ox_df.columns:
    vc = ox_df[c].value_counts()
    if ox_df.shape[0] == 1:
        break
    if vc[0] == vc[1]:
        ox_df = ox_df[ox_df[c] == 1]
    else:
        ox_df = ox_df[ox_df[c] == ox_df[c].value_counts().index[0]]
# print(ox_df)

co2_df = pd.DataFrame(puzzle_input)
for c in co2_df.columns:
    vc = co2_df[c].value_counts()
    if co2_df.shape[0] == 1:
        break
    elif vc[0] == vc[1]:
        co2_df = co2_df[co2_df[c] == 0]
    else:
        co2_df = co2_df[co2_df[c] == co2_df[c].value_counts().index[1]]
# print(co2_df)
answer = sum([v * (2 ** i) for i, v in enumerate(ox_df.values[0][::-1])]) * sum(
    [v * (2 ** i) for i, v in enumerate(co2_df.values[0][::-1])]
)
print(f"Part 2:{answer}")
# 1007985
if __name__ == "__main__":
    pass
