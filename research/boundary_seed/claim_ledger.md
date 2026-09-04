# Claim ledger: the boundary derivation

`AuthorityEffect: None`.  One entry per claim used by `paper.md`.  IDs
are stable and prefixed `B<challenge>-`.  The admitted boundary is listed
first.  Statuses: DEFINITION (true by unfolding a declaration; never
counted as content), PROVED (Lean theorem named), COMPUTED (deterministic
Python receipt, bounded), LIMITATION, OPEN.

### B-BOUNDARY

- **Statement**: The boundary with two sides is the one admitted primitive
  exception carried by the supplied opaque whole.  A regime records, for
  each later admitted mark, its side; the boundary is implicit and unique.
- **Status**: admitted primitive.  Never called free.
- **Dependencies**: the seed, section 1.
- **Assumptions**: none beyond the declaration.
- **Python evidence**: `Regime` in `code/boundary/model.py`.
- **Lean theorem**: `Regime` structure in `lean/BoundarySeed/Basic.lean`.
- **Axiom report**: not applicable.
- **Falsifier**: not applicable; a declaration.
- **Surviving boundary**: the whole tree.

### B-DATUM

- **Statement**: The initial inscription is one supplied opaque datum at
  genesis, before any later mark is placed.  The boundary is not a second
  datum.
- **Status**: DEFINITION; PROVED for presence in the Lean regime.
- **Dependencies**: the seed, section 1.
- **Assumptions**: the supplied whole is atomic except for the admitted
  boundary exception.
- **Python evidence**: receipt `readings.*.initial_datum`;
  `test_initial_datum_and_boundary_dependence_are_explicit`.
- **Lean theorem**: `BoundarySeed.genesis_initial_datum`,
  `BoundarySeed.genesis_placement_nil`.
- **Axiom report**: none for either.
- **Falsifier**: a genesis regime lacking the initial datum.
- **Surviving boundary**: all Challenge 0 regimes.

### B-PROVENANCE

- **Statement**: The committed tree is source-isolated from named sealed
  paths and identifiable other research-tree references under the checked
  byte populations.  Blind or independent discovery is not established.
- **Status**: LIMITATION.
- **Dependencies**: declared prior exposure in `MANUAL.md` and the Challenge
  0 status; the source-isolation scan.
- **Assumptions**: none about instrument memory or off-tree reads.
- **Python evidence**: `test_write_root_is_source_isolated_before_the_freeze`.
- **Lean theorem**: none; provenance is not object-language mathematics.
- **Axiom report**: not applicable.
- **Falsifier**: any claim that the disclosed prior exposure is a clean-room
  or independent-discovery receipt.
- **Surviving boundary**: all results in this tree.

### B0-COLLAPSE-U

- **Statement**: Under U at genesis, the two sides have equal extensional
  profiles of the closed positive judgment grammar.
- **Status**: PROVED.
- **Dependencies**: definitions 2, 4, and 8 to 11 of the paper.
- **Assumptions**: profiles are metatheoretic enumerations, not internal
  collection values.
- **Python evidence**: receipt `readings.U.sides_collapsed`;
  `test_sides_collapsed_under_U_and_named_under_O`.
- **Lean theorem**: `BoundarySeed.sides_collapsed_at_genesis_U`.
- **Axiom report**: propext, Quot.sound.
- **Falsifier**: unequal U profiles at genesis under the declared grammar.
- **Surviving boundary**: genesis only; one admitted mark separates the
  sides (`test_one_mark_separates_the_sides_under_both_readings`).

### B0-NAMES-O

- **Statement**: Under O at genesis, both side-name judgments hold and the
  two extensional profiles differ in the name component only.
- **Status**: DEFINITION.
- **Dependencies**: definitions 2, 4, and 8 to 10.
- **Assumptions**: the names `near` and `far` are admitted by the
  reading.
- **Python evidence**: receipt `readings.O.side_profiles`; score C0-2.
- **Lean theorem**: `BoundarySeed.O_name_judgment_at_genesis`,
  `BoundarySeed.sides_distinct_at_genesis_O`,
  `BoundarySeed.side_names_distinct`.
- **Axiom report**: propext; propext, Quot.sound; none.
- **Falsifier**: a proof that the O-distinction has content beyond the
  declaration.
- **Surviving boundary**: every O-state; the names never change.

### B0-INERTIA

- **Statement**: Supply changes no admitted state; replay is deterministic;
  any already-provided
  event that changes it is a placement; the declared Challenge 0
  event-follows relation is empty.  Certifying replay refuses a new mark
  without a prior supply.  A resolved-annotation census separately finds no
  public Python function whose return annotation contains an event type.
- **Status**: PROVED (Lean state/event clauses); DEFINITION and COMPUTED
  (Python replay precondition and supplementary API census).
- **Dependencies**: definitions 4 to 7.
- **Assumptions**: the event grammar of Challenge 0.
- **Python evidence**: receipt `readings.*.supply_leaves_state_unchanged`,
  `event_follows_relation_empty`, `state_event_generators`;
  `test_supply_is_not_admission`,
  `test_certifying_replay_refuses_unsupplied_admission`,
  `test_no_event_follows_from_challenge0_state`,
  `test_no_state_event_generator_in_the_kernel`,
  `test_generator_census_sees_a_planted_generator`,
  `test_generator_census_sees_an_optional_event`.
- **Lean theorem**: `BoundarySeed.supply_no_op`,
  `BoundarySeed.step_changes_only_by_place`,
  `BoundarySeed.replay_deterministic`, `BoundarySeed.replay_supply_inert`,
  `BoundarySeed.no_event_follows`.
- **Axiom report**: none; none; none; none; propext.
- **Falsifier**: an event satisfying the declared `EventFollows`, or a
  certifying replay that accepts a newly admitted token without prior supply.
- **Surviving boundary**: the event grammar as declared; a later
  challenge that adds an event kind re-runs the census.

### B0-NO-JUDGMENT

- **Statement**: At genesis under both readings, no positive `OnSide`
  judgment holds.  The closed Challenge 0 grammar contains only `OnSide`
  and `SideNamed`, with no primitive empty-side or counting judgment.  Under
  O, the two positive `SideNamed` judgments do hold.
- **Status**: PROVED (holding facts); DEFINITION (the closed grammar).  This
  does not prove a general nondefinability theorem for emptiness.  Frozen
  prediction C0-4 is PARTIAL because its separate “no observation fires”
  rationale is false under O.
- **Dependencies**: definitions 4, 8, and 9.
- **Assumptions**: no negative observation is admitted.
- **Python evidence**: receipt `readings.*.mark_observations`,
  `readings.*.name_observations`, `observation_vocabulary`;
  `test_closed_observation_grammar_and_holds`.
- **Lean theorem**: `BoundarySeed.no_observation_at_genesis`,
  `BoundarySeed.O_name_judgment_at_genesis`,
  `BoundarySeed.U_no_name_judgment_at_genesis`,
  `BoundarySeed.contents_genesis` (metatheoretic extension only).
- **Axiom report**: propext for the three judgment reports; propext and
  Quot.sound for `contents_genesis`.
- **Falsifier**: an `Empty` or counting constructor in the declared grammar,
  or a true `OnSide` judgment at genesis.
- **Surviving boundary**: the closed Challenge 0 judgment grammar only.

### B0-REFLECTION-U

- **Statement**: Under reading U the exchange of sides is a permitted
  renaming, an involution, and a permitted automorphism at genesis.  A
  reflected pair can share a canonical orbit key without reflection
  stabilizing either member.
- **Status**: PROVED (involution, fixes genesis); DEFINITION (permitted).
- **Dependencies**: definitions 2, 4, 12, 15, and 16.
- **Assumptions**: reading U.
- **Python evidence**: receipt `readings.U.reflect_genesis_equals_genesis`,
  `readings.U.reflection_is_permitted_automorphism`;
  `test_canonical_identifies_the_reflection_under_U_only`,
  `test_reflection_automorphism_at_genesis`,
  `test_reflect_is_an_involution_and_swaps_sides`.
- **Lean theorem**: `BoundarySeed.reflect_reflect`,
  `BoundarySeed.reflect_genesis`, `BoundarySeed.reflection_permitted_U`,
  `BoundarySeed.map_not_not`.
- **Axiom report**: propext; none; none; propext.
- **Falsifier**: failure of permission or involution under U, or failure to
  stabilize genesis up to mark renaming.
- **Surviving boundary**: permission and involution hold for every U-state;
  stabilization is claimed at genesis and computed at the bounded
  equal-count placements below.

### B0-REFLECTION-O

- **Statement**: Under reading O the exchange of sides is not a permitted
  renaming or automorphism; it nevertheless fixes genesis as raw regime
  data and moves any placed mark.
- **Status**: DEFINITION (not permitted); PROVED (moves any placed mark).
- **Dependencies**: definitions 2, 4, 12, and 16.
- **Assumptions**: reading O.
- **Python evidence**: receipt `readings.O.reflection_is_permitted_renaming`,
  `readings.O.reflection_is_permitted_automorphism`, and
  `readings.O.reflect_genesis_equals_genesis`;
  `test_reflection_automorphism_at_genesis`.
- **Lean theorem**: `BoundarySeed.reflect_genesis`,
  `BoundarySeed.reflection_not_permitted_O`,
  `BoundarySeed.reflect_moves_a_mark`.
- **Axiom report**: none; propext; propext.
- **Falsifier**: an O-state with a placed mark whose reflection equals it.
- **Surviving boundary**: every O-state.

### B0-EQUAL-COUNTS

- **Statement**: Within zero through four marks, reflection followed by a
  mark renaming fixes exactly the equal-count placements.  The comparison
  is computable under either reading, but is a permitted automorphism only
  under U.
- **Status**: COMPUTED, bound four marks.
- **Dependencies**: definitions 12 to 14.
- **Assumptions**: mark renaming is permitted under both readings.
- **Python evidence**: receipt `reflection_census.fixed_iff_equal_counts`
  and `rows`; `test_census_rows`.
- **Lean theorem**: none; not claimed beyond the bound.
- **Axiom report**: not applicable.
- **Falsifier**: a placement within the bound fixed with unequal counts
  or unfixed with equal counts.
- **Surviving boundary**: the enumerated zero-through-four-mark domain.

### B0-CLASSES

- **Statement**: For each `n` from zero through four, the canonical key sees
  `n + 1` classes under O and `floor(n/2) + 1` under U.
- **Status**: COMPUTED, bound four marks; the closed forms describe the
  table and are not theorems.
- **Dependencies**: definitions 12 to 15.
- **Assumptions**: none beyond the readings.
- **Python evidence**: receipt `reflection_census.rows`; `test_census_rows`.
- **Lean theorem**: none.
- **Axiom report**: not applicable.
- **Falsifier**: a row of the census that departs from the closed form.
- **Surviving boundary**: the enumerated zero-through-four-mark domain.

### B0-CANONICAL-SCOPE

- **Statement**: `canonical` is the implemented minimum over mark
  permutations and, under U, reflection.  No unbounded completeness or
  injectivity theorem is claimed for its keys.
- **Status**: DEFINITION with bounded COMPUTED checks.
- **Dependencies**: definitions 13 to 16 of the paper.
- **Assumptions**: validated Challenge 0 regimes.
- **Python evidence**: `test_canonical_is_invariant_under_mark_renaming`,
  `test_census_rows`; receipt `reflection_census.rows`.
- **Lean theorem**: none.
- **Axiom report**: not applicable.
- **Falsifier**: a failed invariance or class-separation check within the
  declared census bound.
- **Surviving boundary**: zero through four marks.

### B0-BOUNDARY-DEPENDENCE

- **Statement**: The supplied opaque datum, supply inertia, and the empty
  Challenge 0 event-follows relation do not require the admitted boundary.
  All side, placement, name, profile, reflection, collapse, and class-count
  results do require it and are not formulated after removing it.
- **Status**: DEFINITION-level dependency classification.
- **Dependencies**: the seed's per-stage boundary-cost requirement.
- **Assumptions**: removal means deleting the admitted boundary structure,
  not adding a third reading.
- **Python evidence**: receipt `boundary_dependence`;
  `test_initial_datum_and_boundary_dependence_are_explicit`.
- **Lean theorem**: none; the counterfactual boundary-free carrier is not a
  third model in Challenge 0.
- **Axiom report**: not applicable.
- **Falsifier**: a side-specific result expressible after the side structure
  is removed, or loss of the supplied opaque whole merely from that removal.
- **Surviving boundary**: Challenge 0 dependency classification.

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
  *conditionally admitted* mark separating the side profiles under both
  readings, but the prediction is about Challenge 1's still-undeclared
  supply/admission grammar and is scored there.
- **Lean theorem**: none yet.
- **Axiom report**: not applicable.
- **Falsifier**: as written in `challenge0/PREDICTIONS.md`.
- **Surviving boundary**: not yet.
