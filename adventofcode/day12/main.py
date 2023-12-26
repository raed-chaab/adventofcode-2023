import argparse
import os
from logging import Logger
from pathlib import Path
from typing import Dict, List

from utils.error import AdventOfCodeException
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY12_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day12() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day12 = parser.add_argument_group("day12", "Solution for day12.")
    day12.add_argument(
        "--data-day12", type=Path, help="data to decode", default=DEFAULT_DAY12_DATA
    )
    return parser


class Record:
    def __init__(self, record: List[str], duplicate: int = 1) -> None:
        self.spring_states: List[str] = [spring_state for spring_state in record[0]]
        self.spring_states = (self.spring_states + ["?"]) * (
            duplicate - 1
        ) + self.spring_states
        self.contiguous_group: List[int] = [
            int(contiguous) for contiguous in record[1].split(",")
        ] * duplicate

    def __str__(self):
        return f"{''.join(self.spring_states)} {self.contiguous_group}"

    def count_arrangement(self) -> int:
        """
        List and count all arrangement for each spring_states

        An arrangement must respect a contiguous_group description e.g [1,1,3]
        The spring_states could be split in several spring subgroups:
            - [.](#.) [.](#.) (###)[.]
            - [.](#) [.](.#) [.](.###) (easiest to implement i think)

        For a spring_states [?]*8 we have 3 possibilities:
            - (#)(.#)(..###)
            - (#)(..#)(.###)
            - (.#)(.#)(.###)

        A way to construct those arrangement is to consider the max size of each sub-groups
            - the first subgroup (#) take 1 to len(spring_states)(8) - sum(min(next subgroup))(2+4) = 2
            => (#) or (.#)
            - the second subgroup (.#) take 2 to len(spring_states)(8)
                                               - len(previous subgroup)(1or2)
                                               - sum(next subgroup)(4) = 2 or 3
            => (#) or (.#) (if the first subgroup is #)
            - the last subgroup (.###) take len(spring_states)(8)
                                          - len(previous subgroup)(3or4)
                                          - sum(next subgroup)(0) = 4 or 5
            => (###) or (.###) (if the previos subgroups are # and .#)

        Now take a more complicate case with a spring_states .[?]*7 we have only 1 possibility:
            - (.#)(.#)(.###)

        A way to construct those arrangement is to stop the calcul if there is an impossibility
        Like before we got:
            - (#), NOK we continue
            - (.#), ... OK

        Another one case with a spring #[?]*7 for a spring [1,1,2] we have 3 possibilities:
            - (#)(.#)(...##)
            - (#)(..#)(..##)
            - (#)(...#)(.##)

        A way to construct those arrangement is to stop the calcul if there is an impossibility
        Like before we got:
            - ([]#), ...  OK we continue
            - ([.]#) NOK we stop ([..]#) will not working either
        If a # is in [] we can break the for loop
        """
        # We supose there is at least 1 solution which start at the position 0
        logger.debug(self)
        arrangements: Dict[int, int] = {0: 1}
        # For each contiguous_group we will update the arrangements Dict
        for current_group, contiguous in enumerate(self.contiguous_group):
            next_arrangements = {}
            # We continue the arrangements Dict, if there is an impossibility we don't keep the arrangement
            for pos, nb_way_to_go in arrangements.items():
                # For each index between [pos ; total - sum(next_sub_groups + 1) - current_group]
                for index in range(
                    pos,
                    len(self.spring_states)
                    - sum(self.contiguous_group[current_group:])
                    - len(self.contiguous_group[current_group + 1 :])  # noqa: E203
                    + (1 if current_group == 0 else 0),
                ):
                    # We check we got '.' or '?' at start except for the first group
                    if current_group != 0 and self.spring_states[index] == "#":
                        break
                    # For the first group we doesn't need a '.' as first element
                    i = 1 if current_group != 0 else 0
                    # We check that the  part only contains "#"
                    if (
                        "."
                        not in self.spring_states[
                            index + i : index + i + contiguous  # noqa: E203
                        ]
                    ):
                        if current_group != len(self.contiguous_group) - 1 or (
                            "#"
                            not in self.spring_states[
                                index + i + contiguous :  # noqa: E203
                            ]  # for the last group we check there is no more '#'
                        ):
                            next_arrangements[index + i + contiguous] = (
                                next_arrangements[index + i + contiguous] + nb_way_to_go
                                if index + i + contiguous in next_arrangements
                                else nb_way_to_go
                            )
                    # We don't need to continue if the first element is an '#' only for the first group
                    if current_group == 0 and self.spring_states[index] == "#":
                        break
            arrangements = next_arrangements
            logger.debug(arrangements)
        return sum(arrangements.values())


class Records:
    def __init__(self) -> None:
        self.records: List[Record] = []

    def add_record(self, record: str, part2: bool) -> None:
        self.records.append(Record(record.split(), duplicate=5 if part2 else 1))

    def count_arrangements(self) -> int:
        return sum([record.count_arrangement() for record in self.records])


def day12(part2: bool = False, **kwargs) -> int:
    """
    Main routines for Day 12

    :param data_day12: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day12" not in kwargs:
        raise AdventOfCodeException("Undefined parameter 'data_day12'")

    conditions = parse_data(kwargs["data_day12"], part2)
    result = conditions.count_arrangements()
    # Print the result
    logger.info("The solution of day12 PART%d is: %d", 2 if part2 else 1, result)
    return result


def parse_data(data_path: Path, part2=False) -> Records:
    """Read Each Line and parse the content"""
    records: Records = Records()
    with open(data_path, "r") as f:
        for line in f:
            records.add_record(line.strip(), part2)
    return records
