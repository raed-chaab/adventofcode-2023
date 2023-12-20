import argparse
import os
import re
from logging import Logger
from pathlib import Path
from typing import Dict, List

from utils.error import Day1Exception
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY1_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

NUMBERS_DICT: Dict[str, str] = {
    # "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

logger: Logger = MyLogger().get_logger()


def get_parser_day1() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day1 = parser.add_argument_group("day1", "Solution for day1.")
    day1.add_argument(
        "--data-day1", type=Path, help="data to decode", default=DEFAULT_DAY1_DATA
    )
    return parser


def day1(part2: bool = False, **kwargs) -> None:
    """
    Main routines for Day 1.

    :param data_day1: Path data to consider
    :param part2: Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day1" not in kwargs:
        raise Day1Exception("Undefined parameter 'data_day1'")

    # Parse the file
    numbers: List[int] = parse_data(kwargs["data_day1"], part2)

    # Print the result
    logger.info("The solution of Day1 PART%d is: %d", 2 if part2 else 1, sum(numbers))


def parse_data(data_path: Path, decode: bool) -> List[int]:
    """Read Each Line and parse the content"""
    res: List[int] = []
    with open(data_path, "r") as f:
        for line in f:
            res.append(decode_line(line.strip(), decode))
    # Assert something is parsed
    if len(res) == 0:
        raise Day1Exception(f"no data are found in file {data_path}")
    return res


def decode_line(line: str, decode: bool) -> int:
    """Return the first and the last number"""
    line_to_decode = line.lower()

    # Take into account digits spell out with letters
    if decode:
        for num, value in NUMBERS_DICT.items():
            # Tricky data such as "oneight" should work.
            line_to_decode = line_to_decode.replace(num, num + value + num)

    # Find all number occurence (at least one)
    numbers: List[str] = re.findall(r"\d+", line_to_decode)
    if len(numbers) == 0:
        raise Day1Exception(f"no number found for line {line_to_decode}")

    # Return the first and the last digit
    res: int = int(f"{numbers[0][0]}{numbers[-1][-1]}")
    logger.debug(line + " -> " + line_to_decode + " -> " + str(res))

    return res
