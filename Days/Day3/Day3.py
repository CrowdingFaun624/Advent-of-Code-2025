import Util
from typing import Final, Sequence

class Bank():

    __slots__ = (
        "batteries",
    )

    def __init__(self, batteries: Sequence[int]) -> None:
        self.batteries: Final[Sequence[int]] = batteries

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {"".join(str(battery) for battery in self.batteries)}>"

def parse_input(file_name:str) -> Sequence[Bank]:
    with Util.get_input_path(3, file_name).open() as f:
        lines = f.readlines()
    output:list[Bank] = []
    for line in lines:
        output.append(Bank([int(character) for character in line.rstrip()]))
    return output

def get_biggest_joltage(bank:Bank, limit:int) -> int:
    # moving right is not including this battery. Moving down and right is yes including this battery.
    cache:list[list[tuple[int, int]]] = [[(0, 0)] * (len(bank.batteries) + 1) for i in range(limit + 1)]
    for index in range(len(bank.batteries) - 1, -1, -1):
        for battery_count in range(limit - 1, -1, -1):
            subvoltage, yes_length = cache[battery_count + 1][index + 1]
            joltage_when_yes = bank.batteries[index] * 10 ** yes_length + subvoltage
            joltage_when_no, no_length = cache[battery_count][index + 1]
            if joltage_when_yes > joltage_when_no:
                cache[battery_count][index] = (joltage_when_yes, yes_length + 1)
            else:
                cache[battery_count][index] = (joltage_when_no, no_length)
    return cache[0][0][0]

def main() -> None:
    banks = parse_input("input")
    print(f"Part 1: {sum(get_biggest_joltage(bank, limit =  2) for bank in banks)}")
    print(f"Part 1: {sum(get_biggest_joltage(bank, limit = 12) for bank in banks)}")
