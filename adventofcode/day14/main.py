import argparse
import os
from logging import Logger
from pathlib import Path
from typing import List

from utils.error import AdventOfCodeException
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY14_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day14() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day14 = parser.add_argument_group("day14", "Solution for day14.")
    day14.add_argument(
        "--data-day14", type=Path, help="data to decode", default=DEFAULT_DAY14_DATA
    )
    return parser


class Platform:
    def __init__(self) -> None:
        self.grid: List[str] = [[]]

    def add_line(self, line: str):
        self.grid[0].append(line)

    def tilt(self, side="North") -> None:
        # la flemme
        if side == "North":
            self.grid[-1] = ["".join(col) for col in zip(*self.grid[-1])]
            self.tilt("West")
            self.grid[-1] = ["".join(col) for col in zip(*self.grid[-1])]
        elif side == "South":
            self.grid[-1] = ["".join(col) for col in zip(*self.grid[-1])]
            self.tilt("East")
            self.grid[-1] = ["".join(col) for col in zip(*self.grid[-1])]
        elif side == "East":
            self.grid[-1] = [
                "#".join(
                    "." * row.count(".") + "O" * row.count("O")
                    for row in line.split("#")
                )
                for line in self.grid[-1]
            ]
        elif side == "West":
            self.grid[-1] = [
                "#".join(
                    "O" * row.count("O") + "." * row.count(".")
                    for row in line.split("#")
                )
                for line in self.grid[-1]
            ]

    def total_load(self, side="North") -> int:
        if side == "North":
            res = []
            for g in self.grid:
                return sum(
                    [
                        (len(self.grid[-1]) - index) * line.count("O")
                        for index, line in enumerate(self.grid[-1])
                    ]
                )
            return res

    def cycle(self, cycle: int) -> None:
        while (res := self.find_loop()) == 0:
            self.grid.append(self.grid[-1])
            self.tilt("North")
            self.tilt("West")
            self.tilt("South")
            self.tilt("East")
        self.grid.append(self.grid[((cycle - res) % (len(self.grid) - res - 1)) + res])

    def find_loop(self) -> int:
        for index, grid in enumerate(self.grid[:-1]):
            if grid == self.grid[-1]:
                return index
        return 0

    def print(self) -> str:
        logger.info("")
        for line in self.grid[-1]:
            logger.info(line)


def day14(part2: bool = False, **kwargs) -> int:
    """
    Main routines for Day 14

    :param data_day14: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day14" not in kwargs:
        raise AdventOfCodeException("Undefined parameter 'data_day14'")

    platform: Platform = parse_data(kwargs["data_day14"], part2)
    if part2:
        platform.cycle(1000000000)
    else:
        platform.tilt("North")
    result = platform.total_load("North")
    # Print the result
    logger.info("The solution of day14 PART%d is: %d", 2 if part2 else 1, result)
    return result


def parse_data(data_path: Path, part2: bool = False) -> Platform:
    """Read Each Line and parse the content"""
    platform: Platform = Platform()
    with open(data_path, "r") as f:
        for line in f:
            platform.add_line(line.strip())
    return platform
