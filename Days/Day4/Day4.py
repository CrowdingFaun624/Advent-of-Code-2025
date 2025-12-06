from collections import deque
import Util
from typing import Sequence, Final

class Grid():

    __slots__ = (
        "rolls",
        "size_x",
        "size_y",
    )

    def __init__(self, rolls:list[list[bool]]) -> None:
        self.rolls:Final[list[list[bool]]] = rolls
        self.size_x:Final[int] = len(self.rolls[0])
        self.size_y:Final[int] = len(self.rolls)

    def __getitem__(self, position:tuple[int, int]) -> bool:
        return self.rolls[position[1]][position[0]]

    def __setitem__(self, position:tuple[int, int], value:bool) -> None:
        self.rolls[position[1]][position[0]] = value

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.size_x}×{self.size_y}>"

    def copy(self) -> "Grid":
        return Grid([row.copy() for row in self.rolls])

    def get_neighbors(self, x:int, y:int) -> Sequence[tuple[int, int]]:
        """
        Returns all eight (or less if it's on the edge) neighbors.
        """
        output:list[tuple[int, int]] = []
        if x > 0 and y > 0: # top left
            output.append((x - 1, y - 1))
        if y > 0: # top
            output.append((x, y - 1))
        if x < self.size_x - 1 and y > 0: # top right
            output.append((x + 1, y - 1))
        if x < self.size_x - 1: # right
            output.append((x + 1, y))
        if x < self.size_x - 1 and y < self.size_y - 1: # bottom right
            output.append((x + 1, y + 1))
        if y < self.size_y - 1: # bottom
            output.append((x, y + 1))
        if x > 0 and y < self.size_y - 1: # bottom left
            output.append((x - 1, y + 1))
        if x > 0: # left
            output.append((x - 1, y))
        return output

def parse_input(file_name:str|None) -> Grid:
    with Util.get_input_path(4, file_name).open() as f:
        text = f.readlines()
    return Grid([[tile == "@" for tile in row.rstrip()] for row in text])

def part_1(grid: Grid) -> tuple[int, Grid]:
    output:int = 0
    output_grid = grid.copy()
    for y in range(grid.size_y):
        for x in range(grid.size_x):
            if grid[x, y] and sum(grid[neighbor] for neighbor in grid.get_neighbors(x, y)) < 4:
                output_grid[x, y] = False
                output += 1
    return output, output_grid

def part_2(grid: Grid) -> int:
    neighbors:list[list[int]] = [
        [
            sum( # find the count of neighbors for (x, y)
                grid[x + dx, y + dy]
                for dy in range(-1, 2)
                for dx in range(-1, 2)
                if (dx != 0 or dy != 0) and x + dx >= 0 and x + dx < grid.size_x and y + dy >= 0 and y + dy < grid.size_y
            )
            for x in range(grid.size_x) # for each tile
        ]
        for y in range(grid.size_y)
    ]
    has_been_queued:list[list[bool]] = [[False] * grid.size_x for i in range(grid.size_y)]
    total:int = 0
    max_length:int = 0
    queue:deque[tuple[int, int]] = deque()
    # add all rolls that have less than four neighbors.
    for y in range(grid.size_y):
        for x in range(grid.size_x):
            if grid[x, y] and neighbors[y][x] < 4:
                has_been_queued[y][x] = True
                queue.append((x, y))
    while True:
        if len(queue) == 0:
            break
        x, y = queue.popleft()
        if not grid[x, y]: continue # if it hasn't already been consumed before.
        total += 1
        grid[x, y] = False

        # add neighbors to queue
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0 or x + dx < 0 or x + dx >= grid.size_x or y + dy < 0 or y + dy >= grid.size_y or not grid[x + dx, y + dy]:
                    continue
                neighbors[y + dy][x + dx] -= 1
                if neighbors[y + dy][x + dx] < 4 and not has_been_queued[y + dy][x + dx]:
                    queue.append((x + dx, y + dy))
                    has_been_queued[y + dy][x + dx] = True
        max_length = max(max_length, len(queue))
    return total

def main() -> None:
    grid = parse_input("input")
    print(f"Part 1: {part_1(grid)[0]}")
    print(f"Part 2: {part_2(grid)}")
