# Audit: ResidualClosure

| field | value |
|---|---|
| Path | lean4/Derivation/ResidualClosure.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | c78b7dd4c854db24 |
| Lines | 122 |
| Imported by root `Derivation.lean` | yes (line 56) |
| Imports | Derivation.ClosureSymmetry |
| Declarations | 1 def (`InvariantUnderOn`), 7 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 7 lines; axioms seen: `Quot.sound` (4), `propext, Quot.sound` (3) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

Given an internal symmetry break `b` of the attempted closure `p → q` on a represented domain `D` (ClosureSymmetry), and a further presentation `r` that carries both faces (`FactorsOn D r p` and `FactorsOn D r q`), the module shows what happens to the *current* obstruction: `r` is not invariant under the symmetry that generated it, `r` separates the witnessing pair, `r` has strictly more represented classes than `p`, and no residual or symmetry break remains for the correspondence `r → q`. It is a statement about closing the obstruction at hand; it does not produce `r`, does not say a later comparison yields no new residual, and names no observer or preferred repair.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `InvariantUnderOn D f sigma` | 29 | def | `∀ x ∈ D, f (sigma x) = f x`. | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `factorization_preserves_invariance` | 35 | If `FactorsOn D r q`, `sigma` preserves `D`, and `r` is invariant under `sigma` on `D`, then `q` is. | CONDITIONAL: `FactorsOn D r q`, `hsigma` | Quot.sound | A |
| `carrying_right_face_loses_generating_invariance` | 46 | For `b : InternalSymmetryBreak D p q` and `FactorsOn D r q`: `¬ InvariantUnderOn D r b.symmetry`. | CONDITIONAL: `b`, `FactorsOn D r q` | Quot.sound | S |
| `carrying_right_face_splits_generating_pair` | 57 | Same hypotheses: `r (b.symmetry b.point) ≠ r b.point`. | CONDITIONAL: `b`, `FactorsOn D r q` | Quot.sound | A |
| `common_refinement_strictly_splits_left_face` | 72 | With also `FactorsOn D r p`: `classCount D [p] < classCount D [r]`. | CONDITIONAL: `b`, `FactorsOn D r p`, `FactorsOn D r q` | propext, Quot.sound | S |
| `current_directional_residual_is_empty` | 86 | `FactorsOn D r q → ¬ Nonempty (DirectionalResidual D r q)`. | CONDITIONAL: `FactorsOn D r q` | Quot.sound | A |
| `current_internal_symmetry_break_is_empty` | 95 | `FactorsOn D r q → ¬ Nonempty (InternalSymmetryBreak D r q)`. | CONDITIONAL: `FactorsOn D r q` | propext, Quot.sound | A |
| `common_refinement_closes_current_obstruction` | 106 | Conjunction of the five preceding conclusions under `b`, `FactorsOn D r p`, `FactorsOn D r q`. | CONDITIONAL: same | propext, Quot.sound | S |

## 4. External and admitted assumptions

- From ClosureSymmetry: `InternalSymmetryBreak` with its fields; `residual_refutes_factorization`; `closure_failure_iff_internal_symmetry_break`. From PresentationRelativity: `classCount_lt_of_refinement_split`, `DirectionalResidual`. From Compression: `FactorsOn`, `factors_iff_fiberConstant`, `classCount`.
- `r : Nat → Nat` is a *supplied* common refinement; every theorem is conditional on it carrying both faces. The header says "It does not generate `r`".
- `p q r sigma : Nat → Nat` ambient functions restricted to `D` (finitude rule; same remark as ClosureSymmetry).
- Unearned identity / unrestricted universe / silently assumed observer / unspecified correspondence / cost function (beyond `classCount` as a declared count) / admitted-then-forced / finite-as-universal: none found for each.
- Library lemmas doing real work: none beyond the imported theorems.

## 5. Derived consequences

- No module under `lean4/Derivation/` imports or references `ResidualClosure` (grep for `ResidualClosure.` and `InvariantUnderOn`: only this file).
- `code/derivation/completion.py` lines 752–765 bind the seven names; `current_directional_residual_is_empty` is also named in `tests/test_completion.py:308`.
- Paper: change log 2026-08-14 ("`ResidualClosure` closes the current finite residual without claiming future quiescence"); ledger line ~3545 counts "seven `ResidualClosure.*` theorem reports" among the evidence of the integrated chain (CL-FIDELITY-* entries). No dedicated ledger entry and no theorem-by-theorem prose found (grep for the seven names in `paper/`: no hits except the ledger count).

## 6. Counterexamples and limitations

- None of the theorems is a countermodel; all are positive consequences of the hypotheses.
- "Closes the current obstruction" means: after `r` carries `q`, there is no residual *from `r` to `q`*. It says nothing about residuals from `r` to a later comparison `q'`, nor about residuals in the direction `q → r`. The header states this.
- The class-count conclusion needs `FactorsOn D r p` as well; the two "loses invariance / splits pair" conclusions need only `FactorsOn D r q`.

## 7. Axiom dependencies

All within {propext, Quot.sound} (inherited from Compression's `factors_iff_fiberConstant` and `count_lt_of_split`). None exceeds.

## 8. Verification status

- Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0).
- All seven theorems are in `artifacts/lean_axioms.txt`.
- Paper cites the module by count only (see §5).
- Probe: `/tmp/claude-0/-home-claude/47be43b5-43cb-5429-bc31-b53a81ca595d/scratchpad/probes/F2/cs_qr_probe.lean`, exit 0: `common_refinement_closes_current_obstruction` depends on `[propext, Quot.sound]`.

## 9. Related Python implementations

- `code/derivation/completion.py` (tag bindings only); `tests/test_completion.py:308`. No implementation of invariance or class-count growth under a common refinement found.

## 10. Textbook placement proposal

- Prerequisites: ClosureSymmetry's `InternalSymmetryBreak`; `FactorsOn`; `classCount` and `classCount_lt_of_refinement_split`.
- Substantive: `common_refinement_closes_current_obstruction` (as the one packaged statement) and `carrying_right_face_loses_generating_invariance` (the conceptual point: carrying `q` costs the symmetry).
- Auxiliary: `factorization_preserves_invariance`, `carrying_right_face_splits_generating_pair`, `common_refinement_strictly_splits_left_face`, the two `current_*_is_empty` lemmas.
- Suggested lesson: "What does repairing a comparison cost?" — answering: the symmetry that hid the pair, and at least one extra class; and the repaired direction has no residual left.
- Recommend omitting: `current_internal_symmetry_break_is_empty` and `current_directional_residual_is_empty` as separate items (immediate from ClosureSymmetry).

## 11. Interpretation findings

1. Header line 13–14: "Thus no residual or internal symmetry break of that same directional closure remains." Lean: `¬ Nonempty (DirectionalResidual D r q)` and `¬ Nonempty (InternalSymmetryBreak D r q)` — the direction `r → q` only, as the header's "same directional closure" says. None found.
2. Change log: "closes the current finite residual without claiming future quiescence." Matches the conditional, `r`-supplied Lean. None found.
3. Vacuity: hypotheses are jointly satisfiable (e.g. `D = [0,1]`, `p` constant, `q = id`, `r = id`, `b` the transposition break from the probe for ClosureSymmetry; not separately machine-checked). No vacuity found.
