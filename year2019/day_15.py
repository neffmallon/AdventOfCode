import os
import tkinter
from pathlib import Path
from typing import Tuple

from computer import IntcodeComputer

# I could make something to intellegently navigate a maze or even brute force it,
# but I think I want to manually control the robot


class RepairDroid:
    block_size = 10
    n_blocks = 50

    def __init__(self, computer: IntcodeComputer):
        self.map = {(0, 0): 1}
        self.robot_position = (0, 0)
        self.computer = computer
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            bg="white",
            height=self.n_blocks * self.block_size,
            width=self.n_blocks * self.block_size,
        )
        self.canvas.pack()
        self.robot = self.canvas.create_rectangle(
            self.location_to_rec_coords(*self.robot_position), fill="orange"
        )
        self.robot = self.canvas.create_oval(
            self.location_to_rec_coords(*self.robot_position), fill="light blue"
        )
        self.dist_to_o2 = {}
        self.o2_loc = None
        self.origin_counter = tkinter.Label(text="Origin - O2 distance: ???")
        self.origin_counter.pack(side="top")
        self.max_distance_counter = tkinter.Label(text="O2 max distance: ???")
        self.max_distance_counter.pack(side="top")

    def start(self):
        self.bind_controls()
        self.window.mainloop()

    @property
    def rx(self):
        return self.robot_position[0]

    @property
    def ry(self):
        return self.robot_position[1]

    def map_dist_to_02(self, x, y, dist):
        if dist == 0:
            self.o2_loc = (x, y)
        if self.dist_to_o2.get((x, y)) is not None:
            return
        self.dist_to_o2[(x, y)] = dist
        check_dirs = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]
        for d in check_dirs:
            if self.map.get(d) == 0:
                self.dist_to_o2[d] = -1
                continue
            if self.map.get(d) is None:
                continue
            self.map_dist_to_02(*d, dist + 1)

    def location_to_rec_coords(self, x: int, y: int) -> Tuple[int, int, int, int]:
        offset = self.block_size * (self.n_blocks // 2)
        return (
            offset + x * self.block_size,
            offset + y * self.block_size,
            offset + (x + 1) * self.block_size,
            offset + (y + 1) * self.block_size,
        )

    def location_to_small_rec_coords(self, x: int, y: int) -> Tuple[int, int, int, int]:
        offset = self.block_size * (self.n_blocks // 2)
        return (
            offset + x * self.block_size + (self.block_size // 3),
            offset + y * self.block_size + (self.block_size // 3),
            offset + (x + 1) * self.block_size - (self.block_size // 3),
            offset + (y + 1) * self.block_size - (self.block_size // 3),
        )

    def make_wall_at(self, x, y):
        self.map[(x, y)] = 0
        self.canvas.create_rectangle(*self.location_to_rec_coords(x, y), fill="red")

    def bind_controls(self):
        fill_color = {1: "light grey", 2: "green"}

        def up(event):
            self.computer.add_input(1)
            self.computer.do_next_instruction()
            out = self.computer.run_to_output()
            if out == 0:
                # robot did not move
                self.make_wall_at(self.rx, self.ry - 1)
                return
            if out == 2:
                # robot found the O2!
                self.canvas.move(self.robot, 0, -self.block_size)
                self.robot_position = (self.rx, self.ry - 1)
                self.canvas.create_rectangle(
                    *self.location_to_rec_coords(self.rx, self.ry), fill="green"
                )
                self.map_dist_to_02(self.rx, self.ry, 0)
                self.map[self.robot_position] = 1
                return
            # robot did move, bud did not find the 02
            self.canvas.move(self.robot, 0, -self.block_size)
            self.canvas.create_rectangle(
                *self.location_to_small_rec_coords(self.rx, self.ry),
                fill=fill_color[out],
            )
            self.robot_position = (self.rx, self.ry - 1)
            self.map[self.robot_position] = 1

        def down(event):
            self.computer.add_input(2)
            self.computer.do_next_instruction()
            out = self.computer.run_to_output()
            if out == 0:
                # robot did not move
                self.make_wall_at(self.rx, self.ry + 1)
                return
            if out == 2:
                # robot found the O2!
                self.canvas.move(self.robot, 0, self.block_size)
                self.robot_position = (self.rx, self.ry + 1)
                self.canvas.create_rectangle(
                    *self.location_to_rec_coords(self.rx, self.ry), fill="green"
                )
                self.map_dist_to_02(self.rx, self.ry, 0)
                self.map[self.robot_position] = 1
                return
            # robot did move, bud did not find the 02
            self.canvas.move(self.robot, 0, self.block_size)
            self.canvas.create_rectangle(
                *self.location_to_small_rec_coords(self.rx, self.ry),
                fill=fill_color[out],
            )
            self.robot_position = (self.rx, self.ry + 1)
            self.map[self.robot_position] = 1

        def right(event):
            self.computer.add_input(4)
            self.computer.do_next_instruction()
            out = self.computer.run_to_output()
            if out == 0:
                # robot did not move
                self.make_wall_at(self.rx + 1, self.ry)
                return
            if out == 2:
                # robot found the O2!
                self.canvas.move(self.robot, self.block_size, 0)
                self.robot_position = (self.rx + 1, self.ry)
                self.canvas.create_rectangle(
                    *self.location_to_rec_coords(self.rx, self.ry), fill="green"
                )
                self.map_dist_to_02(self.rx, self.ry, 0)
                self.map[self.robot_position] = 1
                return
            # robot did move, bud did not find the 02
            self.canvas.move(self.robot, self.block_size, 0)
            self.canvas.create_rectangle(
                *self.location_to_small_rec_coords(self.rx, self.ry),
                fill=fill_color[out],
            )
            self.robot_position = (self.rx + 1, self.ry)
            self.map[self.robot_position] = 1

        def left(event):
            self.computer.add_input(3)
            self.computer.do_next_instruction()
            out = self.computer.run_to_output()
            if out == 0:
                # robot did not move
                self.make_wall_at(self.rx - 1, self.ry)
                return
            if out == 2:
                # robot found the O2!
                self.canvas.move(self.robot, -self.block_size, 0)
                self.robot_position = (self.rx - 1, self.ry)
                self.canvas.create_rectangle(
                    *self.location_to_rec_coords(self.rx, self.ry), fill="green"
                )
                self.map_dist_to_02(self.rx, self.ry, 0)
                return
            # robot did move
            self.canvas.move(self.robot, -self.block_size, 0)
            self.canvas.create_rectangle(
                *self.location_to_small_rec_coords(self.rx, self.ry),
                fill=fill_color[out],
            )
            self.robot_position = (self.rx - 1, self.ry)
            self.map[self.robot_position] = 1

        def manual_map(event):
            if self.o2_loc is None:
                return
            self.dist_to_o2 = {}
            self.map_dist_to_02(*self.o2_loc, 0)
            self.origin_counter.config(
                text=f"Origin - O2 distance: {self.dist_to_o2[(0,0)]}"
            )
            max_dist = max([v for v in self.dist_to_o2.values()])
            self.max_distance_counter.config(
                text=f"Max O2 distance: {max_dist}"
            )

        self.window.bind("<Left>", left)
        self.window.bind("<Down>", down)
        self.window.bind("<Right>", right)
        self.window.bind("<Up>", up)
        self.window.bind("<space>", manual_map)


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "year2019", "day_15_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    repair_sim = RepairDroid(IntcodeComputer(puzzle_input[0].split(",")))
    repair_sim.start()
    # Distance to center: 318
    # Distance to furthest point: 390
