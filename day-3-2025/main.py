import sys

IN_FILE_PATH = "./input.txt"


def read_file_as_string(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        lines = [line.rstrip("\n") for line in file]
        return lines


def string_to_dig_list(str_list: list[str]) -> list[list[int]]:
    return [[int(d) for d in row] for row in str_list]


def max_array_from_right(nums: list[int]) -> list[int]:
    maxes = [-100] * (len(nums) + 1)
    for idx in range(len(nums) - 1, -1, -1):
        maxes[idx] = max(nums[idx], maxes[idx + 1])
    return maxes


def find_biggest_joltage(nums: list[int]) -> int:
    maxes = max_array_from_right(nums)
    best = 0
    for idx, num in enumerate(nums):
        best_num_at_idx = num * 10 + maxes[idx + 1]
        best = max(best, best_num_at_idx)
    return best


def part1(nums_list: list[list[int]]) -> int:
    return sum([find_biggest_joltage(nums) for nums in nums_list])


def find_biggest_joltage_part2(nums: list[int]) -> int:
    L = len(nums)
    N = 12

    res = 0
    start_idx = 0

    for i in range(N):
        end_idx = L - (N - 1 - i)
        max_digit = -1
        max_idx = -1

        for current_idx in range(start_idx, end_idx):
            current_digit = nums[current_idx]
            if current_digit > max_digit:
                max_digit = current_digit
                max_idx = current_idx
            if max_digit == 9:
                break

        res = res * 10 + max_digit
        start_idx = max_idx + 1

    return res


def part2(nums_list: list[list[int]]) -> int:
    return sum([find_biggest_joltage_part2(nums) for nums in nums_list])


def validate_and_get_arg() -> str:
    if len(sys.argv) != 2:
        raise ValueError("Exactly one arg is expected")

    arg = sys.argv[1]

    if arg not in ["1", "2"]:
        raise ValueError(
            "Arg can only be 1 or 2 for part 1 or part 2 of the problem respectively"
        )

    return arg


def main():
    try:
        data = read_file_as_string(IN_FILE_PATH)

        nums_list = string_to_dig_list(data)

        arg = validate_and_get_arg()

        if arg == "1":
            print(part1(nums_list))
        else:
            print(part2(nums_list))

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
