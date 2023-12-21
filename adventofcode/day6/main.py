import argparse
import math
import os
import re
from functools import reduce
from logging import Logger
from pathlib import Path
from typing import List

from utils.error import Day6Exception
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY6_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day6() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day6 = parser.add_argument_group("day6", "Solution for day6.")
    day6.add_argument(
        "--data-day6", type=Path, help="data to decode", default=DEFAULT_DAY6_DATA
    )
    return parser


class Races:
    def __init__(self) -> None:
        self.time: List[int] = []
        self.distance: List[int] = []

    def beat_the_record(self) -> List[int]:
        """
        The solution is equivalent to solve k * (t -k) > d
        => ] (t - sqrt(t^2 -4d)) / 2 ; (t + sqrt(t^2 -4d)) / 2 [
        """
        res: List[int] = []
        for index, t in enumerate(self.time):
            d = self.distance[index]
            delta = t**2 - 4 * d
            if delta > 0:
                res.append(
                    math.ceil((t + math.sqrt(delta)) / 2 - 1)
                    - math.floor((t - math.sqrt(delta)) / 2)
                )
        return res


def day6(part2: bool = False, **kwargs) -> None:
    """
    Main routines for Day 6

    :param data_day6: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day6" not in kwargs:
        raise Day6Exception("Undefined parameter 'data_day6'")

    # Parse the file
    race = parse_data(kwargs["data_day6"], part2)

    # beat the record :)
    numbers = race.beat_the_record()

    # Print the result
    logger.info(
        "The solution of day6 PART%d is: %d",
        2 if part2 else 1,
        reduce((lambda x, y: x * y), numbers),
    )


def parse_data(data_path: Path, part2: bool) -> Races:
    """Read Each Line and parse the content"""
    races: Races = Races()
    with open(data_path, "r") as f:
        for line in f:
            strip_line = line.strip()
            match_time = re.match(r"Time: (.+)", strip_line)
            match_distance = re.match(r"Distance: (.+)", strip_line)
            if match_time:
                if part2:
                    races.time = [int(match_time.group(1).replace(" ", ""))]
                else:
                    races.time = [int(x) for x in match_time.group(1).split()]
            elif match_distance:
                if part2:
                    races.distance = [int(match_distance.group(1).replace(" ", ""))]
                else:
                    races.distance = [int(x) for x in match_distance.group(1).split()]
    return races
