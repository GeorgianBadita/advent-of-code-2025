import sys
from dataclasses import dataclass

IN_FILE_PATH = "./input.txt"


@dataclass
class Region:
    width: int
    height: int
    presents: list[int]

    @property
    def area(self) -> int:
        return self.width * self.height


def read_file_as_string(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        lines = [line.rstrip("\n") for line in file]
        return lines


def lines_to_regions(lines: list[str]) -> list[Region]:
    regions: list[Region] = []
    for line in lines:
        if "#" in line or "." in line:
            continue
        elif ":" in line:
            split = line.split(":")
            if split[-1] != "":
                x, y = [int(x) for x in split[0].split("x")]
                presents = [int(x) for x in split[-1].strip().split()]
                regions.append(Region(width=x, height=y, presents=presents))

    return regions


def part1(regions: list[Region]) -> int:
    answer = 0
    for reg in regions:
        if 9 * sum(reg.presents) <= reg.area:
            answer += 1
    return answer


def part2(_: list[Region]) -> int:
    raise ValueError("IT'S DONEEEE!")


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

        regions = lines_to_regions(data)

        arg = validate_and_get_arg()

        if arg == "1":
            print(part1(regions))
        else:
            print(part2(regions))
            pass

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
