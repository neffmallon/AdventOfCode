import os
import tkinter
from enum import Enum
from pathlib import Path
from typing import Dict, Optional, Tuple

from computer import IntcodeComputer

GRID_COLORS = {0: "white", 1: "black", 2: "orange", 3: "light grey", 4: "red"}


class Direction(Enum):
    RIGHT = 1
    LEFT = -1


class GameMode(Enum):
    MANUAL = 1
    AUTO = 0


class ArcadeCabinet:
    block_size = 20

    def __init__(self, computer: IntcodeComputer):
        self.computer = computer
        self.window = tkinter.Tk()
        self.buttons: Dict[str, tkinter.Button] = dict()

        self.score_display = tkinter.Label(self.window, text=f"Score: 0")
        self.score_display.pack()

        self.game_display_dict: Dict[Tuple[int, int], int] = dict()
        self.game_display: Optional[tkinter.Canvas] = None
        self.ball_location = None
        self.ball_direction: Direction = Direction.RIGHT
        self.paddle_location = None

    def start_game(self, mode: GameMode = GameMode.MANUAL):
        # add in your quarters!
        self.computer.code[0] = 2
        # Start the game!
        self.window.title("Arcade Cabinet")

        self.update_game_display_dict()
        self.do_one_frame()

        if mode == GameMode.MANUAL:
            self.bind_controls()
        elif mode == GameMode.AUTO:
            self.window.bind("<Down>", self.ai_play)

        self.window.mainloop()

    def ai_play(self, event):
        if self.computer.is_complete:
            return
        # tell the computer what move to make
        ball_x, ball_y = self.ball_location
        pad_x, pad_y = self.paddle_location
        if ball_y + 1 == pad_y:
            if ball_x == pad_x:
                self.computer.add_input(0)
            elif ball_x > pad_x:
                self.computer.add_input(1)
            else:
                self.computer.add_input(-1)
        else:
            if ball_x == pad_x:
                self.computer.add_input(self.ball_direction.value)
            elif ball_x + self.ball_direction.value == pad_x:
                self.computer.add_input(0)
            elif ball_x + self.ball_direction.value > pad_x:
                self.computer.add_input(1)
            else:
                self.computer.add_input(-1)

        self.computer.do_next_instruction()
        self.do_one_frame()

    def bind_controls(self):
        def left(event):
            self.computer.add_input(-1)
            self.computer.do_next_instruction()
            self.do_one_frame()

        def neutral(event):
            self.computer.add_input(0)
            self.computer.do_next_instruction()
            self.do_one_frame()

        def right(event):
            self.computer.add_input(1)
            self.computer.do_next_instruction()
            self.do_one_frame()

        self.window.bind("<Left>", left)
        self.window.bind("<Down>", neutral)
        self.window.bind("<Right>", right)

    def do_one_frame(self):
        if self.game_display is None:
            x_size = max([x for x, y in self.game_display_dict.keys()])
            y_size = max([y for x, y in self.game_display_dict.keys()])

            self.game_display = tkinter.Canvas(
                self.window,
                bg="white",
                height=(1 + y_size) * self.block_size,
                width=(1 + x_size) * self.block_size,
            )
            self.game_display.pack()

        # run the computer to get update the current display
        self.update_game_display_dict()
        self.game_display.delete("all")
        for (x, y), value in self.game_display_dict.items():
            if x >= 0 and value > 0:
                if value == 4:
                    shape = self.game_display.create_oval
                    # update direction
                    if self.ball_direction is None or self.ball_location is None:
                        self.ball_location = Direction.RIGHT
                    else:
                        if self.ball_location[0] > x:
                            self.ball_direction = Direction.LEFT
                        else:
                            self.ball_direction = Direction.RIGHT
                    # update location
                    self.ball_location = (x, y)
                elif value == 3:
                    self.paddle_location = (x, y)
                    shape = self.game_display.create_rectangle
                else:
                    shape = self.game_display.create_rectangle

                shape(
                    x * self.block_size,
                    y * self.block_size,
                    (x + 1) * self.block_size,
                    (y + 1) * self.block_size,
                    fill=GRID_COLORS[value],
                )

            if x == -1 and y == 0:
                self.score_display.config(text=f"Score: {value}")
                self.score_display.pack()

    def update_game_display_dict(self):
        outputs = self.computer.run_to_input()

        for i in range(0, len(outputs) // 3):
            self.game_display_dict[(outputs[i * 3], outputs[1 + i * 3])] = outputs[
                2 + i * 3
            ]


def build_window(display: Dict[Tuple[int, int], int]):
    window = tkinter.Tk()
    window.title("Arcade Cabinet")

    # Joystick buttons
    left_button = tkinter.Button(window, text="left").pack(side="bottom")
    neutral_button = tkinter.Button(window, text="neutral").pack(side="bottom")
    right_button = tkinter.Button(window, text="right").pack(side="bottom")

    # Score
    score_display = tkinter.Label(window, text=f"Score: {display.get((-1, 0), 0)}")

    x_size = max([x for x, y in display.keys()])
    y_size = max([y for x, y in display.keys()])

    block_size = 20
    canvas = tkinter.Canvas(
        window,
        bg="white",
        height=(1 + y_size) * block_size,
        width=(1 + x_size) * block_size,
    )

    for (x, y), value in display.items():
        if x >= 0 and value > 0:
            if value == 4:
                shape = canvas.create_oval
            else:
                shape = canvas.create_rectangle

            shape(
                x * block_size,
                y * block_size,
                (x + 1) * block_size,
                (y + 1) * block_size,
                fill=GRID_COLORS[value],
            )

        if x == -1 and y == 0:
            score_display.config(str(value))

    canvas.pack()
    score_display.pack()

    window.mainloop()


def main():
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2019", "day_13_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    computer = IntcodeComputer(puzzle_input[0].split(","))

    arcade = ArcadeCabinet(computer)
    arcade.start_game(GameMode.AUTO)

    """display = {}
    while True:
        x = drawing_computer.run_to_output()
        if x is None:
            break
        y = drawing_computer.run_to_output()
        tile_id = drawing_computer.run_to_output()
        display[(x, y)] = tile_id

    build_window(display)"""


if __name__ == "__main__":
    main()
