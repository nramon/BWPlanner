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

################################################################################
# class Solver
################################################################################
class Solver:
    """
    Interface definition for solver classes.
    """

    ############################################################################
    # def __init__
    ############################################################################
    def __init__(self):
        """
        Solver constructor.
        """

        self.expanded = 0

    ############################################################################
    # def num_expanded
    ############################################################################
    def num_expanded(self):
        """
        Return the number of nodes expanded until the goal state was reached.
        Some solvers may not use a state based representation.

        :return: The number of expanded nodes or None.
        """

        return self.expanded

    ############################################################################
    # def reconstruct_path
    ############################################################################
    def reconstruct_path(self):
        """
        Return the path found by the solver.

        :return: The list of actions that make up the path.
        """

        raise NotImplementedError
