# alpha_engine: conservative standing of this land

AuthorityEffect: None.

Baseline pin: `a4dcddff1a8f8029beb9ec538d26150766dbbcd2`
(`SOURCE_MANIFEST.json`).  This tree is a local receipt.  It is not
gate 11.  Receipts are not proofs of an unverified payload.

A prior STATUS sentence that every listed guard is proved by live
injection of the named defect, naming the object and recovering on
reversal, is **WITHDRAWN**.  G4, G13, and G14 were not that.

## What holds, scoped

- `Proposal`, `EvalResult`, and `License` are distinct types.
  `as_event` raises.  `License` is not one of the six sealed `Event`
  constructors.  There is no revoke API.  A score is not a `License`.
- `evaluate` returns an `EvalResult`, not a grade stamp.  It does not
  import `partial_decide`.  Quotient children are local names that are
  deleted.  `EvalResult` has no Event field.  Attempting to persist
  Events onto the declared base raises `EvaluationPersistedEventError`.
  `mutated_declared_base` is a before/after comparison.
- Under sealed `Bounds(max_items=2, max_arity=2)`, `evaluate` on
  Challenge-3 L/mu1 retains three iso classes and F/mu1 retains five.
  That is the sealed finite computation.  It is not a catalog
  completeness theorem of this tree.
- `record_census` refuses a silent drop (`CensusError`) and a key
  absent from its retained tuple (`FabricatedClassError`).
  `apply_licensed` and `explore` rebind a fresh sealed
  `min_responses` / `canonical` via `fresh_retained_keys`.  A forged
  `EvalResult` that claims a key absent from that re-quotient is
  refused.
- Search policy constructors beyond `declared_explore_first` comprise
  `declared_bounded_priority` (bounded key subset in declared rank
  order), `declared_constraint_pruned` (partitioning via a constraint
  predicate), and `declared_cost_budgeted` (exact rational arithmetic
  in Q via `fractions.Fraction`). Each constructor executes
  `record_census` to confirm partition disjointness and completeness
  over the sealed retained keys.
- `apply_unique_delta` always raises.  Uniqueness is not itself a
  `License`.  `explore` has no uniqueness guard: a `License` that names
  the sole retained class still applies it (C3 L/mu2).  The C3 L/mu1
  and F/mu1 folds used in the receipt have three and five classes.
  The receipt field `auto_apply_unique_delta` is the comparison of
  that refusal, not a written literal.
- `license_from_grade` refuses `Tie` / `UniqueClass` / `UniqueDelta` /
  `None` stamps.
- `apply_licensed` with an empty authorized set returns `None` and does
  not construct a child.  `Node` is frozen, so a denied call cannot
  write `node.license` in place.
- `make_license` refuses extra kwargs, including an integer `index`.
  `key_by_index` refuses an integer as a selector among tied classes.
  `License` fields are exactly granter, scope, and authorized keys.
- `leftover_as_demand` raises.  This tree does not feed leftover
  collapsed pairs into a demand generator.
- `occupy` refuses proposer occupancy that exposes `emit`,
  `materialize`, or `host_next_demand`, and refuses non-Delta offerings.
- The PEA JSON decoder refuses duplicate names and CR bytes.
- A first-byte change of fixture `model.py` reports `SOURCE_CHANGED`.
  `prompt/`, `paper/`, and `artifacts/` stay unpinned.  No proved
  equivalence to `code/derivation/` is claimed.
- Local Lean about this harness compiles with reports in
  `{propext, Quot.sound}`.  `evidence/lean.json` records
  `python_driver_refinement: NOT_PROVED`.  `Harness.evaluation_does_not_admit`
  is `rfl` on the first projection of `runEval = (base, eval base target)`.
  It does not call Python `evaluate`.  AE-LEAN-EVAL-INERT names only
  that pair projection.

The `_fold_reading` compute order is evaluate, then wrap
`raw_minima` as a `Proposal`, then `present`, then `License`, then
`explore`.  The receipt field names `proposal` / `evaluation` /
`authorization` are a layout, not a proof that proposal precedes
evaluation.  The receipt records `compute_order` and
`field_layout_is_not_temporal_proof`.

## OPEN

- Demand generation / OB-1: **OPEN**.  Neither driver generates demand.
  There is no endogenous demand generator in this tree.
- Driver B / any lift that would need a new sealed `Event` kind:
  **OPEN** and unimplemented.  No seventh `Event` constructor.

## Receipt comparisons

`mutated_declared_base` is `declared_base_mutated(before, after, history)`.
`auto_apply_unique_delta` is whether `apply_unique_delta` returned a
node.  `leftover_are_observations` is whether `leftover_as_demand`
raised on each child's leftover pairs.

## Injections, classified

Receipts are not rewritten while an injection is live.

Live injections of the named defect (unit tests, reversed in the same
test):

| Gate | Injection | Observed failure |
|---|---|---|
| G1 | `CanonKey` absent from a fresh sealed re-quotient, including a forged `EvalResult` | `FabricatedClassError` |
| G2 | silent drop of a retained class | `CensusError` silent drop |
| G3 | call `apply_unique_delta` on a unique `EvalResult` | `UniqueDeltaAutoApplyError` |
| G4 | call `persist_eval_events_on_base` with an `Impose` | `EvaluationPersistedEventError`; declared base `replay` unchanged |
| G5 | grade stamp `UniqueDelta` / `Tie` / `UniqueClass` / `None` | `GradeIsNotLicenseError` |
| G6 | `License` with empty authorized set | `apply_licensed` returns `None` |
| G7 | extra `make_license` kwargs, including a non-negative integer | `LicenseSelectorError` |
| G8 | first byte of fixture `model.py` | `SOURCE_CHANGED: code/derivation/model.py` |
| G9 | `leftover_as_demand` on collapsed pairs | `LeftoverIsNotDemandError` |
| G11 | duplicate JSON names / CR bytes in synthetic bytes | `duplicate JSON key` / `CR bytes` |
| G12 | proposer occupancy exposing `emit` / `materialize` / `host_next_demand` | `SelectorOccupancyError` |

Not live injections of the named defect:

| Gate | What the test actually is |
|---|---|
| G10 | synthetic `coverage.json` at 94% statements; not a live source deletion |
| G13 | `tests/test_lean_gate.py` parser on a synthetic log containing `Classical.choice`; not a theorem in `lean/Harness.lean` |
| G14 | the same parser on a missing report; not a generated theorem dropped from `#print axioms` |

## Stopped

- No sealed `Event` amendment.  No seventh `Event` constructor.
- OB-1 stays **OPEN**.  No endogenous demand generator.
- Driver B stays **OPEN** and unimplemented.
- UniqueDelta is not auto-applied: `apply_unique_delta` refuses;
  uniqueness is not a `License`.  A declared `License` of a sole class
  is still an apply.
- No visit-count search, UCB, or stochastic rollouts.
- No `partial_decide.decide` import.  No panel-derived `decide()` input.
- No proved equivalence to `code/derivation/`.
- No `paper/coda/`.  No mathlib.  No `Classical.choice` in local Lean
  sources.
- No gate 11 wiring and no `research/README.md` edit (those leave this
  write root).

Next work in this tree would be proposals only, not authorizations.
This land authorizes none of them.
