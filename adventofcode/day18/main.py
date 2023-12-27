import argparse
import os
import re
from logging import Logger
from pathlib import Path
from typing import Dict, List, Tuple

from utils.error import AdventOfCodeException
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY18_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day18() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day18 = parser.add_argument_group("day18", "Solution for day18.")
    day18.add_argument(
        "--data-day18", type=Path, help="data to decode", default=DEFAULT_DAY18_DATA
    )
    return parser


Position = Tuple[int, int]

VECTOR: Dict[str, Position] = {
    "U": (-1, 0),
    "R": (0, 1),
    "D": (1, 0),
    "L": (0, -1),
}

DIRECTION: Dict[str, str] = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}


class DigPlan:
    def __init__(self) -> None:
        self.vertexs: List[Position] = [(0, 0)]
        self.previous_point: Tuple(str, int) = ()
        self.convexe = False

    def add_line(self, line: str, part2: bool = False):
        match = re.match(r"(.) (\d+) \(#(.+)\)", line)
        if part2:
            direction, dist = DIRECTION[match.group(3)[5:]], int(match.group(3)[:5], 16)
        else:
            direction, dist = match.group(1), int(match.group(2))
        self.add_previous_point(direction)
        self.previous_point = (direction, dist)

    def add_previous_point(self, direction: str) -> bool:
        if self.previous_point:
            p_dir, p_dist = self.previous_point
            if self.convexe:
                p_dist -= 1
            # Check if the point is concave or convex
            if (
                (p_dir == "U" and direction == "R")
                or (p_dir == "R" and direction == "D")
                or (p_dir == "D" and direction == "L")
                or (p_dir == "L" and direction == "U")
            ):
                self.convexe = False
                p_dist += 1
            else:
                self.convexe = True
            self.vertexs.append(
                (
                    VECTOR[p_dir][0] * (p_dist) + self.vertexs[-1][0],
                    VECTOR[p_dir][1] * (p_dist) + self.vertexs[-1][1],
                )
            )

    def shoelace_formula(self):
        area = 0.0
        for i in range(len(self.vertexs) - 1):
            area += self.vertexs[i][0] * self.vertexs[i + 1][1]
            area -= self.vertexs[i + 1][0] * self.vertexs[i][1]
        area = abs(area) / 2.0
        return area


def day18(part2: bool = False, **kwargs) -> int:
    """
    Main routines for Day 18

    :param data_day18: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day18" not in kwargs:
        raise AdventOfCodeException("Undefined parameter 'data_day18'")

    plan: DigPlan = parse_data(kwargs["data_day18"], part2)
    result = plan.shoelace_formula()
    # Print the result
    logger.info("The solution of day18 PART%d is: %d", 2 if part2 else 1, result)
    return result


def parse_data(data_path: Path, part2: bool = False) -> DigPlan:
    """Read Each Line and parse the content"""
    plan: DigPlan = DigPlan()
    with open(data_path, "r") as f:
        for line in f:
            plan.add_line(line.strip(), part2)
    return plan
