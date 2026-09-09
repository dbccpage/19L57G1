"""The oracle disqualifier: the machines' source never names the operation
tables, the merged ``F.ops``-reading folds, or a baked result table.  A
check, not a framework.

Scope: the *machine* functions — those that take a graph, a configuration
or a state and nothing else.  The loaders (``init``) read a setting through
the merged encoder and its shape, and ``control.cstep`` is a documented
check the tests consult; neither is the machine."""

from __future__ import annotations

import inspect
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1] / "code"))
sys.path.insert(0, str(ROOT.parent / "setting_translation"))
sys.path.insert(0, str(ROOT))

import control as ct  # noqa: E402
import execution as ex  # noqa: E402

FORBIDDEN = (r"\.ops\b", r"\bops\[", r"\btr\.run\b", r"translation\.run\b", r"\bfollow\b",
             r"\bno_chain", r"\blru_cache\b", r"\bcache\b", r"\bcstep\b")
PY_MACHINE = {
    ex: ("lookup", "step", "iterate", "run", "eval_word", "resume"),
    ct: ("enabled", "enabled_at", "fire", "successors", "step_det", "run_det", "run"),
}
LEAN_MACHINE = {
    ROOT / "lean" / "Execution.lean": ("isEdge", "value", "lookup", "step", "iterate", "run", "evalWord",
                                       "resume"),
    ROOT / "lean" / "Control.lean": ("enabled", "enabledAt", "fire", "successors", "stepDet", "runDet",
                                     "run"),
}


def lean_def_bodies(source: str, wanted: tuple[str, ...]) -> dict[str, str]:
    bodies: dict[str, str] = {}
    blocks = re.split(r"\n(?=(?:/--|def |abbrev |theorem |structure |inductive |end |#print))", source)
    for block in blocks:
        match = re.match(r"(?:/--.*?-/\s*)?def (\w+)", block, re.DOTALL)
        if match and match.group(1) in wanted:
            bodies[match.group(1)] = block
    return bodies


class NoHostOracle(unittest.TestCase):
    def test_python_machines_name_no_oracle(self) -> None:
        for module, names in PY_MACHINE.items():
            for name in names:
                source = inspect.getsource(getattr(module, name))
                for pattern in FORBIDDEN:
                    self.assertIsNone(re.search(pattern, source), (module.__name__, name, pattern))

    def test_execution_module_as_a_whole_names_no_oracle(self) -> None:
        source = (ROOT / "execution.py").read_text(encoding="utf-8")
        for pattern in FORBIDDEN:
            self.assertIsNone(re.search(pattern, source), pattern)

    def test_lean_machine_definitions_read_only_the_state(self) -> None:
        for path, names in LEAN_MACHINE.items():
            bodies = lean_def_bodies(path.read_text(encoding="utf-8"), names)
            self.assertEqual(set(bodies), set(names), (path.name, sorted(bodies)))
            for name, body in bodies.items():
                # Word boundaries: the parameter `nops` is a count, not the tables.
                for pattern in (r"\.ops\b", r"\bops\b", r"\bChains\b", r"\bfollow\b", r"\bCStep\b"):
                    self.assertIsNone(re.search(pattern, body), (path.name, name, pattern))


if __name__ == "__main__":
    unittest.main()
