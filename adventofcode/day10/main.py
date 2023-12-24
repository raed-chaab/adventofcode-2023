import argparse
import os
from logging import Logger
from pathlib import Path
from typing import List, Tuple

from utils.error import AdventOfCodeException
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY10_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day10() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day10 = parser.add_argument_group("day10", "Solution for day10.")
    day10.add_argument(
        "--data-day10", type=Path, help="data to decode", default=DEFAULT_DAY10_DATA
    )
    return parser


Pipe = str
Coordonate = Tuple[int]


class Maze:
    def __init__(self) -> None:
        self.pipes: List[List[Pipe]] = []

    def add_pipe(self, pipe: List[Pipe]):
        self.pipes.append(pipe)

    def find_start(self) -> Coordonate:
        return [
            (i, j)
            for i, row in enumerate(self.pipes)
            for j, x in enumerate(row)
            if x == "S"
        ][0]

    def get_loop_size(self) -> int:
        row, col = self.find_start()
        previous_pipe: Coordonate = (row, col)
        next_pipe: Coordonate = self.find_connected_pipe(previous_pipe)[0]
        index = 1
        while self.pipes[next_pipe[0]][next_pipe[1]] != "S":
            previous_pipe, next_pipe = self.next_pipe(previous_pipe, next_pipe)
            index += 1
        return index

    def find_connected_pipe(self, pipe: Coordonate) -> Tuple[Coordonate, Coordonate]:
        if (
            pipe[0] < 0
            or pipe[1] < 0
            or pipe[0] >= len(self.pipes)
            or pipe[1] >= len(self.pipes[0])
        ):
            return ()
        pipe_value = self.pipes[pipe[0]][pipe[1]]
        pipe_coords = {
            "|": [(pipe[0] + 1, pipe[1]), (pipe[0] - 1, pipe[1])],
            "-": [(pipe[0], pipe[1] + 1), (pipe[0], pipe[1] - 1)],
            "L": [(pipe[0] - 1, pipe[1]), (pipe[0], pipe[1] + 1)],
            "J": [(pipe[0] - 1, pipe[1]), (pipe[0], pipe[1] - 1)],
            "7": [(pipe[0] + 1, pipe[1]), (pipe[0], pipe[1] - 1)],
            "F": [(pipe[0] + 1, pipe[1]), (pipe[0], pipe[1] + 1)],
        }
        if pipe_value == "S":
            adjacent_pipe: List[Coordonate] = [
                coord
                for coord in pipe_coords["|"] + pipe_coords["-"]
                if pipe in self.find_connected_pipe(coord)
            ]
            if len(adjacent_pipe) != 2:
                raise AdventOfCodeException(
                    "There are not 2 pipes connected to the start"
                )
            return tuple(adjacent_pipe)
        elif pipe_value in pipe_coords:
            return tuple(pipe_coords[pipe_value])
        else:
            return ()

    def next_pipe(
        self, previous_pipe: Coordonate, pipe: Coordonate
    ) -> Tuple[Coordonate, Coordonate]:
        next_pipe = [
            next_p
            for next_p in self.find_connected_pipe(pipe)
            if next_p != previous_pipe
        ]
        if len(next_pipe) != 1:
            raise AdventOfCodeException(
                "Unexpected error: two different pipes are required"
            )
        return pipe, next_pipe[0]


def day10(part2: bool = False, **kwargs) -> int:
    """
    Main routines for Day 10

    :param data_day10: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day10" not in kwargs:
        raise AdventOfCodeException("Undefined parameter 'data_day10'")

    maze: Maze = parse_data(kwargs["data_day10"])
    result = maze.get_loop_size() / 2
    # Print the result
    logger.info("The solution of day10 PART%d is: %d", 2 if part2 else 1, result)
    return result


def parse_data(data_path: Path) -> Maze:
    """Read Each Line and parse the content"""
    maze: Maze = Maze()
    with open(data_path, "r") as f:
        for line in f:
            maze.add_pipe(list(line.strip()))
    return maze
