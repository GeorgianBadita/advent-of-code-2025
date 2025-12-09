import sys
from dataclasses import dataclass
from functools import reduce

IN_FILE_PATH = "./input.txt"


@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int
    z: int


def read_file_as_string(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        lines = [line.rstrip("\n") for line in file]
        return lines


def parse_str_to_point(str_list: list[str]) -> list[Point]:
    points: list[Point] = []
    for line in str_list:
        x, y, z = line.split(",")
        points.append(Point(x=int(x.strip()), y=int(y.strip()), z=int(z.strip())))
    return points


def validate_and_get_arg() -> str:
    if len(sys.argv) != 2:
        raise ValueError("Exactly one arg is expected")

    arg = sys.argv[1]

    if arg not in ["1", "2"]:
        raise ValueError(
            "Arg can only be 1 or 2 for part 1 or part 2 of the problem respectively"
        )

    return arg


def get_point_dist(p1: Point, p2: Point) -> int:
    return (p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2 + (p2.z - p1.z) ** 2


def sort_indices_by_dist(points: list[Point]) -> list[tuple[int, int]]:
    dist_map: list[list[int]] = [[10**9] * len(points) for _ in range(len(points))]
    for idx in range(len(points)):
        for jdx in range(idx):
            dist_map[idx][jdx] = get_point_dist(points[idx], points[jdx])

    indices: list[tuple[int, int]] = []
    for idx in range(len(points)):
        for jdx in range(len(points)):
            indices.append((idx, jdx))

    return sorted(indices, key=lambda point: dist_map[point[0]][point[1]])


def add_one_edge_to_graph(
    current_graph: dict[Point, set[Point]],
    points: list[Point],
    sorted_ind: list[tuple[int, int]],
    edge_idx: int,
) -> tuple[dict[Point, set[Point]], Point | None, Point | None]:
    if edge_idx >= len(sorted_ind):
        return current_graph, None, None

    closest_points = sorted_ind[edge_idx]
    p1_idx, p2_idx = closest_points

    if p1_idx == p2_idx:
        return current_graph, None, None

    point1 = points[p1_idx]
    point2 = points[p2_idx]

    p1_nodes = current_graph.get(point1, set())
    p1_nodes.add(point2)

    p2_nodes = current_graph.get(point2, set())
    p2_nodes.add(point1)

    current_graph[point1] = p1_nodes
    current_graph[point2] = p2_nodes

    return current_graph, point1, point2


def build_graph_with_n_edges(
    points: list[Point], sorted_ind: list[tuple[int, int]], n: int
) -> dict[Point, set[Point]]:
    graph: dict[Point, set[Point]] = {}

    for idx in range(n):
        if idx >= len(sorted_ind):
            break

        closest_points = sorted_ind[idx]
        p1_idx, p2_idx = closest_points

        if p1_idx == p2_idx:
            break

        point1 = points[p1_idx]
        point2 = points[p2_idx]

        p1_nodes = graph.get(point1, set())
        p1_nodes.add(point2)

        p2_nodes = graph.get(point2, set())
        p2_nodes.add(point1)

        graph[point1] = p1_nodes
        graph[point2] = p2_nodes

    return graph


def bfs(graph: dict[Point, set[Point]], start: Point, visited: set[Point]) -> int:
    visited.add(start)
    queue = [start]

    count = 0
    while queue:
        node = queue.pop(0)
        count += 1
        for adj in graph[node]:
            if adj not in visited:
                visited.add(adj)
                queue.append(adj)
    return count


def connected_components(graph: dict[Point, set[Point]]) -> list[int]:
    component_sizes: list[int] = []
    visited: set[Point] = set()

    for node in graph:
        if node not in visited:
            component_sizes.append(bfs(graph, node, visited))

    return component_sizes


def part1(points: list[Point], sorted_ind: list[tuple[int, int]], n: int) -> int:
    graph: dict[Point, set[Point]] = {}
    for idx in range(n):
        graph, _, _ = add_one_edge_to_graph(graph, points, sorted_ind, idx)

    component_sizes = connected_components(graph)
    component_sizes.sort(reverse=True)
    return int(reduce(lambda x, y: x * y, component_sizes[:3], 1))


def none_throws[T](val: T | None) -> T:
    if val is None:
        raise ValueError(f"{val} is None")
    return val


def part2(points: list[Point], sorted_ind: list[tuple[int, int]]) -> int:
    graph: dict[Point, set[Point]] = {}
    for idx in range(len(points) ** 2):
        graph, p1, p2 = add_one_edge_to_graph(graph, points, sorted_ind, idx)
        components = connected_components(graph)
        if len(components) == 1 and len(graph) == len(points):
            return none_throws(p1).x * none_throws(p2).x

    raise ValueError("Did not work")


def main():
    try:
        data = read_file_as_string(IN_FILE_PATH)

        points = parse_str_to_point(data)
        sorted_ind = sort_indices_by_dist(points)
        arg = validate_and_get_arg()

        if arg == "1":
            print(part1(points, sorted_ind, 1000))
        else:
            print(part2(points, sorted_ind))

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
