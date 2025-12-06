import sys
from typing import Callable
from functools import reduce

IN_FILE_PATH = "./input.txt"

type Problem = tuple[list[int], Callable[[list[int]], int]]


def mul(nums: list[int]) -> int:
    return reduce(lambda x, y: x * y, nums, 1)


def add(nums: list[int]) -> int:
    return reduce(lambda x, y: x + y, nums, 0)


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


def parse_string_to_problem_part1(str_list: list[str]) -> list[Problem]:
    signs = list(filter(lambda x: x != " " and x != "", str_list[-1]))
    problems: list[Problem] = []

    all_numbers: list[list[int]] = []
    for nums in str_list[:-1]:
        numbers_str = nums.split(" ")
        nums_list = [
            int(n.strip()) for n in filter(lambda x: x != " " and x != "", numbers_str)
        ]
        all_numbers.append(nums_list)

    for c in range(len(all_numbers[0])):
        nums_for_problem: list[int] = []
        for r in range(len(all_numbers)):
            nums_for_problem.append(all_numbers[r][c])

        if signs[c].strip() == "*":
            func = mul
        else:
            func = add

        problems.append((nums_for_problem, func))

    return problems


def parse_string_to_problem_part2(str_list: list[str]) -> list[Problem]:
    signs = list(filter(lambda x: x != " " and x != "", str_list[-1]))
    problems: list[Problem] = []

    all_numbers: list[list[str]] = []
    for nums in str_list[:-1]:
        final_num_list: list[str] = []
        for c in nums:
            final_num_list.append(c)
        all_numbers.append(final_num_list)

    start_col = len(all_numbers[0]) - 1
    while start_col >= 0:
        numbers_for_now: list[int] = []
        has_num: bool = True
        while start_col >= 0 and has_num:
            has_num = False
            num = 0
            for row in range(len(all_numbers)):
                if all_numbers[row][start_col] != " ":
                    dig = int(all_numbers[row][start_col])
                    num = num * 10 + dig
                    has_num = True
            if not has_num:
                start_col -= 1
                break

            numbers_for_now.append(num)
            start_col -= 1

        curr_sign = signs.pop()
        problems.append(((numbers_for_now), mul if curr_sign == "*" else add))

    return problems


def solve(problems: list[Problem]) -> int:
    return sum([f(lst) for lst, f in problems])


def main():
    try:
        data = read_file_as_string(IN_FILE_PATH)

        arg = validate_and_get_arg()

        if arg == "1":
            print(solve(parse_string_to_problem_part1(data)))
        else:
            print(solve(parse_string_to_problem_part2(data)))

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
