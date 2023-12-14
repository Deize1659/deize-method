import unittest

from my_method.version_check import VersionCheck


class TestVersionCheck(unittest.TestCase):
    def setUp(self) -> None:
        self.version = "2.0.0"
        self.url = "https://github.com/ymorishima030/ymorishima030-method.git"
        self.vc = VersionCheck(self.url, self.version)

    def test_check_version(self) -> None:
        self.assertTrue(self.vc.check_version())
        self.assertTrue(self.vc())
        self.vc._url = ""
        self.assertTrue(self.vc.check_version())
        self.assertTrue(self.vc())
        self.vc._version = "v2.0.0"
        self.assertFalse(self.vc.check_version())
        self.assertFalse(self.vc())
        self.vc_version = ""
        self.assertFalse(self.vc.check_version())
        self.assertFalse(self.vc())
