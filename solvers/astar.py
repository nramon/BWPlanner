#!/usr/bin/env python3
# pylint: disable=R0913
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
import heapq
from .solver import Solver

################################################################################
# class AStarSolver
################################################################################
class AStarSolver(Solver):
    """
    Implementation of the A* search algorithm for the blocks world planner.
    See: https://en.wikipedia.org/wiki/A*_search_algorithm

    This implementation is not optimal unless the given heuristic is
    consistent.
    """

    ############################################################################
    # def __init__
    ############################################################################
    def __init__(self,
                 start,
                 goal,
                 g=lambda x: 1, # Assume an action cost of 1 by default.
                 h=lambda x: 0, # Null heuristic.
                 prune=lambda x, y: True):
        """
        AStarSolver constructor. Runs the A* algorithm.

        :param start: BlocksWorl object for the start state.
        :param goal:  BlocksWorl object for the goal state.
        :param g:     Distance function.
        :param h:     Heuristic function.
        :param prune: Node expansion filter function.
        :return:      Nothing.
        """
        super().__init__()
        self.goal = None    # Found goal.
        self.came_from = {} # Preceding node on the current best path.
        self.expanded = 0   # Keep track of expanded nodes.

        open_set = []       # Set of discovered nodes.
        gscore = {}         # Cost of the current best path to each node.
        fscore = {}         # fscore = gscore + h.

        # Initialization.
        gscore[start] = 0
        fscore[start] = h(start)
        heapq.heappush(open_set, (fscore[start], start))

        # While there are nodes to be visited.
        while open_set:

            # Get the node with the lowest cost.
            current = heapq.heappop(open_set)[1]

            # Are we done?
            if current == goal:
                self.goal = current
                return

            # Expand neighbors.
            self.expanded += 1
            for neighbor in current.expand():
                # tentative_gscore is the distance from start to neighbor
                # through current.
                tentative_gscore = gscore.get(current, float('Inf')) + g(neighbor)

                # Found a better path.
                if tentative_gscore < gscore.get(neighbor, float('Inf')):
                    self.came_from[neighbor] = current
                    gscore[neighbor] = tentative_gscore
                    fscore[neighbor] = gscore[neighbor] + h(neighbor)

                    # With an inconsistent heuristics we would have to check
                    # open_set, since nodes may have to be re-expanded.
                    if not prune(neighbor, self.came_from):
                        heapq.heappush(open_set, (fscore[neighbor], neighbor))

        # The goal was never reached.
        self.goal = None

    ############################################################################
    # def reconstruct_path
    ############################################################################
    def reconstruct_path(self):
        """
        Return the shortest path found by A*.

        :return: The list of actions that make up the path.
        """

        # No path found.
        if self.goal is None:
            return []

        # Reconstruct the path starting from the goal.
        total_path = []
        total_path.insert(0, self.goal.last_action())

        # Follow the path in reverse order.
        current = self.goal
        while current in self.came_from.keys():
            current = self.came_from[current]
            total_path.insert(0, current.last_action())

        # The initial state has no associated action.
        return total_path[1:]
