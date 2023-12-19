#!/usr/bin/env python3
import argparse
import signal
import sys
from types import FrameType
from typing import NoReturn, Optional

from Day1.__main__ import day1, get_parser_day1

def get_parser() -> argparse.ArgumentParser:
    """Create a parser for the application."""
    parser = argparse.ArgumentParser(
        prog="adventofcode" if __name__ == "__main__" else None,
        description="Solutions for adventofcode.",
    )
    parser = argparse.ArgumentParser(parents=[get_parser_day1()])
    return parser

def main() -> None:
    """Main routines."""
    p = get_parser()
    args = p.parse_args()

    day1(args.data_day1)

if __name__ == "__main__":

    def handler(signum: int, frame: Optional[FrameType]) -> NoReturn:
        print(f"✋ signal [{signum}] received → exiting...")
        sys.exit(0)

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    try:
        main()
    except KeyboardInterrupt:
        print("✋ Ctrl-c was pressed. Exiting...")
        sys.exit(0)
    except Exception as exc:
        print(f"⛌ error: {exc}")
    sys.exit(0)