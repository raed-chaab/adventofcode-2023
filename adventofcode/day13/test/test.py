import os
import unittest

from ..main import day13

FILE_PATH = os.path.abspath(__file__)
EXAMPLE_DAY13_VERTICAL = os.path.dirname(FILE_PATH) + "/../data/example-vertical.txt"
EXAMPLE_DAY13_HORIZONTAL = (
    os.path.dirname(FILE_PATH) + "/../data/example-horizontal.txt"
)
EXAMPLE_DAY13_VERTICAL2 = os.path.dirname(FILE_PATH) + "/../data/example-vertical2.txt"


class TestDay13(unittest.TestCase):
    def test_day13_part1(self):
        result = day13(data_day13=EXAMPLE_DAY13_HORIZONTAL)
        self.assertEqual(result, 1400)

    def test2_day13_part1(self):
        result = day13(data_day13=EXAMPLE_DAY13_VERTICAL)
        self.assertEqual(result, 17)

    def test_day13_part2(self):
        result = day13(data_day13=EXAMPLE_DAY13_VERTICAL2, part2=True)
        self.assertEqual(result, 400)


if __name__ == "__main__":
    unittest.main()
