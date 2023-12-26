import os
import unittest

from ..main import day12

FILE_PATH = os.path.abspath(__file__)
EXAMPLE_DAY12_PART1_DATA = os.path.dirname(FILE_PATH) + "/../data/example-part1.txt"
EXAMPLE2_DAY12_PART1_DATA = os.path.dirname(FILE_PATH) + "/../data/example2-part1.txt"
EXAMPLE3_DAY12_PART1_DATA = os.path.dirname(FILE_PATH) + "/../data/example3-part1.txt"
EXAMPLE4_DAY12_PART1_DATA = os.path.dirname(FILE_PATH) + "/../data/example4-part1.txt"
EXAMPLE5_DAY12_PART1_DATA = os.path.dirname(FILE_PATH) + "/../data/example5-part1.txt"
EXAMPLE6_DAY12_PART1_DATA = os.path.dirname(FILE_PATH) + "/../data/example6-part1.txt"


class TestDay12(unittest.TestCase):
    def test_day12_part1(self):
        result = day12(data_day12=EXAMPLE_DAY12_PART1_DATA)
        self.assertEqual(result, 1)

    def test2_day12_part1(self):
        result = day12(data_day12=EXAMPLE2_DAY12_PART1_DATA)
        self.assertEqual(result, 4)

    def test3_day12_part1(self):
        result = day12(data_day12=EXAMPLE3_DAY12_PART1_DATA)
        self.assertEqual(result, 1)

    def test4_day12_part1(self):
        result = day12(data_day12=EXAMPLE4_DAY12_PART1_DATA)
        self.assertEqual(result, 1)

    def test5_day12_part1(self):
        result = day12(data_day12=EXAMPLE5_DAY12_PART1_DATA)
        self.assertEqual(result, 4)

    def test6_day12_part1(self):
        result = day12(data_day12=EXAMPLE6_DAY12_PART1_DATA)
        self.assertEqual(result, 10)

    def test_day12_part2(self):
        result = day12(data_day12=EXAMPLE_DAY12_PART1_DATA, part2=True)
        self.assertEqual(result, 1)

    def test2_day12_part2(self):
        result = day12(data_day12=EXAMPLE2_DAY12_PART1_DATA, part2=True)
        self.assertEqual(result, 16384)

    def test3_day12_part2(self):
        result = day12(data_day12=EXAMPLE3_DAY12_PART1_DATA, part2=True)
        self.assertEqual(result, 1)

    def test4_day12_part2(self):
        result = day12(data_day12=EXAMPLE4_DAY12_PART1_DATA, part2=True)
        self.assertEqual(result, 16)

    def test5_day12_part2(self):
        result = day12(data_day12=EXAMPLE5_DAY12_PART1_DATA, part2=True)
        self.assertEqual(result, 2500)

    def test6_day12_part2(self):
        result = day12(data_day12=EXAMPLE6_DAY12_PART1_DATA, part2=True)
        self.assertEqual(result, 506250)


if __name__ == "__main__":
    unittest.main()
