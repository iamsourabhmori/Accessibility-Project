# tests/test_tools.py

import unittest
from tools.parsers import is_supported_file

class TestParsers(unittest.TestCase):
    def test_supported_file(self):
        self.assertTrue(is_supported_file("document.pdf"))
        self.assertFalse(is_supported_file("image.png"))

if __name__ == "__main__":
    unittest.main()
