"""The oracle disqualifier: the machine's source never names the operation
tables, the merged ``F.ops``-reading folds, or a baked result table.  A
check, not a framework."""

from __future__ import annotations

from pathlib import Path
import re
import unittest

MACHINE = Path(__file__).resolve().parents[1] / "execution.py"
LEAN = Path(__file__).resolve().parents[1] / "lean" / "Execution.lean"
FORBIDDEN_PY = (r"\.ops\b", r"\bops\[", r"\btr\.run\b", r"translation\.run\b",
                r"\bfollow\b", r"\bno_chain", r"\blru_cache\b", r"\bcache\b")
# In the Lean source `F.ops` may appear only inside theorem statements and
# their proofs, never inside a definition of the machine: the definitions
# are the `def` blocks below, scanned individually.
LEAN_MACHINE_DEFS = ("isEdge", "value", "lookup", "step", "iterate", "run", "evalWord", "resume")


def lean_def_bodies(source: str) -> dict[str, str]:
    bodies: dict[str, str] = {}
    blocks = re.split(r"\n(?=(?:/--|def |theorem |structure |end |#print))", source)
    for block in blocks:
        match = re.match(r"(?:/--.*?-/\s*)?def (\w+)", block, re.DOTALL)
        if match and match.group(1) in LEAN_MACHINE_DEFS:
            bodies[match.group(1)] = block
    return bodies


class NoHostOracle(unittest.TestCase):
    def test_python_machine_names_no_oracle(self) -> None:
        source = MACHINE.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_PY:
            self.assertIsNone(re.search(pattern, source), pattern)

    def test_lean_machine_definitions_read_only_the_graph(self) -> None:
        bodies = lean_def_bodies(LEAN.read_text(encoding="utf-8"))
        self.assertEqual(set(bodies), set(LEAN_MACHINE_DEFS), sorted(bodies))
        for name, body in bodies.items():
            self.assertNotIn("ops", body, name)
            self.assertNotIn("Chains", body, name)
            self.assertNotIn("follow", body, name)


if __name__ == "__main__":
    unittest.main()
