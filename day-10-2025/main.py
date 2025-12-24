import sys
from dataclasses import dataclass
import z3

IN_FILE_PATH = "./input.txt"


@dataclass
class Buttons:
    light_diagram: str
    buttons: list[list[int]]
    joltage_reqs: list[int]


def read_file_as_string(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        lines = [line.rstrip("\n") for line in file]
        return lines


def file_to_buttons(file_strs: list[str]) -> list[Buttons]:
    all_buttons: list[Buttons] = []
    for line in file_strs:
        elems = line.split(" ")
        light_diagram = elems[0][1:-1]
        buttons: list[list[int]] = []
        for btn_str in elems[1:-1]:
            buttons.append(list(map(int, btn_str[1:-1].split(","))))

        joltage_reqs_str = elems[-1][1:-1].split(",")
        joltage_reqs: list[int] = []
        for joltage_req in joltage_reqs_str:
            joltage_reqs.append(int(joltage_req))

        all_buttons.append(
            Buttons(
                light_diagram=light_diagram, buttons=buttons, joltage_reqs=joltage_reqs
            )
        )
    return all_buttons


def subsets_of_size_k(n: int, k: int, sol: list[int], sols: list[list[int]]) -> None:
    for candidate in range(0 if not sol else sol[-1] + 1, n):
        if len(sol) < k:
            sol.append(candidate)
            if len(sol) == k:
                sols.append(sol[:])

            subsets_of_size_k(n, k, sol, sols)
            sol.pop()


def combination_powers_light(comb: list[int], buttons_conf: Buttons) -> bool:
    buttons_to_apply = [buttons_conf.buttons[x] for x in comb]
    count_dict: dict[int, int] = {}
    for buttons in buttons_to_apply:
        for button in buttons:
            count_dict[button] = count_dict.get(button, 0) + 1

    light_diagram = [0 if ch == "." else 1 for ch in buttons_conf.light_diagram]
    for idx, val in enumerate(light_diagram):
        combination_parity = count_dict.get(idx, 0) % 2
        if combination_parity != val:
            return False
    return True


def part1(buttons: list[Buttons]) -> int:
    sol = 0
    for button_conf in buttons:
        k = 1
        while k < len(button_conf.buttons):
            n = len(button_conf.buttons)
            combinations: list[list[int]] = []
            subsets_of_size_k(n, k, [], combinations)
            if any(
                [combination_powers_light(comb, button_conf) for comb in combinations]
            ):
                sol += k
                break
            k += 1

        if k == len(button_conf.buttons):
            raise RuntimeError("Something is wrong")

    return sol


def part2(buttons: list[Buttons]) -> int:
    answer = 0
    for button_conf in buttons:
        b_vars = [z3.Int(f"b_{idx}") for idx in range(len(button_conf.buttons))]
        optimizer = z3.Optimize()

        optimizer.add(
            [
                z3.Sum(
                    b_vars[idx]
                    for idx, button in enumerate(button_conf.buttons)
                    if jdx in button
                )
                == joltage
                for jdx, joltage in enumerate(button_conf.joltage_reqs)
            ]
        )
        optimizer.add([b >= 0 for b in b_vars])
        optimizer.minimize(z3.Sum(b_vars))
        optimizer.check()
        model = optimizer.model()
        answer += sum(model[b].as_long() for b in b_vars)

    return answer


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

        buttons = file_to_buttons(data)

        arg = validate_and_get_arg()

        if arg == "1":
            print(part1(buttons))
        else:
            print(part2(buttons))

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
