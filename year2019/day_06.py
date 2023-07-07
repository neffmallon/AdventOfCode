from treelib.tree import Tree


def map_maker(orbit_map: list):
    orbit_tree = Tree()
    orbit_map_copy = [tuple(o.strip().split(")")) for o in orbit_map]
    done_orbits = set()
    orbit_tree.create_node(identifier="COM")
    while len(orbit_map_copy) > len(done_orbits):
        for orbit in orbit_map_copy:
            if orbit in done_orbits:
                continue
            if orbit_tree.get_node(orbit[0]) is not None or orbit[0] == "COM":
                orbit_tree.create_node(identifier=orbit[1], parent=orbit[0])
                done_orbits.add(orbit)
    return orbit_tree


def count_orbits(orbit_tree: Tree):
    total_orbits = 0
    for node in orbit_tree.all_nodes():
        if node.tag == "COM":
            continue
        total_orbits += orbit_tree.depth(node)
    return total_orbits


def orbit_transfer_distance(orbit_tree: Tree):
    y = [(n, orbit_tree.depth(n)) for n in orbit_tree.rsearch("YOU")]
    s = [(n, orbit_tree.depth(n)) for n in orbit_tree.rsearch("SAN")]
    both = [n for n in y if n in s]
    return (orbit_tree.depth("YOU") + orbit_tree.depth("SAN")) - (both[0][1] + 1) * 2


if __name__ == "__main__":

    with open("day_06_input.txt", "r") as f:
        orbit_list = f.readlines()
    orbit_map = map_maker(orbit_list)
    print(f"Part 1: {count_orbits(orbit_map)}")
    print(f"Part 2: {orbit_transfer_distance(orbit_map)}")
