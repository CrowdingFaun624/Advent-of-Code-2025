from typing import Final, Sequence

import Util


class Present():

    __slots__ = (
        "area",
        "configurations",
        "index",
        "size",
    )

    def __init__(self, configurations:Sequence[tuple[Sequence[int], int, int]], area:int, size:int, index:int) -> None:
        self.configurations: Final[Sequence[tuple[Sequence[int], int, int]]] = configurations
        self.area: Final[int] = area
        self.size: Final[int] = size
        self.index: Final[int] = index

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.index}>"

    @classmethod
    def rotate(cls, grid:Sequence[Sequence[bool]], size:int) -> Sequence[Sequence[bool]]:
        return [
            [
                grid[x][size - y - 1] for x in range(size)
            ]
            for y in range(size)
        ]

    @classmethod
    def flip(cls, grid:Sequence[Sequence[bool]], size:int) -> Sequence[Sequence[bool]]:
        return [
            [
                grid[y][size - x - 1] for x in range(size)
            ]
            for y in range(size)
        ]

    @classmethod
    def integify_grid(cls, grid:Sequence[Sequence[bool]]) -> Sequence[int]:
        return [sum(cell << index for index, cell in enumerate(row)) for row in grid]

    @classmethod
    def get_size(cls, grid:Sequence[Sequence[bool]], size:int) -> tuple[int, int]:
        max_width:int = size
        while max_width > 0:
            if not any(grid[y][max_width - 1] for y in range(size)):
                max_width -= 1
            else: break
        max_height:int = size
        while max_height > 0:
            if not any(grid[max_height - 1]):
                max_height -= 1
            else: break
        return max_width, max_height

    @classmethod
    def evaluate_configurations(cls, grid:Sequence[Sequence[bool]], size:int) -> tuple[Sequence[tuple[Sequence[int], int, int]], int]:
        output:list[tuple[Sequence[int], int, int]] = []
        output.append((cls.integify_grid(grid), *cls.get_size(grid, size)))
        rotation1 = cls.rotate(grid, size)
        if rotation1 not in output:
            output.append((cls.integify_grid(rotation1), *cls.get_size(rotation1, size)))
        rotation2 = cls.rotate(rotation1, size)
        if rotation2 not in output:
            output.append((cls.integify_grid(rotation2), *cls.get_size(rotation2, size)))
        rotation3 = cls.rotate(rotation2, size)
        if rotation3 not in output:
            output.append((cls.integify_grid(rotation3), *cls.get_size(rotation3, size)))
        flip0 = cls.flip(grid, size)
        if flip0 not in output:
            output.append((cls.integify_grid(flip0), *cls.get_size(flip0, size)))
        flip1 = cls.rotate(flip0, size)
        if flip1 not in output:
            output.append((cls.integify_grid(flip1), *cls.get_size(flip1, size)))
        flip2 = cls.rotate(flip1, size)
        if flip2 not in output:
            output.append((cls.integify_grid(flip2), *cls.get_size(flip2, size)))
        flip3 = cls.rotate(flip2, size)
        if flip3 not in output:
            output.append((cls.integify_grid(flip3), *cls.get_size(flip3, size)))
        area:int = sum(cell for row in grid for cell in row)
        return output, area

class Region():

    __slots__ = (
        "counts",
        "size_x",
        "size_y",
    )

    def __init__(self, size_x:int, size_y:int, counts:Sequence[int]) -> None:
        self.size_x: Final[int] = size_x
        self.size_y: Final[int] = size_y
        self.counts: Sequence[int] = counts

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.size_x}x{self.size_y}: {" ".join(str(count) for count in self.counts)}>"

    def print_tree(self, tree:int) -> None:
        print("\n".join("".join("." if tree & (1 << x + self.size_x * y) == 0 else "#" for x in range(self.size_x)) for y in range(self.size_y)), "\n")

def parse_input(file_name:str|None) -> tuple[Sequence["Present"], Sequence[Region]]:
    with Util.get_input_path(12, file_name).open() as f:
        text = f.read()
    presents_text = text.split("\n\n")
    regions_text = presents_text.pop(-1)

    presents:list[Present] = []
    for index, present_text in enumerate(presents_text):
        present_lines = present_text.splitlines()
        assert index == int(present_lines[0][:-1])
        size = len(present_lines) - 1 # assume square present
        # I could also assume size == 3, but I won't. Heheheee.
        grid:Sequence[Sequence[bool]] = [[present_lines[row + 1][column] == "#" for column in range(size)] for row in range(size)]
        configurations, area = Present.evaluate_configurations(grid, size)
        presents.append(Present(configurations, area, size, index))

    regions:list[Region] = []
    for region_line in regions_text.splitlines():
        size_string, _, indices_string = region_line.partition(": ")
        size_x_string, _, size_y_string = size_string.partition("x")
        size_x, size_y = int(size_x_string), int(size_y_string)
        counts = [int(index) for index in indices_string.split(" ")]
        regions.append(Region(size_x, size_y, counts))

    return presents, regions

def region_can_fit(presents:Sequence[Present], region: Region) -> bool:
    presents_simple:Sequence[Sequence[tuple[int, int, int]]] = [
        [
            (sum(row << (region.size_x * y) for y, row in enumerate(configuration)), size_x, size_y)
            for configuration, size_x, size_y in present.configurations
        ]
        for present in presents
    ]

    # shortcuts
    total_present_area = sum(present.area * count for present, count in zip(presents, region.counts, strict=True))
    if total_present_area <= region.size_x * region.size_y:
        return True

    output = recursive(presents_simple, tuple(region.counts), 0, region, set())
    return output

def recursive(
    presents: Sequence[Sequence[tuple[int, int, int]]],
    presents_remaining:tuple[int,...],
    tree:int,
    region: Region,
    cache:set[tuple[tuple[int,...], int]],
) -> bool:

    present: Sequence[tuple[int, int, int]]
    for index, remaining in enumerate(presents_remaining):
        if remaining != 0:
            present = presents[index]
            new_remaining:tuple[int,...] = tuple(remaining - (index == index) for index, remaining in enumerate(presents_remaining))
            break
    else: return True

    if (presents_remaining, tree) in cache:
        return False

    for configuration, size_x, size_y in present:
        for present_y in range(region.size_y - size_y + 1):
            for present_x in range(region.size_x - size_x + 1):
                region_int = configuration << (present_x + region.size_x * present_y)
                if tree & region_int != 0:
                    continue # If there are any overlaps

                new_tree:int = tree | region_int
                output = recursive(presents, new_remaining, new_tree, region, cache)
                cache.add((presents_remaining, tree))
                if output: return output

    cache.add((presents_remaining, tree))
    return False

def main() -> None:
    presents, regions = parse_input("input")
    print(f"Part 1: {sum(region_can_fit(presents, region) for region in regions)}")
