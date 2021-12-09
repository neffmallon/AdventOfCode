from enum import Enum

import numpy as np

from computer import IntcodeComputer


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class RobotPainter:

    turn_dict = {
        Direction.UP: {0: Direction.LEFT, 1: Direction.RIGHT},
        Direction.DOWN: {0: Direction.RIGHT, 1: Direction.LEFT},
        Direction.LEFT: {0: Direction.DOWN, 1: Direction.UP},
        Direction.RIGHT: {0: Direction.UP, 1: Direction.DOWN},
    }

    def __init__(self, program: IntcodeComputer, hull_color: dict = None):
        self.position = (0, 0)
        if hull_color is None:
            hull_color = {}
        self.hull_color = hull_color
        self.direction = Direction.UP
        self.program = program

    def display_paint_job(self) -> np.ndarray:
        x_range = [0, 0]
        y_range = [0, 1]

        for key in self.hull_color.keys():
            if key[0] < x_range[0]:
                x_range[0] = key[0]
            if key[0] > x_range[1]:
                x_range[1] = key[0]

            if key[1] < y_range[0]:
                y_range[0] = key[1]
            if key[1] > y_range[1]:
                y_range[1] = key[1]

        x = np.linspace(x_range[0], x_range[1], num=1 + x_range[1] - x_range[0])
        y = np.linspace(y_range[0], y_range[1], num=1 + y_range[1] - y_range[0])
        paint_job = np.zeros((1 + x_range[1] - x_range[0], 1 + y_range[1] - y_range[0]))

        for i, xi in enumerate(x):
            for j, yi in enumerate(y):
                paint_job[i, j] = self.get_hull_color((xi, yi))
        return paint_job.T[::-1, :]

    def get_hull_color(self, position=None):
        if position is None:
            return self.hull_color.get(self.position, 0)
        else:
            return self.hull_color.get(position, 0)

    def paint_hull_and_turn_and_move(self):
        self.program.add_input(self.get_hull_color())
        self.paint_square(square=self.position, color=self.program.run_to_output())
        self.turn_bot(self.program.run_to_output())
        self.update_position()

    def run_until_painted(self):
        while True:
            try:
                self.paint_hull_and_turn_and_move()
            except KeyError:
                break
        n_squares_painted = sum([1 for _ in self.hull_color])
        print(f"Total squares painted: {n_squares_painted}")

    def paint_square(self, square: tuple, color: int):
        self.hull_color[square] = color

    def turn_bot(self, turn_direction: int):
        self.direction = self.turn_dict[self.direction][turn_direction]

    def update_position(self):
        if self.direction == Direction.UP:
            self.position = (self.position[0], self.position[1] + 1)
        elif self.direction == Direction.DOWN:
            self.position = (self.position[0], self.position[1] - 1)
        elif self.direction == Direction.LEFT:
            self.position = (self.position[0] - 1, self.position[1])
        elif self.direction == Direction.RIGHT:
            self.position = (self.position[0] + 1, self.position[1])
        else:
            raise ValueError


if __name__ == "__main__":
    from pathlib import Path
    import os
    import matplotlib.pyplot as plt

    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2019", "day_11_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    botboy = RobotPainter(IntcodeComputer(puzzle_input[0].split(",")))
    botboy.run_until_painted()  # 2441 is correct

    botboy = RobotPainter(
        IntcodeComputer(puzzle_input[0].split(",")), hull_color={(0, 0): 1}
    )
    botboy.run_until_painted()
    botboy_paint_job = botboy.display_paint_job()

    plt.imshow(botboy_paint_job)  # PZRFPRKC
