import Util
from typing import Final, Sequence

class Database():

    __slots__ = (
        "available_ids",
        "fresh_ranges",
    )

    def __init__(self, fresh_ranges: Sequence[tuple[int, int]], available_ids:Sequence[int]) -> None:
        self.fresh_ranges:Final[Sequence[tuple[int, int]]] = fresh_ranges
        self.available_ids:Final[Sequence[int]] = available_ids

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {len(self.available_ids)}>"

def parse_input(file_name:str|None) -> Database:
    with Util.get_input_path(5, file_name).open() as f:
        text = f.read()
    fresh_text, available_text = text.split("\n\n")
    fresh_ranges:Sequence[tuple[int,int]] = [tuple(int(item) for item in line.split("-")) for line in fresh_text.split("\n")] # type: ignore
    available_ids = [int(line) for line in available_text.split("\n")]
    return Database(fresh_ranges, available_ids)

def part_1(database: Database) -> int:
    output:int = 0
    for id in database.available_ids:
        for range in database.fresh_ranges:
            if id >= range[0] and id <= range[1]:
                output += 1
                break
    return output

def part_2(database: Database) -> int:
    # no range in pile_ranges overlaps with another.
    pile_ranges:Sequence[tuple[int, int]] = []
    for range in database.fresh_ranges:
        new_pile_ranges:list[tuple[int, int]] = []
        minimum, maximum = range
        for pile_range in pile_ranges:
            if pile_range[0] > maximum or pile_range[1] < minimum:
                # if the whole pile range is to the right or left of the range
                new_pile_ranges.append(pile_range)
                continue
            # the two below if statements can both run (or only one, or none)
            if pile_range[1] > maximum:
                # if the pile range is on top of the right edge of the range
                maximum = pile_range[1]
            if pile_range[0] < minimum:
                # if the pile range is on top of the left edge of the range
                minimum = pile_range[0]
            # if nothing above was triggered, then pile_range is contained entirely within range
            # and does not need to be added.
        new_pile_ranges.append((minimum, maximum))
        pile_ranges = new_pile_ranges
    return sum(range[1] - range[0] + 1 for range in pile_ranges)

def main() -> None:
    database = parse_input("input")
    print(f"Part 1: {part_1(database)}")
    print(f"Part 2: {part_2(database)}")
