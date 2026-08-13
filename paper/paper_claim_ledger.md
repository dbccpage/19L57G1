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
`lean4/Derivation/DiffInterface.lean` (core-only imports, 35 exported
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
  fields; an active obstruction is exactly their conjunction.  The
  blocking lemmas prove that absence of any conjunct prevents activity.
  The five finite examples specifically exhibit feature-bearing,
  observer-zero pairs in unprotected stages; they do not enumerate every
  proper subset of the conjunction.
- **Class**: definition + theorems.  **Lean**: `ActiveObstruction`,
  `no_guard_no_obstruction`, `unretained_not_active`,
  `distinguished_not_active`.

### CL-DI-REFLECTION
- **Statement**: a bare reflection step (embedding + retraction,
  a point outside the old live image, declared parent, old structure preserved on
  the live region, retained + protected parent/new pair, pre-closure
  zero) certifies an active obstruction on a distinct pair.  The active
  conclusion uses the three declared pair fields and is not derived
  from freshness alone.
- **Class**: theorem.  **Lean**: `BareReflection`,
  `bare_reflection_certifies_active_obstruction`; concrete instance
  `towerReflection`/`tower_obstruction`.

### CL-DI-CLOSURE
- **Statement**: abstract demands are predicates, and closure selects no
  preferred pair; closure steps discharge map-saturated demand sets
  under declared structure-preserving maps, without assuming inverses
  or composition.  `demand_offdiag` makes every demand off-diagonal;
  every step preserves old distinctions, kills every demanded pair,
  and creates no new active obstruction.  The concrete declared
  measure (count of retained, protected, observer-zero ordered pairs)
  strictly decreases (positive before, zero after).
- **Class**: theorem.  **Lean**: `MapSaturated`, `StageMaps`, `ClosureStep`,
  `closure_preserves_old_distinctions`, `closure_kills_demanded`,
  `closure_adds_no_obstruction`, `mem_activePairs`,
  `closed_measure_zero`, `preclose_measure_pos`,
  `towerNext_decrease`.

### CL-DI-PROPOSAL
- **Statement**: when discharge needs new carrier or observer
  structure, `ExtensionProposal` represents request data carrying the
  request kind and demanded set; no stage is ever constructed from a
  proposal in this package.  In the Boolean-view grammar over three
  protected points, every replacement view leaves an active obstruction
  (pigeonhole), so no view in the grammar closes the stage; checked
  exhaustively (8 views) in Python.  `boolProposal` is separately
  available data; no decision theorem forces its selection.
- **Class**: theorem (no closed grammar view) + exhaustive computation;
  proposal selection unresolved.
- **Lean**: `bool_view_pigeonhole`, `bool_grammar_obstruction`,
  `no_bool_view_is_closed`, `boolProposal`.

### CL-DI-TERMINATION
- **Statement**: with fuel exceeding the declared measure, the driver
  reaches `closed` or `proposal` (never out-of-fuel), given strict
  per-step decrease and instantiated for the tower.  Separately, the
  concrete demand enumerator has fixed size 2.  At every `n`, a bare
  reflection and map-saturated closure step are available whose
  application is definitionally the next closed stage; this is a
  pointwise successor-step family, not a formal trace object or a
  finite-prefix induction theorem.  Old distinctions persist to every
  later horizon.
- **Class**: theorem.  **Lean**: `drive_terminates`,
  `tower_fuel_terminates`, `tower_demand_bound`,
  `tower_demand_characterized`, `tower_successor_step`,
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
  conditional on the declared measure decrease; axioms of all 35
  exported theorems within {propext, Quot.sound}.
- **Class**: boundary record.  **Falsifier**: an import of any
  development module or external vocabulary into
  `DiffInterface.lean`; an exported theorem outside the axiom set.

## Represented-progress claims (the kernel without an outside)

Full statements and the exact ceiling:
`paper/represented_progress.md`; evidence:
`lean4/Derivation/Represented.lean` (native, core-only, 48 exported
theorems) and `artifacts/represented.json`.  Externally imposed
challenge (caller assignment, 2026-08-12).

### CL-RP-TERMINAL
- **Statement**: scoped to a fixed kernel constitution.  The
  constitution — event grammar, sep/sat laws, response menu,
  acceptance predicates, history producer — is fixed metatheory.
  Relative to that fixed `step` semantics:
  REPRESENTED_KERNEL_EXISTS (every *runtime* input — evaluator,
  requirement, scheduler, tie-break, fresh-name source, fuel,
  authorization, stopping condition — occurs in the represented state
  or history, and the eight target theorems hold in their declared
  scopes); HIDDEN_INPUT_CLASSES_REFUTED (four hidden-runtime-input
  countermodels, plus four neighboring semantic/inference failures,
  split and machine-checked);
  CERTIFICATION_BOUNDED_BY_PANEL_QUOTIENT (internal certification is
  exactly the panel's joint quotient, never correspondence).  The
  constitution does not derive itself.
- **Class**: theorem (kernel-scoped) + countermodels + bounded
  computation.  **Axioms**: within {propext, Quot.sound}.
- **Falsifier**: a runtime input changing a kernel result without
  occurring in `supp`/history; a countermodel failing its exhibited
  divergence; a certified claim exceeding the panel's joint separation
  power.

### CL-RP-DEFINITIONS
- **Statement**: the ten required notions defined natively —
  representation (`World`), admitted transformation (guarded `step`),
  history/replay, recorded requirement, obstruction (recorded
  requirement + exhaustive menu failure, never lookalikeness),
  same-structure repair, structure-creating augmentation, represented
  support (`supp`), internally determined successor family
  (`repairFamily`, all ties kept), replay-equivalence (`WEquiv`).
- **Class**: definition.

### CL-RP-REPLAY
- **Statement**: replay determinism (definitional for the kernel — the
  step type admits no unrepresented argument) and composition
  (`replay_append`).  **Class**: theorem.
- **Lean**: `replay_deterministic`, `replay_nil`, `replay_append`.

### CL-RP-SUPPORT
- **Statement**: operational-support factorization — the step factors
  through the `supp` projection: support-agreeing worlds have
  support-equal successors for every event; contrapositively, runs
  whose successor supports differ already differ in represented
  support.  A factorization theorem, not a claim of per-datum result
  causation.  The inert notes field is provably inert.
- **Class**: theorem.
- **Lean**: `support_determines`, `internal_support`, `notes_inert`.

### CL-RP-NO-HIDDEN-CHOICE
- **Statement**: scoped to `repairFamily` — the same-structure
  successor family is the complete set of accepted responses with all
  ties retained (sound + complete filter, no selector);
  replay-equivalent worlds step to replay-equivalent worlds with
  membership-identical successor families.  The progress theorem's
  structural branch exhibits the canonical augmentation `[i]`, whose
  orientation is supplied by the ordered, recorded requirement — a
  represented datum and a stated scoping; augmentation candidates are
  not gathered into a retained family, and this claim does not extend
  to them.  **Class**: theorem (scoped).
- **Lean**: `repairFamily_sound`, `repairFamily_complete`,
  `repairFamily_retains_ties`, `equiv_step`, `equiv_replay`,
  `equiv_repairFamily`.

### CL-RP-REPAIR-AUG
- **Statement**: accepted repairs discharge a recorded violation and
  preserve every previously satisfied requirement; accepted
  augmentations satisfy the exact positive-satisfaction delta equation
  (`satB_aug`) and preserve every satisfied positive requirement
  (`aug_preserves_satisfied`) while verifiably adding expressive
  capacity.  Old *non-separation* judgments are not preserved —
  changing them is the licensed content of augmentation; the earlier
  word "conservativity" is withdrawn as an overclaim.
- **Class**: theorem.
- **Lean**: `mark_discharges`, `mark_preserves`, `step_mark_sound`,
  `satB_aug`, `aug_preserves_satisfied`, `aug_increases`.

### CL-RP-PROGRESS
- **Statement**: under replay well-formedness (an invariant) and a
  recorded violation, the repair family is non-empty or the violation
  is a certified obstruction whose canonical singleton augmentation is
  accepted and discharges it; the isolated remaining hypotheses are
  the represented budget and license.  Refusal records verified
  same-level exhaustion and is non-absorbing: it certifies, it does
  not terminalize; ending a bounded run belongs to the metatheoretic
  history producer, and no terminalization-in-refusal is claimed.
- **Class**: theorem.
- **Lean**: `represented_progress`, `wf_genesis`, `wf_step`,
  `wf_replay`, `progress_needs_budget`, `progress_needs_license`,
  `refusal_needs_certificate`, `refusals_are_represented`.
- **Python**: the pigeonhole story (violation → empty family →
  obstruction certificate → accepted augmentation → discharge →
  quiescence).

### CL-RP-CLOSURE
- **Statement**: new violations arise only from represented `require`
  events; quiescent worlds stay quiescent under every non-`require`
  event.  **Class**: theorem.
- **Lean**: `violation_only_from_require`, `quiescent_stable`.

### CL-RP-PRODUCTIVITY
- **Statement**: one prefix-compatible unbounded run under an
  *explicitly supplied* event stream (the history producer is
  metatheory, never called endogenous), with carrier literally
  `range (k+1)` reached through the acceptance-guarded kernel;
  per-event acceptance and per-stage quiescence verified exhaustively
  to the 15-round bound (Python) with a Lean quiescence instance at
  k = 3; productivity is separated by proof from per-length witnessing
  (the represented König failure: witnesses at every length, no
  compatible infinite source).  **Class**: theorem + finite
  computation.
- **Lean**: `histUpTo_prefix`, `admit_data_fresh` (spelled
  `admitTok`), `worldAt_data`, `worldAt_growth`, `productive_run`,
  `worldAt_three_quiescent`, `wit_all_lengths`, `wit_no_infinite`.

### CL-RP-CERTIFICATION
- **Statement**: internal certification by represented evaluators is
  exactly joint separation by the panel's own columns; it is not
  correspondence (a unanimous panel certifies an equivalence an
  outside column refutes) and not monotone under panel extension.
  Classification: the panel is an explicit certification argument —
  represented data by type but not carried in `World` or admitted by
  events; certification is not replay-integrated in this kernel.
- **Class**: theorem + countermodels.
- **Lean**: `cert_scope`, `cert_not_correspondence`,
  `cert_panel_relative`.

### CL-RP-COUNTERMODELS
- **Statement**: eight minimal machine-checked witnesses, split by
  class.  Hidden runtime inputs (an input in neither state nor
  history): unrecorded scheduler, unrecorded fresh-name source, hidden
  evaluator, order-sensitive tie-break.  Neighboring
  semantic/inference failures (no hidden input; a wrong definition or
  reading): incomplete search (false obstruction), destructive rewrite
  (vs append-only augmentation), repetition-as-progress, per-length
  witnesses without a compatible infinite history.
- **Class**: countermodels.
- **Lean**: `scheduler_hidden`, `gensym_hidden`, `oracle_hidden`,
  `incomplete_search_false_alarm`,
  `augmentation_destroys_old_replay`, `repetition_not_progress`,
  `order_sensitivity_splits_equivalents`.
- **Python**: countermodel table; mutation tests (every single-event
  mutation of the story history changes the replay).

### CL-RP-CEILING
- **Statement**: representability of runtime inputs is proved relative
  to the fixed constitution (which does not derive itself); uniqueness
  is not proved (policies are represented choices); progress is
  conditional on represented budget/license, with refusal
  non-absorbing; certification never exceeds the panel quotient and is
  not replay-integrated; admission order is semantic (occurrence
  identity) while view/requirement/refusal order is provably not; the
  carrier is the naturals in both formalisms (negative inputs rejected
  in the mirror, matching Lean's `Nat` exactly); the two standing
  rules are proved consistent and sufficient for this kernel within
  bounds — their general forms remain conjectures.
- **Class**: boundary record + conjecture (general forms).

## Ultra-closure claims (the completed native derivation)

Full statements: `paper/native_derivation_completion.md`; bridge
table: `paper/native_derivation_map.md`; machine evidence: the five
`completion_*.json` artifacts; Lean:
`Completion/NoOutside/Constitution/Initiality` (57 new exported
theorems; 291 total, all within {propext, Quot.sound}).

### CL-NC-TERMINALS
- **Statement**: RELATIVE_REPLAY_CLOSURE_ONLY;
  EVENT_SOURCE_INTERNALIZED_RELATIVE_TO_FIXED_INTERPRETER;
  KERNEL_CONSTITUTION_INTERNALIZED_RELATIVE_TO_FIXED_INTERPRETER;
  KERNEL_CONSTITUTION_REMAINS_META (outermost layer — the single OPEN
  edge in the declared graph, which does not claim to exhaust every
  possible bridge);
  UNIQUE_PROBE_COMPLIANT_DESCRIPTOR_IN_DECLARED_TOGGLE_CLASS;
  ABSOLUTE_NO_OUTSIDE_UNFORMULABLE.  FULL_NATIVE_COMPOSITION is not
  claimed; categorical initiality is not claimed.
- **Class**: theorem (relative closures) + boundary record (the OPEN
  bridge and the unformulable absolute).
- **Falsifier**: a represented member of the constitution family that
  executes its own family interpreter; a kernel result changed by an
  input outside represented support/history/constitution; a second
  compliant member of the declared class.

### CL-NC-COMMON-STATE
- **Statement**: one common native state carries the do-not-erase
  distinctions as separate fields, with retention, protection, and
  observer-zero as three independent obstruction conditions
  (`obstC_conditions_independent`; the kernel transport instantiates
  retention and protection from one store — a stated identification);
  the kernel, the reflective chain, the two-element difference
  objects, and the early collapse checkpoint transport with
  preservation theorems; S2 symmetry is scoped to the relation store
  (`s2_state_not_swap_invariant` for the whole-state boundary);
  witness does not transport to separation, separation does not
  transport to witness, and metatheoretic inequality is operationally
  inert.
- **Class**: definition + theorem + countermodels.
- **Lean**: `ofWorld_sep`, `ofWorld_obstruction`, `ofWorld_quiescent`,
  `obstC_conditions_independent`, `chain_transport`,
  `d2_transport_oriented`, `s2_transport_symmetric`,
  `s2_state_not_swap_invariant`, `witness_not_separation`,
  `separation_not_witness`, `meta_distinctness_inert`,
  `early_collapse_transports`.

### CL-NC-RULE1
- **Statement**: Rule 1's strongest forms — the operational
  dichotomy (repair family versus exhaustion-plus-extension family)
  with tie-retained extension family (both orientations proved
  accepted); refusal a parallel, non-absorbing record, proved
  object-inert and outside the binary action algebra
  (preserve-presentation / change-presentation, by the signature
  measure); budget/license execution a separate represented gate; the
  fidelity reduction (no protected requirement, no obstruction); the
  retraction countermodel bounding the preservation law to what the
  acceptance guard buys.  Classification: derived for the fixed
  kernel, fidelity-relative in general, primitive nowhere.
- **Class**: conditional theorem + countermodels.
- **Lean**: `rule1_repair_or_extension`, `augFamily_retains_ties`,
  `refusal_recordable`, `refusal_object_inert`,
  `refusal_non_absorbing`, `action_dichotomy`, `rule1_needs_fidelity`,
  `retraction_breaks_preservation`.

### CL-NC-RULE2
- **Statement**: Rule 2's strongest forms — support factorization
  extended to histories, successor families, certificates, and
  verdicts; the effectual-outside dichotomy (operational,
  constitution-relative; the absolute form is unformulable in this
  calculus); the family-valued invariance ceiling; the certification
  panel replay-integrated by a conservative extension, with
  panel-induced non-separation proved an equivalence and the
  certificate proved equal to joint-quotient membership.
- **Class**: theorem + boundary record.
- **Lean**: `support_replay`, `support_repairFamily`,
  `support_obstructed`, `support_quiescent`,
  `effectual_outside_dichotomy`, `equivariant_family_invariant`,
  `stepC_conservative`, `admitEvaluator_base_inert`, `panel_equiv`,
  `certNeg_iff_panelEquiv`, `certC_ceiling`.

### CL-NC-EVENT-SOURCE
- **Statement**: the event source is internalized relative to the
  fixed interpreter, under metatheoretic iteration: the policy is
  represented data; the generator invokes the next-family interpreter
  on the replayed state and appends the unique family member
  (state-derived, prefix-compatible generation — no internal-trigger
  claim: no represented transition invokes the interpreter); the
  interpreter emits complete tied families (singleton for the tower —
  proved; both augmentation orientations for closure); fresh names
  are canonical numerals, fresh on the tower invariant
  (`freshName_fresh_on_tower`) and not in general
  (`freshName_not_fresh_generally`) — a recorded arithmetic/ordering
  import; budget replenishment is an emitted represented event; the
  stop outcome is the represented empty family; and the generator
  reproduces the previously supplied tower stream exactly
  (`driver_reproduces_tower`).
- **Class**: theorem (relative) + declared policy (the generation
  policy itself).
- **Lean**: `nextFamily_tower_singleton`,
  `closeBlocks_complete_repair`, `closeBlocks_complete_aug`,
  `nextFamily_stop`, `towerBlock_eq`, `driver_reproduces_tower`,
  `nextFamily_complete`, `budget_replenishment_represented`,
  `gen_growth`, `gen_three_quiescent`.
- **Python**: `completion_protocols.json` (reproduction and
  acceptance exhaustive to the 15-round bound).

### CL-NC-AUTONOMY
- **Statement**: autonomy separated from iterability by the
  nine-level ladder, assessed for the tower generation: levels 1-3
  and 5-9 proved (steps, prefix compatibility, interpreter-computed
  families, selection-freeness, represented replenishment, lawfulness
  across extension, explicit productivity); level 4 (internal
  trigger) explicitly NOT attained — the iteration is metatheoretic.
  Arbitrary iterability is levels 1-2 only.  Level 8 (lawfulness) is
  carried by the Horizon module at every stage, not only at stage 3:
  the generated world's complete record is characterized by induction
  (`worldAt_spec`), quiescence and well-formedness hold at every
  horizon (`gen_quiescent`, `gen_wf`), and every emitted event of
  every block is accepted (`block_all_accepted`,
  `genesis_accepted`).  PR #12 correction C6: the prior version of
  this entry cited `tower_driver_autonomy` alone for "lawfulness
  across extension", but that theorem has no lawfulness conjunct —
  the only Lean lawfulness fact was the stage-3 instance
  `gen_three_quiescent`.  The gap is closed upward, not rescoped.
- **Class**: theorem (relative).
- **Lean**: `tower_driver_autonomy`, `Horizon.worldAt_spec`,
  `Horizon.gen_quiescent`, `Horizon.gen_wf`,
  `Horizon.block_all_accepted`, `Horizon.genesis_accepted`.

### CL-NC-CONSTITUTION
- **Statement**: the kernel constitution is represented as data
  within a completely enumerated 64-member family; the fixed family
  interpreter executes any description; the kernel's own description
  executes to exactly the sealed step (verified self-description).
  Quotation, executable description, and verified self-description
  are distinct definitions.  The outermost interpretation relation
  remains metatheoretic — the named irreducible obligation and the
  graph's single OPEN bridge.
- **Class**: theorem (family-relative) + OPEN (absolute).
- **Lean**: `interp_describe`, `allDescs_length`, `allDescs_complete`.

### CL-NC-INITIALITY
- **Statement**: in the declared 64-member class under the declared
  probe battery: every guard is load-bearing (six concrete
  separations); the sealed kernel's description is the unique
  probe-compliant member; both declared cost orders agree on the
  singleton; and the panel extension retracts onto the kernel (split
  retract).  Categorical initiality is NOT claimed — a six-probe
  singleton and one split retract do not establish it.  Scope:
  class-relative; "most primitive engine" is underdetermined as an
  absolute claim and proved as this class-relative one.
- **Class**: theorem (class-scoped) + bounded computation (the
  64-member compliance table).
- **Lean**: `dedup_load_bearing`, `require_guard_load_bearing`,
  `accept_guard_load_bearing`, `budget_gate_load_bearing`,
  `license_gate_load_bearing`, `refusal_certificate_load_bearing`,
  `unique_compliant`, `minimum_unique_in_class`, `extension_retract`,
  `extension_retract_replay`, `retract_section`.
- **Python**: `completion_minimality.json`.

### CL-NC-INVENTORY
- **Statement**: the theorem inventory is source-derived (names and
  axiom sets from the axiom artifact; statements extracted from
  sources; consumers and citing claims by search) and pinned by test
  to exactly the exported estate; the dependency graph classifies all
  thirty bridges with resolving evidence; exactly one bridge is OPEN.
- **Class**: finite computation + declared metadata (kind/role
  labels).
- **Python**: `completion_dependency_graph.json`,
  `completion_countermodels.json`, `completion_receipt.json`.


## PR #12 — Primitive Difference contact and passage

### CL-PD2-HORIZON
- **Statement**: the generated run's complete record is characterized
  at every stage by induction; quiescence, well-formedness, and
  per-event acceptance hold at every horizon; the family
  interpreter's budget semantics is pinned as a trichotomy (unchanged
  / saturating decrement / explicit set) for every descriptor and
  event, and the Python mirror implements exactly that semantics.
- **Class**: theorem (horizon-free) + refuted-and-repaired prior
  claim (see change log, PR #12 Phase I).
- **Lean**: `Horizon.worldAt_spec`, `Horizon.worldAt_quiescent`,
  `Horizon.worldAt_wf`, `Horizon.block_all_accepted`,
  `Horizon.genesis_accepted`, `Horizon.gen_quiescent`,
  `Horizon.gen_wf`, `Horizon.interp_budget_bound`,
  `Horizon.budget_saturation_noop`,
  `Horizon.mark_saturation_all_descs`.
- **Python**: `test_budget_saturation_matches_lean_nat`,
  `test_budget_trichotomy_every_descriptor_event`.

### CL-PD2-MATRIX
- **Statement**: nine candidate readings of primitive difference over
  one signature; all 72 ordered implication cells settled: 17
  implications proved, 51 finite countermodels compiled (minimum
  carrier proved where cited), 4
  located cells OPEN with exact metatheoretic scope (every decidable
  relation is located; no internal countermodel can exist).
  Cotransitivity is automatic on the two-element carrier, making the
  three-element countermodels minimum-carrier.
- **Class**: theorem + countermodel + OPEN (scoped), cross-verified
  by exhaustive finite computation.
- **Lean**: `PrimitiveCore.matrixCells`, the 68 `imp_*`/`nimp_*`
  theorems, `PrimitiveCore.cotrans_auto_on_two`,
  `PrimitiveCore.located_of_decidable`, `PrimitiveCore.D_iff_ne`,
  `PrimitiveCore.e_empty_iff_d`.
- **Python**: `primitive_candidates.json`,
  `primitive_implication_matrix.json` (expected_equals_computed).

### CL-PD2-INITIALITY
- **Statement**: the oriented two-element realization is initial in
  the category of ALL pointed witnessed relations (true universal
  property, category laws proved).  Scope (review pass): `PtdRel`
  carries no irreflexivity, so this initiality characterizes the
  bare-witness reading W — the free pointed object on one witnessed
  arrow — and restricts to the irreflexive subcategory
  (`d2_initial_irrefl`); initiality does not itself select
  irreflexivity, whose independent justification is `imp_a_d`
  against `nimp_w_d`.  The symmetric realization is initial exactly
  in the symmetric subcategory and not weakly initial in the full
  one; initiality is unique up to isomorphism only, distinct from
  presentation identity and from minimum cardinality; pointed
  automorphisms are trivial for both realizations — orientation
  lives in the pointing.
- **Class**: theorem.
- **Lean**: `PrimitiveCats.d2_initial`,
  `PrimitiveCats.d2_initial_irrefl`, `PrimitiveCats.s2_initial_sym`,
  `PrimitiveCats.s2_not_weakly_initial`, `PrimitiveCats.initials_iso`,
  `PrimitiveCats.two_initials_not_identical`,
  `PrimitiveCats.larger_not_initial`, `PrimitiveCats.pointed_rigid`.

### CL-PD2-BRANCHING
- **Statement**: the faithful-presentation category of a
  three-occurrence source has no weakly terminal object: the maximal
  observer cuts are incomparable and both retained.  On the two-point
  source the cut-branching vanishes but unrestricted terminality
  fails anyway, constructively (`no_terminal_pres2`, review-pass
  closure of the former OPEN cell: the free-point presentation gives
  every target two distinct commuting maps); the positive fragment
  is uniqueness against surjective presentations (no classical
  choice used).  Cut census on carriers 2-5: 1, 2, 4, 8.
- **Class**: theorem + OPEN (scoped) + finite computation.
- **Lean**: `PrimitiveCats.no_terminal_pres`,
  `PrimitiveCats.no_phom_mergeA_mergeB`,
  `PrimitiveCats.no_terminal_pres2`,
  `PrimitiveCats.phom2_unique_of_epi`;
  `HigherStructure.cut_census_growth`.

### CL-PD2-APARTNESS
- **Statement**: positive apartness (irreflexive, symmetric,
  cotransitive) makes indistinguishability an equivalence, with each
  law spent at exactly one clause; omissions are refuted by minimal
  finite countermodels (carriers 1, 2, 3; minimality proved).  Both
  orientations of the two-point relation generate the same apartness
  and the same indistinguishability while remaining distinct data;
  the oriented-witness preservers are exactly the identity, the
  apartness preservers exactly the identity and the swap, constants
  preserve neither; the closure of any admitted family preserves the
  oriented witness iff every generator does.
- **Class**: theorem + countermodel, exhaustively mirrored to
  carrier 3 with preservation censuses to carrier 4.
- **Lean**: `Apartness.indist_equivalence`,
  `Apartness.bare_breaks_refl`, `Apartness.irrefl_alone_breaks_symm`,
  `Apartness.subsingleton_indist_total`,
  `Apartness.symm_without_cotrans_breaks_trans`,
  `Apartness.two_point_indist_trans`, `Apartness.s2_isApart`,
  `Apartness.orientations_same_apartness`,
  `Apartness.orientations_differ`,
  `Apartness.oriented_preserver_unique`,
  `Apartness.apart_preserver_pair`, `Apartness.clos_oriented_iff`,
  `Apartness.oriented_family_trivial`.
- **Python**: `apartness.json`.

### CL-PD2-CONTACT
- **Statement**: the declared contact package is absent at
  blind-native-base and at completion; the contact phases terminate
  CONTACT_INPUT_ABSENT; no contents invented; the native kernel
  interface any future contact must meet is committed (kernel
  binding, universal status, orientation fork, branching, matrix).
- **Class**: declared protocol outcome + runtime check.
- **Lean**: `PrimitiveContact.native_kernel_initial`.
- **Python**: `primitive_contact.json`.

### CL-PD2-PASSAGE
- **Statement**: each of the thirteen arrows of the passage chain
  has exactly one status with executable evidence.  Review-pass
  composition repair: the passage now carries a separate ASSERTED
  store — `assertWit` supplies the positive witness, `admitWit`
  retains an asserted difference — so a pre-retention Primitive
  Difference state exists (`assertion_not_retained`), retention
  demonstrably requires assertion (`retention_requires_assertion`),
  and candidate A transports into the passage as a theorem
  (`assert_transport` on every replayed state via the off-diagonal
  invariant `asserted_offdiag`; canonical instance
  `kernel_enters_preretained`).  Active obstruction is a
  four-condition conjunction (retained, protected, observation
  DECLARED, observer-zero) with every maximal proper subset refuted;
  primitive difference precedes observation as a theorem; ZeroRel is
  an equivalence before quotienting; THE TWO-RULE THEOREM, exactly
  scoped: under the DECLARED singleton-column extension universe
  (which contains a separator for every well-formed pair — the
  obstruction identifies one, it does not manufacture the
  constructor) and the declared same-level menu, an active
  obstruction with an in-bounds protected pair has a nonempty repair
  family or certified exhaustion plus a nonempty extension family;
  `setBudget 1` in emitted blocks is a declared self-funding policy;
  refusal is an inert record, the terminal absorbs, proposal is not
  execution; the represented next-family has
  stop/nonempty/completeness theorems and its iteration remains
  metatheoretic (stated).
- **Class**: theorem (+ declarations priced as admission events with
  countermodels).
- **Lean**: `PrimitivePassage.assert_transport`,
  `PrimitivePassage.kernel_enters_preretained`,
  `PrimitivePassage.assertion_not_retained`,
  `PrimitivePassage.retention_requires_assertion`,
  `PrimitivePassage.asserted_offdiag`,
  `PrimitivePassage.retained_sub_asserted`,
  `PrimitivePassage.obst_requires_observation`,
  `PrimitivePassage.obst_conditions_independent`,
  `PrimitivePassage.zero_refl`, `PrimitivePassage.zero_symm`,
  `PrimitivePassage.zero_trans`, `PrimitivePassage.menu_complete`,
  `PrimitivePassage.extension_always_available`,
  `PrimitivePassage.two_rule`,
  `PrimitivePassage.proposal_not_execution`,
  `PrimitivePassage.budget_gates_execution`,
  `PrimitivePassage.refusal_object_inert`,
  `PrimitivePassage.terminal_absorbing`,
  `PrimitivePassage.extension_resolves`,
  `PrimitivePassage.nextFamilyP_stop`,
  `PrimitivePassage.nextFamilyP_nonempty`.
- **Python**: `primitive_passage.json` (arrows + growth reports).

### CL-PD2-GROWTH
- **Statement**: the growth driver iterates the passage; the grown
  state at every stage is exactly the path graph with per-edge
  protection and one observation column per resolved obstruction
  (characterized by induction); each round's obstruction, nonempty
  response family, resolution, and creation record are theorems;
  quiescence is restored after every round; the connectivity residue
  is 1 at every stage (the path form itself is `graphAt_spec`; the
  residue alone proves neither connectedness nor acyclicity).
  Provenance, exact: the DRIVER supplies the graph data (occurrence,
  assertion, retention, protection); the OBSTRUCTION creates the
  observation column that resolves it.
- **Class**: theorem (horizon-free), mirrored to 15 rounds.
- **Lean**: `HigherStructure.graphAt_spec`,
  `HigherStructure.round_obstruction`,
  `HigherStructure.round_two_rule`,
  `HigherStructure.round_resolution`,
  `HigherStructure.round_creation_record`,
  `HigherStructure.graph_growth`,
  `HigherStructure.graphAt_quiescent`,
  `HigherStructure.path_connectivity_residue`.

### CL-PD2-LADDER
- **Statement**: the declared cell calculus admits a k+1-cell exactly
  over a complete unfilled boundary of k-cells — the shell guards
  `shell1/2/3` (complete boundaries, deliberately NOT simplicial
  horns, which omit a face).  The ladder recurrence — the two-rule
  shape one dimension up — is PROVED at dimensions 2 and 3
  (`ladder_dim2`, `ladder_dim3`); recurrence at every dimension is a
  frontier conjecture.  Shell guards are load-bearing and the shell
  does not fill itself (higher structure admitted, never forced);
  the four-occurrence demonstration grows 0-, 1-, 2-, 3-simplices in
  replayable creation order with the 1-skeleton equal to the passage
  witness store; the alternating cell-count statistic runs 4, -2, 2,
  1 along the stages (a statistic, not an invariant); with declared
  integer coefficients and boundaries the composite boundary
  vanishes on every demonstration cell, and two distinct conventions
  both work — the convention is declared content.
- **Class**: theorem + finite computation; non-forcing by
  countermodel.
- **Lean**: `HigherStructure.ladder_dim2`,
  `HigherStructure.ladder_dim3`,
  `HigherStructure.shell_guard_load_bearing`,
  `HigherStructure.filling_not_forced`, `HigherStructure.k4_builds`,
  `HigherStructure.k4_skeleton_agrees`,
  `HigherStructure.altNum_stages`,
  `HigherStructure.d2_zero_triangles`, `HigherStructure.d2_zero_tet`,
  `HigherStructure.boundary_not_forced`.

### CL-PD2-CONTROLLER
- **Statement**: in the declared 1024-member variable-event-grammar
  class, response-liveness is exactly the two-rule support (all 128
  live members execute the resolution at the certified obstruction;
  each response kind load-bearing by countermodel); the live family
  is essentially non-unique (full vs no-refuse agree on every
  refusal-free event, differ at a certified obstruction) — the sealed
  six-toggle uniqueness is class-relative; the simulation category
  has proved laws, every ordered pair is connected by constant
  simulations, and initiality is refuted everywhere (including the
  live subcategory); the strict refinement excludes constants yet
  global uniqueness still fails by an invariant-twist countermodel;
  uniqueness holds exactly on the genesis-reachable orbit.
- **Class**: theorem + countermodel + finite computation.
- **Lean**: `ControllerCategory.allKinds_complete`,
  `ControllerCategory.interpK_full`,
  `ControllerCategory.live_census`,
  `ControllerCategory.tworule_executable_of_live`,
  `ControllerCategory.dead_without_addcol`,
  `ControllerCategory.dead_without_budget`,
  `ControllerCategory.dead_without_refine`,
  `ControllerCategory.nonrefuse_agree`,
  `ControllerCategory.refuse_distinguishes`,
  `ControllerCategory.erase_sim`,
  `ControllerCategory.every_pair_connected`,
  `ControllerCategory.no_initial_ctrl`,
  `ControllerCategory.no_initial_live_ctrl`,
  `ControllerCategory.const_not_strict`,
  `ControllerCategory.strict_not_unique`,
  `ControllerCategory.strict_agree_on_reachable`.
- **Python**: `primitive_controller_category.json`.

### CL-PD2-INTERPRETER
- **Statement** (review-pass scope): every finite code list under
  any evaluation map is missed by a same-type function — FINITE
  extensional incompleteness, via a diagonal that differs only at
  the operationally inert notes field; NOT a self-interpretation
  impossibility, NOT "the evaluator cannot be coded", NOT a semantic
  tower theorem.  The declared 64-family has an exact universal
  code/evaluator, scoped; a typed-refusal top closes by partiality
  what totality cannot; description-level fixed point without an
  evaluation-level one (`family_missed`).  A DECLARED model of the
  description/interpreter boundary satisfies candidates A and F with
  obstructed collapse; its relation/retention/protection are
  inserted by definition, and no theorem links the uncoded
  occurrence to the missed function.  The identification of the
  boundary with a Primitive Difference is a FRONTIER CONJECTURE
  whose missing theorem (denotational/operational grounding) is
  stated in the receipt.  Absolute no-outside not claimed.
- **Class**: theorem + countermodel + finite computation +
  CONJECTURE (boundary identification) + OPEN (absolute closure).
- **Lean**: `InterpreterBoundary.tower_persists`,
  `InterpreterBoundary.i2_universal_in_class`,
  `InterpreterBoundary.i3_partial_top_refuses`,
  `InterpreterBoundary.i3_partial_covers`,
  `InterpreterBoundary.family_missed`,
  `InterpreterBoundary.i5_boundary_is_A`,
  `InterpreterBoundary.i5_boundary_is_F`,
  `InterpreterBoundary.i5_collapse_obstructed`,
  `InterpreterBoundary.i5_family_not_extensionally_complete`
  (audit repair: renamed from `i5_difference_grounded`, whose
  statement is `family_missed` and mentions neither the
  boundary pair nor the uncoded occurrence; the denotational
  bridge is recorded as the unproved Prop
  `InterpreterBoundary.openDenotationalBridge`).
- **Python**: `primitive_interpreter.json`.

### CL-PD2-RECEIPT
- **Statement**: the completion receipt binds base commit, contact
  status, prompt hashes, toolchain pins, the axiom-report hash, all
  declared finite bounds, ten terminal claims each mapped to theorem
  or countermodel evidence, five open obligations, the twenty-attack
  adversarial record, and the two withdrawn-or-repaired claims.
- **Class**: finite computation (deterministic generator).
- **Python**: `primitive_completion_receipt.json`,
  `run_primitive_receipt.py`.

### CL-PD2-ATTACHMENT (repaired, final pass)
- **Statement**: one-edge attachment (a fresh walking edge glued
  along a represented parent: assert, retain, protect) is lawful at
  every stage for every LAWFUL policy — a `LawfulPolicy` carries
  the proof that each chosen parent is represented; NO CLAMPING
  occurs anywhere (the retired clamp survives only as the recorded
  countermodel `clamp_rewrote_input`, and an illegal choice meets
  the typed refusal `AttachOutcome.refusedParent`, never a
  rewrite).  Occurrence identity is resolved: `occ` stores TOKENS
  in admission order, POSITIONS are the identities used by every
  relational store; the canonical fresh token is one past the
  maximum, fresh on EVERY carrier (`freshTok_fresh`), while
  length-as-token fails on non-initial carriers
  (`length_not_fresh_countermodel`); on canonical tree states
  tokens and positions provably coincide and the tree block IS the
  Up block (`freshTok_treeState`, `attachBlock_is_upBlock`).
  Completeness is REGISTRY-RELATIVE and an iff:
  `b ∈ Up(s) ↔ LegalOneEdgeExtension s b` (`up_iff_legal`), for the
  exact declared one-edge grammar and nothing else; every Up block
  executes to a strict legal extension on live store-bounded states
  (`up_exec_eq`, `up_executes`), and tree states are store-bounded
  (`treeState_wf`).  Presentation invariance is a genuine
  positional renaming ACTION: blocks and the family transport along
  it and replay commutes with it on the supply fragment
  (`upBlock_transport`, `upFamily_transport`, `act_up_comm`);
  the old length-equality survives only as grammar uniformity over
  an IDENTICAL carrier (`upFamily_grammar_uniform`) — equal-size
  states with literally equal families need not be related by any
  renaming (`equal_size_not_renaming_related`).  Every lawful
  policy produces a tree — unique ascending parent, root
  reachability, V−E=1 (`treeAt_spec`, `all_reach`,
  `attach_residue`); global shape is NOT forced
  (`path4_star4_not_isomorphic`), and two legal equal-cost
  extensions genuinely diverge
  (`equal_cost_non_isomorphic_extensions`) — the complete family
  never selects.  Orbit-valued choices where symmetry remains (star
  leaves one orbit; the ORIENTED path rigid — the orientation
  residue at work).  The unique map out of the two-element kernel
  is injective into every irreflexive target and provably not so
  without irreflexivity.  Imported inputs stated: fresh token
  supply, protection, observer transport, budget, activation.
- **Class**: theorem + countermodel + finite computation.
- **Lean**: `Attachment.up_iff_legal`, `Attachment.up_exec_eq`,
  `Attachment.up_executes`, `Attachment.attachChecked_refuses`,
  `Attachment.unlawful_refused`, `Attachment.clamp_rewrote_input`,
  `Attachment.freshTok_fresh`,
  `Attachment.length_not_fresh_countermodel`,
  `Attachment.freshTok_treeState`,
  `Attachment.attachBlock_is_upBlock`, `Attachment.treeState_wf`,
  `Attachment.upBlock_transport`, `Attachment.upFamily_transport`,
  `Attachment.act_up_comm`, `Attachment.upFamily_grammar_uniform`,
  `Attachment.equal_size_not_renaming_related`,
  `Attachment.equal_cost_non_isomorphic_extensions`,
  `Attachment.treeAt_spec`, `Attachment.attach_residue`,
  `Attachment.parent_lt`, `Attachment.parent_unique`,
  `Attachment.parent_exists`, `Attachment.all_reach`,
  `Attachment.path4_star4_not_isomorphic`,
  `Attachment.star_orbit_swap`, `Attachment.path_oriented_rigid`,
  `Attachment.path_center_separate`,
  `Attachment.halted_up_inert`,
  `PrimitiveCats.d2_map_injective`,
  `PrimitiveCats.d2_map_not_injective_without_irrefl`.
- **Python**: `attachment_ladder.json` (lawful policies to 15
  rounds; registry iff; renaming commutation over the full
  permutation group on the sample carriers; both countermodels;
  orbit computation via store automorphisms).

### CL-PD2-LADDER-GENERAL (repaired and reconciled with
CL-PD2-LADDER)
- **Statement**: the dimension-indexed declared cell calculus
  carries ONE well-formed shell guard uniform in the dimension —
  exact arity, STRICT ASCENT (the legacy guard admitted the
  repeated-vertex pseudo-cell `[0, 0]`;
  `pseudo_cell_countermodel`), complete unfilled boundary — and
  the UNIFORM GUARDED FILLER THEOREM (`uniform_guarded_filler`,
  renamed and NARROWED from the former "general ladder theorem"):
  at every dimension a complete well-formed unfilled boundary
  admits its filler and the admission strictly extends the
  complex.  This is a theorem about the declared guarded step, NOT
  a homology claim.  Reconciliation with CL-PD2-LADDER: the
  hard-coded `ladder_dim2/dim3` are the dimension-2/3 instances of
  the two-rule shape inside the PASSAGE-ADJACENT calculus of
  `HigherStructure`; `uniform_guarded_filler` is its
  dimension-uniform generalization in the standalone generalized
  calculus, and the review-pass conjecture
  GENERAL_DIMENSIONAL_LADDER is settled ONLY in this narrowed
  filler sense.  Well-formedness is a replayed invariant
  (`wf_nreplay`, `d4_wf`); guards are load-bearing and shells
  never self-fill; the dimension-4 demonstration replays
  completely (5/10/10/5/1); the composite boundary vanishes at
  dimensions 2–5 (decided/computed); the GENERAL composite
  vanishing (∂∂ = 0 at every dimension) REMAINS OPEN — recorded as
  the boundary-calculus conjecture, not claimed.
- **Class**: theorem (uniform guarded filler; wf invariant) +
  countermodel (pseudo-cell; guard load-bearing) + finite
  computation (dims 2–5) + CONJECTURE (general composite
  vanishing).
- **Lean**: `LadderGeneral.uniform_guarded_filler`,
  `LadderGeneral.shell_refuses_general`,
  `LadderGeneral.shell_no_self_fill`,
  `LadderGeneral.pseudo_cell_countermodel`,
  `LadderGeneral.wf_nreplay`, `LadderGeneral.d4_demo`,
  `LadderGeneral.d4_wf`, `LadderGeneral.d4_guard_load_bearing`,
  `LadderGeneral.d2_zero_dims_2_3_4`.
- **Python**: `attachment_ladder.json` (dims 2–5; repaired guard;
  pseudo-cell countermodel; wf invariant).

### CL-PD2-COMPRESSION
- **Statement** (target-relative presentation compression; all
  notions relative to a DECLARED finite domain `D` and DECLARED
  represented question family `Q`): (A) a presentation map factors
  through the Q-signature exactly when it is constant on
  Q-signature fibers over `D` (`factors_iff_fiberConstant`); the
  factoring map is unique ON THE IMAGE of `D` and provably not
  unique off it (`factor_unique_on_image`,
  `factor_not_unique_off_image`).  (B) the signature quotient `pQ`
  is exact, Q-adequate, and COARSEST among Q-adequate
  presentations, with the universal property scoped to the image
  (`pQ_exact`, `pQ_adequate`, `pQ_coarsest`,
  `pQ_unique_on_image`) — no claim off-image or for undeclared
  families.  (C) every descent failure — two points merged by the
  compression yet separated by some declared question — is
  witnessed by an explicit separator (`descent_witness`).  (D)
  enlarging the family refines the agreement relation, and a class
  SPLITS exactly when the enlargement contains a NEW separator for
  previously agreeing points (`enlarge_refines`,
  `splits_iff_new_separator`).  (E) there is NO absolute adequacy
  without a declared family: adequacy for every family is exactly
  injectivity on `D` — no compression at all
  (`absolute_adequacy_iff_injective`, forward by indicator
  questions).  (F) repetition, digests/hashes, and replay records
  are functions of the old signature and separate nothing new
  (`dup_no_refine`, `postcompose_no_refine`,
  `refine_requires_separator`) — what makes replay EVIDENTIAL is
  a new separating question, never re-presentation.  Iteration is
  bounded by the declared domain: class counts are positive,
  bounded by `|D|`, strictly increase on splits, and any strict
  refinement chain has fewer than `|D|` steps (`refine_bounded`,
  `classCount_pos`, `strict_split_increases`, `chain_bounded`,
  `strict_steps_lt`).  Repaired-attachment connection tested and
  bounded by countermodel: refinement is NOT unique and ties are
  retained (`refinement_not_unique`, `refinement_tie`) — no
  unique-minimum refinement, no endogenous selection, no unlimited
  iteration.
- **Class**: theorem + countermodel + finite computation
  (exhaustive within declared bounds n ≤ 3, m ≤ 3, |Q| ≤ 2).
- **Lean**: `Compression.factors_iff_fiberConstant`,
  `Compression.factor_unique_on_image`,
  `Compression.factor_not_unique_off_image`,
  `Compression.pQ_exact`, `Compression.pQ_adequate`,
  `Compression.pQ_coarsest`, `Compression.pQ_unique_on_image`,
  `Compression.descent_witness`, `Compression.enlarge_refines`,
  `Compression.splits_iff_new_separator`,
  `Compression.absolute_adequacy_iff_injective`,
  `Compression.dup_no_refine`, `Compression.postcompose_no_refine`,
  `Compression.refine_requires_separator`,
  `Compression.refinement_not_unique`,
  `Compression.refinement_tie`, `Compression.refine_bounded`,
  `Compression.classCount_pos`,
  `Compression.strict_split_increases`,
  `Compression.chain_bounded`, `Compression.strict_steps_lt`,
  `Compression.sigEq_iff_sigList`.
- **Python**: `compression.json` (757 families per size pair up to
  (3,3); 37736 witnessed descent instances; 10006 split instances;
  digest quantification over all signature functions).

### CL-PD2-RECEIPT-BYTES
- **Statement**: the completion receipt is byte-reproducible
  across platforms because every hashed prompt input is hashed in
  CANONICAL BYTES — the Git blob bytes (LF), equal to the
  CRLF→LF-normalized checkout bytes; the original supplied CRLF
  rendering of the seed prompt is recorded alongside as
  provenance.  The blob/checkout distinction is tested against
  `git show HEAD:...`; content mutation detection is tested (any
  content byte change moves the canonical hash; a pure line-ending
  re-rendering does not — it is the same canonical content).
- **Class**: finite computation + tests.
- **Python**: `run_primitive_receipt.py` (`canonical_sha256`),
  `tests/test_primitive_receipt.py` (blob/checkout distinction,
  mutation detection, dual seed hashes).

### CL-PD2-TRACE-STABILITY (audit repair; supersedes the withdrawn CL-PD2-STABLE-CONTENT)
- **WITHDRAWN CLAIM**: the review draft asserted "stable content is
  exactly protected separation".  The word *exactly* was an
  OVERCLAIM: only sufficiency was proved, and the converse is FALSE.
  The claim is withdrawn and replaced by the following; every body,
  receipt, and docstring site was weakened to match.
- **Statement** (native scope: the declared event grammar of the
  passage calculus).  Trace stability is now DEFINED, not assumed:
  `TraceStableSep s i j` says the pair stays separated by the
  declared observation after EVERY replay; `IntStableSep` is the
  same over the INTERNAL fragment only (no environment-owned
  occurrence supply, budget setting, or license setting).
  (i) **SUFFICIENCY (theorem)**: protected AND separated implies
  trace stable (`protSep_trace_stable`, via `protSep_persists` /
  `protSep_replays`) - supply events do not touch observation, new
  columns only add separators, and same-level refinement is guarded
  by precisely the monotone preservation of protected separations.
  (ii) **THE CONVERSE IS FALSE - two countermodels.**  On an
  ABSORBED (halted) state every replay is inert, so an UNPROTECTED
  separation is trace stable (`halted_stable_not_protected`).  On a
  LIVE but UNFUNDED state no internal event can change the
  observation - the two structure-creating moves are budget-gated
  and no internal event replenishes the budget - so an UNPROTECTED
  separation is internally stable
  (`unfunded_internal_stable_not_protected`).  Neither pair is
  protected.
  (iii) **INSTABILITY IS WITNESS-BORNE (theorem)**: an unprotected
  separation is destroyed only when a concrete breaking witness
  exists - a funded, accepted refinement routed through the
  separating column (`separation_breakable`), instantiated
  concretely by `unprotected_separation_unstable`.  Protection is
  load-bearing, but only against witnesses.
  (iv) **OPEN**: sufficiency and witness-borne instability sandwich
  the truth WITHOUT meeting.  Whether trace stability implies
  protected separation on the live, funded class is OPEN and is
  recorded as a Prop, never as a theorem
  (`openExactStabilityCharacterization`).
  (v) **Quiescence** (unchanged, and NOT a stability claim): on a
  declared state, no pair is actively obstructed exactly when every
  retained protected pair is protected-separated
  (`quiescent_iff_protected_separated`,
  `quiescence_is_protected_separation`).  The corollary that does
  follow is `quiescent_retained_protected_trace_stable`.
- **Class**: theorem (sufficiency; witness-borne instability;
  quiescence iff) + countermodel (converse, twice) + OPEN (exact
  characterization) + finite computation.
- **Lean**: `StableContent.protSep_trace_stable`,
  `StableContent.protSep_persists`,
  `StableContent.protSep_replays`,
  `StableContent.trace_stable_int_stable`,
  `StableContent.sep_preserved`, `StableContent.prot_mono`,
  `StableContent.sepP_refine`, `StableContent.replay_halted`,
  `StableContent.halted_stable_not_protected`,
  `StableContent.internal_step_inert_unfunded`,
  `StableContent.internal_replay_inert_unfunded`,
  `StableContent.unfunded_internal_stable_not_protected`,
  `StableContent.separation_breakable`,
  `StableContent.unprotected_separation_unstable`,
  `StableContent.quiescent_iff_protected_separated`,
  `StableContent.quiescence_is_protected_separation`,
  `StableContent.quiescent_retained_protected_trace_stable`;
  OPEN statement `StableContent.openExactStabilityCharacterization`.
- **Python**: `primitive_passage.json` (`stable_content` section:
  single-step and bounded-trace sufficiency, both converse
  countermodels, the witness-borne instability countermodel, the
  quiescence coincidence, and the recorded open gap; declared
  bounds: carrier 3, trace depth 2, breadth 24).

### CL-PD2-RENAMING-STRUCTURE (Goal 1)
- **Statement**: the renaming structure around `Up` is completed and
  its laws proved, and only afterwards is the vocabulary
  "equivariant" used.  (i) `Renaming n` carries IDENTITY (`idRen`),
  INVERSE (`invRen`) and COMPOSITION (`compRen`) satisfying the group
  laws `comp_id`, `id_comp`, `comp_assoc`, `inv_comp`, `comp_inv`,
  `inv_inv`, proved through a componentwise extensionality principle
  (`Renaming.ext`: the two remaining fields are propositions, so a
  renaming is its function pair).  (ii) `act` is an ACTION:
  `act_id` holds UNCONDITIONALLY, and `act_comp` holds on the exact
  scope `n <= s.occ.length` — the scope in which positional
  re-indexing of the carrier is meaningful, and deliberately weaker
  than equality so that the EXTENDED state (length `n+1`) is covered
  too; `act_inv` follows.  (iii) block and family transport respect
  identity and composition (`upBlock_id`, `upBlock_comp`,
  `upFamily_id`, `upFamily_comp`, `upFamily_transport_id`,
  `upFamily_transport_comp`).  (iv) COHERENCE: replay of an `Up`
  block commutes with a COMPOSED renaming and the composite route
  equals the two-step route (`act_up_comm_comp`,
  `act_up_comm_twostep`) — the naturality square closes under
  composition.  (v) NO SELECTED REPRESENTATIVE: the family is closed
  under the action, carries the whole orbit, and has exactly one
  block per represented parent (`upFamily_orbit_closed`,
  `star_orbit_both_present`, `upFamily_length`).
  (vi) COUNTERMODELS — none of this is supplied by weaker data: an
  arbitrary NON-BIJECTIVE map has no left inverse
  (`collapse_not_a_renaming`) and its pushforward turns an
  irreflexive store into self-pairs that the well-formedness guard
  refuses (`collapse_pushforward_ill_formed`); equal carrier size
  supplies no law (`equal_size_supplies_no_law`); equal cost supplies
  no law (`equal_cost_supplies_no_law`).
- **Scope of the earned vocabulary** (`equivariance_summary`): the
  supply fragment of the declared one-edge grammar, on live
  store-bounded states.  NOT the observation calculus, NOT
  multi-edge or relational extensions, NOT any map that is not a
  renaming.
- **Class**: theorem + countermodel + finite computation.
- **Lean**: `RenamingStructure.Renaming.ext`, `.comp_id`,
  `.id_comp`, `.comp_assoc`, `.inv_comp`, `.comp_inv`, `.inv_inv`,
  `.map_getD_range`, `.act_id`, `.act_comp`, `.act_inv`,
  `.upBlock_id`, `.upBlock_comp`, `.upFamily_id`, `.upFamily_comp`,
  `.upFamily_transport_id`, `.upFamily_transport_comp`, `.wf_act`,
  `.act_up_comm_comp`, `.act_up_comm_twostep`,
  `.upFamily_orbit_closed`, `.star_orbit_both_present`,
  `.upFamily_length`, `.collapse_not_a_renaming`,
  `.collapse_pushforward_ill_formed`, `.equal_size_supplies_no_law`,
  `.equal_cost_supplies_no_law`, `.equivariance_summary`.
- **Python**: `renaming_structure.json` — exhaustive over the whole
  symmetric group at carrier 3 (216 associativity triples, all 6
  permutations against both sample states for every action,
  transport, and coherence law) plus all three countermodels.

### CL-PD2-GRAPH-GENESIS (Goal 5)
- **Statement, part 1 (the negative theorems)**: in the declared
  calculus, graph growth is SUPPLIED, not generated by the represented
  `nextFamilyP` response semantics.
  `refineCol` and `addCol` provably leave seven state fields
  unchanged - occurrences, asserted, retained, protected, refusals,
  license, halted - so only observation and budget are even
  candidates for change (`refineCol_only_obs`, `addCol_only_obs`).
  The internal response family ranges over columns on EXISTING
  occurrences only (`extensionProposals_range_over_existing`,
  `repairFamily_range_over_existing`), and has exactly two block
  shapes, with no third (`nextFamilyP_block_shape`,
  `nextFamilyP_range_over_existing`).  Along EVERY internal trace the
  four graph stores are fixed
  (`internal_family_cannot_grow_carrier`).  The corollary states it
  in one line: growth comes from the external driver or the `Up`
  grammar, never from `nextFamilyP`
  (`graph_growth_is_supplied`).
- **Statement, part 2 (an explicit sufficient proposal schema)**:
  `ProposalRecord s` carries exactly - one NAMED member of the COMPLETE
  `Up` family with its membership proof (not a canonical or unique
  representative); an old-position embedding with its retraction and
  the retraction law; fresh-token evidence; preservation of every old
  asserted, retained, protected and separated item; the new pair with
  its provenance (parent position, fresh position); and a declared
  cost.  It carries NO license, execution, or activation field, and
  `proposal_confers_no_execution` witnesses that a proposal on a
  terminal state moves nothing.  The family transports under renaming
  within exactly `act_up_comm`'s scope (`proposal_transports`) and
  retains equal-cost non-isomorphic branches
  (`proposal_family_retains_ties`).
- **Statement, part 3 (the verdict)**: `nextFamilyP` does NOT request
  the carrier-changing lift at an active obstruction.  On the blind pair - all four
  obstruction conditions satisfied - the complete internal family is
  nonempty, every member discharges the obstruction, and every member
  leaves the graph stores fixed; and no state anywhere admits an
  internal family member that grows the carrier
  (`family_never_grows_carrier`).  Generalized:
  `obstruction_resolved_in_carrier` answers every obstruction meeting
  the kernel's own hypotheses inside the existing carrier.  Therefore
  the growth demand is a SEPARATELY DECLARED PREMISE, not entailed by
  the represented `nextFamilyP` semantics
  (`growth_demand_not_obstruction_consequence`).  No minimality or
  universal property is proved for `ProposalRecord`.
- **Scope limits, stated**: the field-invariance theorems prove
  invariance of the other seven fields only and do not claim that
  observation or budget do change (guards may refuse).
  `repairFamily_range_over_existing` bounds the NEW point only; points
  already inside a declared column are not bounded by any kernel
  invariant on hand-built states.  `proposal_transports` covers
  exactly the supply fragment on store-bounded live states.  Part 3
  covers the family the kernel computes (`nextFamilyP`); it does NOT
  exclude that some other declared family could grow the carrier -
  that remains OPEN.  On a terminal state the obstruction persists
  because nothing moves at all, so the resolution theorem is an
  implication and not a blanket claim.  "The record carries no
  authority" is structural (there is no such field), not a theorem.
- **Class**: theorem + countermodel + finite computation + OPEN
  (other response families).
- **Lean**: `GraphGenesis.refineCol_only_obs`, `.addCol_only_obs`,
  `.extensionProposals_range_over_existing`,
  `.repairFamily_range_over_existing`, `.nextFamilyP_block_shape`,
  `.nextFamilyP_range_over_existing`, `.IsInternal_exact`,
  `.internal_family_cannot_grow_carrier`,
  `.response_replay_fixes_graph`, `.nextFamilyP_block_fixes_graph`,
  `.graph_growth_is_supplied`, `.proposal_confers_no_execution`,
  `.upProposal_executes`, `.proposal_transports`,
  `.proposal_family_retains_ties`,
  `.obstruction_resolved_in_carrier`, `.family_never_grows_carrier`,
  `.growth_demand_not_obstruction_consequence`,
  `.blindPair_resolution_keeps_carrier`.
- **Python**: `graph_genesis.json` - 8 sample states, 600 battery
  checks (probing one past the carrier), 11104 internal traces of
  length at most 2, the full symmetric group at carrier 3 for
  transport, tie carrier 4; bounds recorded in the artifact.

