import contextlib
import io
import os
import runpy
import signal
import sys
import tempfile
import unittest
"""
Tests for the bwplanner.py command line script.
"""

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, 'bwplanner.py')
PROBLEMS = os.path.join(ROOT, 'problems')

PARTIAL_GOAL = """(define (problem p)
  (:domain blocksworld)
  (:objects b1 b2 b3 b4 - block)
  (:init
    (handempty)
    (ontable b1)
    (ontable b2)
    (on b3 b2)
    (on b4 b3)
    (clear b1)
    (clear b4)
  )
  (:goal
    (and
      (on b1 b2)
    )
  )
)
"""

def run_script(*args):
    """
    Run the script in-process. Returns (exit code, stdout, globals).
    """
    out = io.StringIO()
    argv = sys.argv
    sys.argv = [SCRIPT, *args]
    code, env = 0, None
    try:
        with contextlib.redirect_stdout(out):
            env = runpy.run_path(SCRIPT, run_name='bwplanner')
    except SystemExit as e:
        code = e.code
    finally:
        sys.argv = argv
        signal.alarm(0)
        signal.signal(signal.SIGALRM, signal.SIG_DFL)
    return code, out.getvalue(), env

class TestBWPlanner(unittest.TestCase):

    def pddl(self, name):
        return os.path.join(PROBLEMS, name)

    def test_usage(self):
        for args in [(), ('-h', self.pddl('pfile2.pddl')), ('a', 'b')]:
            code, out, _ = run_script(*args)
            self.assertEqual(code, 1)
            self.assertIn('Usage:', out)

    def test_valid_plan(self):
        _, out, _ = run_script('-n', self.pddl('pfile6.pddl'))
        self.assertIn('Found a plan', out)
        self.assertNotIn('A* SOLVER', out)

    def test_default_is_valid_plan(self):
        _, out, _ = run_script(self.pddl('pfile6.pddl'))
        self.assertIn('Found a plan', out)

    def test_optimal_plan(self):
        _, out, _ = run_script('-o', self.pddl('pfile6.pddl'))
        self.assertIn('Found an optimal plan', out)
        self.assertNotIn('Found a plan', out)

    def test_anytime(self):
        _, out, _ = run_script('-n', '-o', self.pddl('pfile8.pddl'))
        self.assertIn('Found a plan', out)
        self.assertIn('Found an optimal plan', out)
        self.assertIn('Done.', out)

    def test_timeout_option(self):
        _, out, _ = run_script('-t', '30', self.pddl('pfile2.pddl'))
        self.assertIn('Setting timeout to 30 seconds.', out)

    def test_timeout_handler(self):
        """
        The handler is called by the signal module with two arguments.
        """
        _, _, env = run_script(self.pddl('pfile2.pddl'))
        with contextlib.redirect_stdout(io.StringIO()) as out:
            with self.assertRaises(SystemExit) as ctx:
                env['timeout'](signal.SIGALRM, None)
        self.assertEqual(ctx.exception.code, 1)
        self.assertIn('Timed out.', out.getvalue())

    def test_timeout_fires(self):
        """
        End to end: the alarm must stop a long running search cleanly.
        """
        code, out, _ = run_script('-o', '-t', '1', self.pddl('pfile25.pddl'))
        self.assertEqual(code, 1)
        self.assertIn('Timed out.', out)

    def test_pddl2arrays(self):
        _, _, env = run_script(self.pddl('pfile4.pddl'))
        s0, goal = env['pddl2arrays'](self.pddl('pfile4.pddl'))
        self.assertCountEqual(s0, [['b2', 'b1', 'b4', 'b3']])
        self.assertCountEqual(goal, [['b2', 'b1'], ['b4', 'b3']])

    def test_pddl2arrays_partial_goal(self):
        """
        Blocks that are not part of the goal end up alone on the table.
        """
        _, _, env = run_script(self.pddl('pfile2.pddl'))
        with tempfile.NamedTemporaryFile('w', suffix='.pddl') as f:
            f.write(PARTIAL_GOAL)
            f.flush()
            s0, goal = env['pddl2arrays'](f.name)
        self.assertCountEqual(s0, [['b1'], ['b2', 'b3', 'b4']])
        self.assertCountEqual(goal, [['b2', 'b1'], ['b3'], ['b4']])

    def test_all_problems_parse_consistently(self):
        _, _, env = run_script(self.pddl('pfile2.pddl'))
        for name in os.listdir(PROBLEMS):
            if name.startswith('pfile'):
                s0, goal = env['pddl2arrays'](self.pddl(name))
                self.assertEqual(sorted(b for s in s0 for b in s),
                                 sorted(b for s in goal for b in s), name)

if __name__ == '__main__':
    unittest.main()
