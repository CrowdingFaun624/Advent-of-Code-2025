from functools import cache
from math import log10, ceil, sqrt
import Util
from typing import Final, Sequence

def get_strength(id:int) -> int: # short for "string length".
    # return len(str(id))
    return ceil(log10(id + 1))

def intpow(exponent:int) -> int:
    return int(10 ** exponent)

@cache
def factors(num:int) -> Sequence[tuple[int,int]]: # returns factors of num, including 1 and num.
    output:list[tuple[int,int]] = []
    for i in range(1, ceil(sqrt(num)) + 1):
        div, mod = divmod(num, i)
        if mod == 0:
            if div >= 2:
                output.append((i, div))
            if i >= 2:
                output.append((div, i))
    return output

class Range():

    __slots__ = (
        "first_id",
        "last_id",
    )

    def __init__(self, first_id:int, last_id:int) -> None:
        self.first_id:Final[int] = first_id
        self.last_id:Final[int] = last_id

    def difference(self) -> int:
        return self.last_id - self.first_id

    def get_all_first_halves(self) -> Sequence[int]:
        """
        Returns all integers such that that integer is the first half of an even-length number in this Range.
        """
        output:list[int] = []
        strength_first = get_strength(self.first_id)
        strength_last = get_strength(self.last_id)
        for strength in range(strength_first, strength_last + 1):
            if strength % 2 == 1: continue
            for digits in range(intpow(strength // 2 - 1), intpow(strength // 2)): # all two-digit numbers that don't start with 0.
                if digits * intpow(strength // 2) + intpow(strength // 2) - 1 >= self.first_id and digits * intpow(strength // 2) <= self.last_id:
                    # if there is any second half which fits in the bounds, then add these digits.
                    output.append(digits)
        return output

    def get_invalid_ids(self) -> Sequence[int]:
        output:list[int] = []
        strength_first, strength_last = get_strength(self.first_id), get_strength(self.last_id)
        if strength_first == strength_last and strength_first % 2 == 1:
            # optimization: odd-length ids are always valid.
            return ()
        for first_half in self.get_all_first_halves():
            half_strength = get_strength(first_half)
            full_id = first_half * intpow(half_strength) + first_half
            if full_id in self:
                output.append(full_id)
        return output

    def get_invalid_ids_2(self) -> Sequence[int]:
        output:list[int] = []
        for id in range(self.first_id, self.last_id + 1):
            strength = get_strength(id)
            for factor1, factor2 in factors(strength):
                piece = str(id)[:factor1]
                pieces = piece * factor2
                if id == int(pieces):
                    output.append(id)
                    break
        return output

    def __contains__(self, id:int) -> bool:
        return id >= self.first_id and id <= self.last_id

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.first_id}-{self.last_id}>"

def parse_input(file_name:str|None) -> Sequence[Range]:
    with Util.get_input_path(2, file_name).open() as f:
        text = f.read()
    range_strings:Sequence[str] = text.split(",") # remember to strip on \n
    output:list[Range] = []
    for range_string in range_strings:
        split_string = range_string.rstrip("\n").split("-")
        output.append(Range(int(split_string[0]), int(split_string[1])))
    return output

def part_1(ranges:Sequence[Range]) -> Sequence[int]:
    output:list[int] = []
    for range in ranges:
        output.extend(range.get_invalid_ids())
    return output

def part_2(ranges:Sequence[Range]) -> Sequence[int]:
    output:list[int] = []
    for range in ranges:
        output.extend(range.get_invalid_ids_2())
    # print(output)
    return output

def main() -> None:
    ranges = parse_input("input")
    print(f"Sum of differences is {sum(range.difference() for range in ranges)}")
    print(f"Part 1: {sum(part_1(ranges))}")
    print(f"Part 2: {sum(part_2(ranges))}")
