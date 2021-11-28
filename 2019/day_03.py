def wire_cross_finder(wire_list: list):
    wire_points = dict()
    for wire_idx, wire in enumerate(wire_list):
        occupied_points = set()
        current_location = [0, 0]
        for segment in wire.strip().split(","):
            direction = segment[0]
            distance = int(segment[1:])
            if direction in ("R", "L"):
                axis = 0
                if direction == "L":
                    distance = 0 - distance
            elif direction in ("U", "D"):
                axis = 1
                if direction == "D":
                    distance = 0 - distance
            else:
                raise ValueError(f"{segment} is not a valid wire")

            if distance < 0:
                direction = -1
            else:
                direction = 1

            for step in range(0, distance, direction):
                current_location[axis] += direction
                occupied_points.add(tuple(current_location))
        wire_points[wire_idx] = occupied_points

    crossed_points = wire_points[0].intersection(wire_points[1])

    min_dist = None
    for point in crossed_points:
        if min_dist is None:
            min_dist = abs(point[0]) + abs(point[1])
        elif point == (0, 0):
            continue
        else:
            min_dist = min(abs(point[0]) + abs(point[1]), min_dist)

    return min_dist


def wire_cross_finder_wire_distance(wire_list: list):

    wire_points = dict()
    wire_dists = dict()
    for wire_idx, wire in enumerate(wire_list):
        occupied_points = set()
        occupied_distances = dict()
        current_location = [0, 0]
        current_wire_length = 0
        for segment in wire.strip().split(","):
            direction = segment[0]
            distance = int(segment[1:])
            if direction in ("R", "L"):
                axis = 0
                if direction == "L":
                    distance = 0 - distance
            elif direction in ("U", "D"):
                axis = 1
                if direction == "D":
                    distance = 0 - distance
            else:
                raise ValueError(f"{segment} is not a valid wire")

            direction = distance // abs(distance)
            assert direction in (1, -1)

            for step in range(0, distance, direction):
                current_location[axis] += direction
                current_wire_length += 1
                if not tuple(current_location) in occupied_points:
                    occupied_points.add(tuple(current_location))
                    occupied_distances[tuple(current_location)] = current_wire_length

        wire_points[wire_idx] = occupied_points
        wire_dists[wire_idx] = occupied_distances

    crossed_points = wire_points[0].intersection(wire_points[1])

    min_dist = None
    for point in crossed_points:
        if min_dist is None:
            min_dist = wire_dists[0][point] + wire_dists[1][point]
        elif point == (0, 0):
            continue
        else:
            min_dist = min(wire_dists[0][point] + wire_dists[1][point], min_dist)

    return min_dist


if __name__ == "__main__":
    with open("day_03_input.txt", "r") as f:
        wire_map = f.readlines()
    print(f"Part 1: {wire_cross_finder(wire_map)}")
    print(f"Part 2: {wire_cross_finder_wire_distance(wire_map)}")
