import unittest
from domain import BlocksWorld
"""
Tests for the domain module.
"""

class TestDomain(unittest.TestCase):

    def test_actions(self):
        """
        Test the application of actions to a given domain.
        """
        bw = BlocksWorld([[3,2,1]])
        for action in [
            ('unstack', 1, 2), ('putdown', 1), ('unstack', 2, 3),
            ('stack', 2, 1), ('pickup', 3), ('stack', 3, 2)]:
           bw.apply(action)
        self.assertEqual(bw, BlocksWorld([[1,2,3]]))

if __name__ == '__main__':
    unittest.main()
