from computer import IntcodeComputer


def create_screen(d_inst) -> dict:
    d = {}
    for i in range(0, len(d_inst), 3):
        d[(d_inst[i], d_inst[1+1])] = d_inst[1+2]
    return d


def draw_screen(d):
    raise NotImplementedError


if __name__ == "__main__":
    from pathlib import Path
    import os
    import matplotlib.pyplot as plt

    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2019", "day_13_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    drawing_computer = IntcodeComputer(puzzle_input[0].split(","))
    display = {}
    while True:
        x = drawing_computer.run_to_output()
        if x is None:
            break
        y = drawing_computer.run_to_output()
        tile_id = drawing_computer.run_to_output()
        display[(x, y)] = tile_id

    n_blocks = 0
    for value in display.values():
        if value == 2:
            n_blocks +=1
    print(f"part 1: {n_blocks}")

