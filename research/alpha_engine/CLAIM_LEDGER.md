# Claims: proposal-evaluation-authorization harness over sealed minima

AuthorityEffect: None.

Native `AE-*` IDs only.  Companion ledger IDs are not used.  Guarded
words appear only with a proof or a scoped negation.  Receipts named
below are not proofs.

### AE-PEA-FOLD

- **Statement**: Proposal, evaluation, and authorization are distinct
  types.  Evaluation never admits.  A score is not a license.  The
  JSON field names `proposal` / `evaluation` / `authorization` are a
  record layout.  They are not a proof that proposal precedes
  evaluation.  The recorded `compute_order` is evaluate, wrap
  raw minima as a Proposal, present, License, explore.
- **Class**: declared harness invariant.
- **Python**: `harness.Proposal`, `evaluate.evaluate`, `harness.License`;
  `evidence/three_phase.json` `compute_order`,
  `field_layout_is_not_temporal_proof`.
- **Falsifier**: a single function that both evaluates and writes an
  admission Event onto the declared base.

### AE-EVAL-INERT

- **Statement**: `evaluate` leaves the declared base unchanged and does
  not persist `delta_events`.  Quotient children are discarded after
  keys.
- **Class**: deterministic computation.
- **Python**: `tests/test_evaluation_events.py`;
  `evaluate.persist_eval_events_on_base`;
  `evaluate.declared_base_mutated`.
- **Falsifier**: `persist_eval_events_on_base` succeeding, or
  `declared_base_mutated` true after `evaluate`.

### AE-TIE-RETENTION

- **Statement**: Under sealed `Bounds(max_items=2, max_arity=2)`,
  Challenge-3 L/mu1 retains three iso classes and F/mu1 retains five.
  This is the sealed finite computation, not a new theorem that the
  catalog is all minima outside that bound.
- **Class**: finite computation.
- **Python**: `evaluate.evaluate` on `READING_L` / `READING_F`;
  `evidence/three_phase.json` `retained_class_count`.
- **Falsifier**: a count other than 3/5 under those bounds.

### AE-LICENSE-NOT-EVENT

- **Statement**: A `License` is not one of the six sealed `Event`
  constructors.  There is no revoke API.
- **Class**: declared harness invariant.
- **Python**: `harness.as_event`; `tests/test_harness.py`.
- **Falsifier**: a `License` accepted by `append_sealed_event`.

### AE-POLICY-SUBSET

- **Statement**: `SearchPolicy` output is a subset of the retained
  iso-class key set.  Every retained class is recorded explored,
  pruned, or open, and those three counts sum to the tie-set size.
- **Class**: declared harness invariant.
- **Python**: `search_policy.record_census`;
  `tests/test_policy_census.py`.
- **Falsifier**: a policy returning a key outside the retained set, or
  a silent drop.

### AE-NO-AUTO-APPLY

- **Statement**: A unique minimum (one raw delta, one iso class) remains
  a proposal.  Uniqueness is not authorization.  `apply_unique_delta`
  always raises.  The receipt field `auto_apply_unique_delta` is the
  comparison of that refusal, not a written literal.
- **Class**: declared harness invariant.
- **Python**: `harness.apply_unique_delta`;
  `driver_a._unique_auto_applied`;
  `tests/test_no_auto_apply.py`.
- **Falsifier**: Driver A applying a unique class without a `License`.

### AE-SOLE-LICENSE-IS-APPLY

- **Statement**: A `License` that names the sole retained class is still
  an apply.  `explore` has no uniqueness guard.  Uniqueness without a
  `License` is refused; uniqueness with a `License` is authorization.
- **Class**: declared harness invariant.
- **Python**: `tests/test_no_auto_apply.py::test_licensed_sole_class_is_still_an_apply`.
- **Falsifier**: a licensed sole class that `explore` refuses because it
  is unique.
- **2026-09-25, narrowed**: "uniqueness with a `License` is
  authorization" holds only for a `License` bound to the declaration in
  use.  The closeout audit admitted the sole mu2 class under a License
  granted for mu1 at `ccd0ab06`; see AE-LICENSE-BOUND.

### AE-NO-INTEGER-SELECTOR

- **Statement**: An integer index, including a non-negative index, is
  not a selector among tied classes.  `License` fields are exactly
  granter, scope, and authorized keys.
- **Class**: declared harness invariant.
- **Python**: `harness.make_license`, `harness.key_by_index`;
  `tests/test_denied_license.py`.
- **Falsifier**: a `License` that selects a tied class by integer index.
- **2026-09-25, superseded in part**: "`License` fields are exactly
  granter, scope, and authorized keys" is superseded.  The fields are
  those three plus the binding fields `source`, `target`, `measure` and
  `bounds` (AE-LICENSE-BOUND).  The rest of the statement stands: no
  integer selector field, and `make_license` refuses an `index` of any
  sign.

### AE-GRADE-NOT-LICENSE

- **Statement**: A partial-Decide grade stamp (`Tie`, `UniqueClass`,
  `UniqueDelta`, or `None`) is not a `License`.
- **Class**: declared harness invariant.
- **Python**: `harness.license_from_grade`;
  `tests/test_grade_stamp.py`.
- **Falsifier**: constructing a `License` from a grade stamp.

### AE-FABRICATED-REFUSED

- **Statement**: A class key absent from a fresh sealed
  `min_responses` / `canonical` quotient is refused, even when a
  stored `EvalResult` claims it.
- **Class**: declared harness invariant.
- **Python**: `evaluate.fresh_retained_keys`;
  `tests/test_fabricated_class.py`.
- **Falsifier**: Driver A expanding a key present only on a forged
  `EvalResult` and absent from a fresh sealed re-quotient.
- **2026-09-25, narrowed**: this claim is about keys only, and it was
  read as more.  Until pass 1 of the closeout audit, Driver A executed
  the first member stored in the caller's `EvalResult` once the keys
  checked out, so a forged `EvalResult` with a legitimate key and a
  substituted or empty member produced a child (B1, reproduced at
  `ccd0ab06`).  The member guarantee is AE-MEMBER-CHECKED.

### AE-LEFTOVER-OBS

- **Statement**: Leftover collapsed pairs after a licensed apply are
  observations, not a next demand.
- **Class**: declared harness invariant.
- **Python**: `harness.leftover_as_demand`;
  `tests/test_driver_a.py`.
- **Falsifier**: leftover pairs used as authorization or as an
  endogenous demand.

### AE-DEMAND-OPEN

- **Statement**: Demand generation and OB-1 remain **OPEN**.  Neither
  Driver A nor this tree supplies an object-language demand generator.
- **Class**: open obstruction.
- **Python**: `evidence/three_phase.json` `demand_generation`, `ob_1`.
- **Falsifier**: a generator in this tree that writes `Regime.reqs`
  without a sealed `Impose`.

### AE-DRIVER-B-OPEN

- **Statement**: Driver B — any lift that needs a new sealed `Event`
  kind — is **OPEN** and unimplemented.  No seventh Event constructor
  is added.
- **Class**: open obstruction.
- **Python**: `evidence/three_phase.json` `driver_b`;
  `harness.append_sealed_event`.
- **Falsifier**: an implemented lift that admits a constructor outside
  the six sealed Event kinds.

### AE-LEAN-LICENSE-NOT-EVENT

- **Statement**: In the local Lean harness, `asEvent` on a `License`
  is `none`.  A `License` is not an `Event`.
- **Class**: local harness theorem.
- **Lean**: `Harness.license_is_not_event`.
- **Python**: `harness.as_event`.
- **Falsifier**: a conversion from `License` to a sealed `Event`
  constructor.

### AE-LEAN-POLICY-SUBSET

- **Statement**: If `censusOk p`, every explored key is a member of
  `p.retained`.  The declared take-1 policy satisfies `censusOk`.
- **Class**: local harness theorem.
- **Lean**: `Harness.policy_explored_subset`,
  `Harness.declaredExploreFirst_censusOk`.
- **Python**: `search_policy.record_census`.
- **Falsifier**: a well-formed policy whose explored bucket contains a
  key absent from the retained set.

### AE-LEAN-NO-AUTO-APPLY

- **Statement**: `applyUnique` is `none` even when the evaluation is
  unique.  Uniqueness does not apply.
- **Class**: local harness theorem.
- **Lean**: `Harness.uniqueness_does_not_apply`.
- **Python**: `harness.apply_unique_delta`.
- **Falsifier**: a unique retained class applied without a `License`.

### AE-LEAN-EVAL-INERT

- **Statement**: In the local Lean harness, `runEval base target eval`
  is the pair `(base, eval base target)`.  The first projection is
  definitionally `base`.  This is not a theorem about Python
  `evaluate.evaluate`.
- **Class**: local harness theorem.
- **Lean**: `Harness.evaluation_does_not_admit`,
  `Harness.eval_carries_no_events`.
- **Falsifier**: a changed `runEval` whose first projection is not
  `base`.

*2026-09-25, scope note for the four AE-LEAN claims:* the Lean
`License` has only granter, scope and authorized keys.  It does not
model the binding (AE-LICENSE-BOUND), node integrity
(AE-NODE-INTEGRITY) or the member check (AE-MEMBER-CHECKED), and no
Lean statement is claimed for them.  `python_driver_refinement` stays
`NOT_PROVED`.

### AE-MEMBER-CHECKED

- **Statement** (2026-09-25): `apply_licensed` and `explore` execute
  only the first member of the authorized class as freshly recomputed
  from the sealed kernel (`min_responses`, `canonical`) for the
  License's declaration.  A caller's `EvalResult` whose claimed members
  for that class differ is refused (`SubstitutedMemberError`); one that
  differs in any other way, including an omitted class, a cost or the
  raw minima, is refused (`ForgedEvaluationError`).
- **Class**: declared harness invariant, checked by finite tests on the
  Challenge-3 fixtures; not a theorem.
- **Python**: `driver_a.bound_evaluation`, `driver_a.check_evidence`;
  `tests/test_admission_boundary.py::B1SubstitutedMember`,
  `::H5Dispositions::test_h5_apply_evidence_omitting_a_class_is_refused`.
- **Injection**: live; `inject_boundary.py` rows B1 and H5 (`STATUS.md`).
- **Falsifier**: a forged `EvalResult` with a legitimate key and a
  substituted or empty member that produces a child.

### AE-NODE-INTEGRITY

- **Statement** (2026-09-25): an admission step refuses a parent `Node`
  whose history carries a constructor outside the six sealed kinds,
  does not replay, or replays to a regime other than the one it states
  (`NodeIntegrityError`).  The check runs at use; constructing such a
  `Node` is not refused.
- **Class**: declared harness invariant.
- **Python**: `harness.check_node_integrity`;
  `tests/test_admission_boundary.py::B2NodeIntegrity`.
- **Injection**: live; `inject_boundary.py` row B2.
- **Falsifier**: a `Node(history=h, regime=r)` with `replay(h) != r`
  accepted as a parent.

### AE-LICENSE-BOUND

- **Statement** (2026-09-25): a `License` records the declaration it
  authorizes (the SHA-256 `history_digest` of the source node's
  history, the target pair, the measure and the bounds), and
  `apply_licensed` and `explore` refuse it, naming each mismatched
  field, when any of the four differs from the call
  (`LicenseBindingError`).  The binding is to the exact history, not to
  canonical identity: a relabelled source with the same canonical keys
  and the same evidence is refused.  The binding is not authentication:
  the harness checks a License's consistency with the call, not who
  built it.
- **Class**: declared harness invariant.
- **Python**: `harness.make_license`, `harness.history_digest`,
  `harness.check_license_binding`;
  `tests/test_admission_boundary.py::B3LicenseBinding`,
  `::H4UniquenessIsNotAuthorization`.
- **Injection**: live; `inject_boundary.py` row B3.
- **Falsifier**: a License granted for one source node, target, measure
  or bounds that admits under another.

### AE-OFFLINE

- **Statement** (2026-09-25): no module of this tree imports a model
  provider or network module, and the reference slice, its
  demonstrations and its replay run with none.
- **Class**: deterministic computation plus a static import scan.
- **Python**: `tests/test_handoff.py::HandoffDemonstrations::test_no_provider_or_network_import_in_the_tree`;
  `handoff_demo.py`.
- **Falsifier**: an import of a provider or network module in this tree.

### AE-ONE-COMMAND

- **Statement** (2026-09-25): `python verify.py` in this directory runs
  every required check of the reference slice in order (sources, tests
  under coverage, the coverage gate, mypy, Lean, the PEA record, the
  handoff demonstrations, the sealed kernel's own tests of the six
  consumed modules), exits non-zero when any fails, lists the steps
  after a failure as `NOT RUN`, and reports every skipped test by name
  as a failed check.
- **Class**: declared scope of a local receipt; not hosted CI and not
  gate 11.
- **Python**: `verify.py`; `tests/test_handoff.py::VerifyCommand`.
- **Injection**: live, by hand (`STATUS.md`, two M8 rows).
- **Falsifier**: `verify.py` exiting 0 with a required check failing or
  skipped.

### AE-HANDOFF-DEMOS

- **Statement** (2026-09-25): on the Challenge-3 fixtures,
  `handoff_demo.py` shows an accepted transition (L, mu1), retained ties
  (three classes for L, five for F, each with one disposition), four
  refused requests (a substituted member, a License reused for another
  measure, a key the License does not name, a parent that does not
  replay), and a bounded stop (`Bounds(1, 2)`: no valid response, the
  unresolved demand exported as the frontier).  Each is checked by
  sealed replay and by a recomputation that does not use the harness's
  `evaluate`.
- **Class**: finite computation; a local receipt, not a proof.
- **Python**: `handoff_demo.py`; `evidence/handoff_demo.json`
  `independent_checks`; `tests/test_handoff.py::HandoffDemonstrations`.
- **Falsifier**: an independent check of the record that is false.

### AE-RECEIPT-NOT-PROOF

- **Statement**: The PEA JSON receipt is a timestamp-free local
  record of a declared fold.  It does not authorize by score and is not
  a proof.
- **Class**: declared scope.
- **Python**: `run.py`; `tests/test_receipt.py`;
  `evidence/three_phase.json` `receipt_is_not_proof`.
- **Falsifier**: treating the receipt bytes as a theorem.
