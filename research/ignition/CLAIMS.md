# Claims: ignition on the sealed carrier

AuthorityEffect: None.  Every claim names its hypotheses, its novelty against
the reused results, its evidence, its falsifier and its remaining obligation.
The words forced, minimal, free, canonical, equivalent, universal and complete
appear only where a proof is named.  All Lean names are in
`lean/Ignition.lean` unless prefixed otherwise; every report lies within
`{propext, Quot.sound}` (`evidence/lean.json`).

Shared definitions: `Mentioned r d` (some instance of `r` names `d`);
`grow r` (the sealed `admitDatum` step); `Good r` (well-formed, rule-free,
every standing requirement separated); `XStep` (growth, or a rule-free sealed
`TransStep`); `block r`, `blockState r`, `runHist`, `runState`;
`questions r` (one question per well-formed context); `carrier r`
(`List.range r.data`).

### CL-IG-01 — the idle history is lawful

- **Statement**: `replayE (List.replicate n (supply 0)) r = some r` for every
  `n` and `r`; more generally any all-supply history replays to its start.
- **Hypotheses**: none.
- **Novelty**: the sealed `supply_no_op` is one step; this is the history-level
  statement used by the boundary.
- **Evidence**: `idle_lawful`, `inert_history`.
- **Falsifier**: a bare-supply history the sealed step refuses or changes.
- **Obligation**: none.

### CL-IG-02 — growth creates exactly the unmentioned pairs

- **Statement**: for well-formed rule-free `r`, `collapsed (grow r) a r.data ↔ ¬ Mentioned r a`.
- **Hypotheses**: `r.wf`, `r.rules = []`.
- **Novelty**: new on the sealed carrier; the `standing_commitment` results are
  on the `World` carrier and count pairs against a declared commitment.
- **Evidence**: `grow_demand_iff`, through `collapsed_with_unmentioned_iff`,
  `wfCtx_holeAt`, `plug_holeAt`, `derivable_unmentioned_iff`; executed as
  `growth_demand_record` (`characterization_holds` on every opening state and
  every closed-export fixpoint).
- **Falsifier**: a growth step whose new demands are not the pairs of the
  fresh datum with the unmentioned data.
- **Obligation**: with rules present the equivalence is not claimed (the
  left-to-right direction uses rule-freeness).

### CL-IG-03 — at most one demand per growth at a fixpoint

- **Statement**: if every pair of admitted data is separated, no two admitted
  data are both collapsed with the fresh datum.
- **Hypotheses**: `∀ a b, a < b → b < r.data → separable r a b`.
- **Novelty**: settles the `two_sided_commitment` conjecture TS-14 on the
  sealed model (its finite finding TS-09 is bounded).
- **Evidence**: `grow_at_most_one_demand`; histogram of new demands at the 19
  closed-export fixpoints lies in `{0, 1}`.
- **Falsifier**: a fixpoint from which one growth creates two demands.
- **Obligation**: none.

### CL-IG-04 — two growths always create a demand; growth changes no verdict

- **Statement**: `collapsed (grow (grow r)) r.data (r.data + 1)` for
  well-formed `r`; and `collapsed (grow r) d d' ↔ collapsed r d d'`.
- **Hypotheses**: `r.wf`.
- **Novelty**: the sealed-carrier form of `fixpoint_reopens`; the second part
  is the sealed R1 lemma instantiated at the growth step.
- **Evidence**: `two_grows_collapsed`, `grow_keeps_verdicts`; `all_two_growths_demand`
  and `no_grow_is_activity` in the record.
- **Falsifier**: two growth steps after which the fresh pair is separated.
- **Obligation**: none.

### CL-IG-05 — enabledness after two growths

- **Statement**: after two growths from a well-formed regime whose standing
  requirements are separated, the mark `[newForm 1, newInst F [r.data+1]]` is a
  valid response to the fresh pair.
- **Hypotheses**: `r.wf`, `∀ q ∈ r.reqs, separable r q.1 q.2`.
- **Novelty**: an instance of the sealed `mark_progress` at the grown state;
  no new proof idea.
- **Evidence**: `two_grows_response`.
- **Falsifier**: a `Good` state after two growths with no valid response.
- **Obligation**: none.

### CL-IG-06 — the invariant is preserved by every extension step

- **Statement**: `Good r → XStep r t → Good t`; in particular every sealed
  rule-free `TransStep` keeps well-formedness and every standing requirement
  separated.
- **Hypotheses**: `Good r`; for a fire, `∀ f, newRuleAll f ∉ δ`.
- **Novelty**: the well-formedness preservation of `applyItem`/`applyDelta`
  and the requirement-carrying transport `applyDelta_reqs_free` were not in
  the sealed tree.
- **Evidence**: `good_xstep`, `good_grow`, `good_fire`, `applyItem_wf`,
  `applyDelta_wf`, `applyDelta_rules`, `applyDelta_reqs_free`; `final_good` in
  every exhibit.
- **Falsifier**: a rule-free valid response whose result is ill-formed or
  collapses a standing requirement.
- **Obligation**: none.

### CL-IG-07 — the decoding square commutes

- **Statement**: every `XStep r t` has a sealed event block replaying to `t`:
  `[admitDatum]` for growth, `impose i j :: δ.map itemEvent` for a fire.
- **Hypotheses**: none beyond the step.
- **Novelty**: assembles the merged `LocalReuse.round_replays` with the
  extension; the event block is the sealed engine's own.
- **Evidence**: `grow_replays`, `fire_replays`, `xstep_replays`; `certified`
  in every exhibit.
- **Falsifier**: an extension step with no sealed event block, or one whose
  block replays elsewhere.
- **Obligation**: none.

### CL-IG-08 — the productive run

- **Statement**: for `Good r` and every `k`,
  `replayE (runHist r k) r = some (runState r k)`, `runState r k` is `Good`,
  with `r.data + 2k` data, `r.forms.length + k` forms and `r.reqs.length + k`
  requirements; `runHist r k` is a prefix of `runHist r (k+1)`; each block is
  three extension steps and its round changes the verdict on its target.
- **Hypotheses**: `Good r`; growth supplied at every block (L1); the fresh
  pair taken as the demand (L2); the block executed (L3).
- **Novelty**: the first horizon-uniform productive run in the sealed event
  language; the sealed tree carried the closed bound and finite exports only.
  The `Constitution` tower is the analogous statement on the `World` carrier
  with a represented policy; this one has no policy field and is priced as
  three laws.
- **Evidence**: `runHist_replays`, `runState_good`, `runState_data`,
  `runState_forms`, `runState_reqs`, `runHist_prefix`, `block_is_xsteps`,
  `block_is_activity`, `rootL_good`, `rootF_good`.
- **Falsifier**: a `Good` state from which the block fails to replay, or a
  horizon at which the counts break.
- **Obligation**: the block uses the mark response, always valid; the sealed
  engine's minimum at the same state may be a one-item instance when a form
  exists — the run is a witness of the class, not the engine's minimum-cost
  history.

### CL-IG-09 — two interpretations of the same static facts

- **Statement**: from every `Good` state the bare-supply history and the block
  are both lawful; the first leaves the state unchanged and the second changes
  it and separates a collapsed pair.
- **Hypotheses**: `Good r`.
- **Novelty**: the boundary theorem of this family.
- **Evidence**: `idle_and_active_both_lawful`, `blockState_ne`,
  `block_is_activity`.
- **Falsifier**: a sealed premise the idle history violates.
- **Obligation**: the statement that the sealed signature cannot formulate
  occurrence is a grammar observation (no transition without an event), not a
  theorem, and is recorded as such.

### CL-IG-10 — the closure demand is the residual relative to identity

- **Statement**: for admitted `i, j`: `i ≠ j ∧ collapsed r i j` iff the
  signature quotient of `questions r` identifies `i` and `j` and `id` separates
  them; signature agreement over `questions r` is collapse.
- **Hypotheses**: `i < r.data`, `j < r.data`.
- **Novelty**: the sealed `Compression` and `PresentationRelativity` results
  are over abstract `Nat → Nat` presentations; this lands them on the sealed
  carrier through the represented context family.
- **Evidence**: `demand_iff_residual`, `demand_residual`, `sigEq_iff_collapsed`,
  `mem_ctxList`, `mem_tuples`, `mem_slotOptions`.
- **Falsifier**: a collapsed distinct pair the quotient separates, or a
  separated pair it identifies.
- **Obligation**: none.

### CL-IG-11 — the demand's comparison is not a digest of the profile

- **Statement**: if some distinct pair is collapsed, no function of the
  profile signature reproduces the identity comparison; and the identity does
  not factor through the profile presentation.
- **Hypotheses**: a collapsed distinct pair.
- **Novelty**: locates the comparison `q` of the residual exactly: the
  carrier's numbering, read by the closure policy and by no represented
  operation.
- **Evidence**: `identity_not_signature_determined`,
  `demand_refutes_factorization`; the glyph-reader negative case.
- **Falsifier**: a signature-determined function equal to the identity on a
  carrier with a collapsed pair.
- **Obligation**: OB-1 unchanged: the read is licensed by declaration.

### CL-IG-12 — the joint presentation: fibers, idempotence, order

- **Statement**: on the carrier, `pQ D [p,q] x = pQ D [p,q] y ↔ p x = p y ∧ q x = q y`;
  `SigEq [pQ D [p,q], q] ↔ SigEq [p,q]`; the partition is the same for two
  carrier lists of equal membership; the representative depends on order.
- **Hypotheses**: `x, y ∈ D`.
- **Novelty**: small corollaries of the sealed `pQ_exact`, recorded because
  the work order asked for them.
- **Evidence**: `joint_eq_iff`, `joint_idempotent`, `sigEq_pair`,
  `partition_order_free`, `representative_order_dependent`.
- **Falsifier**: a pair on which the joint fiber and the conjunction disagree.
- **Obligation**: none.

### CL-IG-13 — the future factors through the endpoint

- **Statement**: two histories replaying to one regime have identical
  continuations; the commit-early and commit-late routes share an endpoint,
  differ in span total (2 against 3) and agree on every continuation.
- **Hypotheses**: none.
- **Novelty**: the negative form of exhibit 1 on the sealed carrier; the
  route example is the merged `path_dependent_cost` witness restated, not a
  new result.
- **Evidence**: `future_factors_through_endpoint`, `routes_agree`,
  `routes_cost_differ`, `routes_indistinguishable`; `route_pair` in the record.
- **Falsifier**: a continuation distinguishing the two routes.
- **Obligation**: storing a route-dependent quantity is a separately
  classified extension, not built.

### CL-IG-14 — the exhibits are certified computations

- **Statement**: `linked_episodes`, `disabled_components`, `route_pair` and
  `fixpoint_census` in `evidence/ignition.json` replay byte-identically; every
  realized history certifies by the sealed `certify`; every fire is activity
  and no growth is; removal of L2 removes all activity and removal of L1 stops
  at the fixpoint; the root families are L/mu1 3 classes of 6, F/mu1 5 of 10,
  mu2 1 of 2 for both readings.
- **Class**: finite computation.
- **Evidence**: `run.py --check`; `tests/test_ignition.py`,
  `tests/test_evidence.py`.
- **Falsifier**: a differing byte on recomputation, or an uncertified history.
- **Obligation**: none.

### CL-IG-15 — the negative and positive controls

- **Statement**: the eight named defects are rejected by the check they
  attack and the two positive controls are accepted (section 8 of
  `README.md`).
- **Class**: finite computation.
- **Evidence**: `tests/test_ignition.py::NegativeCases`, `RootFamilies`.
- **Falsifier**: a defect that passes its check, or a control it rejects.
- **Obligation**: none.

## What is not claimed

* Seed entailment of any law: the three laws are declared, and CL-IG-01 is
  the reason the third cannot be derived on the sealed signature.
* Engine refinement: the engine's minimum selection, orbit quotient and node
  guards are not formalized; its exports are members of the class by
  construction, not proved to be its quotient.
* Necessity of `{grow, fire}` outside that grammar; a commitment over
  profiles rather than indices; a represented budget on this carrier.
* Anything about three-item responses, other measures, the `World`, passage or
  described-execution carriers, or exhibit 3.
* Termination of closed runs whose minimum responses admit data (OPEN).
