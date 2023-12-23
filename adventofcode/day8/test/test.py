import os
import unittest

from ..main import day8

FILE_PATH = os.path.abspath(__file__)
EXAMPLE_DAY8_PART1_DATA = os.path.dirname(FILE_PATH) + "/../data/example-part1.txt"
EXAMPLE2_DAY8_PART1_DATA = os.path.dirname(FILE_PATH) + "/../data/example2-part1.txt"
EXAMPLE_DAY8_PART2_DATA = os.path.dirname(FILE_PATH) + "/../data/example-part2.txt"


class TestDay8(unittest.TestCase):
    def test_day8_part1(self):
        result = day8(data_day8=EXAMPLE_DAY8_PART1_DATA)
        self.assertEqual(result, 2)

    def test2_day8_part1(self):
        result = day8(data_day8=EXAMPLE2_DAY8_PART1_DATA)
        self.assertEqual(result, 6)

    def test_day8_part2(self):
        result = day8(data_day8=EXAMPLE_DAY8_PART2_DATA, part2=True)
        self.assertEqual(result, 6)


if __name__ == "__main__":
    unittest.main()
