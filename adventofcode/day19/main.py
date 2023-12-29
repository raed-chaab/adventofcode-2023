import argparse
import copy
import math
import os
import re
from logging import Logger
from pathlib import Path
from typing import Dict, List

from utils.error import AdventOfCodeException
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY19_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day19() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day19 = parser.add_argument_group("day19", "Solution for day19.")
    day19.add_argument(
        "--data-day19", type=Path, help="data to decode", default=DEFAULT_DAY19_DATA
    )
    return parser


Rule = List[str]


class Part:
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)

    def apply_rules(self, rules: Dict[str, Rule], next_rule: str = "in") -> int:
        while next_rule:
            if next_rule == "A":
                return sum([x for x in self.__dict__.values()])
            elif next_rule == "R":
                return 0
            next_rule = self.apply_rule(rules[next_rule])
        raise AdventOfCodeException("no next rule found")

    def apply_rule(self, rules: Rule) -> str:
        if not rules:
            return ""
        for rule in rules[:-1]:
            if eval("self." + rule.split(":")[0], {"self": self}):
                return rule.split(":")[1]
        return rules[-1]


class Condition:
    def __init__(self, rule_name: str) -> None:
        self.rule_name = rule_name
        self.condition: Dict[str, range] = {key: range(1, 4001) for key in "xmas"}
        self.accepted_condition: List[Dict[str, range]] = []

    def add_condition(self, next_rule: str, condition: str = "") -> None:
        rule_condition = copy.copy(self.condition)
        if condition:
            match = re.match(r"(?P<key>.+)(<(?P<inf>.+)|>(?P<sup>.+))", condition)
            current_range, key = self.condition[match.group("key")], match.group("key")
            if match.group("inf"):
                inf = int(match.group("inf"))
                rule_condition[key] = range(
                    current_range[0], min(current_range[-1] + 1, inf)
                )
                self.condition[key] = range(
                    max(current_range[0], inf), current_range[-1] + 1
                )
            else:
                sup = int(match.group("sup")) + 1
                rule_condition[key] = range(
                    max(current_range[0], sup), current_range[-1] + 1
                )
                self.condition[key] = range(
                    current_range[0], min(current_range[-1] + 1, sup)
                )
        if next_rule == "A":
            self.accepted_condition.append(rule_condition)

    def possible(self) -> int:
        total = 1
        for i in range(4):
            total *= max((min((self.upper[i], 4001)) - max((self.lower[i], 0)) - 1, 0))
        return total

    def __str__(self) -> str:
        return f"{self.rule_name} if {self.accepted_condition}"


class Workflows:
    def __init__(self) -> None:
        self.rules_dict: Dict[str, Rule] = {}
        self.parts: List[Part] = []
        self.conditions: Dict[str, List[Dict[str, range]]] = {
            "in": [{key: range(1, 4001) for key in "xmas"}]
        }
        # self.conditions["in"][0]["name"] = ["in"]

    def add_rule(self, name_rule: str, rules: Rule):
        self.rules_dict[name_rule] = rules

    def add_part(self, **kwargs):
        self.parts.append(Part(**kwargs))

    def accept_parts(self) -> int:
        return sum(part.apply_rules(self.rules_dict) for part in self.parts)

    def process_rule(self) -> bool:
        accepted_condition: Dict[str, List[Dict[str, range]]] = {"A": [], "R": []}
        for name, conditions in self.conditions.items():
            if name in "AR":
                accepted_condition[name].extend(conditions)
            else:
                for next_cond in conditions:
                    # next_cond["name"].append("")
                    for rule in self.rules_dict[name]:
                        current_cond = copy.deepcopy(next_cond)
                        match_accept_rule = re.match(
                            r"((?P<operation>.+):)?(?P<next_rule>.+)", rule
                        )
                        operation, next_rule = match_accept_rule.group(
                            "operation"
                        ), match_accept_rule.group("next_rule")
                        if operation:
                            match = re.match(
                                r"(?P<key>.+)(<(?P<inf>.+)|>(?P<sup>.+))", operation
                            )
                            key = match.group("key")
                            if match.group("inf"):
                                inf = int(match.group("inf"))
                                next_cond[key] = range(
                                    max(current_cond[key][0], inf),
                                    current_cond[key][-1] + 1,
                                )
                                current_cond[key] = range(
                                    current_cond[key][0],
                                    min(current_cond[key][-1] + 1, inf),
                                )
                            else:
                                sup = int(match.group("sup")) + 1
                                next_cond[key] = range(
                                    current_cond[key][0],
                                    min(current_cond[key][-1] + 1, sup),
                                )
                                current_cond[key] = range(
                                    max(current_cond[key][0], sup),
                                    current_cond[key][-1] + 1,
                                )
                        # current_cond["name"][-1] = next_rule
                        if next_rule in accepted_condition:
                            accepted_condition[next_rule].append(current_cond)
                        else:
                            accepted_condition[next_rule] = [current_cond]
        self.conditions = accepted_condition
        return True if any(key not in "AR" for key in self.conditions.keys()) else False

    def accept_rules(self) -> int:
        while self.process_rule():
            pass
        return sum(
            list(
                map(
                    lambda cond: math.prod([len(x) for x in cond.values()]),
                    self.conditions["A"],
                )
            )
        )


def day19(part2: bool = False, **kwargs) -> int:
    """
    Main routines for Day 19

    :param data_day19: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day19" not in kwargs:
        raise AdventOfCodeException("Undefined parameter 'data_day19'")

    workflow: Workflows = parse_data(kwargs["data_day19"])
    if part2:
        result = workflow.accept_rules()
    else:
        result = workflow.accept_parts()
    # Print the result
    logger.info("The solution of day19 PART%d is: %d", 2 if part2 else 1, result)
    return result


def parse_data(data_path: Path) -> Workflows:
    """Read Each Line and parse the content"""
    workflow: Workflows = Workflows()
    with open(data_path, "r") as f:
        for line in f:
            strip_line = line.strip()
            match_rule = re.match(r"(?P<name>.+){(?P<rule>.+)}", strip_line)
            match_part = re.match(
                r"{x=(?P<x>.+),m=(?P<m>.+),a=(?P<a>.+),s=(?P<s>.+)}", strip_line
            )
            if match_rule:
                workflow.add_rule(
                    match_rule.group("name"), match_rule.group("rule").split(",")
                )
            elif match_part:
                workflow.add_part(
                    **{k: int(v) for k, v in match_part.groupdict().items()}
                )
    return workflow
