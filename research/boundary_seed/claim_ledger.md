# Claim ledger: the boundary derivation

`AuthorityEffect: None`.  One entry per claim used by `paper.md`.  IDs
are stable and prefixed `B<challenge>-`.  The admitted boundary is
listed first.  Statuses: DEFINITION (true by unfolding a declaration;
never counted as content), PROVED (Lean theorem named), COMPUTED
(deterministic Python receipt, bounded), OPEN.

### B-BOUNDARY

- **Statement**: The boundary with its two sides is the one admitted
  primitive.  A regime records, for each admitted mark, the side it lies
  on; the boundary is implicit and unique.
- **Status**: admitted primitive.  Never called free.
- **Dependencies**: the seed, section 1.
- **Assumptions**: none beyond the declaration.
- **Python evidence**: `Regime` in `code/boundary/model.py`.
- **Lean theorem**: `Regime` structure in `lean/BoundarySeed/Basic.lean`.
- **Axiom report**: not applicable.
- **Falsifier**: not applicable; a declaration.
- **Surviving boundary**: the whole tree.

### B0-COLLAPSE-U

- **Statement**: Under reading U, at genesis, the two sides have equal
  side profiles: the sides are observationally collapsed.
- **Status**: PROVED.
- **Dependencies**: definitions 7 to 9 of the paper.
- **Assumptions**: side observation is contents.
- **Python evidence**: receipt `readings.U.sides_collapsed`;
  `test_sides_collapsed_under_U_and_named_under_O`.
- **Lean theorem**: `BoundarySeed.sides_collapsed_at_genesis_U`.
- **Axiom report**: propext, Quot.sound.
- **Falsifier**: a definition of side observation under which the empty
  sides differ without an admitted name.
- **Surviving boundary**: genesis only; one admitted mark separates the
  sides (`test_one_mark_separates_the_sides_under_both_readings`).

### B0-NAMES-O

- **Statement**: Under reading O, at genesis, the two sides are
  distinguished, and the difference of their profiles is the name
  component only.
- **Status**: DEFINITION.
- **Dependencies**: definition 8.
- **Assumptions**: the names `near` and `far` are admitted by the
  reading.
- **Python evidence**: receipt `readings.O.side_profiles`; score C0-2.
- **Lean theorem**: `BoundarySeed.side_names_distinct`.
- **Axiom report**: none.
- **Falsifier**: a proof that the O-distinction has content beyond the
  declaration.
- **Surviving boundary**: every O-state; the names never change.

### B0-INERTIA

- **Statement**: A supply changes no state; a step that changes the state
  is a placement carrying an external side; no function of the kernel
  produces an event from a state.
- **Status**: PROVED (first two clauses); COMPUTED (third: the
  generator census of the kernel module).
- **Dependencies**: definitions 4 and 5.
- **Assumptions**: the event grammar of Challenge 0.
- **Python evidence**: receipt `readings.*.supply_leaves_state_unchanged`,
  `state_event_generators`; `test_supply_is_not_admission`,
  `test_no_state_event_generator_in_the_kernel`,
  `test_generator_census_sees_a_planted_generator`.
- **Lean theorem**: `BoundarySeed.supply_no_op`,
  `BoundarySeed.step_changes_only_by_place`,
  `BoundarySeed.replay_supply_inert`.
- **Axiom report**: none.
- **Falsifier**: a state change with no admission event in its history.
- **Surviving boundary**: the event grammar as declared; a later
  challenge that adds an event kind re-runs the census.

### B0-NO-JUDGMENT

- **Statement**: At genesis, under both readings, no (mark, side)
  observation fires, and the observation relation has no negative or
  counting form, so "this side is empty" is not an internally available
  judgment.
- **Status**: PROVED (no observation fires); DEFINITION (the relation's
  form).
- **Dependencies**: definition 10.
- **Assumptions**: no negative observation is admitted.
- **Python evidence**: receipt `readings.*.observations`,
  `observation_vocabulary`; `test_genesis_contents_empty_on_both_sides`.
- **Lean theorem**: `BoundarySeed.no_observation_at_genesis`,
  `BoundarySeed.contents_genesis`.
- **Axiom report**: propext (first); propext, Quot.sound (second).
- **Falsifier**: an internal judgment "this side is empty" derivable at
  genesis without a new admission.
- **Surviving boundary**: until a negative or counting observation is
  admitted, if ever.

### B0-REFLECTION-U

- **Statement**: Under reading U the exchange of sides is a permitted
  renaming, an involution, and fixes genesis.
- **Status**: PROVED (involution, fixes genesis); DEFINITION (permitted).
- **Dependencies**: definitions 11, 14, 15.
- **Assumptions**: reading U.
- **Python evidence**: receipt `readings.U.reflect_genesis_equals_genesis`,
  `reflection_automorphism_by_key`;
  `test_canonical_identifies_the_reflection_under_U_only`,
  `test_reflect_is_an_involution_and_swaps_sides`.
- **Lean theorem**: `BoundarySeed.reflect_reflect`,
  `BoundarySeed.reflect_genesis`, `BoundarySeed.map_not_not`.
- **Axiom report**: propext; none; propext.
- **Falsifier**: a U-state fixed by nothing.
- **Surviving boundary**: every U-state.

### B0-REFLECTION-O

- **Statement**: Under reading O the exchange of sides is not a permitted
  renaming; it fixes the genesis regime as data but moves any placed
  mark.
- **Status**: DEFINITION (not permitted); PROVED (moves any placed mark).
- **Dependencies**: definitions 11, 15.
- **Assumptions**: reading O.
- **Python evidence**: receipt `readings.O.reflection_is_permitted_renaming`;
  `test_reflection_automorphism_at_genesis`.
- **Lean theorem**: `BoundarySeed.reflect_moves_a_mark`.
- **Axiom report**: propext.
- **Falsifier**: an O-state with a placed mark whose reflection equals it.
- **Surviving boundary**: every O-state.

### B0-EQUAL-COUNTS

- **Statement**: For every placement of up to four marks, the reflection
  fixes the placement up to mark renaming exactly when the two sides
  carry equally many marks, under both readings.
- **Status**: COMPUTED, bound four marks.
- **Dependencies**: definitions 11 to 13.
- **Assumptions**: mark renaming is permitted under both readings.
- **Python evidence**: receipt `reflection_census.fixed_iff_equal_counts`
  and `rows`; `test_census_rows`.
- **Lean theorem**: none; not claimed beyond the bound.
- **Axiom report**: not applicable.
- **Falsifier**: a placement within the bound fixed with unequal counts
  or unfixed with equal counts.
- **Surviving boundary**: four marks.

### B0-CLASSES

- **Statement**: For `n` marks up to four, the canonical key sees
  `n + 1` classes under O and `floor(n/2) + 1` under U.
- **Status**: COMPUTED, bound four marks; the closed forms describe the
  table and are not theorems.
- **Dependencies**: definition 14.
- **Assumptions**: none beyond the readings.
- **Python evidence**: receipt `reflection_census.rows`; `test_census_rows`.
- **Lean theorem**: none.
- **Axiom report**: not applicable.
- **Falsifier**: a row of the census that departs from the closed form.
- **Surviving boundary**: four marks.

### B0-X

- **Statement**: After one mark is admitted on a side, the sides become
  observationally separable under U with no augmentation beyond the
  admission, and under O nothing becomes distinguishable that was not
  already.
- **Status**: OPEN; the extrapolation of Challenge 0, scored by
  Challenge 1.
- **Dependencies**: the admission grammar Challenge 1 declares.
- **Assumptions**: none yet.
- **Python evidence**: none yet.  A Challenge 0 test already shows one
  admitted mark separating the sides under both readings, but the
  prediction is about Challenge 1's grammar and is scored there.
- **Lean theorem**: none yet.
- **Axiom report**: not applicable.
- **Falsifier**: as written in `challenge0/PREDICTIONS.md`.
- **Surviving boundary**: not yet.
