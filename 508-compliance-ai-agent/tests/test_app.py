# tests/test_app.py

import unittest
import app.main

class TestApp(unittest.TestCase):
    def test_main_import(self):
        self.assertIsNotNone(app.main)

if __name__ == "__main__":
    unittest.main()
