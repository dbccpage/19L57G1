# alpha_engine: conservative standing of this land

AuthorityEffect: None.

Baseline pin: `a4dcddff1a8f8029beb9ec538d26150766dbbcd2`
(`SOURCE_MANIFEST.json`).  This tree is a local receipt.  It is not
gate 11.  Receipts are not proofs of an unverified payload.

A prior STATUS sentence that every listed guard is proved by live
injection of the named defect, naming the object and recovering on
reversal, is **WITHDRAWN**.  G4, G13, and G14 were not that.

## 2026-09-25: closeout audit of the admission boundary

Work package C of the author's Genesis closeout
(`docs/GENESIS_CLOSEOUT.md`, sections 3 and 4).  Every hypothesis was
tested through the real public path (`evaluate` -> `make_license` ->
`apply_licensed` / `explore`) at `ccd0ab06`, before any repair, and
each adversarial test in `tests/test_admission_boundary.py` is paired
with a positive control that admits a legitimate transition, checked by
sealed replay and by an independent `min_responses` / `canonical`
recomputation.

| Hypothesis | Verdict at `ccd0ab06` | Observed behaviour before repair | Tests |
|---|---|---|---|
| B1 (M1): a legitimate key with a substituted member in a forged `EvalResult` | **REPRODUCED** | an empty member produced a child whose history ends in a bare `Impose(0, 1)` and which does not satisfy its own requirement; a member of another class produced a child whose key is not the authorized key; the same through `explore`; a forged cost was accepted | `B1SubstitutedMember.*` |
| B2 (M2): a parent whose history does not replay to its regime | **REPRODUCED** | `Node(history=F genesis, regime=L regime)` was accepted by `apply_licensed` and `explore`; the child's history does not replay to the child's regime | `B2NodeIntegrity.*` |
| B3 (M3): a License reused away from its declaration | **REPRODUCED** for source, target, measure and bounds | a License granted at L was accepted at the relabelled source `(<ab>, <a>)` (same canonical keys), where it marked `<ab>` instead of `<a>`; at L plus one `Supply`; for target `(1, 2)` used at `(0, 1)` on F; for mu1 used on mu2 (the License naming only the shared key); for `Bounds(2, 2)` used under `Bounds(2, 3)` and `Bounds(2, 1)`.  A License naming all three mu1 keys was refused on mu2 only incidentally, by the extra-key check | `B3LicenseBinding.*` |
| 4 (M4): a unique result admitted without an applicable authorization | **REFUTED** without a License (`apply_unique_delta` raises; an empty License admits nothing); **REPRODUCED** with an inapplicable one (the unique mu2 class was admitted under a License granted for mu1), the same root cause as B3 | see B3 | `H4UniquenessIsNotAuthorization.*` |
| 5 (M5): a retained alternative disappearing without a disposition | **REFUTED** through `explore` (a census that drops a class raises `CensusError`; evidence omitting classes raises `FabricatedClassError`); **REPRODUCED** through `apply_licensed`, which accepted evidence from which two of three retained classes had disappeared | `apply_licensed` returned a child | `H5Dispositions.*` |
| 6 (M6): proposal or evaluation changing state; an OPEN, bound or guard outcome presented as success | **REFUTED** | `present` and `evaluate` leave the regime unchanged; under `Bounds(1, 2)` the evaluation is `found=False`, cost `None`, no classes; `apply_licensed` refuses and `explore` admits nothing (`tie_set_size` 0) | `H6InertAndTypedStops.*` |

**Repairs, pass 1 of the two allowed (commit `b698cf7f`).**  Inside this
tree only; the sealed kernel is untouched.

- `License` records the declaration it authorizes: `source` (SHA-256 of
  a canonical JSON encoding of the source node's history, by
  `history_digest`), `target`, `measure` and `bounds`.  `make_license`
  takes the source node, target, measure and bounds, and still refuses
  every extra field, including an integer index.
  `check_license_binding` refuses a License used away from its
  declaration and names each mismatched field (`LicenseBindingError`).
  The source is bound by history, not by canonical identity: the
  relabelled source above has the same canonical keys and the same
  evidence, so a canonical binding would have accepted it.
- `check_node_integrity` refuses a parent whose history carries a
  constructor outside the six sealed kinds, fails to replay, or replays
  to another regime (`NodeIntegrityError`).  It runs at use.
- `apply_licensed` and `explore` (through `bound_evaluation`) recompute
  the evaluation from the sealed kernel for the License's declaration.
  `check_evidence` refuses a class whose claimed members differ from the
  fresh class (`SubstitutedMemberError`) and any other difference
  (`ForgedEvaluationError`).  The executed member is the first member of
  the fresh class, never the caller's.  Its payload, cost,
  applicability, resulting key and preserved requirements are those the
  sealed `min_responses` and `canonical` computed for that exact
  replay; the positive controls re-check them independently.

No second pass was needed: after pass 1 every adversarial test passes
and every positive control admits.  M1 to M6 hold within the trust
boundary below; M7 and M8 are covered by `tests/test_handoff.py` and
`verify.py` (work package D, `docs/ALPHA_HANDOFF.md`).

**Trust boundary, as the audit found it.**  The harness is a local,
in-process Python library.  Trusted: the sealed kernel's six runtime
modules at the pinned baseline (custody-checked by `verify_sources.py`),
this tree's code, and the host, meaning the code that calls
`apply_licensed` or `explore`.  The host establishes authorization by
that call: it builds the License itself with `make_license`, from its
own declared policy, at the declaration it chose, and passes it.
Checked at use, as untrusted data: the `EvalResult` (evidence only), the
parent `Node`, the License's binding and keys, the `PolicyCensus`, and
proposer offerings (Supply-shaped, never executed).  *Correction to the
frozen hypothesis:* a License can be checked for consistency with the
call, not for provenance.  A License a proposer built that is consistent
with the call is indistinguishable from the host's, so authority rests
on the host's act of passing it; a host must never forward a License it
did not build.  A scope string, a granter string, a digest and a Python
type are not authentication.  Excluded: process compromise, including
objects that override equality, hashing or attribute access, and
mutation of frozen objects through `object.__setattr__`; tampering with
the sealed kernel or this tree (the custody check detects edits to
pinned sources, it does not defend against a live attacker); SHA-256
collisions; concurrent use; any network, identity or multi-party
authentication.

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
  *2026-09-25, narrowed:* this bullet covered keys only.  The executed
  member was read from the caller's `EvalResult` after the key check, so
  a forged `EvalResult` with a legitimate key and a substituted member
  was admitted (B1, reproduced above).  Since pass 1 the whole
  `EvalResult` must equal the fresh recomputation and the executed
  member comes from the recomputation; `explore` and `apply_licensed`
  no longer call `fresh_retained_keys`, which remains a public helper.
- Search policy constructors beyond `declared_explore_first` comprise
  `declared_bounded_priority` (bounded key subset in declared rank
  order), `declared_constraint_pruned` (partitioning via a constraint
  predicate), and `declared_cost_budgeted` (exact rational arithmetic
  in Q via `fractions.Fraction`). Each constructor executes
  `record_census` to confirm partition disjointness and completeness
  over the sealed retained keys.
- `apply_unique_delta` always raises.  Uniqueness is not itself a
  `License`.  `explore` has no uniqueness guard: a `License` that names
  the sole retained class still applies it (C3 L/mu2).
  *2026-09-25, narrowed:* a `License` applies only when bound to the
  declaration in use; the sole mu2 class was admitted under a License
  granted for mu1 before pass 1 (hypothesis 4).  The C3 L/mu1
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
  *2026-09-25, superseded:* they are now those three plus the four
  binding fields `source`, `target`, `measure` and `bounds`.  There is
  still no integer selector field and no revoke API.
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
  *2026-09-25:* the Lean `License` structure still has only granter,
  scope and authorized keys; it does not model the binding, node
  integrity or the evidence check.  No Lean statement covers M1 to M3.

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

Closeout audit, 2026-09-25.  Each row reverts a repair in the real
`driver_a.py` (or corrupts a real input of the real command), requires
the named failure, restores the bytes and requires recovery.  The first
four rows are reproducible with `python inject_boundary.py` on a clean
worktree; the last two were run by hand against `python verify.py`.
No receipt was regenerated while any of them was live.  All six are
**live** injections of the named defect.

| Gate | Injection | Observed failure | Recovery |
|---|---|---|---|
| B1 member (M1) | `apply_licensed` executes `representative_delta(result, key)` again and both `check_evidence` calls are removed | `B1 REPRODUCED: apply_licensed executed an empty substituted member of an authorized key`; the same for a member of an unauthorized class, through `explore`, and for a forged cost (4 tests) | 4 tests pass with the bytes restored |
| H5 evidence (M5) | the `check_evidence` call in `apply_licensed` removed and the caller's member executed | `H5 REPRODUCED: apply_licensed accepted evidence from which two retained classes had disappeared` | 1 test passes |
| B2 node integrity (M2) | `check_node_integrity(node)` removed from `bound_evaluation` | `B2 REPRODUCED: apply_licensed accepted a parent whose history does not replay to its stated regime`; the same through `explore` | 2 tests pass |
| B3 binding (M3, M4) | `check_license_binding` removed and the fresh evaluation taken from the call (target, the evidence's measure and bounds), as before the repair | `B3 REPRODUCED: a License granted at one source node was accepted at a relabelled source`; also another history, target `(1, 2)` used at `(0, 1)`, mu1 used for mu2, `Bounds(2, 2)` used under `(2, 3)` and `(2, 1)`, through `explore`; and `H4 REPRODUCED: a unique mu2 class was admitted under a License granted for mu1` (8 lines, 7 tests) | 7 tests pass |
| One command, failing check (M8) | one byte of `evidence/handoff_demo.json` changed | `FAIL: test_committed_record_matches (test_handoff.HandoffDemonstrations...)`, `FAIL: tests exited 1`, the seven later steps listed `NOT RUN`, exit 1 | exit 0, all nine steps PASS |
| One command, skipped check (M8) | `evidence/lean.json` moved aside, so a unit test skips | `SKIPPED CHECK: tests: test_lean_gate.CommittedRecord.test_record_is_within_the_whitelist_and_not_a_proof`, `FAIL: tests skipped a check`, later steps `NOT RUN`, exit 1 | exit 0 |

Not live injections of the named defect:

| Gate | What the test actually is |
|---|---|
| G10 | synthetic `coverage.json` at 94% statements; not a live source deletion |
| G13 | `tests/test_lean_gate.py` parser on a synthetic log containing `Classical.choice`; not a theorem in `lean/Harness.lean` |
| G14 | the same parser on a missing report; not a generated theorem dropped from `#print axioms` |

## Guarantees still failing after the closeout audit

None of M1 to M8 fails after pass 1, within the trust boundary above.
Residuals that remain (not blockers of M1 to M8, and not repaired here):
G10, G13 and G14 are still not live injections;
`python_driver_refinement` is still `NOT_PROVED`; the Lean harness does
not model the binding.

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
