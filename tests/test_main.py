import unittest

from src.helpers_main import extract_title


class TestSiteGen(unittest.TestCase):
    def test_extract_title(self):
        md: str = "# title\n\nhello world"
        self.assertEqual(extract_title(md), "title")
