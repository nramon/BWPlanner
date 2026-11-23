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

    def test_invalid_action(self):
        """
        Unknown actions must be rejected.
        """
        with self.assertRaises(ValueError):
            BlocksWorld([[1]]).apply(('jump', 1))

    def test_illegal_actions(self):
        """
        Actions that violate the domain preconditions must be rejected.
        """
        with self.assertRaises(AssertionError):
            BlocksWorld([[1, 2]]).apply(('pickup', 1))
        with self.assertRaises(AssertionError):
            BlocksWorld([[1]]).apply(('putdown', 1))
        with self.assertRaises(AssertionError):
            BlocksWorld([[1], [2]]).apply(('stack', 1, 2))

    def test_copy_is_independent(self):
        """
        Applying an action to a copy must not modify the original.
        """
        bw = BlocksWorld([[2, 1]])
        new = bw.copy(('unstack', 1, 2))
        self.assertEqual(new.arm, 1)
        self.assertEqual(new.last_action(), ('unstack', 1, 2))
        self.assertIsNone(bw.arm)
        self.assertEqual(bw.stacks, {1: [2, 1]})

    def test_expand(self):
        """
        Test the successors of a state with and without a held block.
        """
        bw = BlocksWorld([[1], [3, 2]])
        self.assertCountEqual(
            [s.last_action() for s in bw.expand()],
            [('pickup', 1), ('unstack', 2, 3)])

        held = bw.copy(('pickup', 1))
        self.assertCountEqual(
            [s.last_action() for s in held.expand()],
            [('putdown', 1), ('stack', 1, 2)])

    def test_h(self):
        """
        Test the heuristic.
        """
        goal = BlocksWorld([[1, 2, 3]])
        self.assertEqual(goal.h(BlocksWorld([[1, 2, 3]])), 0)

        # Every block has to move once.
        self.assertEqual(goal.h(BlocksWorld([[1], [2], [3]])), 4)

        # Block 2 is in place but sits on block 1, which has to move: 2 moves
        # twice.
        self.assertEqual(goal.h(BlocksWorld([[3, 1, 2]])), 2 * 3 + 2 * 1)

        # The held block is not counted.
        held = BlocksWorld([[1], [2], [3]]).copy(('pickup', 3))
        self.assertEqual(goal.h(held), 2)

    def test_prune(self):
        """
        A state that repeats in its own path must be pruned.
        """
        a = BlocksWorld([[1]])
        b = a.copy(('pickup', 1))
        self.assertTrue(BlocksWorld.prune(a, {b: a, a: b}))
        self.assertFalse(BlocksWorld.prune(b, {b: a}))
        self.assertFalse(BlocksWorld.prune(a, {}))

    def test_eq_hash(self):
        """
        Equal states must have equal hashes, whatever the stack order.
        """
        x = BlocksWorld([['a'], ['b']])
        y = BlocksWorld([['b'], ['a']])
        self.assertEqual(x, y)
        self.assertEqual(hash(x), hash(y))
        self.assertEqual(len({x, y}), 1)
        self.assertNotEqual(x, BlocksWorld([['a', 'b']]))

    def test_eq_tuple(self):
        """
        States can be compared against the (priority, state) queue entries.
        """
        x = BlocksWorld([['a']])
        self.assertTrue(x == (0, BlocksWorld([['a']])))
        self.assertFalse(x == (0, BlocksWorld([['b']])))

    def test_lt_str(self):
        """
        Test the remaining dunder methods.
        """
        x = BlocksWorld([['b', 'a'], ['c']])
        self.assertTrue(x < x)
        self.assertEqual(str(x), "{None}['b', 'a']['c']")
        self.assertEqual(str(x.copy(('pickup', 'c'))), "{c}['b', 'a']")

if __name__ == '__main__':
    unittest.main()
