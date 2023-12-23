import argparse
import os
from enum import Enum
from functools import total_ordering
from logging import Logger
from pathlib import Path
from typing import List

from utils.error import AdventOfCodeException
from utils.logger import MyLogger

FILE_PATH = os.path.abspath(__file__)
DEFAULT_DAY7_DATA = os.path.dirname(FILE_PATH) + "/data/input.txt"

logger: Logger = MyLogger().get_logger()


def get_parser_day7() -> argparse.ArgumentParser:
    """Create a parser for the module."""
    parser = argparse.ArgumentParser(
        description="Provide the sum of all of the calibration values.",
        add_help=False,
    )
    day7 = parser.add_argument_group("day7", "Solution for day7.")
    day7.add_argument(
        "--data-day7", type=Path, help="data to decode", default=DEFAULT_DAY7_DATA
    )
    return parser


CardRanks = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

CardRanksJ = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}


@total_ordering
class HandType(Enum):
    FiveKind = 6
    FourKind = 5
    FullHouse = 4
    ThreeKind = 3
    TwoPair = 2
    OnePair = 1
    HighCard = 0

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


def get_hand_type(hand: str, part2: bool = False) -> HandType:
    """Returns the HandType enum value corresponding to the given card label."""
    if part2:
        hand_card = [(card, hand.count(card)) for card in set(hand.replace("J", ""))]
        joker = hand.count("J")
    else:
        hand_card = [(card, hand.count(card)) for card in set(hand)]
        joker = 0
    if len(hand_card) == 1 or len(hand_card) == 0:
        return HandType.FiveKind
    elif len(hand_card) == 2:
        if max(hand_card[0][1], hand_card[1][1]) + joker == 4:
            return HandType.FourKind
        else:
            return HandType.FullHouse
    elif len(hand_card) == 3:
        if max(hand_card[0][1], hand_card[1][1], hand_card[2][1]) + joker == 3:
            return HandType.ThreeKind
        else:
            return HandType.TwoPair
    elif len(hand_card) == 4:
        return HandType.OnePair
    else:
        return HandType.HighCard


class Hand:
    def __init__(self, cards: str, bid: int, part2: bool = False) -> None:
        self.bid = bid
        self.cards = cards
        self.type = get_hand_type(cards, part2)
        self.jcard = part2

    def __lt__(self, other):
        if self.type != other.type:
            return self.type < other.type
        for index, card in enumerate(self.cards):
            if card != other.cards[index]:
                if self.jcard:
                    return CardRanksJ[card] < CardRanksJ[other.cards[index]]
                else:
                    return CardRanks[card] < CardRanks[other.cards[index]]
        return True

    def __str__(self):
        return self.cards


def day7(part2: bool = False, **kwargs) -> int:
    """
    Main routines for Day 7

    :param data_day7: Path data to consider
    :param part2: bool Calculate solution for PART2 otherwise for PART1

    :return: None.
    """
    if "data_day7" not in kwargs:
        raise AdventOfCodeException("Undefined parameter 'data_day7'")

    hands: List[Hand] = parse_data(kwargs["data_day7"], part2)
    hands.sort()
    result = sum([hand.bid * (index + 1) for index, hand in enumerate(hands)])
    # Print the result
    logger.info("The solution of day7 PART%d is: %d", 2 if part2 else 1, result)
    return result


def parse_data(data_path: Path, part2: bool = False) -> None:
    """Read Each Line and parse the content"""
    hands: List[Hand] = []
    with open(data_path, "r") as f:
        for line in f:
            hand, bid = line.strip().split()
            hands.append(Hand(hand, int(bid), part2))
    return hands
