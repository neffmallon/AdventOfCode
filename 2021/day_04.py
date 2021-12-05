from pathlib import Path
import os
import numpy as np
import pandas as pd

project_dir = Path(__file__).resolve().parents[1]
file = os.path.join(project_dir, "2021", "day_04_in.txt")
with open(file, "r") as f:
    puzzle_input = [s.strip() for s in f]

bingo_balls = puzzle_input[0].split(",")

def extract_board(string_list):
    board = [[]]*5
    for idx, s in enumerate(string_list):
        board[idx] = [c for c in s.split(" ") if c]
    return np.array(board)


def extract_board_from_index(idx):
    return extract_board(puzzle_input[2+6*idx:7+6*idx])


def get_numbers_to_win(board):
    bingo = False
    n_index = -1
    counts = {f"r{d}":[] for d in range(5)}
    counts.update({f"c{d}":[] for d in range(5)})
    counts.update({f"d{d}":[] for d in range(2)})
    while not bingo:
        n_index += 1
        n = bingo_balls[n_index]
        if n in board:
            r, c = np.where(board == n)
            counts[f"r{r[0]}"] += [n]
            counts[f"c{c[0]}"] += [n]
        if max([len(v) for v in counts.values()]) == 5:
            bingo = True
    return n_index


def get_score(board: np.ndarray):
    b = board.flatten()
    n  = get_numbers_to_win(board)
    s = sum([int(n) for n in board if n not in bingo_balls[: n + 1]])
    return s*int(bingo_balls[n])

board_marks_to_win = []
for idx in range(100):
    # for pointer in range(2, 20, 6):
    bb = extract_board_from_index(idx)
    board_marks_to_win.append(get_numbers_to_win(bb))

print(bingo_balls[min(board_marks_to_win)])

winning_board = board_marks_to_win.index(min(board_marks_to_win))

board = extract_board(puzzle_input[2+6*winning_board:7+6*winning_board]).flatten()

s = sum([int(n) for n in board if n not in bingo_balls[:min(board_marks_to_win)+1]])
print("part 1 ", s*int(bingo_balls[min(board_marks_to_win)]))

print(bingo_balls[max(board_marks_to_win)])
losing_board = board_marks_to_win.index(max(board_marks_to_win))
board = extract_board(puzzle_input[2+6*losing_board:7+6*losing_board]).flatten()
s = sum([int(n) for n in board if n not in bingo_balls[:max(board_marks_to_win)+1]])
print("part 2 ", s*int(bingo_balls[max(board_marks_to_win)]))

# you get a bingo if you get a whole row, a whole column, or either diagonal
if __name__ == "__main__":
    pass