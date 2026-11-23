#!/usr/bin/env python3
"""
Domain dependent planner for blocks world problems.

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
import argparse
import datetime
import re
import signal
import sys
import time
from domain import BlocksWorld
from solvers import AlgorithmicSolver, AStarSolver

# Program version.
__version__ = "0.1.0"

################################################################################
# def log
################################################################################
def log(source, *msg):
    """
    Simple message logger.
    """
    print(f"{time.time():.6f} [{source}]", *msg)

################################################################################
# def pddl2arrays
################################################################################
def pddl2arrays(fname):
    """
    Helper function to generate arrays for the initial and goal states from a
    PDDL file.
    """
    s0_array = {}   # Array corresponding to the initial state.
    goal_array = {} # Array corresponding to the goal state.

    bottoms = {} # Stack bottoms (they may not be part of the goal).
    ontable = {} # (ontable) blocks.
    ontop = {}   # (on) propositions.

    # Helper function to generate the arrays themselves.
    def get_array():
        state = []

        for bottom in ontable:
            stack = [bottom]
            block = bottom
            while block in ontop:
                block = ontop[block]
                stack.append(block)
            state.append(stack)

        return state

    # Parse the PDDL file.
    with open(fname, encoding='utf-8') as f:
        while line := f.readline():
            if re.search(r'\(:goal', line):

                # Save the initial state.
                s0_array = get_array()

                # Start processing the goal state.
                bottoms = {}
                ontable = {}
                ontop = {}
            elif m := re.search(r'\(ontable\s+([^\)]+)\)', line):
                ontable[m.group(1)] = m.group(1)
            elif m := re.search(r'\(on\s+(\S+)\s+([^\)]+)\)', line):
                ontop[m.group(2)] = m.group(1)
                bottoms[m.group(1)] = m.group(2)

    # Fix ontable blocks.
    for block in ontop:
        if not block in bottoms and not block in ontable:
            ontable[block] = block

    goal_array = get_array()

    # Add blocks not present in the goal.
    flat_goal_array = [block for stack in goal_array for block in stack]
    for block in [block for stack in s0_array for block in stack]:
        if block not in flat_goal_array:
            goal_array.append([block])

    return (s0_array, goal_array)

################################################################################
# def find_valid_plan
################################################################################
def find_valid_plan(s0_state, goal_state):
    """
    Look for a valid (not necessarily optimal) plan.

    :param s0_state:   Array for the initial state.
    :param goal_state: Array for the goal state.
    :return:           The plan.
    """
    s0 = BlocksWorld(s0_state)
    goal = BlocksWorld(goal_state)

    log("BLOCKSWORLD SOLVER", "Looking for a valid plan...")
    t0 = datetime.datetime.now()
    plan = AlgorithmicSolver(s0, goal)
    t1 = datetime.datetime.now()
    elapsed = (t1 - t0).total_seconds()

    path = plan.reconstruct_path()
    log("BLOCKSWORLD SOLVER", f"Found a plan in {elapsed} seconds: {path}")
    log("BLOCKSWORLD SOLVER", f"Plan length: {len(path)}")
    return path

################################################################################
# def find_optimal_plan
################################################################################
def find_optimal_plan(s0_state, goal_state):
    """
    Look for an optimal plan.

    :param s0_state:   Array for the initial state.
    :param goal_state: Array for the goal state.
    :return:           The plan.
    """
    s0 = BlocksWorld(s0_state)
    goal = BlocksWorld(goal_state)

    log("A* SOLVER", "Looking for an optimal plan...")
    t0 = datetime.datetime.now()
    plan = AStarSolver(s0, goal, h=goal.h, prune=BlocksWorld.prune)
    t1 = datetime.datetime.now()
    elapsed = (t1 - t0).total_seconds()

    path = plan.reconstruct_path()
    log("A* SOLVER", f"Found an optimal plan in {elapsed} seconds: {path}")
    log("A* SOLVER", f"Expanded nodes: {plan.num_expanded()}")
    log("A* SOLVER", f"Plan length: {len(path)}")
    return path

################################################################################
# def timeout
################################################################################
def timeout(signum, frame): # pylint: disable=unused-argument
    """
    Timeout signal handler.
    """
    log("SYSTEM", "Timed out.")
    sys.exit(1)

################################################################################
# def parse_args
################################################################################
def parse_args(argv):
    """
    Parse the command line arguments.

    :param argv: List of command line arguments, without the program name.
    :return:     The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog="bwplanner",
        description=f"BWPlanner v{__version__}",
        epilog="Options -n and -o can be combined to perform anytime search.")
    parser.add_argument("problem", help="PDDL problem file.")
    parser.add_argument("-n", dest="valid", action="store_true",
                        help="Look for a valid plan (the default behavior).")
    parser.add_argument("-o", dest="optimal", action="store_true",
                        help="Look for an optimal plan.")
    parser.add_argument("-t", dest="timeout", type=int, metavar="timeout",
                        help="Timeout in seconds.")
    return parser.parse_args(argv)

################################################################################
# def main
################################################################################
def main(argv=None):
    """
    Entry point.

    :param argv: List of command line arguments, without the program name.
    :return:     The exit code.
    """
    args = parse_args(sys.argv[1:] if argv is None else argv)

    # Configure the timeout.
    if args.timeout is not None:
        log("SYSTEM", f"Setting timeout to {args.timeout} seconds.")
        signal.signal(signal.SIGALRM, timeout)
        signal.alarm(args.timeout)

    # Parse the problem definition files and convert the states to
    # BlocksWorld objects.
    log("PROBLEM PARSER", f"Parsing PDDL file: {args.problem}")
    s0_state, goal_state = pddl2arrays(args.problem)

    # Sanity check.
    assert sum(len(s) for s in s0_state) == sum(len(s) for s in goal_state)

    # Print some problem related stats.
    num_blocks = sum(len(s) for s in s0_state)
    s0_stacks = len(s0_state)
    goal_stacks = len(goal_state)
    upper_lim = 4 * num_blocks - 2 * s0_stacks - 2 * goal_stacks

    log("PROBLEM PARSER", f"Number of blocks: {num_blocks}")
    log("PROBLEM PARSER", f"Number of stacks in the initial state: {s0_stacks}")
    log("PROBLEM PARSER", f"Number of stacks in the goal state: {goal_stacks}")
    log("PROBLEM PARSER", f"Upper length limit for an optimal plan: {upper_lim}")

    # Save plan paths to perform sanity checks.
    path_o = path_no = None

    # Non-optimal plan search.
    if args.valid or not args.optimal:
        path_no = find_valid_plan(s0_state, goal_state)

    # Optimal plan search.
    if args.optimal:
        path_o = find_optimal_plan(s0_state, goal_state)

    # Sanity check.
    if path_o and path_no:
        assert len(path_o) <= len(path_no)

    log("SYSTEM", "Done.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
