import argparse
import os
from enum import Enum
from logging import Logger
from pathlib import Path
from typing import Dict, List, Tuple

from utils.error import AdventOfCodeException
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY16_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day16() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day16 = parser.add_argument_group("day16", "Solution for day16.")
    day16.add_argument(
        "--data-day16", type=Path, help="data to decode", default=DEFAULT_DAY16_DATA
    )
    return parser


Position = Tuple[int, int]


class Direction(Enum):
    North = 0
    South = 1
    East = 2
    West = 3


North = Direction.North
South = Direction.South
East = Direction.East
West = Direction.West

VECTOR: Dict[Direction, Position] = {
    North: (-1, 0),
    South: (1, 0),
    East: (0, 1),
    West: (0, -1),
}

NEXT_DIRECTIONS: Dict[str, Dict[Direction, List[Direction]]] = {
    ".": {
        North: [North],
        South: [South],
        East: [East],
        West: [West],
    },
    "-": {
        North: [East, West],
        South: [East, West],
        East: [East],
        West: [West],
    },
    "|": {
        North: [North],
        South: [South],
        East: [North, South],
        West: [North, South],
    },
    "/": {
        North: [East],
        South: [West],
        East: [North],
        West: [South],
    },
    "\\": {
        North: [West],
        South: [East],
        East: [South],
        West: [North],
    },
}


class Cell:
    def __init__(self, value: str) -> None:
        self._value = value
        self.energize: List[bool] = [False, False, False, False]

    def energize_cell(self, direct: Direction) -> bool:
        """return True if the position is already energize"""
        if self.energize[direct.value]:
            return False
        self.energize[direct.value] = True
        return True

    def is_energize(self, reset: bool = False) -> bool:
        res = any(self.energize)
        if reset:
            self.energize = [False, False, False, False]
        return res

    def beam(self) -> str:
        if self._value != ".":
            return self._value
        if not any(self.energize):
            return "."
        if any(self.energize[2:]) and any(self.energize[:2]):
            return "2"
        if self.energize[South.value]:
            return "v"
        if self.energize[North.value]:
            return "^"
        if self.energize[West.value]:
            return ">"
        else:
            return "<"

    @property
    def value(self) -> str:
        return self._value


class Contraption:
    def __init__(self) -> None:
        self.grid: List[List[Cell]] = []

    def processs(self, part2: bool = False) -> int:
        if part2:
            res: List[int] = []
            for i in range(0, len(self.grid)):
                res.append(self.energizes_title([((i, 0), East)]))
                res.append(self.energizes_title([((i, len(self.grid[0]) - 1), West)]))
            for j in range(0, len(self.grid[0])):
                res.append(self.energizes_title([((0, j), South)]))
                res.append(self.energizes_title([((len(self.grid) - 1, j), North)]))
            return max(res)
        else:
            return self.energizes_title([((0, 0), East)])

    def energizes_title(self, cells: List[Tuple[Position, Direction]]) -> int:
        for pos, direct in cells:
            self.get_cell(pos).energize_cell(direct)
        while cells:
            cells = [
                (n_pos, n_dir)
                for pos, direct in cells
                for n_pos, n_dir in self.next_move(pos, direct)
                if not (
                    n_pos[0] < 0
                    or n_pos[1] < 0
                    or n_pos[0] >= len(self.grid)
                    or n_pos[1] >= len(self.grid[0])
                )
                if self.get_cell(n_pos).energize_cell(n_dir)
            ]
        return sum([cell.is_energize(reset=True) for row in self.grid for cell in row])

    def print(self):
        logger.info("")
        for cells in self.grid:
            logger.info("".join(["#" if cell.is_energize() else "." for cell in cells]))

    def print_beam(self):
        logger.info("")
        for cells in self.grid:
            logger.info("".join([cell.beam() for cell in cells]))

    def next_move(
        self, pos: Position, direction: Direction
    ) -> List[Tuple[Position, Direction]]:
        return [
            (tuple(map(sum, zip(pos, VECTOR[n_dir]))), n_dir)
            for n_dir in NEXT_DIRECTIONS[self.get_value(pos)][direction]
        ]

    def get_value(self, pos: Position) -> str:
        return self.get_cell(pos).value

    def get_cell(self, pos: Position) -> Cell:
        try:
            return self.grid[pos[0]][pos[1]]
        except IndexError:
            raise AdventOfCodeException(f"Undefined position: {pos}")

    def add_line(self, line: str) -> None:
        self.grid.append([Cell(li) for li in line])


def day16(part2: bool = False, **kwargs) -> int:
    """
    Main routines for Day 16

    :param data_day16: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day16" not in kwargs:
        raise AdventOfCodeException("Undefined parameter 'data_day16'")

    contraption: Contraption = parse_data(kwargs["data_day16"])
    result = contraption.processs(part2)
    # Print the result
    logger.info("The solution of day16 PART%d is: %d", 2 if part2 else 1, result)
    return result


def parse_data(data_path: Path) -> Contraption:
    """Read Each Line and parse the content"""
    contraption: Contraption = Contraption()
    with open(data_path, "r") as f:
        for line in f:
            contraption.add_line(line.strip())
    return contraption
