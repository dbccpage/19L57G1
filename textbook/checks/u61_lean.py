"""Book-Lean verification for Textbook Unit 61: Compressing a presentation against a question list.

Usage: python textbook/checks/u61_lean.py

Invokes ``lake env lean -DwarningAsError=true`` on an ephemeral driver that
imports ``Derivation.Compression``, checks the signatures and axiom sets of the
22 artifact theorems in ``Compression``, and verifies four book-Lean theorems
in ``Textbook.U61``:
  1. ``splits_iff_without_sub`` — ``splits_iff_new_separator`` proved without
     the unused ``_hsub : ∀ q, q ∈ Q → q ∈ Q'`` hypothesis;
  2. ``non_sub_split_preserves_count`` — on ``D = [0, 1, 2]`` with
     ``Q = [ind 0]`` and ``Q' = [ind 1]`` (where ``Q ⊈ Q'``), point ``1`` splits
     yet ``classCount`` stays at ``2``, showing ``hsub`` is load-bearing in
     ``strict_split_increases`` even though it is idle in
     ``splits_iff_new_separator``;
  3. ``d4_chain_counts`` — on ``D = [0, 1, 2, 3]``, the chain
     ``[] -> [x % 2] -> [x % 2, x / 2]`` has class counts ``1, 2, 4`` and
     quotient maps ``[0, 0, 0, 0]``, ``[0, 1, 0, 1]``, ``[0, 1, 2, 3]``;
  4. ``first_match_order_changes_labels`` — domain order changes the chosen
     representative while preserving the taught pair's grouping.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "lean4"

NONE = "does not depend on any axioms"
QUOT = "depends on axioms: [Quot.sound]"
PROPEXT = "depends on axioms: [propext]"
BOTH = "depends on axioms: [propext, Quot.sound]"

EXPECTED: dict[str, str] = {
    "Compression.sigEq_iff_sigList": NONE,
    "Compression.factors_iff_fiberConstant": QUOT,
    "Compression.factor_unique_on_image": NONE,
    "Compression.factor_not_unique_off_image": NONE,
    "Compression.pQ_exact": QUOT,
    "Compression.pQ_adequate": QUOT,
    "Compression.pQ_coarsest": QUOT,
    "Compression.pQ_unique_on_image": NONE,
    "Compression.descent_witness": NONE,
    "Compression.enlarge_refines": NONE,
    "Compression.splits_iff_new_separator": NONE,
    "Compression.absolute_adequacy_iff_injective": NONE,
    "Compression.dup_no_refine": PROPEXT,
    "Compression.postcompose_no_refine": PROPEXT,
    "Compression.refine_requires_separator": NONE,
    "Compression.refinement_not_unique": NONE,
    "Compression.refinement_tie": NONE,
    "Compression.refine_bounded": BOTH,
    "Compression.classCount_pos": NONE,
    "Compression.strict_split_increases": BOTH,
    "Compression.chain_bounded": BOTH,
    "Compression.strict_steps_lt": BOTH,
    "Textbook.U61.splits_iff_without_sub": NONE,
    "Textbook.U61.non_sub_split_preserves_count": NONE,
    "Textbook.U61.d4_chain_counts": NONE,
    "Textbook.U61.first_match_order_changes_labels": NONE,
}

BOOK_LEAN = """import Derivation.Compression

namespace Textbook.U61

open Compression

/-- `splits_iff_new_separator` without the unused `_hsub : ∀ q, q ∈ Q → q ∈ Q'`
hypothesis. -/
theorem splits_iff_without_sub (D : List Nat)
    (Q Q' : List (Nat → Nat)) (x : Nat) :
    SplitsAt D Q Q' x ↔
      ∃ x', x' ∈ D ∧ SigEq Q x x' ∧
        ∃ q', q' ∈ Q' ∧ q' x ≠ q' x' := by
  constructor
  · intro h
    obtain ⟨x', hx', hsig, hnot⟩ := h
    obtain ⟨q', hm, hne⟩ := exists_separator_of_not_sigEq Q' x x' hnot
    exact ⟨x', hx', hsig, q', hm, hne⟩
  · intro h
    obtain ⟨x', hx', hsig, q', hm, hne⟩ := h
    exact ⟨x', hx', hsig, fun hs => hne (hs q' hm)⟩

/-- When `Q` is not a subfamily of `Q'`, a split at `x = 1` on `D = [0, 1, 2]`
between `Q = [ind 0]` and `Q' = [ind 1]` need not increase `classCount`:
both families have `classCount = 2`. -/
theorem non_sub_split_preserves_count :
    SplitsAt [0, 1, 2] [ind 0] [ind 1] 1 ∧
      classCount [0, 1, 2] [ind 0] = 2 ∧
      classCount [0, 1, 2] [ind 1] = 2 := by
  refine ⟨⟨2, ?_, ?_, ?_⟩, rfl, rfl⟩
  · exact List.mem_cons_of_mem _ (List.mem_cons_of_mem _ List.mem_cons_self)
  · intro q hq
    cases hq with
    | head => decide
    | tail _ hm => cases hm
  · intro hs
    exact absurd (hs (ind 1) List.mem_cons_self) (by decide)

def qParity (x : Nat) : Nat := x % 2
def qHalf (x : Nat) : Nat := x / 2

/-- On `D = [0, 1, 2, 3]`, the chain `[] -> [qParity] -> [qParity, qHalf]`
realizes class counts `1, 2, 4` and quotient maps `[0, 0, 0, 0]`,
`[0, 1, 0, 1]`, `[0, 1, 2, 3]`. -/
theorem d4_chain_counts :
    classCount [0, 1, 2, 3] [] = 1 ∧
    classCount [0, 1, 2, 3] [qParity] = 2 ∧
    classCount [0, 1, 2, 3] [qParity, qHalf] = 4 ∧
    ([0, 1, 2, 3].map (pQ [0, 1, 2, 3] [])) = [0, 0, 0, 0] ∧
    ([0, 1, 2, 3].map (pQ [0, 1, 2, 3] [qParity])) = [0, 1, 0, 1] ∧
    ([0, 1, 2, 3].map (pQ [0, 1, 2, 3] [qParity, qHalf])) = [0, 1, 2, 3] := by
  exact ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩

/-- Reordering changes these labels, not the answer grouping. -/
theorem first_match_order_changes_labels :
    pQ [0,1,2] [ind 2] 0 = 0 ∧ pQ [1,0,2] [ind 2] 0 = 1 ∧
    pQ [0,1,2] [ind 2] 0 = pQ [0,1,2] [ind 2] 1 ∧
    pQ [1,0,2] [ind 2] 0 = pQ [1,0,2] [ind 2] 1 :=
  ⟨rfl, rfl, rfl, rfl⟩

end Textbook.U61
"""


def build_driver() -> str:
    checks = "\n".join(f"#check @{name}" for name in EXPECTED)
    prints = "\n".join(f"#print axioms {name}" for name in EXPECTED)
    return f"{BOOK_LEAN}\n{checks}\n{prints}\n"


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
        f"Unit 61 Lean check: exit={proc.returncode}; "
        f"axiom reports as expected: {matched} of {len(EXPECTED)}; "
        f"failures: {failures}"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
