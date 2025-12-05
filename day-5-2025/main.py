import sys
from dataclasses import dataclass

IN_FILE_PATH = "./input.txt"


@dataclass
class Range:
    start: int
    end: int


type Ranges = list[Range]
type RangesAndIngredients = tuple[Ranges, list[int]]


def read_file_as_string(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        lines = [line.rstrip("\n") for line in file]
        return lines


def str_to_ranges_and_ingredients(str_list: list[str]) -> RangesAndIngredients:
    empty_pos = str_list.index("")
    ranges_part = str_list[:empty_pos]
    ingredients_part = str_list[empty_pos + 1 :]

    ranges: list[Range] = []
    for rng_str in ranges_part:
        start_str, end_str = rng_str.split("-")
        ranges.append(Range(start=int(start_str.strip()), end=int(end_str.strip())))

    ingredients: list[int] = []
    for ingredient in ingredients_part:
        ingredients.append(int(ingredient.strip()))

    return ranges, ingredients


def validate_and_get_arg() -> str:
    if len(sys.argv) != 2:
        raise ValueError("Exactly one arg is expected")

    arg = sys.argv[1]

    if arg not in ["1", "2"]:
        raise ValueError(
            "Arg can only be 1 or 2 for part 1 or part 2 of the problem respectively"
        )

    return arg


def is_fresh(rngs: list[Range], ingredient: int) -> bool:
    for rng in rngs:
        if rng.start <= ingredient <= rng.end:
            return True
    return False


def can_merge_ranges(rng1: Range, rng2: Range) -> bool:
    return rng1.end >= rng2.start


def merge_ranges(rng1: Range, rng2: Range) -> Range:
    return Range(start=min(rng1.start, rng2.start), end=max(rng1.end, rng2.end))


def merge_list_ranges(rngs: list[Range]) -> list[Range]:
    rngs.sort(key=lambda x: x.start)
    merged_ranges: list[Range] = [rngs[0]]
    for idx in range(1, len(rngs)):
        if can_merge_ranges(merged_ranges[-1], rngs[idx]):
            merged_ranges[-1] = merge_ranges(merged_ranges[-1], rngs[idx])
        else:
            merged_ranges.append(rngs[idx])

    return merged_ranges


def part1(rng_and_ingredients: RangesAndIngredients) -> int:
    ranges, ingredients = rng_and_ingredients
    count = 0
    for ingredient in ingredients:
        if is_fresh(ranges, ingredient):
            count += 1
    return count


def part2(rng_and_ingredients: RangesAndIngredients) -> int:
    ranges, _ = rng_and_ingredients
    merged_ranges = merge_list_ranges(ranges)

    count = 0
    for rng in merged_ranges:
        count += rng.end - rng.start + 1
    return count


def main():
    try:
        data = read_file_as_string(IN_FILE_PATH)

        ranges_and_ingredients = str_to_ranges_and_ingredients(data)

        arg = validate_and_get_arg()

        if arg == "1":
            print(part1(ranges_and_ingredients))
        else:
            print(part2(ranges_and_ingredients))

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
