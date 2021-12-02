from pathlib import Path
import os
from numpy import arctan, pi
import cmath


class AsteroidField:
    def __init__(self, field_rows: list):
        self.asteroids = set()
        self._populate_asteroids(field_rows)
        self.station = None

    def count_visible_asteroids(self, row, col):
        ratios = set()
        for r, c in self.asteroids:
            if (r, c) == (row, col):
                continue
            side = r > row or (r == row and c > col)
            ratios.add(self._get_angle(r - row, c - col))
        return len(ratios)

    def find_best_asteroid_station(self):
        best = -1
        best_rock = None
        for rock in self.asteroids:
            new_candidate_counts = self.count_visible_asteroids(rock[0], rock[1])
            if best < new_candidate_counts:
                best_rock = rock
                best = new_candidate_counts
        self.station = best_rock
        return best

    def find_zap_order(self):
        asteroid_distances = self._calculate_asteroid_distances()
        angles = [k for k in asteroid_distances.keys()]
        angles.sort(reverse=True)
        zap_list = []
        cycle_zap_list = [None]
        while len(cycle_zap_list) > 0 and len(zap_list) < len(self.asteroids):
            cycle_zap_list = []
            for angle in angles:
                if len(asteroid_distances[angle]) > 0:
                    # sort by distance to get the closest asteroid at that angle
                    asteroid_distances[angle].sort(key=lambda x: x[0])
                    cycle_zap_list.append((asteroid_distances[angle].pop(0)))
            # flip the order b/c I have them backwards relative to the problem literally everywhere
            zap_list += [(location[1], location[0]) for _, location in cycle_zap_list]
        return zap_list

    def _calculate_asteroid_distances(self):
        if self.station is None:
            self.find_best_asteroid_station()
        if self.station is None:
            raise ValueError

        polar_map = dict()
        for rock in self.asteroids:
            if rock == self.station:
                continue

            distance, angle = self.get_angle_from_station(*rock)

            if angle in polar_map.keys():
                polar_map[angle].append((distance, rock))
            else:
                polar_map[angle] = [(distance, rock)]

        return polar_map

    def get_angle_from_station(self, row, column):
        return cmath.polar(
            -1 * (self.station[0] - row) + 1j * (column - self.station[1])
        )

    @staticmethod
    def _get_angle(delta_r, delta_c):
        return cmath.polar(-delta_r + 1j * delta_c)[1]

    def _populate_asteroids(self, field_rows):
        for row_idx, row in enumerate(field_rows):
            for col_idx, value in enumerate(row):
                if value == "#":
                    self.asteroids.add((row_idx, col_idx))


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2019", "day_10_input.txt")
    with open(file, "r") as f:
        m = [s.strip("\n") for s in f]

    f = AsteroidField(m)
    print(f"Part 1: {f.find_best_asteroid_station()}")  # should be 296
    zap_order = f.find_zap_order()
    answer = zap_order[199][0] * 100 + zap_order[199][1]
    print(f"Part 2: {answer}")
    # s = ".#..##.###...#######\n##.############..##.\n.#.######.########.#\n.###.#######.####.#.\n#####.##.#.##.###.##\n..#####..#.#########\n####################\n#.####....###.#.#.##\n##.#################\n#####.##.###..####..\n..######..##.#######\n####.##.####...##..#\n.#####..#.######.###\n##...#.##########...\n#.##########.#######\n.####.#.###.###.#.##\n....##.##.###..#####\n.#.#.###########.###\n#.#.#.#####.####.###\n###.##.####.##.#..##"
    # f = AsteroidField(s.split('\n'))
    # f.find_best_asteroid_station()
