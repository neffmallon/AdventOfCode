import os
from pathlib import Path

import pytest
from day_14 import Reaction, get_needed_ore


def test_simple():
    reactions_str = """10 ORE => 10 A
    1 ORE => 1 B
    7 A, 1 B => 1 C
    7 A, 1 C => 1 D
    7 A, 1 D => 1 E
    7 A, 1 E => 1 FUEL""".split(
        "\n"
    )
    reactions_list = [Reaction.from_string(s) for s in reactions_str]
    reaction_dict = {r.product_name: r for r in reactions_list}

    reactants_needed = get_needed_ore(reaction_dict, "FUEL", 1, dict(), dict())
    assert reactants_needed["ORE"] == 31


def test_2():
    reactions_str = """9 ORE => 2 A
    8 ORE => 3 B
    7 ORE => 5 C
    3 A, 4 B => 1 AB
    5 B, 7 C => 1 BC
    4 C, 1 A => 1 CA
    2 AB, 3 BC, 4 CA => 1 FUEL""".split(
        "\n"
    )
    reactions_list = [Reaction.from_string(s) for s in reactions_str]
    reaction_dict = {r.product_name: r for r in reactions_list}

    reactants_needed = get_needed_ore(reaction_dict, "FUEL", 1, dict(), dict())
    assert reactants_needed["ORE"] == 165


def test_problem():
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "year2019", "day_14_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    reactions_list = [Reaction.from_string(s) for s in puzzle_input]
    reaction_dict = {r.product_name: r for r in reactions_list}

    reactants_needed = get_needed_ore(reaction_dict, "FUEL", 1, dict(), dict())
    assert reactants_needed["ORE"] == 504284
