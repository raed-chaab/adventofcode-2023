import argparse
import itertools
import math
import os
import re
from logging import Logger
from pathlib import Path
from typing import Dict, List, Tuple

from utils.error import AdventOfCodeException
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY8_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day8() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day8 = parser.add_argument_group("day8", "Solution for day8.")
    day8.add_argument(
        "--data-day8", type=Path, help="data to decode", default=DEFAULT_DAY8_DATA
    )
    return parser


Node = str


class Maps:
    def __init__(self) -> None:
        # Note: All seeds are store into range object (faster than one by one)
        self.instructions: str = ""
        self.network: Dict[Node, Tuple[Node, Node]] = {}

    def set_instruction(self, instructions: str) -> None:
        self.instructions = instructions
        self.loop = len(self.instructions)

    def add_node(self, node: str) -> None:
        match = re.match(r"(.+) = \((.+), (.+)\)", node)
        self.network[match.group(1)] = (match.group(2), match.group(3))

    def follow_one_path(self) -> int:
        return self.follow_path(["AAA"], "ZZZ")

    def follow_all_path(self) -> int:
        # mmh don't work
        # return self.follow_path([key for key in self.network.keys() if key.endswith("A")], "Z")
        # OK they cheated...
        # Each path are constructed to be cyclic (path is a multiple of the instruction lenght)
        res = 1
        for my_key in [key for key in self.network.keys() if key.endswith("A")]:
            res = math.lcm(res, self.follow_path([my_key], "Z"))
        return res

    def follow_path(self, starts: List[str], endswith: str) -> int:
        index = 0
        for instruction in itertools.cycle(self.instructions):
            if all(start.endswith(endswith) for start in starts):
                return index
            if any(start.endswith(endswith) for start in starts):
                logger.debug(f"{starts}: {index}")
            if instruction == "L":
                starts = [self.network[start][0] for start in starts]
            else:
                starts = [self.network[start][1] for start in starts]
            index += 1
        return index


def day8(part2: bool = False, **kwargs) -> int:
    """
    Main routines for Day 8

    :param data_day8: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day8" not in kwargs:
        raise AdventOfCodeException("Undefined parameter 'data_day8'")

    maps: Maps = parse_data(kwargs["data_day8"])

    if part2:
        result = maps.follow_all_path()
    else:
        result = maps.follow_one_path()

    # Print the result
    logger.info("The solution of day8 PART%d is: %d", 2 if part2 else 1, result)
    return result


def parse_data(data_path: Path) -> Maps:
    """Read Each Line and parse the content"""
    maps: Maps = Maps()
    with open(data_path, "r") as f:
        for line in f:
            strip_line = line.strip()
            if len(strip_line) != 0:
                if all(c == "L" or c == "R" for c in strip_line):
                    maps.set_instruction(strip_line)
                else:
                    maps.add_node(strip_line)
    return maps
