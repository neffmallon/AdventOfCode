from pathlib import Path
import os
import pandas as pd

# solution goes here

if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2017", "day_02_in.txt")

    data = pd.read_csv(file, sep="\t", header=None)
    print(f"Part 1: {(data.max(axis=1) - data.min(axis=1)).sum()}")

    answer = 0
    for rdx, row in data.iterrows():
        do_row = True
        for idx, v in enumerate(row):
            for i in range(len(row)):
                if idx == i:
                    continue
                if row[i] % v == 0 or v % row[i] == 0:
                    answer += max(row[i]//v, v//row[i])
                    do_row = False
                    break
            if not do_row:
                break

    print(f"Part 2: {answer}")


