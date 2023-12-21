import argparse
import os
import re
from logging import Logger
from pathlib import Path
from typing import List

from utils.error import Day5Exception
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY5_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day5() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day5 = parser.add_argument_group("day5", "Solution for day5.")
    day5.add_argument(
        "--data-day5", type=Path, help="data to decode", default=DEFAULT_DAY5_DATA
    )
    return parser


class Correspondance:
    def __init__(self, correspondance: List[str]) -> None:
        self.source = int(correspondance[1])
        self.destination = int(correspondance[0])
        self.range_lenght = int(correspondance[2])

    def apply(self, old_object: List[range], new_object: List[range]) -> None:
        old_object_to_remove: List[range] = []
        old_object_to_extend: List[range] = []
        for my_object in old_object:
            # If the first element of the range is higher than the end of the correspondance
            # S....E...[object]
            # or the last element of the range is lesser than the beggining of the correspondance
            # [object]...S....E
            # There is no correspondance
            if (
                my_object.start >= self.source + self.range_lenght
                or my_object.stop <= self.source
            ):
                pass
            # Otherwise there is correspondance
            else:
                # We remove the range from the old_object list
                old_object_to_remove.append(my_object)
                # If the first element of the range is lesser than the start of the correspondance
                # [obj....S ....]
                if my_object.start < self.source:
                    old_object_to_extend.append(range(my_object.start, self.source))
                # If the last element of the range is higher than the end of the correspondance
                # [...E...ect]
                if my_object.stop > self.source + self.range_lenght:
                    old_object_to_extend.append(
                        range(self.source + self.range_lenght, my_object.stop)
                    )
                new_object.append(
                    range(
                        max(my_object.start, self.source)
                        - self.source
                        + self.destination,
                        min(my_object.stop, self.source + self.range_lenght)
                        - self.source
                        + self.destination,
                    )
                )
        for object_to_remove in old_object_to_remove:
            old_object.remove(object_to_remove)
        old_object.extend(old_object_to_extend)

    def get_correspondance(self, id: int) -> int:
        return self.destination + (id - self.source)

    def __str__(self) -> str:
        return (
            f"[{self.source}{self.source+self.range_lenght-1}]"
            "=>"
            f"[{self.destination}-{self.destination+self.range_lenght-1}]"
        )


class AlmanacMap:
    def __init__(self) -> None:
        self.correspondances: List[Correspondance] = []

    def add_correspondence(self, correspondance: Correspondance):
        self.correspondances.append(correspondance)

    def apply_correspondance(self, old_objects: List[range]) -> None:
        """
        Apply each correspondence stored in this AlmanacMap to each objects.

        To accomplish this, we create a new list:
        - new_objects: list of the next object

        We attempt to transform each old_objects thanks to the correspondences
        stored in the AlmanacMap. All old object will be consider as new
        object if no transformation work.
        """
        new_objects: List[range] = []
        for correspondance in self.correspondances:
            correspondance.apply(old_objects, new_objects)
        old_objects.extend(new_objects)


class Almanac:
    def __init__(self) -> None:
        # Note: All seeds are store into range object (faster than one by one)
        self.seeds: List[range] = []
        self.almanac_maps: List[AlmanacMap] = []

    def set_seeds(self, seeds: List[range]):
        self.seeds = seeds

    def add_almanac_map(self, almanc_map: AlmanacMap):
        self.almanac_maps.append(almanc_map)

    def find_lowest_position(self) -> int:
        """
        Find the lowest postion for the seed list

        Note: The 'seeds' list is updated to become a 'position' list.
              We could avoid modifying the original list by passing a
              shallow copy instead.
        """
        logger.debug(self.seeds)
        for almanac_map in self.almanac_maps:
            # Note: Only work because an List is mutable
            almanac_map.apply_correspondance(self.seeds)
            logger.debug(self.seeds)
        return min(self.seeds, key=lambda r: r.start).start


def day5(part2: bool = False, **kwargs) -> None:
    """
    Main routines for Day 5.

    :param data_day5: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day5" not in kwargs:
        raise Day5Exception("Undefined parameter 'data_day5'")

    # Parse the file
    almanac: Almanac = parse_data(kwargs["data_day5"], part2)

    # Find the lowest position
    numbers = almanac.find_lowest_position()

    # Print the result
    logger.info("The solution of day5 PART%d is: %d", 2 if part2 else 1, numbers)


def parse_data(data_path: Path, part2: bool) -> Almanac:
    """Read Each Line and parse the content into an Almanac"""
    almanac: Almanac = Almanac()
    with open(data_path, "r") as f:
        almanac_map: AlmanacMap = None
        for line in f:
            strip_line = line.strip()
            match = re.match(r"seeds: (.+)", strip_line)
            if match:
                seeds = match.group(1).split()
                if part2:
                    almanac.set_seeds(
                        [
                            range(int(seeds[i]), int(seeds[i + 1]) + int(seeds[i]))
                            for i in range(0, len(seeds), 2)
                        ]
                    )
                else:
                    almanac.set_seeds([range(int(val), int(val) + 1) for val in seeds])
            elif "map" in strip_line:
                almanac_map = AlmanacMap()
            elif "" == strip_line:
                if almanac_map:
                    almanac.add_almanac_map(almanac_map)
            else:
                almanac_map.add_correspondence(Correspondance(strip_line.split()))
        if almanac_map:
            almanac.add_almanac_map(almanac_map)
    return almanac
