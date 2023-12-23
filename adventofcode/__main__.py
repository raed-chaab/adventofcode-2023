#!/usr/bin/env python3
import argparse
import sys

from day1 import day1, get_parser_day1
from day2 import day2, get_parser_day2
from day3 import day3, get_parser_day3
from day4 import day4, get_parser_day4
from day5 import day5, get_parser_day5
from day6 import day6, get_parser_day6
from day7 import day7, get_parser_day7
from day8 import day8, get_parser_day8
from utils.error import AdventOfCodeException


def get_parser() -> argparse.ArgumentParser:
    """Create a parser for the application."""
    parser = argparse.ArgumentParser(
        prog="adventofcode" if __name__ == "__main__" else None,
        description="Solutions for adventofcode.",
    )
    parser = argparse.ArgumentParser(
        parents=[
            get_parser_day1(),
            get_parser_day2(),
            get_parser_day3(),
            get_parser_day4(),
            get_parser_day5(),
            get_parser_day6(),
            get_parser_day7(),
            get_parser_day8(),
        ]
    )
    return parser


def main() -> None:
    """Main routines."""
    p = get_parser()
    args = p.parse_args()

    # TBD take into account SOLUTION env var

    day1(**vars(args))
    day1(part2=True, **vars(args))
    day2(**vars(args))
    day2(part2=True, **vars(args))
    day3(**vars(args))
    day3(part2=True, **vars(args))
    day4(**vars(args))
    day4(part2=True, **vars(args))
    day5(**vars(args))
    day5(part2=True, **vars(args))
    day6(**vars(args))
    day6(part2=True, **vars(args))
    day7(**vars(args))
    day7(part2=True, **vars(args))
    day8(**vars(args))
    day8(part2=True, **vars(args))

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
