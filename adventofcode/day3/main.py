import argparse
import os
import re
from logging import Logger
from pathlib import Path
from typing import List

from utils.error import AdventOfCodeException
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY3_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day3() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day3 = parser.add_argument_group("day3", "Solution for day3.")
    day3.add_argument(
        "--data-day3", type=Path, help="data to decode", default=DEFAULT_DAY3_DATA
    )
    return parser


SYMBOLS = r"[^.0-9]"
GEARS = r"[*]"
NUMBERS = r"[0-9]+"


class Coordinate:
    def __init__(self, row, column) -> None:
        self._row = row
        self._column = column

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    def __eq__(self, other) -> bool:
        return self._column == other._column and self._row == other._row

    def __str__(self) -> str:
        return f"[{self._column}][{self._row}]"


class Number:
    def __init__(
        self, row: int, column: int, value: str, max_row: int, max_column: int
    ) -> None:
        self._value = value
        self._start_coordonate = Coordinate(row=row, column=column)
        self._coordonates = [
            Coordinate(row=row, column=column_t)
            for column_t in range(column, column + len(value))
        ]
        self._adjacent_values = [
            Coordinate(row=row_t, column=column_t)
            for row_t in [row - 1, row, row + 1]
            for column_t in range(column - 1, column + len(value) + 1)
            if -1 < row_t < max_row
            and -1 < column_t < max_column
            and not (
                row_t == row
                and (column_t != column - 1 and column_t != column + len(value))
            )
        ]

    @property
    def value(self):
        return self._value

    @property
    def adjacent_values(self):
        return self._adjacent_values

    def __str__(self):
        return f"{self._start_coordonate}={self._value}"


class EngineShema:
    """Cube set of a game"""

    def __init__(self) -> None:
        self._engine_map: List[str] = []
        self._symboles: List[Coordinate] = []
        self._numbers: List[Number] = []
        self._gears: List[Coordinate] = []

    def add_row(self, row: str):
        """Construct the engine shema row by row"""
        self._engine_map.append(row)

    def process(self):
        """Construct the symboles and numbers attribute"""
        max_row = len(self._engine_map)
        max_column = len(self._engine_map[0])
        for row_index, row in enumerate(self._engine_map):
            for column_index in [match.start() for match in re.finditer(SYMBOLS, row)]:
                self._symboles.append(Coordinate(row=row_index, column=column_index))
            for column_index in [match.start() for match in re.finditer(GEARS, row)]:
                self._gears.append(Coordinate(row=row_index, column=column_index))
            for number_index, column_index in enumerate(
                [match.start() for match in re.finditer(NUMBERS, row)]
            ):
                self._numbers.append(
                    Number(
                        row=row_index,
                        column=column_index,
                        value=re.findall(NUMBERS, row)[number_index],
                        max_row=max_row,
                        max_column=max_column,
                    )
                )

    def get_value_from(self, column: int, row: int) -> str:
        """Get value from engine_map (Debug purpose)"""
        return self._engine_map[row][column]

    def get_number_adjacent_to_a_symbol(self) -> List[int]:
        """List of all number adjacent to at least one symbol"""
        return [
            int(number.value)
            for number in self._numbers
            # If at least one adjacent value is a symbole
            if any(
                adjacent_value in self._symboles
                for adjacent_value in number.adjacent_values
            )
        ]

    def get_gears_adjacent_to_two_numbers(self) -> List[int]:
        """Identify the gears in an array that are connected to exactly two integers.
        Create a list of the products resulting from multiplying those two integers together.
        """
        res: List[int] = []
        for gears in self._gears:
            adjacent_numbers = [
                int(number.value)
                for number in self._numbers
                if gears in number.adjacent_values
            ]
            if len(adjacent_numbers) == 2:
                res.append(adjacent_numbers[0] * adjacent_numbers[1])
        return res

    def __str__(self) -> str:
        """human readable representation"""
        return "\n".join(self._engine_map)


def day3(part2: bool = False, **kwargs) -> None:
    """
    Main routines for Day 3.

    :param data_day3: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day3" not in kwargs:
        raise AdventOfCodeException("Undefined parameter 'data_day3'")

    # Parse the file
    engine_schema: EngineShema = parse_data(kwargs["data_day3"])

    if part2:
        numbers = engine_schema.get_gears_adjacent_to_two_numbers()
    else:
        numbers = engine_schema.get_number_adjacent_to_a_symbol()

    # Print the result
    logger.info("The solution of Day3 PART%d is: %d", 2 if part2 else 1, sum(numbers))


def parse_data(data_path: Path) -> EngineShema:
    """Read Each Line and parse the content"""
    res: EngineShema = EngineShema()
    with open(data_path, "r") as f:
        for line in f:
            res.add_row(line.strip())
    res.process()
    return res
