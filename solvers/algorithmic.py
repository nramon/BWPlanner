#!/usr/bin/env python3
"""
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
from .solver import Solver

################################################################################
# class AlgorithmicSolver
################################################################################
class AlgorithmicSolver(Solver):
    """
    Non-optimal algorithmic blocks world solver.
    """

    ################################################################################
    # def __init__
    ################################################################################
    def __init__(self, start, goal):
        """
        AlgorithmicSolver constructor.

        :param start: BlocksWorld object representing the initial state.
        :param goal:  BlocksWorld object representing the goal state.
        :return:      Nothing.
        """
        super().__init__()
        self.actions = []
        self.inplace = {}

        # Build subgoals from the bottom up.
        subgoals = update_subgoals(start, goal)

        # While all the stacks are not complete.
        while subgoals:

            # Put as many blocks as we can in their final place.
            while self.__place_block(start, subgoals):
                subgoals = update_subgoals(start, goal)

            # Unstack once and see if we can put more blocks in their final place.
            # Sort the stacks by size in increasing order.
            for top, stack in sorted(start.stacks.items(), key=lambda x: len(x[1])):
                if not top in self.inplace and len(stack) > 1:
                    self.actions.append(('unstack', top, stack[-2]))
                    start.apply(('unstack', top, stack[-2]))
                    self.actions.append(('putdown', top))
                    start.apply(('putdown', top))
                    break

    ################################################################################
    # def reconstruct_path
    ################################################################################
    def reconstruct_path(self):
        """
        Return the path found by the solver.

        :return:      The list of actions that make up the path.
        """

        return self.actions

    ################################################################################
    # def __place_block
    ################################################################################
    def __place_block(self, start, subgoals):
        """
        Look for a block that can be placed in its goal position.

        :param start:    BlocksWorld object representing the initial state.
        :param goal:     BlocksWorld object representing the goal state.
        :param subgoals: Dictionary of goals that have to be achieved now.
        :return:         True if a block was placed, False otherwise.
        """

        # Can we place any blocks?
        for top, stack in start.stacks.items():

            # We can't do anything with this stack yet. We need to unstack
            # it first.
            if not (top in subgoals and
                    (subgoals[top] is None or subgoals[top] in start.stacks.keys())):
                continue

            # Remove the block.
            if len(stack) == 1:
                action = ('pickup', top)
            else:
                action = ('unstack', top, stack[-2])
            self.actions.append(action)
            start.apply(action)

            # Put it in its place.
            if subgoals[top] is None:
                action = ('putdown', top)
            else:
                action = ('stack', top, subgoals[top])
            self.actions.append(action)
            start.apply(action)
            self.inplace[top] = 1

            return True

        return False

################################################################################
# def __update_subgoals
################################################################################
def update_subgoals(start, goal):
    """
    Find the goals that must be achieved first.

    :param start:    BlocksWorld object representing the initial state.
    :param goal:     BlocksWorld object representing the goal state.
    :return:         A dictionary containing the goals.
    """
    subgoals = {}
    for stack in goal.stacks.values():
        for block in stack:
            if goal.ontop[block] != start.ontop[block]:
                subgoals[block] = goal.ontop[block]
                break

    return subgoals
