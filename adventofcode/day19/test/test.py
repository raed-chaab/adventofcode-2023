import os
import unittest

from ..main import day19

FILE_PATH = os.path.abspath(__file__)
EXAMPLE_DAY19 = os.path.dirname(FILE_PATH) + "/../data/example.txt"


class TestDay19(unittest.TestCase):
    # def test_day19_part1(self):
    #     result = day19(data_day19=EXAMPLE_DAY19)
    #     self.assertEqual(result, 19114)

    def test_day19_part2(self):
        result = day19(data_day19=EXAMPLE_DAY19, part2=True)
        self.assertEqual(result, 167409079868000)


if __name__ == "__main__":
    unittest.main()
