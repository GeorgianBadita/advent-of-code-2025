import sys
from dataclasses import dataclass

IN_FILE_PATH = "./input.txt"


@dataclass
class Point:
    x: int | float
    y: int | float


def read_file_as_string(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        lines = [line.rstrip("\n") for line in file]
        return lines


def str_list_to_points(strings: list[str]) -> list[Point]:
    points: list[Point] = []
    for row in strings:
        x_str, y_str = row.split(",")
        points.append(Point(x=int(x_str.strip()), y=int(y_str.strip())))
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


def calc_area(p1: Point, p2: Point) -> int | float:
    return (abs(p2.x - p1.x) + 1) * (abs(p2.y - p1.y) + 1)


def part1(points: list[Point]) -> int | float:
    largest_area = 0
    for idx in range(len(points)):
        for jdx in range(idx + 1, len(points)):
            largest_area = max(largest_area, calc_area(points[idx], points[jdx]))

    return largest_area


def is_inside(p: Point, poly: list[Point]):
    x, y = (p.x, p.y)
    n = len(poly)
    inside = False
    p1x, p1y = poly[0].x, poly[0].y

    for i in range(n + 1):
        p2x, p2y = poly[i % n].x, poly[i % n].y
        if min(p1x, p2x) <= x <= max(p1x, p2x) and min(p1y, p2y) <= y <= max(p1y, p2y):
            if p1x == p2x or p1y == p2y:
                return True
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        x_intersection = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= x_intersection:
                            inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def is_contained(p1: Point, p2: Point, poly: list[Point]) -> bool:
    x_min, x_max = min(p1.x, p2.x), max(p1.x, p2.x)
    y_min, y_max = min(p1.y, p2.y), max(p1.y, p2.y)

    if not is_inside(Point(x=(x_min + x_max) / 2, y=(y_min + y_max) / 2), poly):
        return False

    n = len(poly)
    for i in range(n):
        v1 = poly[i]
        v2 = poly[(i + 1) % n]

        seg_x_min, seg_x_max = min(v1.x, v2.x), max(v1.x, v2.x)
        seg_y_min, seg_y_max = min(v1.y, v2.y), max(v1.y, v2.y)

        overlap_x = max(x_min, seg_x_min) < min(x_max, seg_x_max)
        overlap_y = max(y_min, seg_y_min) < min(y_max, seg_y_max)

        if v1.x == v2.x:
            if x_min < v1.x < x_max and overlap_y:
                return False
        elif v1.y == v2.y:
            if y_min < v1.y < y_max and overlap_x:
                return False

    return True


def part2(points: list[Point]) -> int | float:
    largest_area = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p1, p2 = points[i], points[j]

            if is_contained(p1, p2, points):
                largest_area = max(largest_area, calc_area(p1, p2))
    return largest_area


def main():
    try:
        data = read_file_as_string(IN_FILE_PATH)

        points = str_list_to_points(data)

        arg = validate_and_get_arg()

        if arg == "1":
            print(part1(points))
        else:
            print(part2(points))

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
