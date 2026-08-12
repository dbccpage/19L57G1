# Claim ledger

Field key — **ID**: stable identifier. **Statement**: exact claim.
**Class**: one of declared metatheory / definition / finite computation /
theorem / bounded theorem / conjecture / counterexample / unresolved.
**Deps**: claims this one depends on. **Assumptions**: declared metatheory
it rests on. **Python**: evidence (artifact key and/or test).
**Lean**: theorem name(s) in `lean4/Derivation/`. **Axioms**: from
`artifacts/lean_axioms.txt` (`--` = no Lean formalization).
**Falsifier / boundary**: what would refute it, or the boundary that
survives.

Shared assumptions for every claim: the metatheory of `paper.md`
sections 2-3 (regimes, events, replay, contexts, profiles, declared
separability), and — where marked *bounded* — the declared bounds of
section 1.  Lean evidence is stated in the token-erased abstraction,
connected to the token-aware semantics by the proved simulation
CL-TOKEN-ERASURE; Lean is never claimed to literally mirror the Python
implementation.

---

### CL-0-INERTIA
- **Statement**: With nothing admitted, nothing is derivable and no
  successor state is internally forced; a bare supply never changes the
  admitted state.
- **Class**: theorem.
- **Deps**: none. **Assumptions**: shared only.
- **Python**: `challenges.json:challenge0`; `test_challenge0_inertia`,
  `test_supply_is_not_admission`.
- **Lean**: `supply_no_op`, `genesis_underivable`, `underivable_of_empty`.
- **Axioms**: `propext` (supply_no_op); none (the other two).
- **Falsifier / boundary**: a derivation or state change from the empty
  regime without an admission event.  None exists in the model; the
  boundary is the model itself (transitions are event-indexed by
  construction).

### CL-0-NO-PROPOSAL-MUTATION
- **Statement**: A proposed transition cannot alter admitted state without
  a separate admission event; ill-formed admissions are rejected.
- **Class**: theorem (model-scoped).
- **Deps**: CL-0-INERTIA. **Assumptions**: shared.
- **Python**: `test_model.py` (rejection of every ill-formed event kind);
  `test_replay_certify_and_tamper_detection`.
- **Lean**: `stepE` totality with `Option` rejection; `supply_no_op`.
- **Axioms**: `propext`.
- **Falsifier / boundary**: a state change reachable without an event.

### CL-1-SUPPLY-NOT-ADMISSION
- **Statement**: The Challenge 1 supply of `<a>` is a new external
  presentation and not an admission; no internal observable distinction
  arises.
- **Class**: theorem.
- **Deps**: CL-0-INERTIA. **Assumptions**: shared.
- **Python**: `challenges.json:challenge1`;
  `test_challenge1_supply_vs_admission_and_convergence`.
- **Lean**: `supply_no_op`, `collapsed_of_no_insts`.
- **Axioms**: `propext`; none.
- **Falsifier / boundary**: an internal test distinguishing anything at
  Challenge 1.

### CL-1-READING-CONVERGENCE
- **Statement**: The two Challenge 1 sub-readings (admit `<a>` on supply /
  do not) converge to the same regime at Challenge 2 close.
- **Class**: finite computation.
- **Deps**: CL-1-SUPPLY-NOT-ADMISSION. **Assumptions**: shared +
  presentation-identity dedup of admissions (declared).
- **Python**: `challenges.json:challenge1.sub_readings_converge_at_
  challenge2 = true`; same test.
- **Lean**: --. **Axioms**: --.
- **Falsifier / boundary**: differing replays of the two extended
  histories.

### CL-2-COLLAPSED
- **Statement**: After Challenge 2 both readings admit externally distinct
  tokens whose every pair is observationally collapsed.
- **Class**: theorem.
- **Deps**: CL-0-INERTIA. **Assumptions**: shared.
- **Python**: `challenges.json:challenge2` (observational classes = 1);
  `test_challenge2_collapse_and_no_expressive_increase`.
- **Lean**: `R2L_collapsed`, `R2F_collapsed`, `historyL_replays`,
  `historyF_replays`.
- **Axioms**: none; none; `propext`; `propext`.
- **Falsifier / boundary**: a well-formed context separating any pair in
  the Challenge 2 regime.

### CL-2-NONINCREASE
- **Statement**: A new external inscription does not necessarily increase
  internal expressive power: admitting a fresh datum changes the state but
  leaves the collapsed pair collapsed.
- **Class**: counterexample (to the necessity claim).
- **Deps**: CL-2-COLLAPSED. **Assumptions**: shared.
- **Python**: `challenges.json:challenge2.*.expressive_increase_over_
  challenge0 = false`.
- **Lean**: `admission_without_expressive_increase`.
- **Axioms**: `propext`.
- **Falsifier / boundary**: n/a (a counterexample refutes the general
  necessity claim; the boundary is that *some* inscriptions plus
  judgments do increase power — Challenge 3).

### CL-3-FAIL-CURRENT
- **Statement**: The Challenge 2 regime does not satisfy the declared
  internal separability of `<a>` and `<ab>` in either reading.
- **Class**: theorem.
- **Deps**: CL-2-COLLAPSED. **Assumptions**: shared + declared
  separability (definition 3.5).
- **Python**: `claims.json:CL-3-FAIL-CURRENT = {L: false, F: false}`;
  `test_challenge3_reading_l_classes`.
- **Lean**: `R2L_collapsed`, `R2F_collapsed` with
  `separable_not_collapsed`.
- **Axioms**: none.
- **Falsifier / boundary**: a witness context in the unaugmented regime.

### CL-3-COST1-IMPOSSIBLE
- **Statement**: No delta of at most one item is a valid response to the
  Challenge 3 requirement, in either reading.  *Bounds: none — absolute
  over the item grammar (any arity, any argument tuple). Measure: mu1.*
- **Class**: theorem.
- **Deps**: CL-3-FAIL-CURRENT. **Assumptions**: shared + candidate grammar
  (definition 3.6).
- **Python**: `test_c3_cost1_all_fail_and_min_is_two` (exhaustive over the
  bounded slice, consistent with the grammar-wide theorem).
- **Lean**: `cost1_insufficient_general`, `cost1_insufficient`,
  `cost1_insufficient_F`.
- **Axioms**: `propext`.
- **Falsifier / boundary**: a single admissible item separating the pair.

### CL-3-MIN-TWO
- **Statement**: The minimum valid response cost at Challenge 3 is exactly
  two items in both readings.  *Bounds: none. Measure: mu1. Uniqueness:
  see CL-3-NONUNIQUE-MU1.*
- **Class**: theorem.
- **Deps**: CL-3-COST1-IMPOSSIBLE. **Assumptions**: shared.
- **Python**: `challenges.json:challenge3.*.mu1.minimum_cost = [2, -1]`.
- **Lean**: existence — `deltaU0_valid`, `deltaU0F_valid`; floor —
  CL-3-COST1-IMPOSSIBLE.
- **Axioms**: `propext, Quot.sound`.
- **Falsifier / boundary**: a valid one-item response (excluded) or
  failure of the two-item witnesses (machine-checked).

### CL-3-NONUNIQUE-MU1
- **Statement**: Under mu1 the minimum corrective augmentation is not
  unique: the unary mark and the binary link are both minimum valid
  responses with non-isomorphic results.  *Bounds: none. Measure: mu1.
  Uniqueness: refuted absolutely.*
- **Class**: theorem.
- **Deps**: CL-3-MIN-TWO. **Assumptions**: shared + implemented
  isomorphism (definition 3.8).
- **Python**: `claims.json:CL-3-NONUNIQUE-MU1 = {L: 3, F: 5}`.
- **Lean**: `mu1_minimum_not_unique`, `U0_not_iso_BL`.
- **Axioms**: `propext, Quot.sound`.
- **Falsifier / boundary**: an isomorphism between the mark and the link
  (excluded: arity is an invariant).

### CL-3-TIE-CLASSES
- **Statement**: The tied mu1 minima at Challenge 3 form exactly 3
  isomorphism classes in reading L (unary mark, binary link, binary
  self-loop) and exactly 5 in reading F (adding link-to and link-from the
  genesis datum).  *Bounds: max_items 2, max_arity 2. Measure: mu1.
  Uniqueness: class counts complete only within these bounds.*
- **Class**: bounded theorem.
- **Deps**: CL-3-NONUNIQUE-MU1, CL-PRUNE-RULE, CL-PRUNE-STRUCTURAL,
  CL-ISO-SOUND. **Assumptions**: shared + bounds.
- **Python**: `challenges.json:challenge3` iso_classes; cross-check
  against the unpruned space
  (`test_pruned_cost2_contains_every_valid_full_delta`);
  `test_challenge3_reading_f_has_five_classes`.
- **Lean**: class distinctness — `U0_not_iso_BL`, `U0_not_iso_BD`,
  `BL_not_iso_BD`; class collapse — `isoU1U0`.
- **Axioms**: `propext, Quot.sound`.
- **Falsifier / boundary**: a valid bounded delta outside the listed
  classes, or a missed isomorphism.  Boundary: arity > 2 candidates exist
  and are tied (CL-3-INFINITE-TIES).

### CL-3-INFINITE-TIES
- **Statement**: For every arity k >= 1 the k-ary mark is a two-item
  minimum valid response, and distinct arities give non-isomorphic
  results: the mu1 tie class is countably infinite.  *Bounds: none.
  Measure: mu1.*
- **Class**: theorem.
- **Deps**: CL-3-COST1-IMPOSSIBLE. **Assumptions**: shared.
- **Python**: consistent bounded slice (arities 1, 2 both appear).
- **Lean**: `deltaK_valid`, `deltaK_length`, `markK_pairwise_noniso`,
  `deltaK_applies`, `markK_separable`.
- **Axioms**: `propext, Quot.sound` (`propext` only for the non-iso).
- **Falsifier / boundary**: an isomorphism between marks of different
  arity.

### CL-3-UNIQUE-MU2-L
- **Statement**: Under mu2, every valid two-item response with new-form
  arity sum <= 1 in reading L produces a regime isomorphic to the unary
  mark; with the cost floor this makes the mu2-minimum unique up to
  isomorphism.  *Bounds: item grammar-wide. Measure: mu2. Uniqueness:
  absolute over the grammar, up to the implemented isomorphism.*
- **Class**: theorem.
- **Deps**: CL-3-MIN-TWO. **Assumptions**: shared.
- **Python**: `claims.json:CL-3-UNIQUE-MU2.L = 1`;
  `test_c3_mu2_minimum_is_unary_mark`.
- **Lean**: `mu2_unique` (with `isoRefl`, `isoU1U0`).
- **Axioms**: `propext, Quot.sound`.
- **Falsifier / boundary**: a valid (2, <=1) delta with a non-mark result.

### CL-3-UNIQUE-MU2-F
- **Statement**: Under mu2 reading F has exactly one minimum class within
  the declared bounds (the unary mark on a required datum).  *Bounds:
  max_items 2, max_arity 2. Measure: mu2. Uniqueness: within bounds; the
  grammar-wide analogue is unformalized.*
- **Class**: bounded theorem.
- **Deps**: CL-3-UNIQUE-MU2-L (method), CL-ISO-SOUND.
- **Python**: `claims.json:CL-3-UNIQUE-MU2.F = 1`.
- **Lean**: -- (grammar-wide version unresolved).
- **Axioms**: --.
- **Falsifier / boundary**: a second bounded class.  Boundary: Lean
  formalization outstanding (paper section 12).

### CL-PRUNE-RULE
- **Statement**: (i) Separation witnesses never inhabit uniformly ruled
  forms, so shrinking the final rule set preserves every separation —
  proved.  (ii) The delta-level corollary "a delta containing a
  uniform-rule item is never a minimum valid response" additionally needs
  the bridge that rule items commute out of a delta leaving the same
  regime with a smaller rule set — computational.
- **Class**: (i) theorem; (ii) bounded theorem (full-space computational
  check).
- **Deps**: none. **Assumptions**: shared (+ bounds for (ii)).
- **Python**: `test_rule_never_appears_in_minimum_responses` (full-space
  check on a mixed regime: every valid rule-bearing delta has a valid
  rule-free sub-delta).
- **Lean**: (i) `separable_of_subrules`; (ii) -- (bridge unresolved).
- **Axioms**: (i) none.
- **Falsifier / boundary**: a minimum valid response containing a rule.

### CL-PRUNE-STRUCTURAL
- **Statement**: In the cost-2 enumeration, unreferenced fresh data and
  unreferenced fresh forms never affect validity, and an instance-only
  delta changes the target pair's separability only if some instance
  mentions a target datum; the pruned enumeration therefore contains every
  minimum.  *Bounds: cost <= 2 deltas over the declared grammar slice.*
- **Class**: bounded theorem.
- **Deps**: none. **Assumptions**: shared + bounds.
- **Python**: `test_pruned_cost2_contains_every_valid_full_delta` (every
  valid excluded delta has a valid strict sub-delta), plus
  `test_new_datum_alone_never_separates`,
  `test_fast_equals_naive_on_full_space`.
- **Lean**: -- (unresolved).
- **Axioms**: --.
- **Falsifier / boundary**: a valid full-space delta absent from the
  pruned space with no valid sub-delta.  Boundary: certified
  computationally on bare, marked, and mixed base regimes; Lean proof
  outstanding.

### CL-PROGRESS
- **Statement**: On any well-formed regime whose imposed requirements are
  all separated, every *supplied* separation demand has a valid response
  (fresh unary form + one mark) that preserves every existing separation.
  Scope: response existence only — this claim does not assert autonomous
  demand generation and does not assert an unbounded tower.
- **Class**: theorem.
- **Deps**: none. **Assumptions**: shared.
- **Python**: engine assertion (no `terminal_no_response` node in any
  run); `test_min_responses_cost1_path` and tree runs.
- **Lean**: `mark_progress` (with `derivable_extend`,
  `getD_concat_self`, `getD_append_lt`).
- **Axioms**: `propext, Quot.sound`.
- **Falsifier / boundary**: a challenged accepted regime with no valid
  bounded response.

### CL-CLOSURE-POLICY
- **Statement**: No object-language endogenous demand generator was
  derived: a collapsed pair is not an active obstruction unless
  separation is required, and the requirement pattern originates
  externally.  What is declared instead is the *pair-separation closure
  policy*: reissue the admitted requirement pattern on collapsed pairs,
  one challenge branch per automorphism orbit — token-blind, no fresh
  data, no new goal kind, isomorphism-equivariant.
- **Class**: declared metatheory + finite computation (token-blindness
  and equivariance); the Lean model even lacks the vocabulary for glyph
  inspection (regimes carry no tokens).
- **Deps**: CL-2-COLLAPSED, CL-TRANSITION-EQUIVARIANCE.
  **Assumptions**: shared + the declared policy itself.
- **Python**: `closure_challenge_orbits`;
  `test_closure_policy_is_token_blind`, `test_closure_policy_fixpoint`.
- **Lean**: token-freeness by construction of `Regime`.
- **Axioms**: n/a.
- **Falsifier / boundary**: any dependence of the challenge orbits on
  token renaming or representative labeling.  Selection of this policy
  among conceivable ones is a declared-metatheory judgment.

### CL-CLOSURE-TERMINATION
- **Statement**: Pair-separation closure terminates: with the external
  policy disabled, every maximal branch ends at the all-pairs-separated
  fixpoint within n(n-1)/2 rounds (L: 1 round, 3 terminal branches, 0
  guard-cut, 0 round-cut, 0 open; F: 3 rounds, 16 terminal branches,
  0/0/0).  *Bounds: declared engine bounds; the counting laws are
  grammar-wide but conditional (see Lean field).*
- **Class**: bounded theorem.
- **Deps**: CL-CLOSURE-POLICY, CL-PROGRESS. **Assumptions**: shared +
  bounds.
- **Python**: `claims.json:CL-CLOSURE-TERMINATION` (branch reports over
  *all* maximal branches, `every_maximal_branch_terminates = true`,
  `within_bound = true`);
  `test_no_supply_variant_terminates_within_pair_bound`,
  `test_closed_system_terminal_at_round_boundary`.
- **Lean**: `index_le_strict_mono`, `strict_bounded_length`,
  `no_supply_round_bound`, `allPairs_length`.  Conditionality: these are
  abstract laws over strictly-growing bounded measures; that the engine's
  accepted separation rounds satisfy the hypotheses (exactly one new
  requirement per round, fixed datum count) is discharged computationally
  for the exported runs; a Lean theorem connecting the hypotheses to the
  transition system is unresolved.
- **Axioms**: `propext, Quot.sound`.
- **Falsifier / boundary**: a closed-system branch that is guard-cut,
  round-cut, open, or exceeds the pair bound.

### CL-CLOSURE-FIXPOINT
- **Statement**: Beyond the fixpoint the closure policy yields nothing:
  the requirement language of n data has exactly n(n-1)/2 elements, all
  exhausted at the fixpoint; any further requirement needs a fresh datum
  (external supply) or a new requirement kind (external goal).  Further
  continuation requires the declared external continuation policy.
- **Class**: theorem (language-size law) + declared metatheory (policy
  boundary).
- **Deps**: CL-CLOSURE-TERMINATION. **Assumptions**: shared + the
  admitted requirement language (separation over admitted data).
- **Python**: `test_closure_policy_fixpoint`.
- **Lean**: `allPairs_length`.
- **Axioms**: `propext, Quot.sound`.
- **Falsifier / boundary**: an admitted-structure-only challenge issuable
  at the fixpoint.

### CL-TRANSITION-EQUIVARIANCE
- **Statement**: The quotiented transition is well defined: expanding a
  regime by one challenge per automorphism orbit of collapsed pairs (all
  non-isomorphic challenge orbits retained) commutes with renaming — for
  every bijection, the renamed regime expands to exactly the same set of
  child isomorphism classes.  Raw least-pair selection violates this:
  on the regression regime (four data, one unary form, marks on data 2
  and 3, collapsed pairs (0,1) and (2,3), renaming (2,3,0,1)) the
  canonical keys agree while the same-index least-pair challenges produce
  non-isomorphic children.
- **Class**: finite computation — **finite adversarial evidence only**
  (exhaustive congruence over all renamings of the sample regimes,
  including the adversarially chosen regression) + counterexample
  (against the old policy).  The general transports — candidates, costs,
  validity, minima, and children under regime isomorphism — are
  **unresolved** as theorems; no general transport is claimed.
- **Deps**: CL-ISO-SOUND. **Assumptions**: shared.
- **Python**: `tests/test_equivariance.py` (regression, orbit
  distinctness, exhaustive congruence, orbit coverage);
  `claims.json:CL-TRANSITION-EQUIVARIANCE` (policy record and
  multi-orbit statistics: 0 in every exported run — the repaired defect
  was latent within the explored bounds); every merge edge in every
  export carries an explicitly verified isomorphism certificate
  (CL-REPLAY).
- **Lean**: -- (transport under isomorphism unresolved; see paper
  section 12).
- **Axioms**: --.
- **Falsifier / boundary**: a regime and bijection whose expansions
  yield different child class sets; boundary: the sampled regimes and
  their full symmetric groups.

### CL-BRANCH-REPORTS
- **Statement**: Per-tree branch evidence — terminal, guard-cutoff,
  round-cutoff, and open branch counts with the
  every-maximal-branch-terminates flag — as tabulated in paper
  section 8.3/8.4.
- **Class**: finite computation.
- **Deps**: CL-REPLAY. **Assumptions**: shared + bounds.
- **Python**: `claims.json:CL-BRANCH-REPORTS`;
  `test_run_main_produces_all_artifacts`.
- **Lean**: --. **Axioms**: --.
- **Falsifier / boundary**: recount from the exported trees.

### CL-TREE-MU2-COMPLETE
- **Statement**: The isomorphism-quotient trees under mu2 are fully
  enumerated to the requested 15 rounds with zero guard cutoff: 963
  nodes / 1022 edges (L), 1847 / 1960 (F); all leaves are round-cut.
  *Bounds: declared bounds; completeness is of the quotient tree within
  them.*
- **Class**: bounded theorem.
- **Deps**: CL-ISO-SOUND, CL-PRUNE-STRUCTURAL, CL-REPLAY.
- **Python**: `tree_L_mu2_summary.json` / `full/tree_L_mu2.json.gz` and
  the F analogues; stats in
  `claims.json:CL-TREE-SUMMARY`.
- **Lean**: --. **Axioms**: --.
- **Falsifier / boundary**: a reachable bounded node missing from the
  export.

### CL-TREE-MU1-FRONTIER
- **Statement**: The mu1 trees are guard-bounded at the 1200-node pre-expansion guard with exact
  exported frontiers: depth 7 with 927 frontier leaves (L), depth 6 with
  886 (F); enumeration is complete above the cut.
- **Class**: finite computation.
- **Deps**: as CL-TREE-MU2-COMPLETE.
- **Python**: `tree_L_mu1.json`, `tree_F_mu1.json`.
- **Lean**: --. **Axioms**: --.
- **Falsifier / boundary**: the frontier is the boundary, exported
  exactly for continuation.

### CL-REACHES-REQUESTED-DEPTH-WITH-EXTERNAL-SUPPLY
- **Statement**: With the external continuation policy, the process
  reaches the requested depth in the mu2 trees (15 of 15 rounds; mu1
  trees reach 7 / 6 before the pre-expansion node guard).  Reaching a
  finite requested
  depth is not a proof of unboundedness; no unboundedness claim is made,
  and the behavior beyond the exported depths is unresolved.
- **Class**: finite computation.
- **Deps**: CL-PROGRESS (response existence only). **Assumptions**:
  shared + bounds.
- **Python**:
  `claims.json:CL-REACHES-REQUESTED-DEPTH-WITH-EXTERNAL-SUPPLY`.
- **Lean**: supporting core — `mark_progress` (response existence for a
  supplied demand; not demand generation, not a tower).  **Axioms**:
  `propext, Quot.sound`.
- **Falsifier / boundary**: recount from exports; the boundary is the
  exported depth itself.

### CL-CLOSURE-VS-EXTERNAL
- **Statement**: Side-by-side comparison of the closed-system towers
  (4 / 20 nodes, all branches terminal) with the external-policy trees
  (963-1847 node complete mu2 quotients; 1200-node mu1 frontiers).
- **Class**: finite computation.
- **Deps**: CL-CLOSURE-TERMINATION, CL-TREE-MU2-COMPLETE.
- **Python**: `claims.json:CL-CLOSURE-VS-EXTERNAL`.
- **Lean**: --. **Axioms**: --.
- **Falsifier / boundary**: recount from exports.

### CL-ROLES
- **Statement**: The recurring transition roles that emerge are supply,
  discrimination (one instance), innovation (fresh form + instance), and
  rare double discrimination (6 edges, F mu2 only); the enumerated
  auxiliary-witness shape never appears among accepted minima in the
  observed runs.
- **Class**: finite computation.
- **Deps**: CL-TREE-MU2-COMPLETE, CL-TREE-MU1-FRONTIER.
- **Python**: role counts in `claims.json:CL-TREE-SUMMARY`;
  `test_role_classification_of_rare_response_shapes`.
- **Lean**: --. **Axioms**: --.
- **Falsifier / boundary**: bounded to the observed runs; deeper or
  wider bounds could surface the auxiliary-witness role.

### CL-TOKEN-ERASURE
- **Statement**: The Lean development is a token-erased abstraction of
  the token-aware admission semantics, connected by **two** proved
  components — never by duplicate-admission idempotence alone:
  (i) the erasure simulation: one token-aware step followed by erasure
  equals one erased step of the erased event (a duplicate datum
  admission erases to a bare supply, a proved no-op), and the same for
  whole histories; (ii) membership extensionality: Python's admitted
  collections are sets, Lean's are deduplicated lists, and under the
  proved relation `RegimeExt` every observable transports — derivability,
  context well-formedness, collapse, separability, item/delta
  application, response validity — so no exported claim depends on list
  order or representation.
- **Class**: theorem.
- **Deps**: CL-0-INERTIA (`supply_no_op` makes the duplicate case a
  no-op). **Assumptions**: shared.
- **Python**: set semantics of the admitted collections (frozensets in
  `model.py`); `test_admit_datum_dedups_on_presentation_identity`.
- **Lean**: `insertNew` (+ `mem_insertNew`, `insertNew_of_not_mem`,
  `insertNew_of_mem`), `erase_step`, `erase_replay` (with
  `replayT_cons`, `replayE_cons`) in `Derivation/Erasure.lean`;
  `derivable_ext`, `wfCtx_ext`, `collapsed_ext`, `separable_ext`,
  `applyItem_ext`, `applyDelta_ext`, `validResponse_ext` in
  `Derivation/Ext.lean`.
- **Axioms**: `propext, Quot.sound` (simulation); the extensionality
  family reports per-theorem in `artifacts/lean_axioms.txt`.
- **Falsifier / boundary**: a repeated admission of any event kind on
  which the two sides disagree; two membership-equal list
  representations supporting different claims; or a token-aware history
  whose erased replay differs from its replayed erasure.  Boundary:
  Python-side structures beyond events (token strings vs numbers) are
  related by the declared opaque-token reading.

### CL-REPLAY
- **Statement**: Every certified regime equals the replay of its recorded
  history from genesis; replay is compositional; tampering is detected.
  The normalized DAG exports certify **every edge**, not only one
  creation edge per node: a creation edge must replay from its parent to
  the exact stored child (hash equality), and a merge edge carries
  explicit datum/form bijections, computed and re-verified at attach
  time, that `verify_full_export` independently checks to map the
  replayed result exactly onto the stored child representative.  A single
  invalid merge edge is rejected even when every node retains a valid
  creation path.
- **Class**: theorem (compositionality) + finite computation
  (certification of all 5240 exported nodes and all 5498 exported edges,
  in-engine and again from the exports).
- **Deps**: none. **Assumptions**: shared.
- **Python**: `all_certified = true` in every tree;
  `test_replay_certify_and_tamper_detection`,
  `test_replay_from_base_composes`,
  `test_full_export_replays_and_verifies`,
  `test_verify_full_export_detects_tampering`,
  `test_every_edge_is_certified_including_merges`,
  `test_verify_rejects_invalid_merge_edge_despite_valid_creation_paths`;
  `test_run_main_produces_all_artifacts` verifies every exported tree.
- **Lean**: `replayE_append`, `historyL_replays`, `historyF_replays`.
- **Axioms**: `propext, Quot.sound`; `propext`; `propext`.
- **Falsifier / boundary**: a certified node whose history replays
  elsewhere, or an edge whose certificate fails independent re-checking.

### CL-QUOT-BARRIER
- **Statement**: If an abstraction identifies two cases, no operation
  defined only on the abstraction recovers the distinction: every function
  out of the quotient is constant on identified elements; instantiated at
  the Challenge 2 collapse.
- **Class**: theorem.
- **Deps**: CL-2-COLLAPSED. **Assumptions**: shared.
- **Python**: n/a (purely logical).
- **Lean**: `quotient_barrier`, `quot_barrier`, `barrier_R2L`.
- **Axioms**: `Quot.sound`.
- **Falsifier / boundary**: none within the model; recovering the
  distinction requires changing the abstraction (which is what
  Challenge 3 forces).

### CL-ISO-SOUND
- **Statement**: The implemented canonical form decides exactly the
  declared isomorphism relation: equality of refined canonical keys agrees
  with equality of brute-force keys, and the key is invariant under every
  bijection pair.  The automorphism search (used by the closure policy's
  orbit decomposition) enumerates within isomorphism-invariant color
  classes and is budget-guarded like canonicalization.  *Bounds: verified
  exhaustively on the Challenge 3 class representatives and mixed
  regimes; budget-guarded in general.*
- **Class**: finite computation.
- **Deps**: none. **Assumptions**: shared.
- **Python**: `test_agreement_with_bruteforce_on_pairs`,
  `test_canonical_invariant_under_rename`, `test_perm_budget_error`,
  `test_regression_orbits_are_distinct_and_both_retained`,
  `test_orbit_representatives_cover_all_collapsed_pairs`.
- **Lean**: -- (unresolved). **Axioms**: --.
- **Falsifier / boundary**: a pair of regimes on which refined and
  brute-force equality disagree, or an orbit decomposition that misses or
  double-counts a collapsed pair.

### CL-COUNT-INVARIANCE
- **Statement**: The unresolved-requirement count (collapsed pairs) is
  invariant under token renaming and index bijections.
- **Class**: finite computation (exhaustive over the Challenge 3 classes
  and mixed regimes); the general Lean transport is **unresolved**.
- **Deps**: CL-ISO-SOUND. **Assumptions**: shared.
- **Python**: canonical-invariance tests (the count is a component of the
  canonical key); `test_closure_policy_is_token_blind`.
- **Lean**: language-size law `allPairs_length` only.
- **Axioms**: `propext, Quot.sound`.
- **Falsifier / boundary**: a renaming changing the collapsed-pair count.

### CL-DETERMINISM
- **Statement**: The entire artifact set is byte-identical across
  independent runs on one platform; across platforms the JSON artifacts
  are byte-identical and the compressed full exports are
  content-identical and hash-pinned by the committed summaries.
- **Class**: finite computation.
- **Deps**: none. **Assumptions**: shared.
- **Python**: `test_run_main_is_deterministic`,
  `test_write_json_and_gz_are_deterministic`,
  `test_build_tree_small_deterministic_and_certified`;
  `ci/compare_artifacts.py` (regeneration gate, run locally and in CI).
- **Lean**: --. **Axioms**: --.
- **Falsifier / boundary**: any content difference across runs.

### CL-READING-UNDERDETERMINATION
- **Statement**: The challenge text underdetermines admission semantics;
  readings L and F both survive the full derivation and no internal fact
  separates them.
- **Class**: unresolved (deliberately retained branches; the Challenge 1
  sub-reading convergence is finite computation, CL-1-READING-CONVERGENCE).
- **Deps**: all Challenge results (computed for both readings).
- **Python**: every artifact is produced per reading.
- **Lean**: both `R2L` and `R2F` variants where formalized.
- **Axioms**: as per constituent claims.
- **Falsifier / boundary**: an internal criterion selecting a reading
  (none exists: the difference is a metatheoretic fact about the
  challenge text).

### CL-NO-UNIVERSAL-PROPERTY
- **Statement**: The final process is minimal or initial among a defined
  class of finite processes satisfying the same challenges.
- **Class**: unresolved — **claim refused**.  No universal property was
  proved; per the discipline, the word "minimal" for the whole process is
  therefore not used.
- **Deps**: n/a. **Python / Lean / Axioms**: --.
- **Falsifier / boundary**: what survives instead: per-stage minimality
  with declared scope (CL-3-*), engine determinism (CL-DETERMINISM), and
  bounded completeness (CL-TREE-MU2-COMPLETE).

---

## Frontier Run 006 claims (refusal, reflection, the remaining bridge)

Full statements, dependencies, and boundaries:
`paper/refusal_as_difference.md`; evidence:
`artifacts/refusal_frontier.json` and
`lean4/Derivation/RefusalFrontier.lean`.

### CL-FR6-TERMINAL
- **Statement**: split by target (per PR #7 verdict; supersedes the
  earlier single-line MULTIPLE_MINIMUM_BRIDGES, which conflated three
  bridge targets): FREE_REFUSAL_BRIDGE_FAILS (the free fragment reaches
  nothing); UNIQUE_MINIMUM_WITNESSED_BRIDGE_IN_CLASS (one minimum
  protocol — datum retention + relation rule, no tag, singleton
  algebra, one token — for witnessed_relation and
  witnessed_irreflexive, identical under both cost orders);
  MULTIPLE_MINIMUM_WEAKER_BRIDGES (three ties for two_carrier and two
  ties for separable/oriented pair under order A, with order B
  selecting different winners).  Irreflexivity as a law is not reached
  and remains separately declared.
- **Class**: bounded theorem (exhaustive in class) + theorem (cores).
- **Python**: `refusal_frontier.json` (minimum_table, normal_form).
- **Lean**: the CL-FR6-T* theorems, incl.
  `min_witnessed_route_closes`.  **Axioms**: within
  {propext, Quot.sound}.
- **Falsifier**: an in-class route with no listed purchase; a second
  minimum protocol at a witnessed milestone under either order; or a
  weaker-milestone tie eliminated under both orders.

### CL-FR6-T1-INERTIA
- **Statement**: horizon-free silent-refusal inertia under arbitrary
  repetition.  **Class**: theorem.
- **Lean**: `RefusalFrontier.silent_repetition_inert`.

### CL-FR6-T2-TRACE
- **Statement**: result streams never feed back; distinct histories
  erase to one object state.  **Class**: theorem.
- **Lean**: `trace_erasure`, `histories_collapse`.

### CL-FR6-T3-CONSTRUCTORS
- **Statement**: constructor-channel dependency (singleton algebras are
  monochrome, swap-invariant, collapsed); the search scopes the three
  import channels *by target* — constructors are required for
  result-outcome distinction, tags or relations for carrier-pair
  separability, relations for witnessed relations.  Result codes never
  enter carrier profiles; no target-independent interchangeability of
  the channels is claimed.
- **Class**: theorem + bounded computation.
- **Lean**: `singleton_algebra_monochrome`, `mono_code_swap_invariant`,
  `distinct_code_not_swap_invariant`,
  `distinction_needs_two_constructors`.
- **Python**: matrix cell `separable_pair -> two_result_constructors`
  refuted (tag-route countermodel); target-relative checks
  `separable_without_tag_or_relation`,
  `oriented_without_tag_or_relation`,
  `result_distinction_without_binary_algebra` all empty in class.

### CL-FR6-T4-CARRIER
- **Statement**: refusal-to-carrier per variant; judgment mode gives a
  second judgment, never a datum (horizon-free carrier bound).
- **Class**: theorem + bounded computation.
- **Lean**: `judgment_variant_second_judgment_not_datum`,
  `judgment_carrier_bound`.

### CL-FR6-T5-BRIDGE
- **Statement**: a sufficient non-minimum bridge closes (`stepP`:
  occurrence-style reification + tag + relation; no result store —
  witnessed, irreflexive-as-fact, oriented from one token in two
  presentations); and the unique minimum witnessed route (datum
  retention + relation rule only, on a state with no tag store and no
  result store) closes in Lean, matching the search's single minimum
  under both cost orders.  The tag/relation tie and the order
  disagreement live at the weaker milestones (separable/oriented pair),
  not at the witnessed milestones.
- **Class**: theorem + bounded computation (ties).
- **Lean**: `priced_bridge_closes`, `priced_bridge_oriented`,
  `min_witnessed_route_closes`.

### CL-FR6-T6-LAW
- **Statement**: bridge facts do not entail the irreflexivity law; in
  class every refusal link is born off-diagonal (receipts fresh).
- **Class**: theorem + bounded computation.
- **Lean**: `bridge_facts_not_law`.

### CL-FR6-T7-CEILING
- **Statement**: the invariance ceiling, general form: equivariant
  constructions fix outputs of symmetry-fixed states; tagged/relational
  refusal states bypass it by never being fixed points.
- **Class**: theorem (general lemma).
- **Lean**: `equivariant_output_invariant`; bypass
  `priced_bridge_oriented`.

### CL-FR6-T8-DYNAMICS
- **Statement**: reflective dynamics classified — fixpoint, two-cycle,
  horizon-free growth; the *declared* reflective semantics realizes a
  successor chain for every n (carrier `range (n+1)`, relation
  successor, every link irreflexive).  Realization by declaration, not
  derivation: `stepRefl` itself appends the current length and inserts
  the predecessor edge; refusal alone derives no numerals.  Initiality
  is open (F4).
- **Class**: theorem.
- **Lean**: `untyped_reflect_fixpoint`, `toggle_two_cycle`,
  `reflective_chain_growth`, `reflective_chain_is_initial_segment`,
  `reflective_chain_successor_relation`,
  `reflective_chain_irreflexive_facts`.

### CL-FR6-T9-PRICES
- **Statement**: minimum-price table under two cost orders with all
  ties, split by target: three tied purchases for two-ness under order
  A (order B selects occurrence); tag vs relation routes tied for
  separability under order A (order B selects the tag route); a unique,
  order-independent minimum (the relation route) for witnessed_relation
  and witnessed_irreflexive.  The order disagreement concerns the
  weaker milestones only.
- **Class**: finite computation (exhaustive in class).
- **Python**: `minimum_table`.

### CL-FR6-T10-NORMAL-FORM
- **Statement**: target-relative provenance dependencies, each checked
  exhaustively over the 44 protocols, claims matching checks
  one-for-one: every witnessed-irreflexive reacher makes a declared
  purchase (zero violations); witnessed relations require the relation
  rule; one-token carrier growth requires reification or occurrence
  retention; separable and oriented pairs require a tag or a relation;
  result-outcome distinction requires the binary algebra.
  `normal_form_holds_in_class` is the conjunction of exactly these
  checks.  The class-general Lean form is the named unresolved
  obligation.
- **Class**: bounded theorem (exhaustive in class).
- **Python**: `normal_form_check`.

## F5 claims (the composite generator)

Full statements, dependencies, and boundaries:
`paper/endogenous_generator.md`; evidence: `artifacts/generator.json`
and `lean4/Derivation/Generator.lean`.

### CL-G-TERMINAL
- **Statement**: split by claim — ENDOGENOUS_GENERATION_PROVED (the
  composite of reflective growth and pair-separation closure has a
  live obstruction at every round from the third on, horizon-free,
  with no per-round external act: the first horizon-free generator
  exhibited here, without a minimality or uniqueness claim);
  ENDOGENOUS_REPAIR_FAILS_IN_DECLARED_CLASS (over the five declared
  strategies and 15-round computation, the
  fires-repairs-never-imports class is empty);
  GENERATION_REPAIR_EXCLUSION_IN_CLASS (within those declared bounds,
  no strategy both fires, clears every firing round, and avoids
  recurring imports; valued marking prevents rather than repairs a
  fired demand).
- **Class**: theorem (generation; depth-1 strategy cores) + bounded
  computation (exclusion over the declared class; depth-2 leg
  instance-backed and bounded) + open conjecture (general depth-d,
  G2).
- **Lean**: `generation_never_dries` and the CL-G-* theorems below.
  **Axioms**: within {propext, Quot.sound}.
- **Python**: `generator.json` (trajectories, classification table,
  `endogenous_cycle_found: false`, Lean agreement checks).
- **Falsifier**: within the declared bound, a declared strategy
  classified `endogenous_cycle`; or a round ≥ 3 with no obstruction
  under the bare composite.

### CL-G-GENERATION
- **Statement**: for every chain length ≥ 3, elements 1 and 2 are
  distinct carrier elements with equal depth-1 profiles; the only
  event consumed is the internally enabled reflection.  **Class**:
  theorem (horizon-free).
- **Lean**: `generation_never_dries`; regime characterizations
  `reflective_chain_tags`, `chain_tagged_iff`, `chain_hasIn_iff`,
  `chain_hasOut_iff`.

### CL-G-OBSTRUCTIONS-EXACT
- **Statement**: at depth 1 the obstruction set of the bare chain is
  exactly the interior pairs — an iff, for distinct elements within
  the carrier; profile classes seed/interior/tip are pairwise
  distinct.  **Class**: theorem.
- **Lean**: `depth1_obstructions_are_exactly_middle_pairs`,
  `middle_profile`, `endpoint0_profile`, `endpointN_profile`.
- **Python**: agreement check over lengths 1..15.

### CL-G-REPAIR-FATES
- **Statement**: presence automark is vacuous (receipts are already
  tagged; the interior still collapses); every finite marking is
  outgrown, so per-pair repair recurs forever with a fresh import per
  repair; valued automark separates every pair and kills generation —
  its price is an unbounded observable alphabet (presentation identity
  made observable).  **Class**: theorem (each horizon-free).
- **Lean**: `automark_presence_vacuous`, `le_foldr_max`,
  `finite_marks_outrun`, `valued_marks_collapse_generation`.
- **Python**: bounded trajectories; per-pair imports at every firing
  round within the bound.

### CL-G-DEPTH2
- **Statement**: raising the regime to depth 2 separates the near-end
  pair (1, 3) at length 4 and is outrun by the deep-interior pair
  (2, 3) at length 5; within the 15-round bound the depth-2 branch
  fires unrepaired from length 5.  The general depth-d statement is
  open (G2).  **Class**: theorem (decidable instances) + bounded
  computation + open conjecture.
- **Lean**: `depth2_separates_near_ends_n4`, `depth2_obstruction_n5`.

### CL-G-DIRECT-SWAP
- **Statement**: directly transposing interior points 1 and 2 does not
  preserve the successor relation.  This distinguishes the example
  from the earlier branch where that swap is an admitted symmetry.
  It does not quantify over all automorphisms or prove full directed-
  chain rigidity.  **Class**: theorem plus explicit nonclaim.
- **Lean**: `middle_swap_not_relation_preserving`; contrast
  `equivariant_output_invariant`,
  `PrimDiff.symmetric_no_equivariant_classifier`.

### CL-G-EXCLUSION
- **Statement**: over the declared five-strategy class within the
  15-round bound, no strategy fires, repairs, and never imports
  (`endogenous_cycle_found: false`); classification per strategy:
  bare/presence/depth-2 fire unrepaired, per-pair repairs with
  recurring imports, valued is generation-dead.  Depth-1 fates are
  horizon-free theorems; the depth-2 fate is instance-backed and
  bounded.  **Class**: exhaustive finite computation over the declared
  class and bound + theorem cores.
- **Python**: `exclusion_check`.

### CL-G-OPEN
- **Statement**: G1 (no non-identity repair channel, class-general),
  G2 (general depth-d outrun; named single best next theorem target),
  G3 (repair-power = generation-poison as a conservation law), G4
  (the sealed engine as the import branch), F4 carried (chain
  initiality).  **Class**: open conjectures / carried obligations.

## Native primitive-difference interface claims

Full statements, boundaries, and the delivery table:
`paper/difference_interface.md`; evidence:
`lean4/Derivation/DiffInterface.lean` (core-only imports, 34 exported
theorems) and `artifacts/diff_interface.json`.  Externally imposed
challenge (caller request, 2026-08-12); the caller's independent
adapter is external evidence, assumed nowhere.

### CL-DI-EQUIVALENCE
- **Statement**: for every admitted difference observer
  (`δ : X → X → R`, `Zero : R → Prop` with the three laws),
  `ZeroRel x y := Zero (δ x y)` is an equivalence relation; the
  quotient realization is constructible only downstream of this proof
  (it consumes the `Setoid` built from it), and identifies exactly
  the zero-pairs in the sound direction.
- **Class**: theorem.  **Lean**: `zeroRel_equivalence`,
  `obsQuotient_eq_of_zero`; kernel observers inherit the laws from
  `kernelObs` once.

### CL-DI-OBSTRUCTION
- **Statement**: retained / observer-zero / protected are independent
  predicates; an active obstruction is exactly their conjunction;
  every proper subset is realized without the conjunction (blocking
  lemmas + the five countermodels).
- **Class**: definition + theorems.  **Lean**: `ActiveObstruction`,
  `no_guard_no_obstruction`, `unretained_not_active`,
  `distinguished_not_active`.

### CL-DI-REFLECTION
- **Statement**: a bare reflection step (embedding + retraction,
  genuinely fresh point, declared parent, old structure preserved on
  the live region, retained + protected parent/new pair, pre-closure
  zero) produces an active obstruction on a metatheoretically
  distinct pair.
- **Class**: theorem.  **Lean**: `BareReflection`,
  `bare_reflection_active_obstruction`; concrete instance
  `towerReflection`/`tower_obstruction`.

### CL-DI-CLOSURE
- **Statement**: demands are predicates (no ordering, no least
  representative anywhere); closure steps discharge orbit-complete
  demand sets by same-carrier, same-result-type refinement; every
  step preserves old distinctions, kills every demanded off-diagonal
  pair, and creates no new active obstruction; the concrete declared
  measure (count of retained, protected, observer-zero ordered pairs)
  strictly decreases (positive before, zero after).
- **Class**: theorem.  **Lean**: `OrbitComplete`, `ClosureStep`,
  `closure_preserves_old_distinctions`, `closure_kills_demanded`,
  `closure_adds_no_obstruction`, `mem_activePairs`,
  `closed_measure_zero`, `preclose_measure_pos`,
  `towerNext_decrease`.

### CL-DI-PROPOSAL
- **Statement**: when discharge needs new carrier or observer
  structure, the pipeline returns an `ExtensionProposal` — data
  carrying the request kind and the demanded set; no stage is ever
  constructed from a proposal in this package.  In the Boolean-view
  grammar over three protected points, every view and every
  same-grammar refinement leaves an active obstruction (pigeonhole),
  so closure must propose; checked exhaustively (8 views) in Python.
- **Class**: theorem (per-grammar) + exhaustive computation.
- **Lean**: `bool_view_pigeonhole`, `bool_grammar_obstruction`,
  `bool_grammar_must_propose`, `boolProposal`.

### CL-DI-TERMINATION
- **Statement**: with fuel exceeding the declared measure, the driver
  reaches `closed` or `proposal` (never out-of-fuel), given strict
  per-step decrease; instantiated for the tower with the fixed
  uniform orbit bound B = 2.  Without fuel, the tower is an infinite
  compatible trace: at every n, a bare reflection and an
  orbit-complete closure step whose application is definitionally the
  next closed stage; old distinctions persist to every later horizon.
- **Class**: theorem.  **Lean**: `drive_terminates`,
  `tower_fuel_terminates`, `tower_orbit_bound`,
  `tower_orbit_characterized`, `tower_infinite_trace`,
  `tower_step_composes`, `cview_distinct_mono`, `tower_closed`.

### CL-DI-COUNTERMODELS
- **Statement**: freshness, tagging, an edge, a new hash, and
  repetition each fail, alone, to produce observer-visible difference
  — and, unprotected, fail to produce an active obstruction.
- **Class**: countermodels (concrete finite instances).
- **Lean**: `cm_freshness`, `cm_tagging`, `cm_edge`, `cm_hash`,
  `cm_repetition`.  **Python**: countermodel table in the artifact.

### CL-DI-BOUNDARIES
- **Statement**: the package imports core Lean only and assumes
  nothing about downstream consumers; `zero_preserved`/`zero_pres`
  are live-region-scoped; the abstract termination theorem is
  conditional on the declared measure decrease; axioms of all 34
  exported theorems within {propext, Quot.sound}.
- **Class**: boundary record.  **Falsifier**: an import of any
  development module or external vocabulary into
  `DiffInterface.lean`; an exported theorem outside the axiom set.
