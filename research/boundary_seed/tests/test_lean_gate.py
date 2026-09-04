"""Tests of the tree-local Lean gate's import-closure census: every module
under lean/BoundarySeed/ must be reached by the root, or it is text-scanned
but never elaborated."""

from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

TREE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TREE))

import verify_lean  # noqa: E402


class ImportClosureTests(unittest.TestCase):
    def test_every_tree_module_is_reached_by_the_root(self) -> None:
        self.assertEqual(
            verify_lean.module_census(), ["BoundarySeed.Basic", "BoundarySeed.Challenge1"]
        )
        self.assertEqual(
            verify_lean.import_closure(), {"BoundarySeed.Basic", "BoundarySeed.Challenge1"}
        )
        self.assertEqual(verify_lean.unreached_modules(), [])

    def test_planted_unreached_module_is_named(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            lean = pathlib.Path(tmp)
            (lean / "BoundarySeed" / "Sub").mkdir(parents=True)
            (lean / "BoundarySeed.lean").write_text("import BoundarySeed.Basic\n", encoding="utf-8")
            (lean / "BoundarySeed" / "Basic.lean").write_text(
                "import BoundarySeed.Sub.Deep\n", encoding="utf-8"
            )
            (lean / "BoundarySeed" / "Sub" / "Deep.lean").write_text("", encoding="utf-8")
            (lean / "BoundarySeed" / "Zzz.lean").write_text("", encoding="utf-8")
            with (
                patch.object(verify_lean, "LEAN", lean),
                patch.object(verify_lean, "ROOT_MODULE", lean / "BoundarySeed.lean"),
            ):
                self.assertEqual(
                    verify_lean.import_closure(),
                    {"BoundarySeed.Basic", "BoundarySeed.Sub.Deep"},
                )
                self.assertEqual(verify_lean.unreached_modules(), ["BoundarySeed.Zzz"])


if __name__ == "__main__":
    unittest.main()
