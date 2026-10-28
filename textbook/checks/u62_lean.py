"""Book-Lean verification for Textbook Unit 62: What protection buys.

Usage: python textbook/checks/u62_lean.py

Invokes ``lake env lean -DwarningAsError=true`` on an ephemeral driver that
imports ``Derivation.StableContent``, checks the signatures and axiom sets of
all 18 theorems in ``StableContent`` plus the open proposition
``StableContent.openExactStabilityCharacterization : Prop``, and verifies two
book-Lean theorems in ``Textbook.U62``:
  1. ``reachable_halted_stable_not_protected`` — a genesis-reachable halted
     state (unlike ``sHalt``, whose ``prot = []`` with a nonempty column is not
     genesis-reachable) where ``(0, 1)`` is unprotected yet ``TraceStableSep``
     and ``(1, 2)`` is protected-separated;
  2. ``reachable_unfunded_restricted_but_not_trace_stable`` — the corresponding
     genesis-reachable live unfunded state (dropping the final ``.halt``) where
     ``(0, 1)`` is ``RestrictedStableSep``, unprotected, and NOT
     ``TraceStableSep`` because a 5-event continuation starting with
     ``.setBudget 1`` refines column ``[1]`` into ``[0, 1]`` and destroys the
     separation of ``(0, 1)``.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "lean4"

BOTH = "depends on axioms: [propext, Quot.sound]"

EXPECTED: dict[str, str] = {
    "StableContent.sepP_append": BOTH,
    "StableContent.sepP_refine": BOTH,
    "StableContent.prot_mono": BOTH,
    "StableContent.sep_preserved": BOTH,
    "StableContent.protSep_persists": BOTH,
    "StableContent.protSep_replays": BOTH,
    "StableContent.protSep_trace_stable": BOTH,
    "StableContent.trace_stable_restricted_stable": BOTH,
    "StableContent.replay_halted": BOTH,
    "StableContent.halted_stable_not_protected": BOTH,
    "StableContent.restricted_step_inert_unfunded": BOTH,
    "StableContent.restricted_replay_inert_unfunded": BOTH,
    "StableContent.unfunded_restricted_stable_not_protected": BOTH,
    "StableContent.separation_breakable": BOTH,
    "StableContent.unprotected_separation_unstable": BOTH,
    "StableContent.quiescent_iff_protected_separated": BOTH,
    "StableContent.quiescence_is_protected_separation": BOTH,
    "StableContent.quiescent_retained_protected_trace_stable": BOTH,
    "Textbook.U62.reachable_halted_stable_not_protected": BOTH,
    "Textbook.U62.reachable_unfunded_restricted_but_not_trace_stable": BOTH,
}

BOOK_LEAN = """import Derivation.StableContent

namespace Textbook.U62

open PrimitivePassage StableContent

/-- Nine-event genesis-reachable history producing a live, unfunded state with
`obs = some [[1]]`, `prot = [(1, 2)]`, and `budget = 0`. -/
def histLive : List PEvent :=
  [.admitOcc 0, .admitOcc 1, .admitOcc 2,
   .assertWit 1 2, .admitWit 1 2, .protect 1 2,
   .declareObs, .setBudget 1, .addCol [1]]

/-- Ten-event genesis-reachable history ending in `.halt`. -/
def histHalt : List PEvent := histLive ++ [.halt]

/-- Five-event continuation from `replayP histLive genesisP` that leaves the
restricted fragment via `.setBudget 1`, protects `(0, 2)`, and refines `[1]`
with `0` into `[0, 1]`, destroying the unprotected separation of `(0, 1)`. -/
def breakTail : List PEvent :=
  [.setBudget 1, .assertWit 0 2, .admitWit 0 2, .protect 0 2,
   .refineCol [1] 0]

/-- Genesis-reachable halted countermodel to the converse of
`protSep_trace_stable`. -/
theorem reachable_halted_stable_not_protected :
    TraceStableSep (replayP histHalt genesisP) 0 1 ∧
      protSep (replayP histHalt genesisP) 0 1 = false ∧
      protSep (replayP histHalt genesisP) 1 2 = true := by
  refine ⟨?_, by decide, by decide⟩
  intro tr
  rw [replay_halted tr (replayP histHalt genesisP) (by decide)]
  exact ⟨[[1]], by decide, by decide⟩

/-- Genesis-reachable live unfunded state where `(0, 1)` is `RestrictedStableSep`
and unprotected, yet NOT `TraceStableSep` under the full event grammar. -/
theorem reachable_unfunded_restricted_but_not_trace_stable :
    RestrictedStableSep (replayP histLive genesisP) 0 1 ∧
      protSep (replayP histLive genesisP) 0 1 = false ∧
      (replayP histLive genesisP).halted = false ∧
      ¬ TraceStableSep (replayP histLive genesisP) 0 1 := by
  refine ⟨?_, by decide, by decide, ?_⟩
  · intro tr hint
    obtain ⟨ho, _⟩ :=
      restricted_replay_inert_unfunded tr (replayP histLive genesisP) [[1]]
        hint (by decide) (by decide)
    exact ⟨[[1]], ho, by decide⟩
  · intro hts
    obtain ⟨cols, hobs, hsep⟩ := hts breakTail
    have hobs_actual :
        (replayP breakTail (replayP histLive genesisP)).obs = some [[0, 1]] := by
      decide
    rw [hobs_actual] at hobs
    have hcols : cols = [[0, 1]] := Option.some.inj hobs.symm
    rw [hcols] at hsep
    exact absurd hsep (by decide)

end Textbook.U62
"""


def build_driver() -> str:
    checks = "\n".join(f"#check @{name}" for name in EXPECTED)
    prints = "\n".join(f"#print axioms {name}" for name in EXPECTED)
    open_check = "#check (StableContent.openExactStabilityCharacterization : Prop)"
    return f"{BOOK_LEAN}\n{open_check}\n{checks}\n{prints}\n"


def main() -> int:
    failures: list[str] = []
    driver = build_driver()

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".lean",
        dir=LEAN_DIR,
        delete=False,
        encoding="utf-8",
    ) as handle:
        handle.write(driver)
        temp_path = Path(handle.name)

    try:
        proc = subprocess.run(
            ["lake", "env", "lean", "-DwarningAsError=true", temp_path.name],
            cwd=LEAN_DIR,
            capture_output=True,
            text=True,
            timeout=120,
        )
    finally:
        temp_path.unlink(missing_ok=True)

    if proc.returncode != 0:
        failures.append(
            f"lean exited {proc.returncode}:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )

    seen: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        if line.startswith("'") and "' " in line:
            name, rest = line[1:].split("' ", 1)
            seen[name] = rest.strip()

    matched = 0
    for name, expected_ax in EXPECTED.items():
        actual = seen.get(name)
        if actual != expected_ax:
            failures.append(f"{name}: expected {expected_ax!r}, got {actual!r}")
        else:
            matched += 1

    print(
        f"Unit 62 Lean check: exit={proc.returncode}; "
        f"axiom reports as expected: {matched} of {len(EXPECTED)}; "
        f"failures: {failures}"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
