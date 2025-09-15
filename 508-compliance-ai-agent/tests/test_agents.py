# tests/test_agents.py

import unittest
from agents.source_and_validation import SourceAndValidationAgent

class TestSourceAndValidationAgent(unittest.TestCase):
    def test_validate_url(self):
        agent = SourceAndValidationAgent()
        self.assertTrue(agent.validate_url("https://example.com"))
        self.assertFalse(agent.validate_url("not_a_url"))

if __name__ == "__main__":
    unittest.main()
