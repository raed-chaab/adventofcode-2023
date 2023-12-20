import argparse
import os
import re
from logging import Logger
from pathlib import Path
from typing import List

from utils.error import Day4Exception
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY4_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day4() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day4 = parser.add_argument_group("day4", "Solution for day4.")
    day4.add_argument(
        "--data-day4", type=Path, help="data to decode", default=DEFAULT_DAY4_DATA
    )
    return parser


class Card:
    def __init__(
        self, winning_numbers: List[int], numbers: List[int], index: int
    ) -> None:
        self._winning_numbers = winning_numbers
        self._numbers = numbers
        self.index = index
        self.total_scratchcards = 1

    @property
    def total_of_winning_point(self) -> int:
        return len(
            [number for number in self._numbers if number in self._winning_numbers]
        )

    def winning_points(self) -> int:
        point = self.total_of_winning_point
        return 2 ** (point - 1) if point else 0

    def __str__(self) -> str:
        return str(self.index)

    def process_total_scratchcards(self, cards: List[object]):
        next_index = self.index + 1
        for card in cards[
            next_index : min(  # noqa: E203
                next_index + self.total_of_winning_point, len(cards)
            )
        ]:
            self.total_scratchcards += card.total_scratchcards


def day4(part2: bool = False, **kwargs) -> None:
    """
    Main routines for Day 4.

    :param data_day4: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day4" not in kwargs:
        raise Day4Exception("Undefined parameter 'data_day4'")

    # Parse the file
    cards: List[Card] = parse_data(kwargs["data_day4"])

    if part2:
        for card in reversed(cards):
            card.process_total_scratchcards(cards)
        numbers = [card.total_scratchcards for card in cards]
    else:
        numbers = [card.winning_points() for card in cards]

    # Print the result
    logger.info("The solution of Day4 PART%d is: %d", 2 if part2 else 1, sum(numbers))


def parse_data(data_path: Path) -> List[Card]:
    """Read Each Line and parse the content"""
    res: List[Card] = []
    with open(data_path, "r") as f:
        for i, line in enumerate(f):
            res.append(decode_line(line.strip(), i))
    return res


def decode_line(line: str, index: int) -> Card:
    """Return a Card"""
    line_to_decode = line
    match = re.match(r"^Card[ ]*(\d+): (.+) \| (.+)$", line_to_decode)
    if not match:
        raise Day4Exception(f"Invalid Card in line : {line_to_decode}")
    winning_numbers: List[int] = [int(i) for i in match.group(2).split()]
    numbers: List[int] = [int(i) for i in match.group(3).split()]
    return Card(winning_numbers, numbers, index)
