import os
import unittest

from ..main import day1, decode_line

FILE_PATH = os.path.abspath(__file__)
EXAMPLE_DAY1_PART1_DATA = os.path.dirname(FILE_PATH) + "/../data/example-part1.txt"
EXAMPLE_DAY1_PART2_DATA = os.path.dirname(FILE_PATH) + "/../data/example-part2.txt"
SOLUTION_PART1 = [12, 38, 15, 77]
SOLUTION_PART2 = [29, 83, 13, 24, 42, 14, 76]


class TestDay1(unittest.TestCase):
    def test_decode_line_part1(self):
        with open(EXAMPLE_DAY1_PART1_DATA, "r") as f:
            for index, line in enumerate(f):
                self.assertEqual(
                    decode_line(line.strip(), part2=False), SOLUTION_PART1[index]
                )

    def test_day1_part1(self):
        result = day1(data_day1=EXAMPLE_DAY1_PART1_DATA, part2=False)
        self.assertEqual(result, 142)

    def test_decode_line_part2(self):
        with open(EXAMPLE_DAY1_PART2_DATA, "r") as f:
            for index, line in enumerate(f):
                self.assertEqual(
                    decode_line(line.strip(), part2=True), SOLUTION_PART2[index]
                )

    def test_day1_part2(self):
        result = day1(data_day1=EXAMPLE_DAY1_PART2_DATA, part2=True)
        self.assertEqual(result, 281)


if __name__ == "__main__":
    unittest.main()
