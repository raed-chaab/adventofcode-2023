#!/usr/bin/env python3
import argparse
import importlib
import sys
from typing import Any, Callable, List

from utils.error import AdventOfCodeException

MODULES = 8


def get_parser() -> argparse.ArgumentParser:
    """Create a parser for the application."""
    parser = argparse.ArgumentParser(
        prog="adventofcode" if __name__ == "__main__" else None,
        description="Solutions for adventofcode.",
    )
    parser = argparse.ArgumentParser(
        parents=[
            getattr(importlib.import_module(f"day{id}"), f"get_parser_day{id}")()
            for id in range(1, MODULES + 1)
        ]
    )
    return parser


def main() -> None:
    """Main routines."""
    p = get_parser()
    args = p.parse_args()

    # TBD take into account SOLUTION env var
    days: List[Callable[[Any], int]] = [
        getattr(importlib.import_module(f"day{id}"), f"day{id}")
        for id in range(1, MODULES + 1)
    ]

    for day in days:
        day(**vars(args))
        day(part2=True, **vars(args))


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
