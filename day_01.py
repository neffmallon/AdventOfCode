import pandas as pd


def fuel_from_mass(mass: float):
    return max(mass // 3 - 2, 0)


def fuel_from_mass_and_fuel(mass: float):
    total_fuel = 0
    step_fuel = fuel_from_mass(mass)
    while step_fuel > 0:
        total_fuel += step_fuel
        step_fuel = fuel_from_mass(step_fuel)
    return total_fuel


if __name__ == "__main__":
    modules = pd.read_csv("day_01_input.txt")
    modules["fuel"] = modules.mass.apply(fuel_from_mass_and_fuel)
    print(modules.fuel.sum())
