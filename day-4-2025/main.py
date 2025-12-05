import sys

IN_FILE_PATH = "./input.txt"


DX: list[int] = [-1, -1, 0, 1, 1, 1, 0, -1]
DY: list[int] = [0, 1, 1, 1, 0, -1, -1, -1]


def read_file_as_string(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        lines = [line.rstrip("\n") for line in file]
        return lines


def str_list_to_matrix(row_list: list[str]) -> list[list[str]]:
    return list([list(x) for x in row_list])


def validate_and_get_arg() -> str:
    if len(sys.argv) != 2:
        raise ValueError("Exactly one arg is expected")

    arg = sys.argv[1]

    if arg not in ["1", "2"]:
        raise ValueError(
            "Arg can only be 1 or 2 for part 1 or part 2 of the problem respectively"
        )

    return arg


def valid_pos(r: int, c: int, matrix: list[list[str]]) -> bool:
    return r >= 0 and r < len(matrix) and c >= 0 and c < len(matrix[0])


def count_neighbouring_rolls(r: int, c: int, matrix: list[list[str]]) -> int:
    count = 0
    for idx in range(len(DX)):
        new_r = r + DX[idx]
        new_c = c + DY[idx]
        if valid_pos(new_r, new_c, matrix) and matrix[new_r][new_c] == "@":
            count += 1
    return count


def count_availalbe_rolls_and_remove(
    matrix: list[list[str]],
) -> tuple[list[list[str]], int, bool]:
    pts: list[tuple[int, int]] = []
    count = 0
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if matrix[r][c] == "@" and count_neighbouring_rolls(r, c, matrix) < 4:
                pts.append((r, c))
                count += 1

    for r, c in pts:
        matrix[r][c] = "."
    return matrix, count, count > 0


def part1(matrix: list[list[str]]) -> int:
    _, count, __ = count_availalbe_rolls_and_remove(matrix)
    return count


def part2(matrix: list[list[str]]) -> int:
    total_count = 0
    new_matrix, count, can_still_access = count_availalbe_rolls_and_remove(matrix)
    while can_still_access:
        total_count += count
        matrix = new_matrix
        new_matrix, count, can_still_access = count_availalbe_rolls_and_remove(matrix)
    return total_count


def main():
    try:
        data = read_file_as_string(IN_FILE_PATH)

        matrix = str_list_to_matrix(data)

        arg = validate_and_get_arg()

        if arg == "1":
            print(part1(matrix))
        else:
            print(part2(matrix))

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
