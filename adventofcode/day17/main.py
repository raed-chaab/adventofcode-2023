import argparse
import os
from collections import defaultdict
from heapq import heappop, heappush
from logging import Logger
from pathlib import Path
from typing import List

from utils.error import AdventOfCodeException
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY17_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day17() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day17 = parser.add_argument_group("day17", "Solution for day17.")
    day17.add_argument(
        "--data-day17", type=Path, help="data to decode", default=DEFAULT_DAY17_DATA
    )
    return parser


class DijkstraSolver:
    def __init__(self) -> None:
        self.grid: List[List[int]] = []
        self.graph = defaultdict(list)

    def make_graph(self, part2: bool = False) -> None:
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                for k in range(4, 11) if part2 else range(1, 4):
                    if j - k >= 0:
                        self.graph[self.gid(i, j, "N")].append(
                            (
                                sum(self.grid[i][j - m] for m in range(1, k + 1)),
                                self.gid(i, j - k, "E"),
                            )
                        )
                        self.graph[self.gid(i, j, "N")].append(
                            (
                                sum(self.grid[i][j - m] for m in range(1, k + 1)),
                                self.gid(i, j - k, "W"),
                            )
                        )
                        if i != 0 or j != 0:
                            self.graph[self.gid(i, j, "S")].append(
                                (
                                    sum(self.grid[i][j - m] for m in range(1, k + 1)),
                                    self.gid(i, j - k, "E"),
                                )
                            )
                            self.graph[self.gid(i, j, "S")].append(
                                (
                                    sum(self.grid[i][j - m] for m in range(1, k + 1)),
                                    self.gid(i, j - k, "W"),
                                )
                            )
                    if j + k < len(self.grid[0]):
                        self.graph[self.gid(i, j, "N")].append(
                            (
                                sum(self.grid[i][j + m] for m in range(1, k + 1)),
                                self.gid(i, j + k, "E"),
                            )
                        )
                        self.graph[self.gid(i, j, "N")].append(
                            (
                                sum(self.grid[i][j + m] for m in range(1, k + 1)),
                                self.gid(i, j + k, "W"),
                            )
                        )
                        if i != 0 or j != 0:
                            self.graph[self.gid(i, j, "S")].append(
                                (
                                    sum(self.grid[i][j + m] for m in range(1, k + 1)),
                                    self.gid(i, j + k, "E"),
                                )
                            )
                            self.graph[self.gid(i, j, "S")].append(
                                (
                                    sum(self.grid[i][j + m] for m in range(1, k + 1)),
                                    self.gid(i, j + k, "W"),
                                )
                            )
                    if i - k >= 0:
                        self.graph[self.gid(i, j, "E")].append(
                            (
                                sum(self.grid[i - m][j] for m in range(1, k + 1)),
                                self.gid(i - k, j, "N"),
                            )
                        )
                        self.graph[self.gid(i, j, "E")].append(
                            (
                                sum(self.grid[i - m][j] for m in range(1, k + 1)),
                                self.gid(i - k, j, "S"),
                            )
                        )
                        if i != 0 or j != 0:
                            self.graph[self.gid(i, j, "W")].append(
                                (
                                    sum(self.grid[i - m][j] for m in range(1, k + 1)),
                                    self.gid(i - k, j, "N"),
                                )
                            )
                            self.graph[self.gid(i, j, "W")].append(
                                (
                                    sum(self.grid[i - m][j] for m in range(1, k + 1)),
                                    self.gid(i - k, j, "S"),
                                )
                            )
                    if i + k < len(self.grid):
                        self.graph[self.gid(i, j, "E")].append(
                            (
                                sum(self.grid[i + m][j] for m in range(1, k + 1)),
                                self.gid(i + k, j, "N"),
                            )
                        )
                        self.graph[self.gid(i, j, "E")].append(
                            (
                                sum(self.grid[i + m][j] for m in range(1, k + 1)),
                                self.gid(i + k, j, "S"),
                            )
                        )
                        if i != 0 or j != 0:
                            self.graph[self.gid(i, j, "W")].append(
                                (
                                    sum(self.grid[i + m][j] for m in range(1, k + 1)),
                                    self.gid(i + k, j, "N"),
                                )
                            )
                            self.graph[self.gid(i, j, "W")].append(
                                (
                                    sum(self.grid[i + m][j] for m in range(1, k + 1)),
                                    self.gid(i + k, j, "S"),
                                )
                            )

    def find_shortest_path(self) -> int:
        """
        source code from: https://gist.github.com/kachayev/5990802
        """
        f = self.gid(0, 0)
        t = self.gid(len(self.grid) - 1, len(self.grid[0]) - 1)
        queue, seen, dist = [(0, f, ())], set(), {f: 0}
        while queue:
            (cost, v1, path) = heappop(queue)
            if v1 in seen:
                continue

            seen.add(v1)
            path += (v1,)
            if v1 == t:
                return (cost, path)

            for c, v2 in self.graph.get(v1, ()):
                if v2 in seen:
                    continue

                if v2 not in dist or cost + c < dist[v2]:
                    dist[v2] = cost + c
                    heappush(queue, (cost + c, v2, path))

        return 0, []

    def gid(self, i: int, j: int, val: str = "") -> int:
        if (i == 0 and j == 0) or (
            i == len(self.grid) - 1 and j == len(self.grid[0]) - 1
        ):
            return f"{i}:{j}"
        return f"{i}{val}{j}"

    def add_line(self, line: str) -> None:
        self.grid.append([int(li) for li in line])


def day17(part2: bool = False, **kwargs) -> int:
    """
    Main routines for Day 17

    :param data_day17: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day17" not in kwargs:
        raise AdventOfCodeException("Undefined parameter 'data_day17'")

    solver: DijkstraSolver = parse_data(kwargs["data_day17"], part2)
    result = solver.find_shortest_path()[0]
    # Print the result
    logger.info("The solution of day17 PART%d is: %d", 2 if part2 else 1, result)
    return result


def parse_data(data_path: Path, part2: bool = False) -> DijkstraSolver:
    """Read Each Line and parse the content"""
    solver: DijkstraSolver = DijkstraSolver()
    with open(data_path, "r") as f:
        for line in f:
            solver.add_line(line.strip())
    solver.make_graph(part2)
    return solver
