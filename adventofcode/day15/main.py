import argparse
import os
import re
from collections import OrderedDict
from functools import reduce
from logging import Logger
from pathlib import Path
from typing import Dict, List

from utils.error import AdventOfCodeException
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY15_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day15() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day15 = parser.add_argument_group("day15", "Solution for day15.")
    day15.add_argument(
        "--data-day15", type=Path, help="data to decode", default=DEFAULT_DAY15_DATA
    )
    return parser


class Crypto:
    def __init__(self, steps: List[str]) -> None:
        self.steps: List[str] = steps
        self.boxs: Dict[int, Dict[str, int]] = {i: OrderedDict() for i in range(256)}

    def processs(self, part2: bool = False) -> List[int]:
        if part2:
            for step in self.steps:
                key, val = re.split(r"=|-", step)
                hash_step = self.hash(key)
                if val:
                    self.boxs[hash_step][key] = int(val)
                elif key in self.boxs[hash_step]:
                    del self.boxs[hash_step][key]
            return [
                (num + 1) * (slot + 1) * focal
                for num, box in self.boxs.items()
                for slot, focal in enumerate(box.values())
            ]
        else:
            return [self.hash(step) for step in self.steps]

    def hash(self, step: str) -> int:
        return reduce(
            lambda current_value, char: (ord(char) + current_value) * 17 % 256, step, 0
        )


def day15(part2: bool = False, **kwargs) -> int:
    """
    Main routines for Day 15

    :param data_day15: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day15" not in kwargs:
        raise AdventOfCodeException("Undefined parameter 'data_day15'")

    crypto: Crypto = parse_data(kwargs["data_day15"], part2)
    result = sum(crypto.processs(part2))
    # Print the result
    logger.info("The solution of day15 PART%d is: %d", 2 if part2 else 1, result)
    return result


def parse_data(data_path: Path, part2: bool = False) -> Crypto:
    """Read Each Line and parse the content"""
    with open(data_path, "r") as f:
        for line in f:
            return Crypto(line.strip().split(","))
