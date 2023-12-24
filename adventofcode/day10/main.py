import argparse
import os
from logging import Logger
from pathlib import Path
from typing import List, Tuple, Union

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


class Pipe:
    def __init__(self, value, connect=False) -> None:
        self._value = value
        self._part_of_loop = connect
        self._inside_the_loop = None
        self.is_start = False

    @property
    def connect(self) -> bool:
        return self._part_of_loop

    @connect.setter
    def connect(self, connect: bool):
        self._part_of_loop = connect

    @property
    def inside(self) -> Union[bool, None]:
        return self._inside_the_loop

    @inside.setter
    def inside(self, inside: bool):
        self._inside_the_loop = inside

    @property
    def is_not_filled(self) -> bool:
        return self._value != "*"

    def __str__(self) -> str:
        return self._value


Coordonate = Tuple[int]


class Maze:
    def __init__(self) -> None:
        self.grid: List[List[Pipe]] = []

    def add_pipe(self, pipe_row: List[Pipe]):
        self.grid.append(pipe_row)

    def find_start(self) -> Coordonate:
        return [
            (i, j)
            for i, row in enumerate(self.grid)
            for j, pipe in enumerate(row)
            if str(pipe) == "S"
        ][0]

    def get_loop_size(self) -> int:
        row, col = self.find_start()
        previous_pipe: Coordonate = (row, col)
        next_pipe: Coordonate = self.find_connected_pipe(previous_pipe)[0]
        self.get_pipe(next_pipe).connect = True
        index = 1
        while not self.get_pipe(next_pipe).is_start:
            previous_pipe, next_pipe = self.next_pipe(previous_pipe, next_pipe)
            index += 1
        return index

    def get_first_pipe_not_process(self) -> Coordonate:
        for i, row in enumerate(self.grid):
            for j, pipe in enumerate(row):
                if not pipe.connect and pipe.inside is None:
                    return (i, j)

    def get_neighbor(self, coord: Coordonate) -> List[Coordonate]:
        x, y = coord
        neighbors: List[Coordonate] = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
            (
                x + 1,
                y + 1,
            ),  # Tricky as hell: "squeezing between pipes is also allowed!"
            (x + 1, y - 1),
            (x - 1, y + 1),
            (x - 1, y - 1),
        ]
        return [
            (row, col)
            for row, col in neighbors
            if 0 <= row < len(self.grid)
            and 0 <= col < len(self.grid[0])  # Not outside the grid
            and not self.get_pipe((row, col)).connect
        ]

    def get_neighborhood(self, coord: Coordonate):
        neighborhoods: List[Coordonate] = []
        neighbors: List[Coordonate] = [coord]
        while neighbors:
            new_neighbors: List[Coordonate] = []
            for neighbor in neighbors:
                new_neighbors.extend(self.get_neighbor(neighbor))
            neighborhoods.extend(neighbors)
            neighbors = [
                neighbor
                for neighbor in set(new_neighbors)
                if neighbor not in neighborhoods
            ]
        return neighborhoods

    def is_outside_pipe(self, coord: Coordonate):
        return (
            coord[0] == 0
            or coord[1] == 0
            or coord[0] == len(self.grid) - 1
            or coord[1] == len(self.grid[0]) - 1
        )

    def fill_pipes(self) -> None:
        """Pain on my a**
        Input:
            .....
            .S-7.
            .|.|.
            .L-J.
            .....

        Output:
            ***********⬇️
            *.*.*.*.*.*➡️
            ***********⬇️
            *.*S---7*.*➡️
            ***|***|***⬇️
            *.*|*.*|*.*➡️
            ***|***|***⬇️
            *.*L---J*.*➡️
            ***********⬇️
            *.*.*.*.*.*➡️
            ***********
        """
        row_n = len(self.grid)
        col_n = len(self.grid[0])
        new_grid: List[List[Pipe]] = [
            [
                Pipe("*") if i == 2 * row_n or j == 2 * col_n else Pipe("?")
                for j in range(2 * col_n + 1)
            ]
            for i in range(2 * row_n + 1)
        ]
        for i in range(row_n):
            for j in range(col_n):
                new_grid[2 * i][2 * j] = Pipe("*")
                new_grid[2 * i + 1][2 * j + 1] = self.grid[i][j]
                if str(self.grid[i][j]) in ["-", "J", "7"] and self.grid[i][j].connect:
                    new_grid[2 * i + 1][2 * j] = Pipe("-", True)
                else:
                    new_grid[2 * i + 1][2 * j] = Pipe("*")
                if str(self.grid[i][j]) in ["|", "J", "L"] and self.grid[i][j].connect:
                    new_grid[2 * i][2 * j + 1] = Pipe("|", True)
                else:
                    new_grid[2 * i][2 * j + 1] = Pipe("*")
        self.grid = new_grid

    def pipe_inside(self) -> int:
        self.fill_pipes()
        pipe: Coordonate = self.get_first_pipe_not_process()
        while pipe:
            neighborhood: List[Coordonate] = self.get_neighborhood(pipe)
            outside = any(self.is_outside_pipe(pipe) for pipe in neighborhood)
            for pipe in neighborhood:
                self.get_pipe(pipe).inside = not outside
            pipe = self.get_first_pipe_not_process()

        return len(
            [
                pipe
                for row in self.grid
                for pipe in row
                if pipe.inside and pipe.is_not_filled
            ]
        )

    def print_grid(self):
        grid = [
            [
                "X"
                if pipe.connect
                else "\033[1;31mI\033[0m"
                if pipe.inside and pipe.is_not_filled
                else str(pipe)
                for pipe in row
            ]
            for row in self.grid
        ]
        for row in grid:
            logger.debug(" ".join(row))

    def get_pipe(self, coor: Coordonate) -> Pipe:
        return self.grid[coor[0]][coor[1]]

    def find_connected_pipe(self, coor: Coordonate) -> Tuple[Coordonate, Coordonate]:
        if (
            coor[0] < 0
            or coor[1] < 0
            or coor[0] >= len(self.grid)
            or coor[1] >= len(self.grid[0])
        ):
            return ()
        pipe_value = str(self.get_pipe(coor))
        pipe_coords = {
            "|": [(coor[0] + 1, coor[1]), (coor[0] - 1, coor[1])],
            "-": [(coor[0], coor[1] + 1), (coor[0], coor[1] - 1)],
            "L": [(coor[0] - 1, coor[1]), (coor[0], coor[1] + 1)],
            "J": [(coor[0] - 1, coor[1]), (coor[0], coor[1] - 1)],
            "7": [(coor[0] + 1, coor[1]), (coor[0], coor[1] - 1)],
            "F": [(coor[0] + 1, coor[1]), (coor[0], coor[1] + 1)],
        }
        if pipe_value == "S":
            adjacent_pipe: List[Coordonate] = [
                coord
                for coord in pipe_coords["|"] + pipe_coords["-"]
                if coor in self.find_connected_pipe(coord)
            ]
            if len(adjacent_pipe) != 2:
                raise AdventOfCodeException(
                    "There are not 2 pipes connected to the start"
                )
            start_pipe = self.get_pipe(coor)
            start_pipe.is_start = True
            start_pipe._value = [
                p_type
                for p_type, coord in pipe_coords.items()
                if coord == adjacent_pipe
            ][0]
            return tuple(adjacent_pipe)
        elif pipe_value in pipe_coords:
            return tuple(pipe_coords[pipe_value])
        else:
            return ()

    def next_pipe(
        self, previous_pipe: Coordonate, pipe: Coordonate
    ) -> Tuple[Coordonate, Coordonate]:
        next_pipes = [
            next_p
            for next_p in self.find_connected_pipe(pipe)
            if next_p != previous_pipe
        ]
        if len(next_pipes) != 1:
            raise AdventOfCodeException(
                "Unexpected error: two different pipes are required"
            )
        next_pipe = next_pipes[0]
        self.get_pipe(next_pipe).connect = True
        return pipe, next_pipe


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
    if part2:
        result = maze.pipe_inside()
    # Print the result
    logger.info("The solution of day10 PART%d is: %d", 2 if part2 else 1, result)
    return result


def parse_data(data_path: Path) -> Maze:
    """Read Each Line and parse the content"""
    maze: Maze = Maze()
    with open(data_path, "r") as f:
        for line in f:
            maze.add_pipe([Pipe(x) for x in line.strip()])
    return maze
