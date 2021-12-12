from pathlib import Path
import os


def build_graph(lines):
    graph = {}
    for line in lines:
        s = line.split("-")
        if s[0] in graph.keys():
            graph[s[0]].add(s[1])
        else:
            graph[s[0]] = {s[1]}
        if s[1] in graph.keys():
            graph[s[1]].add(s[0])
        else:
            graph[s[1]] = {s[0]}
    return graph


def find_all_paths(graph, start_vertex, end_vertex, path=[]):
    path = path + [start_vertex]
    if start_vertex == end_vertex:
        return [path]
    if start_vertex not in graph:
        return []
    paths = []
    for vertex in graph[start_vertex]:
        if vertex not in path or vertex.upper() == vertex:
            extended_paths = find_all_paths(graph, vertex, end_vertex, path)
            for p in extended_paths:
                paths.append(p)
    return paths


def find_all_paths_with_small_double(
    graph, start_vertex, end_vertex, small_double, path=[]
):
    path = path + [start_vertex]
    if start_vertex == end_vertex:
        return [path]
    if start_vertex not in graph:
        return []
    paths = []
    for vertex in graph[start_vertex]:
        if (
            vertex not in path
            or vertex.upper() == vertex
            or (vertex == small_double and path.count(vertex) < 2)
        ):
            extended_paths = find_all_paths_with_small_double(
                graph, vertex, end_vertex, small_double, path
            )
            for p in extended_paths:
                paths.append(p)
    return paths


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2021", "day_12_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    caves = build_graph(puzzle_input)
    all_paths = find_all_paths(caves, "start", "end")
    print(f"Part 1: {len(all_paths)}")

    all_paths_with_doubles = []
    for small_double in [
        k for k in caves.keys() if k.lower() == k and k not in ("start", "end")
    ]:
        all_paths_with_doubles.extend(
            find_all_paths_with_small_double(caves, "start", "end", small_double)
        )

    print(f"Part 2: {len({tuple(p) for p in all_paths_with_doubles})}")
