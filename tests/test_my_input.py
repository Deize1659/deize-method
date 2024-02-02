import os
import sys
import unittest

from src.my_method.my_input import input_int  # noqa: E402
from src.my_method.my_input import input_float, input_str  # noqa: E402


class UnitTest(unittest.TestCase):
    def test1(self) -> None:
        self.assertEqual(input_str("文字列"), "1")

    def test2(self) -> None:
        self.assertEqual(input_int("整数"), 1)

    def test3(self) -> None:
        self.assertEqual(input_float("数"), 1.0)


if __name__ == "__main__":
    unittest.main()
