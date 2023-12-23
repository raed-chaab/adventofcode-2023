import os
import unittest

from ..main import day9

FILE_PATH = os.path.abspath(__file__)
EXAMPLE_DAY9_PART1_DATA = os.path.dirname(FILE_PATH) + "/../data/example-part1.txt"


class TestDay9(unittest.TestCase):
    def test_day9_part1(self):
        result = day9(data_day9=EXAMPLE_DAY9_PART1_DATA)
        self.assertEqual(result, 114)

    def test_day9_part2(self):
        result = day9(data_day9=EXAMPLE_DAY9_PART1_DATA, part2=True)
        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()
