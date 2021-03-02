import unittest
from domain import BlocksWorld
from solvers import AlgorithmicSolver, AStarSolver
"""
Tests for the solvers module.
"""

class TestDomain(unittest.TestCase):

    def test_astar(self):
        """
        Test the A* solver.
        """
        s0 = BlocksWorld([['b1', 'b2', 'b3'],['b4', 'b5', 'b6']])
        goal = BlocksWorld([['b3', 'b2', 'b1'],['b6', 'b5', 'b4']])
        plan = AStarSolver(s0, goal, h=goal.h, prune=BlocksWorld.prune)
        path = plan.reconstruct_path()
        self.assertEqual(len(path), 12)

    def test_algo(self):
        """
        Test the algorithmic solver.
        """
        s0 = BlocksWorld([['b1', 'b2', 'b3'],['b4', 'b5', 'b6']])
        goal = BlocksWorld([['b3', 'b2', 'b1'],['b6', 'b5', 'b4']])
        plan = AlgorithmicSolver(s0, goal)
        path = plan.reconstruct_path()
        self.assertEqual(len(path), 12)

if __name__ == '__main__':
    unittest.main()
