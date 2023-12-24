import os
import unittest

from ..main import day10, parse_data

FILE_PATH = os.path.abspath(__file__)
EXAMPLE_DAY10_PART1_DATA = os.path.dirname(FILE_PATH) + "/../data/example-part1.txt"
EXAMPLE2_DAY10_PART1_DATA = os.path.dirname(FILE_PATH) + "/../data/example2-part1.txt"


class TestDay10(unittest.TestCase):
    def test_find_start(self):
        maze = parse_data(EXAMPLE2_DAY10_PART1_DATA)
        row, col = maze.find_start()
        self.assertEqual(maze.pipes[row][col], "S")

    def test_day10_part1(self):
        result = day10(data_day10=EXAMPLE_DAY10_PART1_DATA)
        self.assertEqual(result, 4)

    def test2_day10_part1(self):
        result = day10(data_day10=EXAMPLE2_DAY10_PART1_DATA)
        self.assertEqual(result, 8)


if __name__ == "__main__":
    unittest.main()
