import os
import unittest

from ..main import day17

FILE_PATH = os.path.abspath(__file__)
EXAMPLE_DAY17 = os.path.dirname(FILE_PATH) + "/../data/example.txt"


class TestDay17(unittest.TestCase):
    def test_day17_part1(self):
        result = day17(data_day17=EXAMPLE_DAY17)
        self.assertEqual(result, 102)

    def test_day17_part2(self):
        result = day17(data_day17=EXAMPLE_DAY17, part2=True)
        self.assertEqual(result, 94)


if __name__ == "__main__":
    unittest.main()
