import unittest

from src.my_method.directory_create import directory_create


class UnitTest(unittest.TestCase):
    def test1(self) -> None:
        self.assertEqual(directory_create("test1"), True)

    def test2(self) -> None:
        self.assertEqual(directory_create("test1"), True)

    def test3(self) -> None:
        self.assertEqual(directory_create(1), False)


if __name__ == "__main__":
    unittest.main()
