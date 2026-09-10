"""Tests for cycle ranks of the depth-3 move multigraph.
AuthorityEffect: None.
"""

from __future__ import annotations

import pathlib
import sys
import unittest

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
_PDC = str(REPO / "research" / "path_dependent_cost")
for _p in (str(HERE), str(REPO / "code"), _PDC):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import movegraph as mg  # noqa: E402


class TestGraphCycles(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = mg.build()

    def test_cycle_rank(self) -> None:
        self.assertEqual(self.graph.rank, 378)

    def test_self_loop_edges_count(self) -> None:
        self.assertEqual(len(self.graph.self_loop_edges), 232)

    def test_nonself_fundamental_cycles_count(self) -> None:
        self.assertEqual(len(self.graph.nonself_cycles), 146)


if __name__ == "__main__":
    unittest.main()
