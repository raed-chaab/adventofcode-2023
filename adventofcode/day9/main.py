import argparse
import os
from logging import Logger
from pathlib import Path
from typing import List

from utils.error import AdventOfCodeException
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY9_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day9() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day9 = parser.add_argument_group("day9", "Solution for day9.")
    day9.add_argument(
        "--data-day9", type=Path, help="data to decode", default=DEFAULT_DAY9_DATA
    )
    return parser


History = List[int]


def get_prediction(history: History, backward: bool = False) -> int:
    diff_hist = [
        number - history[index - 1]
        for index, number in enumerate(history)
        if index != 0
    ]
    if not all(number == 0 for number in diff_hist):
        if backward:
            return history[0] - get_prediction(diff_hist, backward)
        return history[-1] + get_prediction(diff_hist, backward)
    return history[-1]


class Oasis:
    def __init__(self) -> None:
        self.report: List[History] = []

    def add_history(self, history: History) -> None:
        self.report.append(history)

    def get_predictions(self, part2: bool = False) -> List[int]:
        return [get_prediction(history, part2) for history in self.report]


def day9(part2: bool = False, **kwargs) -> int:
    """
    Main routines for Day 9

    :param data_day9: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day9" not in kwargs:
        raise AdventOfCodeException("Undefined parameter 'data_day9'")

    oasis: Oasis = parse_data(kwargs["data_day9"])
    result = sum(oasis.get_predictions(part2))
    # Print the result
    logger.info("The solution of day9 PART%d is: %d", 2 if part2 else 1, result)
    return result


def parse_data(data_path: Path) -> Oasis:
    """Read Each Line and parse the content"""
    oasis: Oasis = Oasis()
    with open(data_path, "r") as f:
        for line in f:
            oasis.add_history([int(val) for val in line.strip().split()])
    return oasis
