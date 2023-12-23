import argparse
import os
import re
from logging import Logger
from pathlib import Path
from typing import Dict, List, Tuple

from utils.error import AdventOfCodeException
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY2_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day2() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day2 = parser.add_argument_group("day2", "Solution for day2.")
    day2.add_argument(
        "--data-day2", type=Path, help="data to decode", default=DEFAULT_DAY2_DATA
    )
    day2.add_argument(
        "--max-red-day2", type=int, help="max number of red cubes in a set", default=12
    )
    day2.add_argument(
        "--max-green-day2",
        type=int,
        help="max number of green cubes in a set",
        default=13,
    )
    day2.add_argument(
        "--max-blue-day2",
        type=int,
        help="max number of blue cubes in a set",
        default=14,
    )
    return parser


COLORS = ["blue", "green", "red"]


class CubeSet:
    """Cube set of a game"""

    blue: int
    green: int
    red: int

    def __init__(self, blue: int = 0, green: int = 0, red: int = 0):
        self.blue = blue
        self.green = green
        self.red = red

    def maximise(self, other):
        """Keep the max value for each colors"""
        self.blue = max(self.blue, other.blue)
        self.green = max(self.green, other.green)
        self.red = max(self.red, other.red)

    def power(self) -> int:
        """Return the power of a set of cubes"""
        return self.blue * self.green * self.red

    def __le__(self, other):
        """Implement an operator '<='."""
        return (
            self.blue <= other.blue
            and self.green <= other.green
            and self.red <= other.red
        )

    def __str__(self) -> str:
        """human readable representation"""
        return f"Set blue={self.blue} red={self.red} green={self.green}"


def day2(part2: bool = False, **kwargs) -> None:
    """
    Main routines for Day 2.

    :param data_day2: Path data to consider
    :param max_red_day2: max number of red cubes in a set
    :param max_green_day2: max number of green cubes in a set
    :param max_blue_day2: max number of blue cubes in a set
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day2" not in kwargs:
        raise AdventOfCodeException("Undefined parameter 'data_day2'")

    # Parse the file
    games: Dict[int, List[CubeSet]] = parse_data(kwargs["data_day2"])

    if part2:
        # Calculate the power of the minimum set of cubes for each game
        numbers = [game_power(cube_sets) for _, cube_sets in games.items()]
    else:
        if "max_red_day2" not in kwargs:
            raise AdventOfCodeException("Undefined parameter 'max_red_day2'")
        if "max_green_day2" not in kwargs:
            raise AdventOfCodeException("Undefined parameter 'max_green_day2'")
        if "max_blue_day2" not in kwargs:
            raise AdventOfCodeException("Undefined parameter 'max_blue_day2'")

        max_cube_set: CubeSet = CubeSet(
            red=kwargs["max_red_day2"],
            green=kwargs["max_green_day2"],
            blue=kwargs["max_blue_day2"],
        )
        # Keep only the games where none of the CubeSet objects used exceed
        # the maximum cube set defined by the max_cube_set
        numbers = [
            val
            for val, cube_sets in games.items()
            # If all cube_set are smaller than max_cube_set
            if all(cube_set <= max_cube_set for cube_set in cube_sets)
        ]

    # Print the result
    logger.info("The solution of Day2 PART%d is: %d", 2 if part2 else 1, sum(numbers))


def game_power(cube_sets: List[CubeSet]) -> int:
    """Construct the minimum set of cubes needed for given set(s) of cubes, and return its power."""
    res = CubeSet()
    for cube_set in cube_sets:
        res.maximise(cube_set)
    return res.power()


def parse_data(data_path: Path) -> Dict[int, List[CubeSet]]:
    """Read Each Line and parse the content"""
    res: Dict[int, List[CubeSet]] = {}
    with open(data_path, "r") as f:
        for line in f:
            id, games = decode_line(line.strip())
            res[id] = games
    return res


def decode_line(line: str) -> Tuple[int, List[CubeSet]]:
    """Return the game ID and each set of cube"""
    line_to_decode = line
    match = re.match(r"^Game (\d+): (.+)$", line_to_decode)
    if not match:
        raise AdventOfCodeException(f"Invalid game in line : {line_to_decode}")
    cube_sets: List[CubeSet] = []
    for cube_set in match.group(2).split(";"):
        # e.g cube_set = "3 green, 7 blue, 5 red"
        # colors = {'green': 3, 'blue': 7, 'red': 5}
        colors: Dict[str, int] = {
            color: int(value)
            # We Match all colors one by one to construct a kwargs dict
            for value, color in re.findall(rf'(\d+) ({"|".join(COLORS)})', cube_set)
        }
        cube_sets.append(CubeSet(**colors))
    return int(match.group(1)), cube_sets
