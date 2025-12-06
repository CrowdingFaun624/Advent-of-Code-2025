import Util
from functools import reduce
from typing import Callable, Sequence
from operator import add, mul

def remove_spaces(line:str) -> str: # removes all double-spaces
    while "  " in line:
        line = line.replace("  ", " ")
    return line.strip()

def parse_input(file_name:str|None) -> Sequence[tuple[Sequence[str], Callable[[int, int], int], int]]:
    with Util.get_input_path(6, file_name).open() as f:
        text = f.read()
    lines = text.rstrip("\n").split("\n")
    cells:list[str] = [""] * len(lines)
    columns:list[list[str]] = []
    for index in range(len(lines[0])):
        if all(line[index] == " " for line in lines):
            columns.append(cells)
            cells = [""] * len(lines)
        else:
            for (i, line) in enumerate(lines):
                cells[i] += line[index]
    columns.append(cells)
    output:list[tuple[list[str], Callable[[int, int], int], int]] = []
    for column in columns:
        cells = column[:-1]
        operator_string = column[-1].strip()
        operator = add if operator_string == "+" else mul
        initial = 0 if operator_string == "+" else 1
        output.append((cells, operator, initial))
    return output

def part_1(data: Sequence[tuple[Sequence[str], Callable[[int, int], int], int]]) -> int:
    return sum(reduce(operator, (int(cell.strip()) for cell in cells), initial) for cells, operator, initial in data)

def part_2(data: Sequence[tuple[Sequence[str], Callable[[int, int], int], int]]) -> int:
    return sum(reduce(operator, (int("".join(number).strip()) for number in list(zip(*cells))), initial) for cells, operator, initial in data)

def main() -> None:
    data = parse_input("input")
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
