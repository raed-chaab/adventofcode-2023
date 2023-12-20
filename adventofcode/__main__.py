#!/usr/bin/env python3
import argparse
import sys
from utils.error import AdventOfCodeException

from day1 import day1, get_parser_day1
from day2 import day2, get_parser_day2


def get_parser() -> argparse.ArgumentParser:
    """Create a parser for the application."""
    parser = argparse.ArgumentParser(
        prog="adventofcode" if __name__ == "__main__" else None,
        description="Solutions for adventofcode.",
    )
    parser = argparse.ArgumentParser(parents=[get_parser_day1(), get_parser_day2()])
    return parser


def main() -> None:
    """Main routines."""
    p = get_parser()
    args = p.parse_args()

    #TBD take into account SOLUTION env var

    day1(**vars(args))
    day1(part2=True, **vars(args))
    day2(**vars(args))
    day2(part2=True, **vars(args))


if __name__ == "__main__":

    try:
        main()
    except AdventOfCodeException as exc:
        print(f"✋ {exc.__class__.__name__} exception occured {exc}")
    except Exception as exc:
        print(f"⛌ Unexpected error: {exc}")
    else:
        sys.exit(0)
    sys.exit(1)
