#!/usr/bin/env python3
import argparse
from logging import DEBUG, Logger
import os
from pathlib import Path
import re
import signal
import sys
from types import FrameType
from typing import Dict, List, NoReturn, Optional

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY1_DATA= os.path.dirname(FILE_PATH) + "/data/input.txt"

NUMBERS_DICT: Dict[str, str] = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
} 

logger: Logger = MyLogger().get_logger()

def get_parser_day1() -> argparse.ArgumentParser:
    """Create a parser for the application."""
    parser = argparse.ArgumentParser(
        prog="day1" if __name__ == "__main__" else None,
        description="Provide the sum of all of the calibration values.",
        add_help=False
    )
    day1 = parser.add_argument_group("day1", "Solution for day1.")
    day1.add_argument("--data-day1", type=Path, help="data to decode", default=DEFAULT_DAY1_DATA)
    day1.add_argument(
        '--decode-day1',
        action='store_true',
        help="consider some of the digits are actually spelled out with letters"
    )
    day1.add_argument(
        '--no-decode-day1',
        dest='decode_day1',
        action='store_false',
        help="only consider digts"
    )
    day1.set_defaults(decode_day1=True) 
    return parser

def day1(data_file: Path, decode: bool = False) -> None:
    """
    Main routines for Day 1.

    Parse arguments with the parser returns by :func:<parse_data>
    """
    # Parse the file 
    numbers: List[int] = parse_data(data_file, decode)

    # Print the result
    logger.info("The solution of Day1 is: %d", sum(numbers))

def parse_data(data_path: Path, decode: bool) -> List[int]:
    """Read Each Line and parse the content"""
    res: List[int] = []
    with open(data_path, "r") as f:
        for line in f:
            res.append(decode_line(line.strip(), decode))
    if len(res) == 0:
        raise Exception(f"no data are found in file {data_file}")
    return res

def decode_line(line: str, decode: bool) -> int:
    """Return the first and the last number"""
    line_to_decode = line.lower()
    if decode:
        for num, value in NUMBERS_DICT.items():
            # Tricky data such as "oneight" should work.
            line_to_decode = line_to_decode.replace(num, num + value + num)
    numbers: List[str] = re.findall(r'\d+', line_to_decode)
    if len(numbers) == 0:
        raise Exception(f"no number found for line {line_to_decode}")
    res: int = int(f"{numbers[0][0]}{numbers[-1][-1]}")
    if logger.isEnabledFor(DEBUG):
        logger.debug(line + " -> " + line_to_decode + " -> " + str(res))
    return res

if __name__ == "__main__":
    p = get_parser_day1()
    args = p.parse_args()

    data_file: Path = args.data_day1
    decode: bool = args.decode_day1

    def handler(signum: int, frame: Optional[FrameType]) -> NoReturn:
        print(f"✋ signal [{signum}] received → exiting...")
        sys.exit(0)

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    try:
        day1(data_file, decode)
    except KeyboardInterrupt:
        print("✋ Ctrl-c was pressed. Exiting...")
        sys.exit(0)
    except Exception as exc:
        print(f"⛌ error: {exc}")
    sys.exit(0)
