"""
A laughably incorrect model of the orbits of the moons of jupyter

"""
import dataclasses
import time


@dataclasses.dataclass
class Vector:
    x: int
    y: int
    z: int


@dataclasses.dataclass
class Moon:
    position: Vector
    velocity: Vector = dataclasses.field(default_factory=lambda: Vector(0, 0, 0))


class MoonSystem:
    def __init__(self, moons: list):
        self.moons = moons

    def take_step(self):
        self._update_velocity()
        self._update_position()

    def _update_velocity(self):
        for moon_idx in range(len(self.moons)):
            for other_moon_idx in range(len(self.moons)):
                if moon_idx == other_moon_idx:
                    continue

                if (
                    self.moons[moon_idx].position.x
                    > self.moons[other_moon_idx].position.x
                ):
                    self.moons[moon_idx].velocity.x -= 1
                elif (
                    self.moons[moon_idx].position.x
                    < self.moons[other_moon_idx].position.x
                ):
                    self.moons[moon_idx].velocity.x += 1

                if (
                    self.moons[moon_idx].position.y
                    > self.moons[other_moon_idx].position.y
                ):
                    self.moons[moon_idx].velocity.y -= 1
                elif (
                    self.moons[moon_idx].position.y
                    < self.moons[other_moon_idx].position.y
                ):
                    self.moons[moon_idx].velocity.y += 1

                if (
                    self.moons[moon_idx].position.z
                    > self.moons[other_moon_idx].position.z
                ):
                    self.moons[moon_idx].velocity.z -= 1
                elif (
                    self.moons[moon_idx].position.z
                    < self.moons[other_moon_idx].position.z
                ):
                    self.moons[moon_idx].velocity.z += 1

    def _update_position(self):
        for moon_idx in range(len(self.moons)):
            self.moons[moon_idx].position.x += self.moons[moon_idx].velocity.x
            self.moons[moon_idx].position.y += self.moons[moon_idx].velocity.y
            self.moons[moon_idx].position.z += self.moons[moon_idx].velocity.z

    def calculate_energy(self):
        total_energy = 0
        for moon in self.moons:
            pot = abs(moon.position.x) + abs(moon.position.y) + abs(moon.position.z)
            kin = abs(moon.velocity.x) + abs(moon.velocity.y) + abs(moon.velocity.z)
            total_energy += pot * kin
        return total_energy


def simulate_one_axis(positions, velocities):
    for moon_idx in range(len(positions)):
        for other_moon_idx in range(len(positions)):
            if moon_idx == other_moon_idx:
                continue

            if positions[moon_idx] > positions[other_moon_idx]:
                velocities[moon_idx] -= 1
            elif positions[moon_idx] < positions[other_moon_idx]:
                velocities[moon_idx] += 1
    # print(f"updated velocities: {velocities}")
    for moon_idx in range(len(positions)):
        positions[moon_idx] += velocities[moon_idx]


def find_frequency(moon_list: list):
    axis_period = {"x": 0, "y": 0, "z": 0}
    for key in axis_period.keys():
        positions = [m.position.__getattribute__(key) for m in moon_list]
        velocities = [0 for _ in moon_list]
        step = 0
        while True:
            simulate_one_axis(positions, velocities)
            step += 1
            if sum(velocities) == 0:
                if sum([abs(x) for x in velocities]) == 0:
                    if positions == [
                        m.position.__getattribute__(key) for m in moon_list
                    ]:
                        break
        axis_period[key] = step

    print(axis_period)
    return axis_period


if __name__ == "__main__":
    # tests first
    pass

if False:
    moons = [
        Moon(position=Vector(-1, 0, 2)),
        Moon(position=Vector(2, -10, -7)),
        Moon(position=Vector(4, -8, 8)),
        Moon(position=Vector(3, 5, -1)),
    ]
    """
    # <editor-fold desc="early work">
    my_moons = MoonSystem(moons)
    past_positions = set()
    for i in range(10):
        my_moons.take_step()
        past_positions.add(str(my_moons.moons))
    assert my_moons.calculate_energy() == 179


    start = time.time()
    my_moons = MoonSystem(moons)

    past_positions = set()
    step = 0
    while str(my_moons.moons) not in past_positions:
        past_positions.add(str(my_moons.moons))
        my_moons.take_step()
        step += 1
    print(step)
    end = time.time()
    print(end - start)

    # </editor-fold desc="early work">
    """
    my_moons = MoonSystem(moons)
    start = time.time()
    find_frequency(moons)
    end = time.time()
    print(f"time: {end-start}")

if False:
    moons = [
        Moon(position=Vector(-8, -10, 0)),
        Moon(position=Vector(5, 5, 10)),
        Moon(position=Vector(2, -7, 3)),
        Moon(position=Vector(9, -8, -3)),
    ]
    my_moons = MoonSystem(moons)
    for i in range(100):
        my_moons.take_step()
    assert my_moons.calculate_energy() == 1940

    my_moons = MoonSystem(moons)
    start = time.time()
    past_positions = set()
    step = 0
    position = [m.x for m in moons]
    velocity = [0 for m in moons]
    while True:
        simulate_one_axis(position, velocity)
        if sum(velocity) == 0:
            if sum([abs(x) for x in velocity]) == 0:
                break

    end = time.time()
    print(position)
    print(velocity)
    print(end - start)

if False:

    # real input
    moons = [
        Moon(position=Vector(10, 15, 7)),
        Moon(position=Vector(15, 10, 0)),
        Moon(position=Vector(20, 12, 3)),
        Moon(position=Vector(0, -3, 13)),
    ]
    my_moons = MoonSystem(moons)
    for i in range(1000):
        my_moons.take_step()
    assert my_moons.calculate_energy() == 8362

    print(f"Part 1: Step {1 + i}, energy: {my_moons.calculate_energy()}")

if True:
    moons = [
        Moon(position=Vector(10, 15, 7)),
        Moon(position=Vector(15, 10, 0)),
        Moon(position=Vector(20, 12, 3)),
        Moon(position=Vector(0, -3, 13)),
    ]
    start = time.time()
    find_frequency(moons)
    end = time.time()
    print(f"time: {end - start}")
    # Answer is the LCM, 478373365921244
