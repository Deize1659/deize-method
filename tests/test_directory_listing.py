import os
import sys
import unittest

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.directory_listing import directory_listing  # noqa: E402


class UnitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.file = ["test.json", "test.mp4", "test.txt", "test.wav"]
        self.ext = (
            ".mp4",
            ".wav",
        )
        self.only_file = ["test.mp4", "test.wav"]
        self.not_file = ["test.json", "test.txt"]
        return super().setUp()

    def test1(self):
        self.assertEqual(directory_listing(), self.file)

    def test2(self):
        self.assertEqual(directory_listing(ext=self.ext), self.only_file)

    def test3(self):
        self.assertEqual(directory_listing(exc_ext=self.ext), self.not_file)


if __name__ == "__main__":
    unittest.main()
