#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import re
import signal
import sys
from types import FrameType
from typing import List, NoReturn, Optional

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY1_DATA= os.path.dirname(FILE_PATH) + "/data/input.txt"

def get_parser_day1() -> argparse.ArgumentParser:
    """Create a parser for the application."""
    parser = argparse.ArgumentParser(
        prog="day1" if __name__ == "__main__" else None,
        description="Provide the sum of all of the calibration values.",
        add_help=False
    )
    day1 = parser.add_argument_group("day1", "Solution for day1.")
    day1.add_argument("--data-day1", type=Path, help="data to decode", default=DEFAULT_DAY1_DATA)
    return parser

def day1(data_file: Path) -> None:
    """Main routines.

    Parse arguments with the parser returns by :func:<get_parser> and call :func:<.echoing_forever>.
    """
    numbers: List[int] = parse_data(data_file)
    assert len(numbers) > 0, f"no data are found in file {data_file}"
    print("The solution of Day1 is: ", sum(numbers))

def parse_data(data_path: Path) -> List[int]:
    """Read Each Line and parse the content"""
    res: List[int] = []
    with open(data_path, "r") as f:
        for line in f:
            res.append(decode_line(line.strip()))
    return res

def decode_line(line: str) -> int:
    """Return the first and the last number"""
    numbers: List[str] = re.findall(r'\d+', line)
    assert len(numbers) > 0, f"Warning no number found for line {line}"
    return int(f"{numbers[0][0]}{numbers[-1][-1]}")

if __name__ == "__main__":
    p = get_parser_day1()
    args = p.parse_args()

    data_file: Path = args.data_day1

    def handler(signum: int, frame: Optional[FrameType]) -> NoReturn:
        print(f"✋ signal [{signum}] received → exiting...")
        sys.exit(0)

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    try:
        day1(data_file)
    except KeyboardInterrupt:
        print("✋ Ctrl-c was pressed. Exiting...")
        sys.exit(0)
    except Exception as exc:
        print(f"⛌ error: {exc}")
    sys.exit(0)
