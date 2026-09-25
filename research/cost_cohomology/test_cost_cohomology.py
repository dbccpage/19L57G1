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

    def test_vertex_edge_and_component_counts(self) -> None:
        # The README states |V| = 262 and |E| = 638; the rank 378 is
        # |E| - |V| + components, with one component per sealed reading.
        self.assertEqual(len(self.graph.states), 262)
        self.assertEqual(len(self.graph.edges), 638)
        self.assertEqual(self.graph.components, 2)
        self.assertEqual(len(self.graph.cycles), self.graph.rank)

    def test_no_numpy_float_rank_module(self) -> None:
        self.assertFalse((HERE / "cohomology.py").exists())
        # 2026-09-24: the pinned file set gained verify_sources.py, which the
        # custody ratchet (2914032f, 2026-09-13) added without updating this
        # pin, so this test failed on main from that commit on.  The pin stays
        # exact: any other module added here still fails it.
        self.assertEqual(
            sorted(p.name for p in HERE.glob("*.py")),
            ["test_cost_cohomology.py", "verify_sources.py"],
        )
        for path in sorted(HERE.glob("*.py")):
            source = path.read_bytes().decode("utf-8")
            self.assertNotRegex(source, r"(?m)^\s*(?:import|from)\s+numpy\b", path.name)
        self.assertEqual(self.graph.rank, mg.build().rank)


if __name__ == "__main__":
    unittest.main()
