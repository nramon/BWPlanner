#!/usr/bin/env python3
# pylint: disable=C0103
"""
Representation of the blocks world domain.
See: https://en.wikipedia.org/wiki/Blocks_world

Copyright (C) 2021 Ramon Novoa ramonnovoa@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

################################################################################
# class BlocksWorld
################################################################################
class BlocksWorld:
    """
    Class used to represent blocks world problems.
    """

    ############################################################################
    # def __init__
    ############################################################################
    def __init__(self, stacks, arm=None, action=None):
        """
        BlocksWorld constructor.

        :param stacks: A list of stacks to initialize the state.
        :param arm:    Block that is held by the arm.
        :param action: An action to be applied.
        :return:       Nothing.
        """

        # Initialize the arm and action.
        self.arm = arm
        self.action = action

        # Used to efficiently compute h.
        self.ontop = {}

        # Initialize the stacks.
        self.stacks = {}
        for stack in stacks:
            self.stacks[stack[-1]] = stack.copy()
            self.ontop.update(dict(zip(stack, [None] + stack)))

        # Apply the given action.
        if action:
            self.apply(action)

    ############################################################################
    # def apply
    ############################################################################
    def apply(self, action):
        """
        Apply the given action.

        :param action: Tuple representing an action.
        :return:       Nothing.
        """

        # Get the action.
        funct = getattr(self, action[0])
        if not funct:
            raise Exception("Invalid action: {}".format(action[0]))

        # Call it.
        funct(*action[1:])

    ############################################################################
    # def copy
    ############################################################################
    def copy(self, action=None):
        """
        Return a copy of this object with an action applied.

        :param action: Action to be passed to the new object.
        :return:       A new BlocksWorld object.
        """
        return type(self)(self.stacks.values(), self.arm, action)

    ############################################################################
    # def expand
    ############################################################################
    def expand(self):
        """
        Return a list of states reachable from the current state.

        :return: A list of BlocksWorld objects.
        """
        states = []

        # We can always put down a block that is being held.
        if self.arm is not None:
            states.append(self.copy(('putdown', self.arm)))

        # Perform actions on the stacks.
        for stack in self.stacks.values():
            if self.arm is None:
                # We can pick up or unstack the tops.
                if len(stack) == 1:
                    states.append(self.copy(('pickup', stack[0])))
                else:
                    states.append(self.copy(('unstack', stack[-1], stack[-2])))
            else:
                # Or stack a block that is being held.
                states.append(self.copy(('stack', self.arm, stack[-1])))

        return states

    ############################################################################
    # def h
    ############################################################################
    def h(self, other):
        """
        Compute a heuristic based on the number of changes needed to
        get each block to its final position.

        :param other: BlocksWorld object the heuristic will target.
        :return:      The computed heuristic value.
        """

        # Look for blocks that have to be moved at least once.
        move_once = {}
        for stack in other.stacks.values():
            for block in stack:
                if (other.ontop[block] in move_once or
                        other.ontop[block] != self.ontop[block]):
                    move_once[block] = 1

        # Look for blocks that have to be moved twice.
        move_twice = {}
        for stack in other.stacks.values():
            for block in stack:
                if (other.ontop[block] == self.ontop[block] and
                        block in move_once):
                    move_twice[block] = 1

        # Blocks that have to be moved twice have been counted too as having to
        # be moved once!
        return 2 * len(move_once) + 2 * len(move_twice)

    ############################################################################
    # def last_action
    ############################################################################
    def last_action(self):
        """
        Return the action that led to the current state.

        :return: A tuple representing an action.
        """

        return self.action

    ############################################################################
    # def pickup
    ############################################################################
    def pickup(self, obj):
        """
        Pick up a block. Must be the only block in its stack.

        :param obj: Block that will be picked up.
        :return:    Nothing.
        """
        assert self.arm is None
        assert obj in self.stacks

        self.arm = obj
        del self.stacks[obj]

        # Used to efficiently compute h.
        del self.ontop[obj]

    ############################################################################
    # @staticmethod def prune
    ############################################################################
    @staticmethod
    def prune(state, came_from):
        """
        Node expansion filter. Checks if a state repeats itself in the path to
        the initial state.

        :param state:     State that should not repeat.
        :param came_from: Hash with parent-child relationships from the initial
                          state to the current state.
        :return:          True if the state repeats, False otherwise.
        """
        current = state
        while current in came_from:
            current = came_from[current]
            if current == state:
                return True

        return False

    ############################################################################
    # def putdown
    ############################################################################
    def putdown(self, obj):
        """
        Put down a block. A new stack will be created.

        :param obj: Block that will be put down.
        :return:    Nothing.
        """
        assert self.arm == obj
        assert obj not in self.stacks

        self.arm = None
        self.stacks[obj] = [obj]

        # Used to efficiently compute h.
        self.ontop[obj] = None

    ############################################################################
    # def stack
    ############################################################################
    def stack(self, top, bottom):
        """
        Stack a block on top of another block.

        :param top:    Block that will be stacked.
        :param bottom: Block on top of the target stack.
        :return:       Nothing.
        """
        assert self.arm == top
        assert bottom in self.stacks

        self.arm = None
        self.stacks[bottom].append(top)
        self.stacks[top] = self.stacks[bottom]
        del self.stacks[bottom]

        # Used to efficiently compute h.
        self.ontop[top] = bottom

    ############################################################################
    # def unstack
    ############################################################################
    def unstack(self, top, bottom):
        """
        Unstack a block.

        :param top:    Block that will be unstacked.
        :param bottom: Block beneath the block that will be unstacked.
        :return:       Nothing.
        """
        assert self.arm is None
        assert top in self.stacks

        self.arm = self.stacks[top].pop()
        self.stacks[bottom] = self.stacks[top]
        del self.stacks[top]

        # Used to efficiently compute h.
        del self.ontop[top]

    ############################################################################
    # def __hash__
    ############################################################################
    def __hash__(self):
        """
        Use the object's state string representation to generate a hash.

        :return: The hash corresponding to the current object.
        """
        return hash(str(self.stacks))

    ############################################################################
    # def __eq__
    ############################################################################
    def __eq__(self, other):
        """
        Compare BlocksWorld objects.

        :return: 1 if self > other, 0 if self == other, -1 if self < other.
        """

        # This allows as to compare BlocksWorld objects against BlocksWorld
        # objects inside the priority queue.
        if isinstance(other, tuple):
            return self.stacks == other[1].stacks

        return self.stacks == other.stacks

    ############################################################################
    # def __lt__
    ############################################################################
    def __lt__(self, other):
        """
        Used by the priority queue to break ties. We don't care about the
        result of this comparison.

        :return: True.
        """
        return True

    ############################################################################
    # def __str__
    ############################################################################
    def __str__(self):
        """
        Generate a string representation of the current object.

        :return: A string representing the current object.
        """

        # Arm.
        string = "{{{}}}".format(self.arm)

        # Stacks.
        for _, stack in sorted(self.stacks.items(), key=lambda x: x[0]):
            string += str(stack)

        return string
