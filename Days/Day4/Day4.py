import Util
from typing import Sequence, Final

class Grid():

    __slots__ = (
        "rolls",
        "size",
    )

    def __init__(self, rolls:list[list[bool]]) -> None:
        self.rolls:Final[list[list[bool]]] = rolls
        self.size:Final[tuple[int,int]] = (len(self.rolls[0]), len(self.rolls))

    def __getitem__(self, position:tuple[int, int]) -> bool:
        return self.rolls[position[1]][position[0]]

    def __setitem__(self, position:tuple[int, int], value:bool) -> None:
        self.rolls[position[1]][position[0]] = value

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.size[0]}×{self.size[1]}>"

    def copy(self) -> "Grid":
        return Grid([row.copy() for row in self.rolls])

    def get_neighbors(self, position:tuple[int, int]) -> Sequence[tuple[int, int]]:
        """
        Returns all eight (or less if it's on the edge) neighbors.
        """
        output:list[tuple[int, int]] = []
        x, y = position
        size_x, size_y = self.size
        if x > 0 and y > 0: # top left
            output.append((x - 1, y - 1))
        if y > 0: # top
            output.append((x, y - 1))
        if x < size_x - 1 and y > 0: # top right
            output.append((x + 1, y - 1))
        if x < size_x - 1: # right
            output.append((x + 1, y))
        if x < size_x - 1 and y < size_y - 1: # bottom right
            output.append((x + 1, y + 1))
        if y < size_y - 1: # bottom
            output.append((x, y + 1))
        if x > 0 and y < size_y - 1: # bottom left
            output.append((x - 1, y + 1))
        if x > 0: # left
            output.append((x - 1, y))
        return output

def parse_input(file_name:str|None) -> Grid:
    with Util.get_input_path(4, file_name).open() as f:
        text = f.readlines()
    return Grid([[tile == "@" for tile in row.rstrip()] for row in text])

def part_1(grid: Grid) -> tuple[int, Grid]:
    size_x, size_y = grid.size
    output:int = 0
    output_grid = grid.copy()
    for y in range(size_y):
        for x in range(size_x):
            if grid[x, y] and sum(grid[neighbor] for neighbor in grid.get_neighbors((x, y))) < 4:
                output_grid[x, y] = False
                output += 1
    return output, output_grid

def part_2(grid: Grid) -> int:
    total:int = 0
    while True:
        removed, grid = part_1(grid)
        total += removed
        if removed == 0:
            break
    return total

def main() -> None:
    grid = parse_input("input")
    print(f"Part 1: {part_1(grid)[0]}")
    print(f"Part 2: {part_2(grid)}")
