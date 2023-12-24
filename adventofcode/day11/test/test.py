import os
import unittest

from ..main import Univers, day11, parse_data

FILE_PATH = os.path.abspath(__file__)
EXAMPLE_DAY11_PART1_DATA = os.path.dirname(FILE_PATH) + "/../data/example-part1.txt"


class TestDay11(unittest.TestCase):
    def test_get_empty_lines(self):
        univers: Univers = parse_data(EXAMPLE_DAY11_PART1_DATA)
        univers.expand()
        self.assertEqual(univers.empty_rows, [3, 7])
        self.assertEqual(univers.empty_cols, [2, 5, 8])

    def test_day11_part1(self):
        result = day11(data_day11=EXAMPLE_DAY11_PART1_DATA)
        self.assertEqual(result, 374)

    def test_day11_part2(self):
        univers: Univers = parse_data(EXAMPLE_DAY11_PART1_DATA, 10)
        univers.expand()
        result = sum(univers.get_shortests_path())
        self.assertEqual(result, 1030)

    def test2_day11_part2(self):
        univers: Univers = parse_data(EXAMPLE_DAY11_PART1_DATA, 100)
        univers.expand()
        result = sum(univers.get_shortests_path())
        self.assertEqual(result, 8410)


if __name__ == "__main__":
    unittest.main()
