import z3
import Util
from typing import Final, Sequence, cast

class Machine():

    __slots__ = (
        "joltages",
        "lights",
        "lights_length",
        "schematics",
        "schematics_integers",
    )

    def __init__(self, buttons:int, schematics: Sequence[Sequence[int]], schematics_integers:Sequence[int], joltages: Sequence[int], length:int) -> None:
        self.lights: Final[int] = buttons
        self.schematics: Final[Sequence[Sequence[int]]] = schematics
        self.schematics_integers: Final[Sequence[int]] = schematics_integers
        self.joltages: Final[Sequence[int]] = joltages
        self.lights_length: Final[int] = length

    def __len__(self) -> int:
        return self.lights_length

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} len {self.lights_length}>"

def parse_input(file_name:str|None) -> Sequence[Machine]:
    with Util.get_input_path(10, file_name).open() as f:
        lines = f.readlines()
    output:list[Machine] = []
    for line in lines:
        things = line.rstrip("\n").split(" ")
        buttons = sum((char == "#") << i for i, char in enumerate(things[0][1:-1]))
        schematics = [[int(item) for item in schematic_string[1:-1].split(",")] for schematic_string in things[1:-1]]
        schematics_integers = [sum(1 << int(item) for item in schematic) for schematic in schematics]
        joltages = [int(item) for item in things[-1][1:-1].split(",")]
        length = len(things[0]) - 2 # minus two for square brackets
        length2 = len(things[-1]) - 2
        output.append(Machine(buttons, schematics, schematics_integers, joltages, length))
    return output

def get_minimum_lights_presses(machine: Machine) -> int:
    output = recursive_part_1(machine, 0, 0, {})
    assert output is not None
    return output

def recursive_part_1(machine:Machine, current_lights:int, button_index:int, cache:dict[tuple[int, int], int|None]) -> int|None:
    if current_lights == machine.lights:
        return 0
    if button_index >= len(machine.schematics_integers):
        return None
    if (cached_output := cache.get((current_lights, button_index), ...)) is not ...:
        return cached_output
    yes_presses = recursive_part_1(machine, current_lights ^ machine.schematics_integers[button_index], button_index + 1, cache)
    if yes_presses is not None: yes_presses += 1
    no_presses = recursive_part_1(machine, current_lights, button_index + 1, cache)
    if yes_presses is not None and no_presses is not None:
        output = min(yes_presses, no_presses)
    elif yes_presses is None:
        output = no_presses
    elif no_presses is None:
        output = yes_presses
    else: output = None
    cache[current_lights, button_index] = output
    return output

def get_minimum_joltage_presses(machine: Machine) -> int:
    # what the heck is this linear algebra. Non-square. Not doing that.
    button_variables:Sequence[z3.ArithRef] = [z3.Int(f"x{str(index).zfill(len(machine.schematics))}") for index in range(len(machine.schematics))]
    buttons:Sequence[Sequence[z3.ArithRef]] = [[] for counter in machine.joltages]
    for schematic, variable in zip(machine.schematics, button_variables, strict=True):
        for counter in schematic:
            buttons[counter].append(variable)
    joltage_conditions:Sequence[z3.BoolRef|bool] = [z3.Sum(*variables) == joltage for variables, joltage in zip(buttons, machine.joltages, strict=True)]
    positive_conditions:Sequence[z3.BoolRef] = [variable >= 0 for variable in button_variables]
    solver = z3.Solver()
    minimum_sum: int|None = None
    while True:
        solver.add(*joltage_conditions, *positive_conditions)
        if minimum_sum is not None:
            solver.add(z3.Sum(*button_variables) < minimum_sum) # minimize
        result = solver.check()
        if result.r == z3.Z3_L_FALSE:
            break
        model = solver.model()
        last_sum = sum(cast(z3.IntNumRef, model[variable]).as_long() for variable in button_variables)
        minimum_sum = last_sum if minimum_sum is None else min(minimum_sum, last_sum)
    assert minimum_sum is not None
    return minimum_sum

def main() -> None:
    machines = parse_input("input")
    print(f"Part 1: {sum(get_minimum_lights_presses(machine) for machine in machines)}")
    print(f"Part 2: {sum(get_minimum_joltage_presses(machine) for machine in machines)}")
