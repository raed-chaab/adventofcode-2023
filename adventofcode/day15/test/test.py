import os
import unittest

from ..main import day15

FILE_PATH = os.path.abspath(__file__)
EXAMPLE_DAY15 = os.path.dirname(FILE_PATH) + "/../data/example.txt"


class TestDay15(unittest.TestCase):
    def test_day15_part1(self):
        result = day15(data_day15=EXAMPLE_DAY15)
        self.assertEqual(result, 1320)

    def test_day15_part2(self):
        result = day15(data_day15=EXAMPLE_DAY15, part2=True)
        self.assertEqual(result, 145)


if __name__ == "__main__":
    unittest.main()
