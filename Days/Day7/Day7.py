import Util
from typing import Final, Sequence, Container

class Manifold():

    __slots__ = (
        "size_x",
        "size_y",
        "start",
        "tiles",
    )

    def __init__(self, tiles:Sequence[Sequence[bool]], start:tuple[int, int]) -> None:
        self.tiles:Final[Sequence[Sequence[bool]]] = tiles
        self.start:Final[tuple[int, int]] = start
        self.size_x:Final[int] = len(self.tiles[0])
        self.size_y:Final[int] = len(self.tiles)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.size_x}×{self.size_y}>"

    def __getitem__(self, position:tuple[int, int]) -> bool:
        return self.tiles[position[1]][position[0]]

    def stringify(self, tachyons:Container[tuple[int, int]]) -> str:
        return "\n".join("".join(
            "|" if (x, y) in tachyons
            else "^" if self[x, y]
            else "S" if (x, y) == self.start
            else "."
            for x in range(self.size_x)
        ) for y in range(self.size_y))

def parse_input(file_name:str|None) -> Manifold:
    with Util.get_input_path(7, file_name).open() as f:
        lines = f.readlines()
    start:tuple[int, int]|None = None
    output:list[list[bool]] = []
    for y, line in enumerate(lines):
        row:list[bool] = []
        for x, tile in enumerate(line.rstrip("\n")):
            if tile == ".":
                row.append(False)
            elif tile == "^":
                row.append(True)
            elif tile == "S":
                start = (x, y)
                row.append(False)
            else: assert False
        output.append(row)
    assert start is not None
    return Manifold(output, start)

def part_1_2(manifold:Manifold) -> tuple[int, int]:
    splittings:int = 0
    tachyons:Sequence[int] = [manifold.start[0]]
    timelines:Sequence[int] = [1]
    # all_positions:set[tuple[int, int]] = {(manifold.start[0], manifold.start[1])}
    for y in range(manifold.start[1] + 1, manifold.size_y):
        new_tachyons:list[int] = []
        new_timelines:list[int] = []
        for x, timeline in zip(tachyons, timelines, strict=True):
            if manifold[x, y]:
                if len(new_tachyons) == 0 or new_tachyons[-1] != x - 1: # if there's not already a beam to the left
                    new_tachyons.append(x - 1)
                    new_timelines.append(timeline)
                else:
                    new_timelines[-1] += timeline
                new_tachyons.append(x + 1)
                new_timelines.append(timeline)
                splittings += 1
            elif len(new_tachyons) == 0 or new_tachyons[-1] != x: # if there's not already a beam here
                new_tachyons.append(x)
                new_timelines.append(timeline)
            else:
                new_timelines[-1] += timeline
        # all_positions.update((x, y) for x in new_tachyons)
        tachyons = new_tachyons
        timelines = new_timelines
    # print(manifold.stringify(all_positions))
    return splittings, sum(timelines)

def main() -> None:
    manifold = parse_input("input")
    splittings, timelines = part_1_2(manifold)
    print(f"Part 1: {splittings}")
    print(f"Part 1: {timelines}")
