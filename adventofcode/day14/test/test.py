import os
import unittest

from ..main import day14

FILE_PATH = os.path.abspath(__file__)
EXAMPLE_DAY14 = os.path.dirname(FILE_PATH) + "/../data/example.txt"


class TestDay14(unittest.TestCase):
    def test_day14_part1(self):
        result = day14(data_day14=EXAMPLE_DAY14)
        self.assertEqual(result, 136)

    def test_day14_part2(self):
        result = day14(data_day14=EXAMPLE_DAY14, part2=True)
        self.assertEqual(result, 64)


if __name__ == "__main__":
    unittest.main()
