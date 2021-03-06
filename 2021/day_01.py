from pathlib import Path
import os

project_dir = Path(__file__).resolve().parents[1]
file = os.path.join(project_dir, "2021", "day_01_in.txt")
with open(file, "r") as f:
    puzzle_input = [s.strip() for s in f]

numbers = [int(s.strip()) for s in numbers]
# Count the number of increasing steps
print(f"Part 1: {sum([numbers[i+1] > numbers[i] for i in range(len(numbers) - 1)])}")
# Count the number of increasing 3-step windows.
# You can do this by comparing values 3 apart, you don't have to compare the windows
print(f"Part 2: {sum([numbers[i+3] > numbers[i] for i in range(len(numbers) - 3)])}")
