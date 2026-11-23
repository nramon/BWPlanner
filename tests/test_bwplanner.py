import contextlib
import io
import os
import runpy
import signal
import sys
import tempfile
import unittest
import bwplanner
"""
Tests for the bwplanner command line script.
"""

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

def run_main(*args):
    """
    Run the planner. Returns (exit code, stdout, stderr).
    """
    out, err = io.StringIO(), io.StringIO()
    code = None
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = bwplanner.main(list(args))
    except SystemExit as e:
        code = e.code
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, signal.SIG_DFL)
    return code, out.getvalue(), err.getvalue()

class TestBWPlanner(unittest.TestCase):

    def pddl(self, name):
        return os.path.join(PROBLEMS, name)

    def test_help(self):
        code, out, _ = run_main('-h')
        self.assertEqual(code, 0)
        self.assertIn('usage:', out)
        self.assertIn('anytime search', out)

    def test_bad_arguments(self):
        for args in [(), ('-x', self.pddl('pfile2.pddl')), ('-t', 'a', 'b')]:
            code, _, err = run_main(*args)
            self.assertEqual(code, 2)
            self.assertIn('usage:', err)

    def test_valid_plan(self):
        code, out, _ = run_main('-n', self.pddl('pfile6.pddl'))
        self.assertEqual(code, 0)
        self.assertIn('Found a plan', out)
        self.assertNotIn('A* SOLVER', out)

    def test_default_is_valid_plan(self):
        _, out, _ = run_main(self.pddl('pfile6.pddl'))
        self.assertIn('Found a plan', out)

    def test_optimal_plan(self):
        _, out, _ = run_main('-o', self.pddl('pfile6.pddl'))
        self.assertIn('Found an optimal plan', out)
        self.assertNotIn('Found a plan', out)

    def test_anytime(self):
        code, out, _ = run_main('-n', '-o', self.pddl('pfile8.pddl'))
        self.assertEqual(code, 0)
        self.assertIn('Found a plan', out)
        self.assertIn('Found an optimal plan', out)
        self.assertIn('Done.', out)

    def test_timeout_option(self):
        _, out, _ = run_main('-t', '30', self.pddl('pfile2.pddl'))
        self.assertIn('Setting timeout to 30 seconds.', out)

    def test_timeout_handler(self):
        """
        The handler is called by the signal module with two arguments.
        """
        with contextlib.redirect_stdout(io.StringIO()) as out:
            with self.assertRaises(SystemExit) as ctx:
                bwplanner.timeout(signal.SIGALRM, None)
        self.assertEqual(ctx.exception.code, 1)
        self.assertIn('Timed out.', out.getvalue())

    def test_timeout_fires(self):
        """
        End to end: the alarm must stop a long running search cleanly.
        """
        code, out, _ = run_main('-o', '-t', '1', self.pddl('pfile25.pddl'))
        self.assertEqual(code, 1)
        self.assertIn('Timed out.', out)

    def test_run_as_script(self):
        """
        Running the file directly must exit with the planner's exit code.
        """
        argv = sys.argv
        sys.argv = ['bwplanner.py', self.pddl('pfile2.pddl')]
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit) as ctx:
                    runpy.run_path(os.path.join(ROOT, 'bwplanner.py'),
                                   run_name='__main__')
        finally:
            sys.argv = argv
        self.assertEqual(ctx.exception.code, 0)

    def test_pddl2arrays(self):
        s0, goal = bwplanner.pddl2arrays(self.pddl('pfile4.pddl'))
        self.assertCountEqual(s0, [['b2', 'b1', 'b4', 'b3']])
        self.assertCountEqual(goal, [['b2', 'b1'], ['b4', 'b3']])

    def test_pddl2arrays_partial_goal(self):
        """
        Blocks that are not part of the goal end up alone on the table.
        """
        with tempfile.NamedTemporaryFile('w', suffix='.pddl') as f:
            f.write(PARTIAL_GOAL)
            f.flush()
            s0, goal = bwplanner.pddl2arrays(f.name)
        self.assertCountEqual(s0, [['b1'], ['b2', 'b3', 'b4']])
        self.assertCountEqual(goal, [['b2', 'b1'], ['b3'], ['b4']])

    def test_all_problems_parse_consistently(self):
        for name in os.listdir(PROBLEMS):
            if name.startswith('pfile'):
                s0, goal = bwplanner.pddl2arrays(self.pddl(name))
                self.assertEqual(sorted(b for s in s0 for b in s),
                                 sorted(b for s in goal for b in s), name)

if __name__ == '__main__':
    unittest.main()
