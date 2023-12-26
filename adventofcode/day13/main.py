import argparse
import os
from logging import Logger
from pathlib import Path
from typing import List

from utils.error import AdventOfCodeException
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY13_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day13() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day13 = parser.add_argument_group("day13", "Solution for day13.")
    day13.add_argument(
        "--data-day13", type=Path, help="data to decode", default=DEFAULT_DAY13_DATA
    )
    return parser


def day13(part2: bool = False, **kwargs) -> int:
    """
    Main routines for Day 13

    :param data_day13: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day13" not in kwargs:
        raise AdventOfCodeException("Undefined parameter 'data_day13'")

    result = sum(parse_data(kwargs["data_day13"], part2))
    # Print the result
    logger.info("The solution of day13 PART%d is: %d", 2 if part2 else 1, result)
    return result


def parse_data(data_path: Path, part2: bool = False) -> List[int]:
    """Read Each Line and parse the content"""
    result: List[int] = []
    with open(data_path, "r") as f:
        mirror: List[List[str]] = []
        for line in f:
            strip_line = line.strip()
            if "" == strip_line:
                result.append(find_reflexion(mirror, part2))
                mirror = []
            else:
                mirror.append([x for x in strip_line])
        if mirror:
            result.append(find_reflexion(mirror, part2))
    return result


def find_reflexion(mirror: List[str], part2: bool) -> int:
    if part2:
        res = fix_horizontal_reflexion(mirror)
        return res * 100 if res else fix_vertical_reflexion(mirror)
    res = find_horizontal_reflexion(mirror)
    return res * 100 if res else find_vertical_reflexion(mirror)


def find_horizontal_reflexion(mirror: List[str]) -> int:
    nb_row = len(mirror)
    for i in range(1, nb_row):
        if i <= nb_row // 2:
            if mirror[0:i] == mirror[i : 2 * i][::-1]:  # noqa: E203
                return i
        else:
            if mirror[2 * i - nb_row : i] == mirror[i:nb_row][::-1]:  # noqa: E203
                return i
    return 0


def find_vertical_reflexion(mirror: List[str]) -> int:
    return find_horizontal_reflexion(["".join(col) for col in zip(*mirror)])


def near_equals(str1: List[str], str2: List[str]) -> int:
    return sum([near_equal(str1[i], str2[i]) for i in range(len(str1))])


def near_equal(str1: str, str2: str) -> int:
    return sum(a != b for a, b in zip(str1, str2))


def fix_horizontal_reflexion(mirror: List[str]) -> List[str]:
    nb_row = len(mirror)
    for i in range(1, nb_row):
        if i <= nb_row // 2:
            if near_equals(mirror[0:i], mirror[i : 2 * i][::-1]) == 1:  # noqa: E203
                return i
        else:
            if (
                near_equals(
                    mirror[2 * i - nb_row : i], mirror[i:nb_row][::-1]  # noqa: E203
                )
                == 1
            ):
                return i
    return 0


def fix_vertical_reflexion(mirror: List[str]) -> int:
    return fix_horizontal_reflexion(["".join(col) for col in zip(*mirror)])
