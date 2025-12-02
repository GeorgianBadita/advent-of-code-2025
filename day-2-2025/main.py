import sys
from dataclasses import dataclass
from typing import Callable

IN_FILE_PATH = "./input.txt"


@dataclass
class Range:
    start: int
    end: int


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


def input_to_ranges(in_str: list[str]) -> list[Range]:
    return [
        Range(start=int(s.split("-")[0]), end=int(s.split("-")[1]))
        for s in in_str[0].split(",")
    ]


def is_invalid_product_id_part_one(num: int) -> bool:
    digits = str(num)
    return (
        len(digits) % 2 == 0
        and digits[: len(digits) // 2] == digits[len(digits) // 2 :]
    )


def is_invalid_product_id_part_two(num: int) -> bool:
    digits = str(num)
    for idx in range(1, len(digits) // 2 + 1):
        if len(digits) % idx != 0:
            continue

        sub_str = digits[:idx]
        all_substrs: list[str] = []
        start = idx
        for k in range(idx, len(digits), idx):
            all_substrs.append(digits[start : idx + k])
            start = idx + k

        if len(all_substrs) > 0 and set(all_substrs) == set([sub_str]):
            return True
    return False


def solve(ranges: list[Range], invalid_num: Callable[[int], bool]) -> int:
    invalid_prods = 0
    for rng in ranges:
        for num in range(rng.start, rng.end + 1):
            if invalid_num(num):
                invalid_prods += num
    return invalid_prods


def part1(ranges: list[Range]) -> int:
    return solve(ranges=ranges, invalid_num=is_invalid_product_id_part_one)


def part2(ranges: list[Range]) -> int:
    return solve(ranges=ranges, invalid_num=is_invalid_product_id_part_two)


def main():
    try:
        data = read_file_as_string(IN_FILE_PATH)

        ranges = input_to_ranges(data)

        arg = validate_and_get_arg()

        if arg == "1":
            print(part1(ranges=ranges))
        else:
            print(part2(ranges=ranges))

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
