# endogenous_demand: status and injection record

AuthorityEffect: None.

Baseline: `cea346d7f3603fd8da374947e76c9b3cd426d122`.
Outcome: **B** for `C_reqs`.  Instance channel: **OPEN**.

## Injections

Every guard is proved by failing on the exact defect it exists to catch,
naming the injected object, and recovering on reversal.  Receipts are
never rewritten while an injection is live.  The unit tests mutate in
memory (`tests/test_injections.py`, `tests/test_sources.py`,
`tests/test_candidates.py`, `tests/test_reader.py`).

| Gate | Injection | Observed failure | Reversed |
|---|---|---|---|
| G1 | census row C1 labelled endogenous | `E1_GUARD: C1 labelled endogenous` | no failure |
| G2 | last event of Challenge-3 L is Impose and grew reqs | recorded as supplying, `e2_violation` is None | — |
| G3 | instance copies a previously supplied pair | `identical_to_supplied` true; fails E3 | — |
| G4 | demand of an already-separable pair | C9 fails E3; `already_separable` true | — |
| G5 | census emptied to C4, C10, I1 | `CLASS_NONVACUITY: missing ...`; `CLASS_NARROW` | no failure |
| G6 | `sorry` / `mathlib` in a scanned string | forbidden-token / mathlib regex names it | — |
| G7 | first bytes of pinned `model.py` in a fixture | `SOURCE_CHANGED: code/derivation/model.py` | no failure |
| G8 | reader source with `regime.reqs` | AST hit `...:reqs` | no failure |
| G9 | census row C5 labelled endogenous | `E1_GUARD: C5 labelled endogenous` | no failure |
| G10 | `assume-unchanged` then edit `Example.lean` | `SOURCE_CHANGED: lean4/Derivation/Example.lean`; `git diff` silent | no failure |
| G11 | 94% statements + 100% branches (`percent_covered` 97) | `COVERAGE_STATEMENT: 94.00%` | pass at 95/95 statements and branches |
| G12 | coverage report containing only `unrelated.py` | `COVERAGE_POPULATION: missing [...]` | required four files restore the pass |

| G13 | delete the `#print axioms` line of `endogenous_termination_bound` | `report/census mismatch: missing=['EndogenousDemandObstruction.endogenous_termination_bound']` | pass |
| G14 | a written theorem with no report line appended to `EndogenousDemandObstruction.lean` | `test_every_written_theorem_has_a_recorded_report` names it; `verify_lean.py --check` names it as a census mismatch | pass |

G2 is a positive control rather than a mutation: the generating step that
writes `reqs` is an `Impose`, which is exactly what E2 forbids of a
non-supplying step.

G10–G12 are the three review defects on `f5e17f6`: index flags hiding a
consumed Lean blob, combined `percent_covered` sold as line coverage, and
a nonempty file set that omitted every computational module.

G13–G14 are the audit gap repaired on 2026-09-24.  From 2026-09-10
(`e57a0886`, `f3ea95fc`, `a7d4c3f4`) until then, `python verify.py` did not
pass on main, and no gate runs it:

* the Lean record left out all seventeen written theorems of
  `EndogenousDemandObstruction.lean`, the termination bound among them.
  The census enumerated one namespace, and the reports of that module were
  never read.  The census is now by module.  A source-text census of written
  theorems must also be covered by the reports: 39 written, 44 with the 5
  compiler-generated ones, all within `{propext, Quot.sound}`;
* `evidence/lean.json` was committed with CRLF line endings, so
  `verify_lean.py --check` failed on every checkout.  It is now rewritten
  by `verify_lean.py --write`;
* `verify_termination.py` was never run by the test step, and coverage
  failed at 57% statements.  `tests/test_termination.py` now runs it.

The G13 and G14 injections were run against the repair commit and reverted.

## What this tree does not claim

No generator on `C_reqs`. OB-1 (demand generator on C_reqs) remains OPEN. The new files `lean/EndogenousDemandObstruction.lean` (now a Lake target) and `verify_termination.py` establish a termination bound for endogenous traces without external growth, but they do NOT construct a demand generator. I1 is OPEN. Second-stake E4 invariance is not attempted. Standing and ignition generation are cited as not E1. No sealed path is written. No CI registration.
