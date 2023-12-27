import os
import unittest

from ..main import day18

FILE_PATH = os.path.abspath(__file__)
EXAMPLE_DAY18 = os.path.dirname(FILE_PATH) + "/../data/example.txt"


class TestDay18(unittest.TestCase):
    def test_day18_part1(self):
        result = day18(data_day18=EXAMPLE_DAY18)
        self.assertEqual(result, 62)

    def test_day18_part2(self):
        result = day18(data_day18=EXAMPLE_DAY18, part2=True)
        self.assertEqual(result, 952408144115)


if __name__ == "__main__":
    unittest.main()
