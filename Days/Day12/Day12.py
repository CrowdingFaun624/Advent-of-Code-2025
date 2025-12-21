from typing import Sequence

import Util

def parse_input(file_name:str|None) -> tuple[Sequence[int], Sequence[tuple[int, int, Sequence[int]]]]:
    with Util.get_input_path(12, file_name).open() as f:
        text = f.read()
    presents_text = text.split("\n\n")
    regions_text = presents_text.pop(-1)

    areas:list[int] = [present_text.count("#") for present_text in presents_text]

    regions:list[tuple[int, int, Sequence[int]]] = []
    for region_line in regions_text.splitlines():
        size_string, _, indices_string = region_line.partition(": ")
        size_x_string, _, size_y_string = size_string.partition("x")
        size_x, size_y = int(size_x_string), int(size_y_string)
        counts = [int(index) for index in indices_string.split(" ")]
        regions.append((size_x, size_y, counts))

    return areas, regions

def main() -> None:
    areas, regions = parse_input("input")
    print(f"Part 1: {sum(
        sum(area * count for area, count in zip(areas, counts, strict=True)) <= size_x * size_y
        for size_x, size_y, counts in regions
    )}")
