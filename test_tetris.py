#!/usr/bin/env python3
"""Tests for tetris.py. Run with: python test_tetris.py"""
import io
import sys
import unittest
from contextlib import redirect_stdout

from tetris import resolve_game, main


class TestExamples(unittest.TestCase):
    # examples from the exercise PDF

    def test_example_1(self):
        self.assertEqual(resolve_game("O0,O2,O4,O6,O8"), 0)

    def test_example_2(self):
        self.assertEqual(resolve_game("L0,J2,O4,L6,J8"), 2)

    def test_example_3(self):
        self.assertEqual(resolve_game("T0,Z3,T5,J8"), 3)

    def test_example_4(self):
        # O2 lands on the T and doesn't fall into the gap under it
        self.assertEqual(resolve_game("T0,Z3,T5,O2,O8"), 3)


class TestOther(unittest.TestCase):

    def test_single_pieces(self):
        expected = {"O": 2, "I": 4, "S": 2, "Z": 2, "L": 3, "J": 3, "T": 2}
        for piece, h in expected.items():
            with self.subTest(piece=piece):
                self.assertEqual(resolve_game(piece + "0"), h)

    def test_stacking(self):
        self.assertEqual(resolve_game("I0,I0,I0"), 12)

    def test_stdin_stdout(self):
        old_stdin = sys.stdin
        sys.stdin = io.StringIO("O0,O2,O4,O6,O8\nL0,J2,O4,L6,J8\nT0,Z3,T5,J8\nT0,Z3,T5,O2,O8\n")
        out = io.StringIO()
        try:
            with redirect_stdout(out):
                main()
        finally:
            sys.stdin = old_stdin
        self.assertEqual(out.getvalue(), "0\n2\n3\n3\n")


if __name__ == "__main__":
    unittest.main()
