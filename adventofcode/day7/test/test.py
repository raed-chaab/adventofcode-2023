import os
import unittest
from typing import List

from ..main import Hand, day7, parse_data

FILE_PATH = os.path.abspath(__file__)
EXAMPLE_DAY7_TYPE_DATA = os.path.dirname(FILE_PATH) + "/../data/example-type.txt"
EXAMPLE_DAY7_TYPE2_DATA = os.path.dirname(FILE_PATH) + "/../data/example-type2.txt"
EXAMPLE_DAY7_PART1_DATA = os.path.dirname(FILE_PATH) + "/../data/example-part1.txt"
SOLUTION_ORDER_PART1 = ["32T3K", "KTJJT", "KK677", "T55J5", "QQQJA"]
SOLUTION_ORDER_PART2 = ["32T3K", "KK677", "T55J5", "QQQJA", "KTJJT"]


class TestDay7(unittest.TestCase):
    def test_parse_data_part1(self):
        hands: List[Hand] = parse_data(EXAMPLE_DAY7_TYPE_DATA)
        for hand in hands:
            self.assertEqual(hand.type.value, hand.bid)

    def test_sort_hands_part1(self):
        hands: List[Hand] = parse_data(EXAMPLE_DAY7_PART1_DATA)
        hands.sort()
        for index, hand in enumerate(hands):
            self.assertEqual(hand.cards, SOLUTION_ORDER_PART1[index])

    def test_day7_part1(self):
        result = day7(data_day7=EXAMPLE_DAY7_PART1_DATA)
        self.assertEqual(result, 6440)

    def test_parse_data_part2(self):
        hands: List[Hand] = parse_data(EXAMPLE_DAY7_TYPE2_DATA, part2=True)
        for hand in hands:
            self.assertEqual(hand.type.value, hand.bid)

    def test_sort_hands_part2(self):
        hands: List[Hand] = parse_data(EXAMPLE_DAY7_PART1_DATA, part2=True)
        hands.sort()
        for index, hand in enumerate(hands):
            self.assertEqual(hand.cards, SOLUTION_ORDER_PART2[index])

    def test_day7_part2(self):
        result = day7(data_day7=EXAMPLE_DAY7_PART1_DATA, part2=True)
        self.assertEqual(result, 5905)


if __name__ == "__main__":
    unittest.main()
