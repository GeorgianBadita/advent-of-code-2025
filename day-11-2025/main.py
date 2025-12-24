from functools import reduce
import sys

IN_FILE_PATH = "./input.txt"

type Graph = dict[str, list[str]]


def read_file_as_string(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        lines = [line.rstrip("\n") for line in file]
        return lines


def file_to_graph(file: list[str]) -> Graph:
    graph: Graph = {}
    for line in file:
        src, dests = line.split(":")
        graph[src.strip()] = [x.strip() for x in dests.split(" ")][1:]
    return graph


def validate_and_get_arg() -> str:
    if len(sys.argv) != 2:
        raise ValueError("Exactly one arg is expected")

    arg = sys.argv[1]

    if arg not in ["1", "2"]:
        raise ValueError(
            "Arg can only be 1 or 2 for part 1 or part 2 of the problem respectively"
        )

    return arg


def search_paths(graph: Graph, node: str, end: str, memo: dict[str, int]) -> int:
    if node in memo:
        return memo[node]
    if node == end:
        return 1

    # I'm assuming we don't have cycles here
    memo[node] = sum(
        [search_paths(graph, neighbour, end, memo) for neighbour in graph.get(node, [])]
    )
    return memo[node]


def part1(graph: Graph) -> int:
    return search_paths(graph, "you", "out", {})


def part2(graph: Graph) -> int:
    return reduce(
        lambda x, y: x * y,
        [
            # Note, this works for my input, because there is no path from
            # dac to fft. If there would be a path from dac to fft, the following values should
            # also be multiplied
            # search_paths(graph, "svr", "dac", {}),
            # search_paths(graph, "dac", "fft", {}),
            # search_paths(graph, "fft", "out", {}),
            search_paths(graph, "svr", "fft", {}),
            search_paths(graph, "fft", "dac", {}),
            search_paths(graph, "dac", "out", {}),
        ],
        1,
    )


def main():
    try:
        data = read_file_as_string(IN_FILE_PATH)

        graph = file_to_graph(data)

        arg = validate_and_get_arg()

        if arg == "1":
            print(part1(graph))
        else:
            print(part2(graph))

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
