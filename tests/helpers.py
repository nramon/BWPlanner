"""
Helpers shared by the test modules.
"""
import collections
import random
from domain import BlocksWorld


def canon(state):
    """
    Order independent representation of a state (arm included).
    """
    return (state.arm, frozenset(tuple(s) for s in state.stacks.values()))


def random_stacks(blocks, rnd):
    """
    Return a random list of stacks containing the given blocks.
    """
    blocks = list(blocks)
    rnd.shuffle(blocks)
    stacks = []
    for block in blocks:
        if not stacks or rnd.random() < 0.4:
            stacks.append([block])
        else:
            rnd.choice(stacks).append(block)
    return stacks


def random_problems(count, max_blocks=5, seed=1):
    """
    Generate (initial, goal) pairs of stacks.
    """
    rnd = random.Random(seed)
    for _ in range(count):
        blocks = [f"b{i}" for i in range(rnd.randint(2, max_blocks))]
        yield random_stacks(blocks, rnd), random_stacks(blocks, rnd)


def plan_reaches_goal(initial, goal, plan):
    """
    Replay a plan on a fresh state. Illegal actions make the domain assert.
    """
    state = BlocksWorld(initial)
    for action in plan:
        state.apply(action)
    return canon(state) == canon(BlocksWorld(goal))


def optimal_length(initial, goal):
    """
    Breadth first search used as an oracle for the optimal plan length.
    """
    target = canon(BlocksWorld(goal))
    start = BlocksWorld(initial)
    seen = {canon(start): 0}
    queue = collections.deque([start])
    while queue:
        state = queue.popleft()
        dist = seen[canon(state)]
        if canon(state) == target:
            return dist
        for neighbor in state.expand():
            if canon(neighbor) not in seen:
                seen[canon(neighbor)] = dist + 1
                queue.append(neighbor)
    return None
