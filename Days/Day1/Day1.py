from typing import Sequence
import Util

def parse_input(file_name:str|None) -> Sequence[int]:
    with Util.get_input_path(1, file_name).open("rt") as f:
        lines = f.readlines()
    return [int(line[1:-1]) * (1 if line[0] == "R" else -1) for line in lines if not line.startswith("#")]

def get_zero_count(rotations: Sequence[int]) -> int:
    current:int = 50
    count:int = 0
    for rotation in rotations:
        current += rotation
        count += current % 100 == 0
    return count

def get_total_zero_count(rotations: Sequence[int]) -> int:
    current:int = 50
    count:int = 0
    for rotation in rotations:
        is_zero = current == 0
        new_count, current = divmod(current + rotation, 100)
        count += abs(new_count) + (0 if rotation > 0 else (-is_zero + (current == 0)))
    return count

def main() -> None:
    rotations = parse_input("input")
    print(f"Part 1: {get_zero_count(rotations)}")
    print(f"Part 2: {get_total_zero_count(rotations)}")

if __name__ == "__main__":
    main()
