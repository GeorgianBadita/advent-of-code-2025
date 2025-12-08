import sys

IN_FILE_PATH = "./input.txt"

type Point = tuple[int, int]


def read_file_as_string(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        lines = [line.rstrip("\n") for line in file]
        return lines


def validate_and_get_arg() -> str:
    if len(sys.argv) != 2:
        raise ValueError("Exactly one arg is expected")

    arg = sys.argv[1]

    if arg not in ["1", "2"]:
        raise ValueError(
            "Arg can only be 1 or 2 for part 1 or part 2 of the problem respectively"
        )

    return arg


def find_s_coords(matrix: list[list[str]]) -> Point:
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if matrix[r][c] == "S":
                return (r, c)

    raise ValueError("Could not find Start coords")


def valid_coord(point: Point, matrix: list[list[str]]) -> bool:
    return (
        point[0] >= 0
        and point[0] < len(matrix)
        and point[1] >= 0
        and point[1] < len(matrix[0])
    )


def part1(start: Point, matrix: list[list[str]]) -> int:
    queue = [start]
    count = 0
    while queue:
        node = queue.pop()
        neighbour = (node[0] + 1, node[1])
        if valid_coord(neighbour, matrix) and matrix[neighbour[0]][neighbour[1]] != "|":
            if matrix[neighbour[0]][neighbour[1]] == ".":
                matrix[neighbour[0]][neighbour[1]] = "|"
                queue.append(neighbour)
            elif matrix[neighbour[0]][neighbour[1]] == "^":
                left_neighbour = (neighbour[0], neighbour[1] - 1)
                right_neighbour = (neighbour[0], neighbour[1] + 1)
                count += 1
                queue.append(left_neighbour)
                queue.append(right_neighbour)
                matrix[left_neighbour[0]][left_neighbour[1]] = "|"
                matrix[right_neighbour[0]][right_neighbour[1]] = "|"

    return count


def part2(node: Point, matrix: list[list[str]]) -> int:
    dp = [[0] * len(matrix[0]) for _ in range(len(matrix))]

    start_r, start_c = node
    dp[start_r + 1][start_c] = 1

    for r in range(1, len(matrix) - 1):
        for c in range(len(matrix[0])):
            if dp[r][c] > 0:
                if matrix[r][c] == ".":
                    next_r, next_c = r + 1, c
                    if valid_coord((next_r, next_c), matrix):
                        dp[next_r][next_c] += dp[r][c]
                elif matrix[r][c] == "^":
                    left_r, left_c = r + 1, c - 1
                    if valid_coord((left_r, left_c), matrix):
                        dp[left_r][left_c] += dp[r][c]

                    right_r, right_c = r + 1, c + 1
                    if valid_coord((right_r, right_c), matrix):
                        dp[right_r][right_c] += dp[r][c]

    return sum(dp[-1])


def main():
    try:
        matrix = [list(row) for row in read_file_as_string(IN_FILE_PATH)]
        start = find_s_coords(matrix)
        arg = validate_and_get_arg()

        if arg == "1":
            print(part1(start, matrix))
        else:
            print(part2(start, matrix))

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
