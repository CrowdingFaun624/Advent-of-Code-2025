from typing import Final, Mapping, Sequence

import Util

class Device():

    __slots__ = (
        "index",
        "name",
        "output_names",
        "outputs",
    )

    def __init__(self, name:str, index:int, outputs:Sequence[str]) -> None:
        self.name:Final[str] = name
        self.index:Final[int] = index
        self.output_names:Final[Sequence[str]] = outputs

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}: {" ".join(self.output_names)}>"

    def link(self, all_devices:Mapping[str, "Device"]) -> None:
        self.outputs = [all_devices[name] for name in self.output_names]

def parse_input(file_name: str|None) -> tuple[Device, Device, Device|None, Sequence[Device], bool]:
    """
    Returns the "out" Device, the "you" Device, the "svr" Device,
    the required Devices in part 2, and if part 2 is possible.
    """
    with Util.get_input_path(11, file_name).open() as f:
        lines = f.readlines()
    output:list[Device] = []
    device_map:dict[str, Device] = {}

    for index, line in enumerate(lines):
        name, _, outputs_string = line.rstrip("\n").partition(": ")
        outputs = outputs_string.split(" ")
        device = Device(name, index, outputs)
        output.append(device)
        device_map[name] = device

    # out device is not in the input
    assert "out" not in device_map
    out_device = Device("out", len(output), ())
    output.append(out_device)
    device_map["out"] = out_device

    for device in output:
        device.link(device_map)

    server_device = device_map.get("svr")
    part_2_possible = server_device is not None
    required_2_devices:list[Device] = []
    if (device := device_map.get("dac")) is not None:
        required_2_devices.append(device)
    else: part_2_possible = False
    if (device := device_map.get("fft")) is not None:
        required_2_devices.append(device)
    else: part_2_possible = False
    return out_device, device_map["you"], device_map.get("svr"), required_2_devices, part_2_possible

def part_1(start_device:Device, end_device:Device) -> int:
    return recursive(start_device, end_device, (), (), {})

def part_2(start_device:Device, end_device:Device, required_devices:Sequence[Device]) -> int:
    return recursive(start_device, end_device, required_devices, tuple([False] * len(required_devices)), {})

def recursive(
    current_device:Device,
    end_device:Device,
    broken_devices:Sequence[Device],
    encountered_broken:tuple[bool,...],
    cache:dict[tuple[int, tuple[bool,...]], int],
) -> int:
    if (cached_output := cache.get((current_device.index, encountered_broken))) is not None:
        return cached_output

    if current_device in broken_devices:
        new_encountered_broken_list = list(encountered_broken)
        new_encountered_broken_list[broken_devices.index(current_device)] = True
        new_encountered_broken = tuple(new_encountered_broken_list)
    else: new_encountered_broken = encountered_broken

    path_count:int
    if current_device is end_device:
        path_count = int(all(encountered_broken))
        cache[current_device.index, encountered_broken] = path_count
        return path_count
    path_count = 0
    for output in current_device.outputs:
        path_count += recursive(output, end_device, broken_devices, new_encountered_broken, cache)
    cache[current_device.index, encountered_broken] = path_count
    return path_count

def main() -> None:
    out_device, you_device, server_device, broken_devices, part_2_possible = parse_input("input")
    print(f"Part 1: {part_1(you_device, out_device)}")
    if part_2_possible and server_device is not None:
        print(f"Part 2: {part_2(server_device, out_device, broken_devices)}")
