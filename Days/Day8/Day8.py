import Util
from collections import deque
from typing import Final, Sequence

class Box():

    __slots__ = ("index", "x", "y", "z")

    def __init__(self, x:int, y:int, z:int, index:int) -> None:
        self.x:Final[int] = x
        self.y:Final[int] = y
        self.z:Final[int] = z
        self.index:Final[int] = index

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.x}, {self.y}, {self.z}>"

    def square_distance(self, other:"Box") -> int:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2

def parse_input(file_name:str|None) -> tuple[int, Sequence[Box]]:
    # I added the first line to be the number of connections.
    with Util.get_input_path(8, file_name).open() as f:
        lines = f.readlines()
    connections:int = int(lines.pop(0).rstrip("\n"))
    boxes:list[Box] = []
    for index, line in enumerate(lines):
        x, y, z = line.rstrip("\n").split(",", maxsplit=2)
        boxes.append(Box(int(x), int(y), int(z), index))
    return connections, boxes

def get_distances(boxes:Sequence[Box]) -> Sequence[tuple[int, Box, Box]]:
    return sorted(
        ((box1.square_distance(box2), box1, box2) for index, box1 in enumerate(boxes) for box2 in boxes[index + 1:]),
        key=lambda item: item[0]
    )

def get_circuit(start_box:Box, connections:Sequence[Sequence[Box]]) -> Sequence[Box]: # gets the circuit that `box` is in.
    queue = deque([start_box])
    explored_boxes:set[Box] = set()
    output:list[Box] = []
    while len(queue) > 0:
        box = queue.popleft()
        if box in explored_boxes: continue
        explored_boxes.add(box)
        output.append(box)
        queue.extend(connection for connection in connections[box.index] if connection not in explored_boxes)
    return output

def get_circuits(boxes:Sequence[Box], connections:list[list[Box]]) -> Sequence[Sequence[Box]]:
    circuits:list[Sequence[Box]] = []
    explored_boxes:list[bool] = [False] * len(boxes)
    for box in boxes:
        if explored_boxes[box.index]: continue
        circuit = get_circuit(box, connections)
        for subbox in circuit:
            explored_boxes[subbox.index] = True
        circuits.append(circuit)
    circuits.sort(key=lambda circuit: len(circuit))
    return circuits

def part_1(boxes:Sequence[Box], distances:Sequence[tuple[int, Box, Box]]) -> int:
    connections:list[list[Box]] = [[] for i in range(len(boxes))]
    for _, box1, box2 in distances:
        connections[box1.index].append(box2)
        connections[box2.index].append(box1)
    circuits = get_circuits(boxes, connections)
    return len(circuits[-1]) * len(circuits[-2]) * len(circuits[-3])

def part_2(boxes:Sequence[Box], distances:Sequence[tuple[int, Box, Box]]) -> int:
    connections:list[list[Box]] = [[] for i in range(len(boxes))]
    for _, box1, box2 in distances:
        connections[box1.index].append(box2)
        connections[box2.index].append(box1)
        circuit_count = len(get_circuits(boxes, connections))
        if circuit_count == 1:
            return box1.x * box2.x
    assert False

def main() -> None:
    connection_count, boxes = parse_input("input")
    distances:Sequence[tuple[int, Box, Box]] = get_distances(boxes)
    print(f"Part 1: {part_1(boxes, distances[:connection_count])}")
    print(f"Part 2: {part_2(boxes, distances)}")
