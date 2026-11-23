import unittest
from domain import BlocksWorld
from solvers import AlgorithmicSolver, AStarSolver
from solvers.solver import Solver
from tests.helpers import (optimal_length, plan_reaches_goal,
                           random_problems)
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
        self.assertGreater(plan.num_expanded(), 0)

    def test_algo(self):
        """
        Test the algorithmic solver.
        """
        s0 = BlocksWorld([['b1', 'b2', 'b3'],['b4', 'b5', 'b6']])
        goal = BlocksWorld([['b3', 'b2', 'b1'],['b6', 'b5', 'b4']])
        plan = AlgorithmicSolver(s0, goal)
        path = plan.reconstruct_path()
        self.assertEqual(len(path), 12)

    def test_algo_keeps_finished_stacks(self):
        """
        Stacks that are already in place must not be taken apart.
        """
        s0 = [['b1', 'b2', 'b0']]
        goal = [['b1', 'b2'], ['b0']]
        path = AlgorithmicSolver(BlocksWorld(s0),
                                 BlocksWorld(goal)).reconstruct_path()
        self.assertEqual(path, [('unstack', 'b0', 'b2'), ('putdown', 'b0')])

    def test_algo_already_solved(self):
        """
        Nothing to do if the initial state is the goal.
        """
        stacks = [['a', 'b'], ['c']]
        plan = AlgorithmicSolver(BlocksWorld(stacks), BlocksWorld(stacks))
        self.assertEqual(plan.reconstruct_path(), [])

    def test_algo_random(self):
        """
        The algorithmic solver must always reach the goal.
        """
        for s0, goal in random_problems(300):
            path = AlgorithmicSolver(BlocksWorld(s0),
                                     BlocksWorld(goal)).reconstruct_path()
            self.assertTrue(plan_reaches_goal(s0, goal, path), (s0, goal))

    def test_astar_random(self):
        """
        A* must find valid optimal plans (checked against a BFS oracle).
        """
        for s0, goal in random_problems(150, max_blocks=5, seed=2):
            goal_state = BlocksWorld(goal)
            path = AStarSolver(BlocksWorld(s0), goal_state, h=goal_state.h,
                               prune=BlocksWorld.prune).reconstruct_path()
            self.assertTrue(plan_reaches_goal(s0, goal, path), (s0, goal))
            self.assertEqual(len(path), optimal_length(s0, goal), (s0, goal))

    def test_astar_no_solution(self):
        """
        No plan is returned if the goal can not be reached.
        """
        plan = AStarSolver(BlocksWorld([['a'], ['b']]),
                           BlocksWorld([['a', 'c']]),
                           prune=BlocksWorld.prune)
        self.assertIsNone(plan.goal)
        self.assertEqual(plan.reconstruct_path(), [])

    def test_astar_default_arguments(self):
        """
        The default g, h and prune must still allow the search to progress.
        """
        plan = AStarSolver(BlocksWorld([['a', 'b']]), BlocksWorld([['b', 'a']]))
        self.assertEqual(len(plan.reconstruct_path()), 4)

    def test_solver_interface(self):
        """
        Test the base class.
        """
        solver = Solver()
        self.assertEqual(solver.num_expanded(), 0)
        with self.assertRaises(NotImplementedError):
            solver.reconstruct_path()

if __name__ == '__main__':
    unittest.main()
