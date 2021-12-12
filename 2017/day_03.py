import itertools
from pathlib import Path
import os

# find location of puzzle input by spiraling out:
def find_value(location: list, values: dict):
    out = 0
    for dx, dy in itertools.product(range(-1, 2), range(-1, 2)):
        out += values.get((location[0] + dx, location[1]+ dy), 0)
    return out


def spiral_out_find_distance(puzzle_input: int):
    i = 1
    current_range = 0
    location = [0, 0]
    while i < puzzle_input:
        # take a step out
        current_range += 1
        location[0] += 1
        i += 1
        if i == puzzle_input:
            break
        # go up:
        go_more = True
        for up in range(2*current_range-1):
            location[1] +=1
            i += 1
            if i == puzzle_input:
                go_more = False
                break
        if go_more:
            # go left
            for left in range(2*current_range):
                location[0] -= 1
                i += 1
                if i == puzzle_input:
                    go_more = False
                    break
        if go_more:
            # go down
            for left in range(2*current_range):
                location[1] -= 1
                i += 1
                if i == puzzle_input:
                    go_more = False
                    break
        if go_more:
            # go right
            for left in range(2*current_range):
                location[0] += 1
                i += 1
                if i == puzzle_input:
                    go_more = False
                    break
    return location


def spiral_out_find_value(puzzle_input: int):
    i = 1
    current_range = 0
    location = [0, 0]
    values = {(0, 0): 1}
    while values[(location[0], location[1])] < puzzle_input:
        # take a step out
        current_range += 1
        location[0] += 1
        i += 1
        values[(location[0], location[1])] = find_value(location, values)
        if i == puzzle_input:
            break
        # go up:
        go_more = True
        for up in range(2*current_range-1):
            location[1] +=1
            i += 1
            values[(location[0], location[1])] = find_value(location, values)
            if values[(location[0], location[1])] > puzzle_input:
                go_more = False
                break
        if go_more:
            # go left
            for left in range(2*current_range):
                location[0] -= 1
                i += 1
                values[(location[0], location[1])] = find_value(location, values)
                if values[(location[0], location[1])] > puzzle_input:
                    go_more = False
                    break
        if go_more:
            # go down
            for left in range(2*current_range):
                location[1] -= 1
                i += 1
                values[(location[0], location[1])] = find_value(location, values)
                if values[(location[0], location[1])] > puzzle_input:
                    go_more = False
                    break
        if go_more:
            # go right
            for left in range(2*current_range):
                location[0] += 1
                i += 1
                values[(location[0], location[1])] = find_value(location, values)
                if values[(location[0], location[1])] > puzzle_input:
                    go_more = False
                    break
    return i, values[(location[0], location[1])]


if __name__ == "__main__":

    test_values = [12, 17, 23, 25, 7**2, 50, 51, 52, 53, 54, 1024, 33**2]
    test_values = []
    for v in test_values:
        address_location = spiral_out_find_distance(v)
        print(f"{v} location: {address_location}")
        print(f"{v} distance: {abs(address_location[0])+abs(address_location[1])}")

    address_location = spiral_out_find_distance(368078)
    print(f"{368078} location: {address_location}")
    print(f"{368078} distance: {abs(address_location[0])+abs(address_location[1])}")

    i, value = spiral_out_find_value(368078)
    print(f"{368078} i: {i}")
    print(f"{368078} value: {value}")
