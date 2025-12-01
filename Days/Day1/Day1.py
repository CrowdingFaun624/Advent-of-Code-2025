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
    # absolutely diabolical
    current:int = 50
    count:int = 0
    for rotation in rotations:
        sign, value = (-1 if rotation < 0 else 1), abs(rotation)
        for i in range(value):
            current += sign
            if current % 100 == 0:
                count += 1
    return count

def test(id: int, rotations:Sequence[int], expected: int) -> None:
    if (value := get_total_zero_count(rotations)) != expected:
        print(f"Test {id} failed; expected {expected} but got {value}")

def main() -> None:
    rotations = parse_input("input")
    count = get_zero_count(rotations)
    print(f"Part 1: {count}")
    count = get_total_zero_count(rotations)
    print(f"Part 2: {count}")

if __name__ == "__main__":
    main()
