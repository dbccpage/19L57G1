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

G2 is a positive control rather than a mutation: the generating step that
writes `reqs` is an `Impose`, which is exactly what E2 forbids of a
non-supplying step.

G10–G12 are the three review defects on `f5e17f6`: index flags hiding a
consumed Lean blob, combined `percent_covered` sold as line coverage, and
a nonempty file set that omitted every computational module.

## What this tree does not claim

No generator on `C_reqs`.  I1 is OPEN.  Second-stake E4 invariance is not
attempted.  Standing and ignition generation are cited as not E1.  No
sealed path is written.  No CI registration.
