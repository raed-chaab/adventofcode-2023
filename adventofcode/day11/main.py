import argparse
import os
from logging import Logger
from pathlib import Path
from typing import Dict, List, Tuple

from utils.error import AdventOfCodeException
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY11_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day11() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day11 = parser.add_argument_group("day11", "Solution for day11.")
    day11.add_argument(
        "--data-day11", type=Path, help="data to decode", default=DEFAULT_DAY11_DATA
    )
    return parser


Position = Tuple[int, int]


class Univers:
    def __init__(self, expand_factor: int = 2) -> None:
        self.univers_map: List[List[str]] = []
        self.galaxies: Dict[int, Position] = {}
        self.shortest_path: List[int] = []
        self.expand_factor = expand_factor - 1

    def get_galaxies_postion(self) -> None:
        index = 1
        for i, row in enumerate(self.univers_map):
            for j, galaxy in enumerate(row):
                if galaxy == "#":
                    expansion_row = len(
                        [empty_row for empty_row in self.empty_rows if empty_row < i]
                    )
                    expansion_col = len(
                        [empty_col for empty_col in self.empty_cols if empty_col < j]
                    )
                    self.galaxies[index] = (
                        i + expansion_row * self.expand_factor,
                        j + expansion_col * self.expand_factor,
                    )
                    index += 1

    def get_shortest_path(self, galaxy_1: int, galaxy_2: int) -> int:
        return abs(self.galaxies[galaxy_1][0] - self.galaxies[galaxy_2][0]) + abs(
            self.galaxies[galaxy_1][1] - self.galaxies[galaxy_2][1]
        )

    def get_shortests_path(self) -> List[int]:
        self.get_galaxies_postion()
        for i in range(1, len(self.galaxies)):
            for j in range(i + 1, len(self.galaxies) + 1):
                self.shortest_path.append(self.get_shortest_path(i, j))
        return self.shortest_path

    def expand(self) -> None:
        self.empty_rows = [
            i for i, galaxy in enumerate(self.univers_map) if "#" not in galaxy
        ]
        self.empty_cols = [
            j
            for j in range(len(self.univers_map[0]))
            if not any(
                "#" in self.univers_map[i][j] for i in range(len(self.univers_map))
            )
        ]

    def print(self):
        for row in self.univers_map:
            logger.info(" ".join(row))

    def add_galaxies(self, galaxies: List[str]) -> None:
        self.univers_map.append([galaxy for galaxy in galaxies])


def day11(part2: bool = False, **kwargs) -> int:
    """
    Main routines for Day 11

    :param data_day11: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day11" not in kwargs:
        raise AdventOfCodeException("Undefined parameter 'data_day11'")

    univers: Univers = parse_data(kwargs["data_day11"], 1000000 if part2 else 2)
    univers.expand()
    result = sum(univers.get_shortests_path())
    # Print the result
    logger.info("The solution of day11 PART%d is: %d", 2 if part2 else 1, result)
    return result


def parse_data(data_path: Path, expand_factor: int = 1) -> Univers:
    """Read Each Line and parse the content"""
    univers: Univers = Univers(expand_factor)
    with open(data_path, "r") as f:
        for line in f:
            univers.add_galaxies(line.strip())
    return univers
