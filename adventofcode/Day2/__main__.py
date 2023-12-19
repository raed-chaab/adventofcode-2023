#!/usr/bin/env python3
import argparse
from logging import DEBUG, Logger
import os
from pathlib import Path
import re
import signal
import sys
from types import FrameType
from typing import Dict, List, NoReturn, Optional, Tuple

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY2_DATA= os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()

def get_parser_day2() -> argparse.ArgumentParser:
    """Create a parser for the application."""
    parser = argparse.ArgumentParser(
        prog="day1" if __name__ == "__main__" else None,
        description="Provide the sum of all of the calibration values.",
        add_help=False
    )
    day2 = parser.add_argument_group("day2", "Solution for day2.")
    day2.add_argument("--data-day2", type=Path, help="data to decode", default=DEFAULT_DAY2_DATA)
    day2.add_argument("--max-red-day2", type=int, help="max number of red cubes in a set", default=12)
    day2.add_argument("--max-green-day2", type=int, help="max number of green cubes in a set", default=13)
    day2.add_argument("--max-blue-day2", type=int, help="max number of blue cubes in a set", default=14)
    return parser

COLORS = ['blue', 'green', 'red']

class CubeSet:
    blue: int
    green: int
    red: int
    def __init__(self, blue: int = 0, green: int = 0, red: int = 0):
        self.blue = blue
        self.green = green
        self.red = red
    def __le__(self, other):
        """Implement an operator '<='."""
        return (self.blue <= other.blue and
               self.green <= other.green and
               self.red <= other.red)
    def __str__(self) -> str:
        return f"Set blue={self.blue} red={self.red} green={self.green}"

def day2(data_file: Path, max_cube_set: CubeSet) -> None:
    """
    Main routines for Day 2.

    Parse arguments with the parser returns by :func:<parse_data>
    """
    # Parse the file 
    games: Dict[int, List[CubeSet]] = parse_data(data_file)

    # keep games that are smaller than max
    numbers = [val for val, cube_sets in games.items() if all(cube_set <= max_cube_set for cube_set in cube_sets)]

    # Print the result
    logger.info("The solution of Day2 is: %d", sum(numbers))

def parse_data(data_path: Path) -> Dict[int, List[CubeSet]]:
    """Read Each Line and parse the content"""
    res: Dict[int, List[CubeSet]] = {}
    with open(data_path, "r") as f:
        for line in f:
            id, games = decode_line(line.strip())
            res[id] = games
    return res

def decode_line(line: str) -> Tuple[int, List[CubeSet]]:
    """Return the first and the last number"""
    line_to_decode = line
    match = re.match(r'^Game (\d+): (.+)$', line_to_decode)
    if not match:
        raise Exception(f"Invalid game in line : {line_to_decode}")
    cube_sets: List[CubeSet] = []
    for cube_set in match.group(2).split(";"):
        # e.g cube_set = "3 green, 7 blue, 5 red"
        # colors = {'green': 3, 'blue': 7, 'red': 5}
        colors: Dict[str, int] = {
            color: int(value)
            # We Match all colors one by one to construct a kwargs dict 
            for value, color in re.findall(fr'(\d+) ({"|".join(COLORS)})', cube_set)
        }
        cube_sets.append(CubeSet(**colors))
    return int(match.group(1)), cube_sets

if __name__ == "__main__":
    p = get_parser_day2()
    args = p.parse_args()

    data_file: Path = args.data_day2
    red: int = args.max_red_day2
    green: int = args.max_green_day2
    blue: int = args.max_blue_day2

    def handler(signum: int, frame: Optional[FrameType]) -> NoReturn:
        print(f"✋ signal [{signum}] received → exiting...")
        sys.exit(0)

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    try:
        day2(data_file, CubeSet(red=red,green=green,blue=blue))
    except KeyboardInterrupt:
        print("✋ Ctrl-c was pressed. Exiting...")
        sys.exit(0)
    except Exception as exc:
        print(f"⛌ error: {exc}")
    sys.exit(0)
