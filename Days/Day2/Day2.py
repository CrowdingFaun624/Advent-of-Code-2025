from functools import cache
from math import log10, floor, sqrt, ceil
import Util
from typing import Sequence

def get_strength(id:int) -> int: # short for "string length".
    return ceil(log10(id + 1))

def intpow(exponent:int) -> int:
    return int(10 ** exponent)

def increasing_sum(low:int, high:int, repeats:int, min:int, max:int) -> Sequence[int]:
    """
    In linear time, returns `[f(i) for i in range(low, high)]`
    where `f(i)` returns `i` with digits repeated `repeats` times.
    """
    return [
        repeated
        for i in range(low, high)
        if (repeated := int(str(i) * repeats)) >= min and repeated <= max
    ]

@cache
def factors(num:int) -> Sequence[tuple[int,int]]: # returns factors of num, including 1 and num.
    output:list[tuple[int,int]] = []
    for i in range(1, floor(sqrt(num)) + 1):
        div, mod = divmod(num, i)
        if mod == 0:
            if div >= 2:
                output.append((i, div))
            if i >= 2 and i != div:
                output.append((div, i))
    return output

def parse_input(file_name:str|None) -> Sequence[tuple[int,int]]:
    with Util.get_input_path(2, file_name).open() as f:
        text = f.read()
    range_strings:Sequence[str] = text.split(",") # remember to strip on \n
    output:list[tuple[int, int]] = []
    for range_string in range_strings:
        split_string = range_string.rstrip("\n").split("-")
        output.append((int(split_string[0]), int(split_string[1])))
    return output

def get_invalid_ids(first_id:int, last_id:int, only_2:bool) -> Sequence[int]:
    output:list[int] = []
    strength_first, strength_last = get_strength(first_id), get_strength(last_id)
    for strength in range(strength_first, strength_last + 1):
        for factor1, factor2 in (([(strength // 2, 2)] if strength % 2 == 0 else []) if only_2 else factors(strength)):
            if strength == strength_first and strength == strength_last: # when this strength is bounded on both sides.
                part_first = first_id // intpow(strength - factor1)
                part_last = last_id // intpow(strength - factor1)
                output.extend(increasing_sum(part_first, part_last + 1, factor2, first_id, last_id))
            elif strength == strength_first: # when this strength is bounded only by the first.
                part_first = first_id // intpow(strength - factor1)
                # part_last is just 10 ** factor1
                output.extend(increasing_sum(part_first, intpow(factor1), factor2, first_id, intpow(factor2)))
            elif strength == strength_last: # when this strength is bounded only by the last.
                # part_first is just 10 ** (factor1 - 1)
                part_last = last_id // intpow(strength - factor1)
                output.extend(increasing_sum(intpow(factor1 - 1), part_last + 1, factor2, intpow(factor2 - 1), last_id))
            else: # when this strength is bounded from neither side.
                output.extend(increasing_sum(intpow(factor1 - 1), intpow(factor1), factor2, intpow(factor2 - 1), intpow(factor2)))
    return output

def get_all_invalid_ranges(ranges:Sequence[tuple[int, int]], only_2:bool) -> Sequence[int]:
    output:list[int] = []
    for first_id, last_id in ranges:
        output.extend(get_invalid_ids(first_id, last_id, only_2=only_2))
    return output

def main() -> None:
    ranges = parse_input("example1")
    print(f"Part 1: {sum(set(get_all_invalid_ranges(ranges, only_2=True)))}")
    print(f"Part 2: {sum(set(get_all_invalid_ranges(ranges, only_2=False)))}")
