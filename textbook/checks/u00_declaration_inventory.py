"""Regression checks for source/compiled inventory reconciliation.

AuthorityEffect: None. Fixtures check comment exclusion, unnamed instances,
and refusal of ambiguous/missing/wrong-kind compiled matches. They do not
certify teaching coverage or replace running the actual Lean inventory.
"""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from textbook.audit.refresh_inventory import bind_candidate, source_candidates  # noqa: E402


class InventoryRegression(unittest.TestCase):
    def test_nested_comments_are_not_declarations(self):
        source = '''/-!
theorem with no declaration here
/- structure hidden where -/
lemma it cites is prose
-/
def value := "-- /- markers in a string -/"
-- structure ghost where
@[simp] theorem actual : True := trivial
instance (x : Nat) : Decidable (x = x) := inferInstance
'''
        rows = source_candidates(Path("fixture.lean"), source)
        self.assertEqual([(r["line"], r["kind"], r["source_name"]) for r in rows],
                         [(6, "def", "value"), (8, "theorem", "actual"),
                          (9, "instance", None)])

    def test_real_comment_regressions(self):
        root = Path(__file__).resolve().parents[2]
        for module, line in [("Pigeonhole", 16), ("PrimitivePassage", 320),
                             ("Compression", 453), ("RenamingStructure", 10)]:
            path = root / "lean4/Derivation" / f"{module}.lean"
            rows = source_candidates(path, path.read_text(encoding="utf-8"))
            self.assertNotIn(line, [r["line"] for r in rows])

    def test_compiled_match_is_not_final_name_alone(self):
        row = dict(path="fixture.lean", line=8, kind="theorem", source_name="actual")
        c = dict(location=dict(line=9), name="Here.actual", instance=False,
                 kind="theorem", axioms=[])
        with self.assertRaisesRegex(ValueError, "found 0"):
            bind_candidate(row, [c])
        c["location"]["line"] = 8
        self.assertEqual(bind_candidate(row, [c])["name"], "Here.actual")
        with self.assertRaisesRegex(ValueError, "found 2"):
            bind_candidate(row, [c, dict(c, name="Else.actual")])
        with self.assertRaisesRegex(ValueError, "compiled kind"):
            bind_candidate(row, [dict(c, kind="definition")])

    def test_unnamed_instance_binds_to_its_generated_name(self):
        row = dict(path="fixture.lean", line=9, kind="instance", source_name=None)
        c = dict(location=dict(line=9), name="Here.instDecidableValue", instance=True,
                 kind="definition", axioms=[])
        self.assertEqual(bind_candidate(row, [c])["name"], c["name"])
        with self.assertRaisesRegex(ValueError, "found 0"):
            bind_candidate(row, [dict(c, instance=False)])


if __name__ == "__main__":
    unittest.main()
