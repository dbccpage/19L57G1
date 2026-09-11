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

### AE-NO-INTEGER-SELECTOR

- **Statement**: An integer index, including a non-negative index, is
  not a selector among tied classes.  `License` fields are exactly
  granter, scope, and authorized keys.
- **Class**: declared harness invariant.
- **Python**: `harness.make_license`, `harness.key_by_index`;
  `tests/test_denied_license.py`.
- **Falsifier**: a `License` that selects a tied class by integer index.

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

### AE-RECEIPT-NOT-PROOF

- **Statement**: The PEA JSON receipt is a timestamp-free local
  record of a declared fold.  It does not authorize by score and is not
  a proof.
- **Class**: declared scope.
- **Python**: `run.py`; `tests/test_receipt.py`;
  `evidence/three_phase.json` `receipt_is_not_proof`.
- **Falsifier**: treating the receipt bytes as a theorem.
