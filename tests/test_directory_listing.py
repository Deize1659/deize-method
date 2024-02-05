import os
import shutil
import tempfile
import unittest
from pathlib import Path

from src.my_method.directory_listing import DirectoryListing as dl
from src.my_method.directory_listing import DirectoryListingPathlib as dlp


class TestDirectoryListing(unittest.TestCase):
    def setUp(self) -> None:
        self.cwd = os.getcwd()
        self.test_dir = os.path.join(self.cwd, "test_dir")
        os.mkdir(self.test_dir)
        os.chdir(self.test_dir)
        self.text_ext = ".txt"
        self.wav_ext = ".wav"
        self.test_file_name = "test_file"
        self.test_name = "test"
        self.test1_num = "1"
        self.test2_num = "2"
        self.test1 = self.test_name + self.test1_num
        self.test2 = self.test_name + self.test2_num
        self.test_txt = self.test_file_name + self.text_ext
        self.test_wav = self.test_file_name + self.wav_ext
        os.mkdir(os.path.join(self.test_dir, self.test1))
        os.mkdir(os.path.join(self.test_dir, self.test2))
        self.test_txt_path = os.path.join(self.test_dir, self.test_txt)
        self.test_wav_path = os.path.join(self.test_dir, self.test_wav)
        with open(self.test_txt, "w"):
            pass
        with open(self.test_wav, "w"):
            pass

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        shutil.rmtree(self.test_dir)

    def test_file_listing(self) -> None:
        self.assertEqual(dl.file_listing(self.test_dir), (self.test_txt, self.test_wav))
        self.assertEqual(dl.file_listing(self.test_dir, self.text_ext), (self.test_txt,))
        self.assertEqual(dl.file_listing(self.test_dir, (self.text_ext,)), (self.test_txt,))
        self.assertEqual(dl.file_listing(self.test_dir, self.wav_ext), (self.test_wav,))
        self.assertEqual(dl.file_listing(self.test_dir, (self.wav_ext,)), (self.test_wav,))
        self.assertEqual(dl.file_listing(self.test_dir, (self.text_ext, self.wav_ext)), (self.test_txt, self.test_wav))
        self.assertEqual(dl.file_listing(self.test_dir, "error"), ())
        self.assertEqual(dl.file_listing(self.test_dir, exc_targets=self.test_txt), (self.test_wav,))
        self.assertEqual(dl.file_listing(self.test_dir, exc_targets=(self.test_txt,)), (self.test_wav,))
        self.assertEqual(dl.file_listing(self.test_dir, exc_targets=self.test_wav), (self.test_txt,))
        self.assertEqual(dl.file_listing(self.test_dir, exc_targets=(self.test_wav,)), (self.test_txt,))
        self.assertEqual(dl.file_listing(self.test_dir, exc_targets=(self.test_txt, self.test_wav)), ())
        self.assertEqual(dl.file_listing(self.test_dir, exc_targets="error"), (self.test_txt, self.test_wav))

    def test_dir_listing(self) -> None:
        self.assertEqual(dl.dir_listing(self.test_dir), (self.test1, self.test2))
        self.assertEqual(dl.dir_listing(self.test_dir, self.test1_num), (self.test1,))
        self.assertEqual(dl.dir_listing(self.test_dir, (self.test1_num,)), (self.test1,))
        self.assertEqual(dl.dir_listing(self.test_dir, self.test2_num), (self.test2,))
        self.assertEqual(dl.dir_listing(self.test_dir, (self.test2_num,)), (self.test2,))
        self.assertEqual(dl.dir_listing(self.test_dir, (self.test1_num, self.test2_num)), (self.test1, self.test2))
        self.assertEqual(dl.dir_listing(self.test_dir, "error"), ())
        self.assertEqual(dl.dir_listing(self.test_dir, exc_targets=self.test1), (self.test2,))
        self.assertEqual(dl.dir_listing(self.test_dir, exc_targets=(self.test1,)), (self.test2,))
        self.assertEqual(dl.dir_listing(self.test_dir, exc_targets=self.test2), (self.test1,))
        self.assertEqual(dl.dir_listing(self.test_dir, exc_targets=(self.test2,)), (self.test1,))
        self.assertEqual(dl.dir_listing(self.test_dir, exc_targets=(self.test1, self.test2)), ())
        self.assertEqual(dl.dir_listing(self.test_dir, exc_targets="error"), (self.test1, self.test2))

    def test_all_listing(self) -> None:
        self.assertEqual(dl.all_listing(self.test_dir), (self.test1, self.test2, self.test_txt, self.test_wav))
        self.assertEqual(dl.all_listing(self.test_dir, self.test1_num), (self.test1,))
        self.assertEqual(dl.all_listing(self.test_dir, (self.test1_num,)), (self.test1,))
        self.assertEqual(dl.all_listing(self.test_dir, self.test2_num), (self.test2,))
        self.assertEqual(dl.all_listing(self.test_dir, (self.test2_num,)), (self.test2,))
        self.assertEqual(dl.all_listing(self.test_dir, self.text_ext), (self.test_txt,))
        self.assertEqual(dl.all_listing(self.test_dir, (self.text_ext,)), (self.test_txt,))
        self.assertEqual(dl.all_listing(self.test_dir, self.wav_ext), (self.test_wav,))
        self.assertEqual(dl.all_listing(self.test_dir, (self.wav_ext,)), (self.test_wav,))
        self.assertEqual(dl.all_listing(self.test_dir, (self.test1_num, self.test2_num)), (self.test1, self.test2))
        self.assertEqual(dl.all_listing(self.test_dir, (self.test1_num, self.wav_ext)), (self.test1, self.test_wav))
        self.assertEqual(dl.all_listing(self.test_dir, (self.test2_num, self.text_ext)), (self.test2, self.test_txt))
        self.assertEqual(dl.all_listing(self.test_dir, (self.text_ext, self.wav_ext)), (self.test_txt, self.test_wav))
        self.assertEqual(
            dl.all_listing(self.test_dir, (self.test1_num, self.test2_num, self.text_ext)),
            (self.test1, self.test2, self.test_txt),
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, (self.test1_num, self.test2_num, self.wav_ext)),
            (self.test1, self.test2, self.test_wav),
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, (self.test1_num, self.text_ext, self.wav_ext)),
            (self.test1, self.test_txt, self.test_wav),
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, (self.test2_num, self.text_ext, self.wav_ext)),
            (self.test2, self.test_txt, self.test_wav),
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, (self.test1_num, self.test2_num, self.text_ext, self.wav_ext)),
            (self.test1, self.test2, self.test_txt, self.test_wav),
        )
        self.assertEqual(dl.all_listing(self.test_dir, "error"), ())
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=self.test1), (self.test2, self.test_txt, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test1,)), (self.test2, self.test_txt, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=self.test2), (self.test1, self.test_txt, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test2,)), (self.test1, self.test_txt, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=self.test_txt), (self.test1, self.test2, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test_txt,)), (self.test1, self.test2, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=self.test_wav), (self.test1, self.test2, self.test_txt)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test_wav,)), (self.test1, self.test2, self.test_txt)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test1, self.test2)), (self.test_txt, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test1, self.test_txt)), (self.test2, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test1, self.test_wav)), (self.test2, self.test_txt)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test2, self.test_txt)), (self.test1, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test2, self.test_wav)), (self.test1, self.test_txt)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test_txt, self.test_wav)), (self.test1, self.test2)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test1, self.test2, self.test_txt)), (self.test_wav,)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test1, self.test2, self.test_wav)), (self.test_txt,)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test1, self.test_txt, self.test_wav)), (self.test2,)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test2, self.test_txt, self.test_wav)), (self.test1,)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test1, self.test2, self.test_txt, self.test_wav)), ()
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets="error"),
            (self.test1, self.test2, self.test_txt, self.test_wav),
        )


class TestDirectoryListingPathlib(unittest.TestCase):
    test_dir: Path
    text_ext: str
    wav_ext: str
    test_file_name: str
    test_name: str
    test1_num: str
    test2_num: str
    test1: str
    test2: str
    test_txt: str
    test_wav: str
    test_txt_path: Path
    test_wav_path: Path

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_dir = Path(tempfile.mkdtemp())
        os.chdir(cls.test_dir)
        cls.text_ext = ".txt"
        cls.wav_ext = ".wav"
        cls.test_file_name = "test_file"
        cls.test_name = "test"
        cls.test1_num = "1"
        cls.test2_num = "2"
        cls.test1 = cls.test_name + cls.test1_num
        cls.test2 = cls.test_name + cls.test2_num
        cls.test_txt = cls.test_file_name + cls.text_ext
        cls.test_wav = cls.test_file_name + cls.wav_ext
        (cls.test_dir / cls.test1).mkdir()
        (cls.test_dir / cls.test2).mkdir()
        cls.test_txt_path = cls.test_dir / cls.test_txt
        cls.test_wav_path = cls.test_dir / cls.test_wav
        with open(cls.test_txt_path.name, "w"):
            pass
        with open(cls.test_wav_path.name, "w"):
            pass
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        os.chdir(str(Path.cwd()))
        shutil.rmtree(str(cls.test_dir))
        cls.test_dir.rmdir()
        return super().tearDownClass()

    def test_file_listing(self) -> None:
        self.assertEqual(dlp.file_listing(self.test_dir), (self.test_txt, self.test_wav))
        self.assertEqual(dlp.file_listing(self.test_dir, self.text_ext), (self.test_txt,))
        self.assertEqual(dlp.file_listing(self.test_dir, (self.text_ext,)), (self.test_txt,))
        self.assertEqual(dlp.file_listing(self.test_dir, self.wav_ext), (self.test_wav,))
        self.assertEqual(dlp.file_listing(self.test_dir, (self.wav_ext,)), (self.test_wav,))
        self.assertEqual(
            dlp.file_listing(self.test_dir, (self.text_ext, self.wav_ext)), (self.test_txt, self.test_wav)
        )
        self.assertEqual(dlp.file_listing(self.test_dir, "error"), ())
        self.assertEqual(dlp.file_listing(self.test_dir, exc_targets=self.test_txt), (self.test_wav,))
        self.assertEqual(dlp.file_listing(self.test_dir, exc_targets=(self.test_txt,)), (self.test_wav,))
        self.assertEqual(dlp.file_listing(self.test_dir, exc_targets=self.test_wav), (self.test_txt,))
        self.assertEqual(dlp.file_listing(self.test_dir, exc_targets=(self.test_wav,)), (self.test_txt,))
        self.assertEqual(dlp.file_listing(self.test_dir, exc_targets=(self.test_txt, self.test_wav)), ())
        self.assertEqual(dlp.file_listing(self.test_dir, exc_targets="error"), (self.test_txt, self.test_wav))


if __name__ == "__main__":
    unittest.main()
