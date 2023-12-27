import os
import unittest

from ..main import day16

FILE_PATH = os.path.abspath(__file__)
EXAMPLE_DAY16 = os.path.dirname(FILE_PATH) + "/../data/example.txt"


class TestDay16(unittest.TestCase):
    def test_day16_part1(self):
        result = day16(data_day16=EXAMPLE_DAY16)
        self.assertEqual(result, 46)

    def test_day16_part2(self):
        result = day16(data_day16=EXAMPLE_DAY16, part2=True)
        self.assertEqual(result, 51)


if __name__ == "__main__":
    unittest.main()
