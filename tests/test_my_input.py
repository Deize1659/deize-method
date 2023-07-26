import os
import sys
import unittest

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from my_method.my_input import input_float, input_int, input_str  # noqa: E402


class UnitTest(unittest.TestCase):
    def test1(self):
        self.assertEqual(input_str("文字列"), "1")

    def test2(self):
        self.assertEqual(input_int("整数"), 1)

    def test3(self):
        self.assertEqual(input_float("数"), 1.0)


if __name__ == "__main__":
    unittest.main()
