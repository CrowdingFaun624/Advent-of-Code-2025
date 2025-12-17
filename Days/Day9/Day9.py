from itertools import pairwise
from typing import Sequence
import Util

def parse_input(file_name:str|None) -> Sequence[tuple[int, int]]:
    with Util.get_input_path(9, file_name).open() as f:
        lines = f.readlines()
    output:list[tuple[int, int]] = []
    for line in lines:
        string_x, _, string_y = line.rstrip("\n").partition(",")
        output.append((int(string_x), int(string_y)))
    return output

def part_1(corners:Sequence[tuple[int, int]]) -> int:
    maximum_area:int = 0
    min_x, max_x, min_y, max_y = 2<<30, 0, 2<<30, 0
    for i, (x1, y1) in enumerate(corners):
        min_x, max_x, min_y, max_y = min(min_x, x1), max(max_x, x1), min(min_y, y1), max(max_y, y1)
        for j, (x2, y2) in enumerate(corners):
            if i == j: continue
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            maximum_area = max(maximum_area, area)
    return maximum_area

def part_2(corners:Sequence[tuple[int, int]]) -> int:
    # assume that the corners are clockwise
    maximum_area:int = 0
    max_i, max_j = 0, 0
    for i, (x1, y1) in enumerate(corners):
        for j, (x2, y2) in enumerate(corners):
            if i >= j: continue
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            min_x, max_x, min_y, max_y = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
            # check that no nodes are inside of the rectangle formed by (x1, y1) and (x2, y2).
            if area > maximum_area and not any(
                x3 > min_x and x3 < max_x and y3 > min_y and y3 < max_y for x3, y3 in corners
            ) and not any( # check if lines intersect the rectangle
                all(( # `all` so that all walri are evaluated.
                    (min_x2 := min((x3 := corners[k % len(corners)][0]), (x4 := corners[l % len(corners)][0]))) > min_x,
                    (max_x2 := max(x3, x4)) < max_x,
                    (min_y2 := min((y3 := corners[k % len(corners)][1]), (y4 := corners[l % len(corners)][1]))) <= min_y,
                    (max_y2 := max(y3, y4)) >= max_y,
                )) or
                min_y2 > min_y and max_y2 < max_y and min_x2 <= min_x and max_x2 >= max_x
                for k, l in pairwise(range(0, len(corners) + 1))
            ):
                maximum_area = area
                max_i, max_j = i, j
    x1, y1 = corners[max_i]
    x2, y2 = corners[max_j]
    return maximum_area

def main() -> None:
    corners = parse_input("input")
    print(f"Part 1: {part_1(corners)}")
    print(f"Part 2: {part_2(corners)}")
