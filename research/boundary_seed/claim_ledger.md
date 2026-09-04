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
- **Surviving boundary**: all Challenge 0 regimes; every event keeps it
  (B1-INERTIA).

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
  sides (`test_one_mark_separates_the_sides_under_both_readings`; PROVED
  at Challenge 1 as B1-SIDES-U).

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
- **Surviving boundary**: every O-state; the names never change, PROVED
  for every event and history at Challenge 1 (B1-ONE-JUDGMENT).

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
  challenge that adds an event kind re-runs the census.  Challenge 1 added
  no event kind; its census fired on a metatheoretic enumerator placed in
  the kernel, which moved out (B1-CENSUS).

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
- **Surviving boundary**: the closed judgment grammar, unchanged by
  Challenge 1.

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
- **Surviving boundary**: the enumerated zero-through-four-mark domain; the
  `n = 1` row is now realized by admitted candidates (B1-SIDES-U,
  B1-CONVENTION-O).

### B0-CANONICAL-SCOPE

- **Statement**: `canonical` is the implemented minimum over mark
  permutations and, under U, reflection.  No unbounded completeness or
  injectivity theorem is claimed for its keys.
- **Status**: DEFINITION with bounded COMPUTED checks.
- **Dependencies**: definitions 13 to 16 of the paper.
- **Assumptions**: validated regimes.
- **Python evidence**: `test_canonical_is_invariant_under_mark_renaming`,
  `test_census_rows`; receipt `reflection_census.rows`;
  `test_isomorphism_agrees_with_canonical_keys_to_three_marks`.
- **Lean theorem**: none.
- **Axiom report**: not applicable.
- **Falsifier**: a failed invariance or class-separation check within the
  declared census bound, or disagreement with the witness search.
- **Surviving boundary**: zero through four marks; agreement with the
  isomorphism witness to three marks.

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
- **Status**: SCORED at Challenge 1: HIT in both halves.  The U half is
  PROVED (`admitted_sides_differ` against `sides_collapsed_at_genesis_U`,
  with a history of one supply and one admission and no new event kind or
  judgment form); the O half is PROVED (the sides distinct before and
  after; the only new holding judgment is the mark's own side).
- **Dependencies**: the admission grammar Challenge 1 declares (definitions
  19, 21, 24).
- **Assumptions**: the declared presentation convention selects the
  designated candidate; both candidates score identically.
- **Python evidence**: receipt `receipts/challenge1.json` `scores.C0-X`;
  `test_scores`, `test_c0_x_halves_miss_independently`.
- **Lean theorem**: `BoundarySeed.admitted_sides_differ`,
  `BoundarySeed.sides_collapsed_at_genesis_U`,
  `BoundarySeed.admitted_onSide_true_iff`,
  `BoundarySeed.admitted_O_sideNamed`.
- **Axiom report**: propext, Quot.sound; propext, Quot.sound; propext,
  Quot.sound; propext.
- **Falsifier**: as written in `challenge0/PREDICTIONS.md`; neither fired.
- **Surviving boundary**: the Challenge 1 one-mark regimes.

### B1-SUPPLY-PRESENTATION

- **Statement**: Under both readings the supply of `<a|>` is a new external
  presentation event and nothing else: the regime after `Supply(a)` equals
  genesis, the supply-only history certifies genesis, and every judgment
  of the closed grammar holds after the supply exactly when it held
  before.
- **Status**: PROVED (state and judgment clauses); COMPUTED (the certified
  history).
- **Dependencies**: definitions 5, 6, 9, 17, 19.
- **Assumptions**: the read whole's token is what the supply presents; the
  presented side is not carried by the event.
- **Python evidence**: receipt `readings.*.supply`;
  `test_supply_is_presentation_only_under_both_readings`; score C1-1;
  `test_c1_1_misses_when_supply_changes_state`.
- **Lean theorem**: `BoundarySeed.supply_preserves_holds`,
  `BoundarySeed.supply_no_op`.
- **Axiom report**: propext; none.
- **Falsifier**: a judgment whose holding changes across a supply, or a
  supply-only history certifying a regime other than genesis.
- **Surviving boundary**: every regime; independent of the admitted
  boundary.

### B1-ADMISSION-RETENTION

- **Statement**: The mark enters the admitted state only through the
  separately declared admission event; certifying replay refuses it
  without the prior supply and accepts it after.  Once admitted, the
  mark's judgment holds after every later event and every later history:
  a supply, a re-designation on either side (designation, not
  duplication), and a hypothetical second admission all leave it holding.
- **Status**: DEFINITION (the replay precondition and the designation
  convention); PROVED (retention under every event and history).
- **Dependencies**: definitions 5, 6, 9, 21, 24.
- **Assumptions**: the Challenge 1 event grammar; the second admission of
  the retention probe is hypothetical and its token was never supplied by
  the caller.
- **Python evidence**: receipt `readings.*.candidates[*].certified`,
  `unsupplied_admission_refused`, `retention.*`;
  `test_each_candidate_adds_exactly_its_own_judgment`; score C1-2;
  `test_c1_2_misses_on_unsupplied_admission_or_lost_retention`.
- **Lean theorem**: `BoundarySeed.step_preserves_onSide`,
  `BoundarySeed.replay_preserves_onSide`,
  `BoundarySeed.getD_append_left`.
- **Axiom report**: propext; propext; propext.
- **Falsifier**: a supply-only history reaching a placed mark, or a later
  event of the grammar that removes or moves an admitted mark.
- **Surviving boundary**: the event grammar as declared; the side the mark
  is retained on requires the admitted boundary, the discipline does not.

### B1-ONE-JUDGMENT

- **Statement**: After admission, under both readings, exactly one
  judgment holds that did not hold before: `OnSide(0, s)` for the placed
  side; `OnSide(0, s')` for the other side does not hold; every side-name
  judgment holds after every event and history exactly as before (none
  under U, both under O).  The mark's profile is that one judgment.  A
  supply adds no holding judgment.
- **Status**: PROVED; the mark-profile clause is DEFINITION.
- **Dependencies**: definitions 8, 9, 22, 24.
- **Assumptions**: the closed judgment grammar, unchanged.
- **Python evidence**: receipt `candidates[*].new_observations`,
  `mark_profile`, `other_side_judgment_holds`,
  `name_observations_unchanged`, `holding_judgments`; score C1-3;
  `test_c1_3_misses_on_a_second_judgment_or_a_changed_name`;
  `test_mark_profile_is_the_side_and_nothing_else`,
  `test_new_observations_is_the_extension_difference`.
- **Lean theorem**: `BoundarySeed.admitted_onSide_true_iff`,
  `BoundarySeed.place_new_judgment`,
  `BoundarySeed.place_other_side_false`,
  `BoundarySeed.step_preserves_sideNamed`,
  `BoundarySeed.replay_preserves_sideNamed`,
  `BoundarySeed.admitted_U_no_sideNamed`,
  `BoundarySeed.admitted_O_sideNamed`,
  `BoundarySeed.getD_append_singleton`.
- **Axiom report**: propext, Quot.sound; propext, Quot.sound; propext;
  propext; propext; propext; propext; propext.
- **Falsifier**: a second new holding judgment, a changed name judgment,
  or a holding judgment added by supply alone.
- **Surviving boundary**: the closed grammar; the judgment itself requires
  the admitted boundary.

### B1-SIDES-U

- **Statement**: Under U, after admission the two extensional side
  profiles differ; the two candidate regimes (`a` on side 0, on side 1)
  are unequal, each the other's reflection, and related by the permitted
  reflection, so they lie in one isomorphism class; no judgment of the
  bounded domain that is invariant under permitted renamings separates
  them.  “The mark lies on exactly one side” is a U fact; “which side”
  is not.
- **Status**: PROVED (profiles differ; candidates unequal and reflected;
  related; invariant judgments do not separate); COMPUTED (one class and
  the empty invariant-separating list, on the declared bounded domains).
- **Dependencies**: definitions 10 to 12, 16, 23, 24, 26, 27.
- **Assumptions**: reading U; the judgment domain names marks below two
  and the regime domain has at most one mark.
- **Python evidence**: receipt `readings.U.candidate_space`,
  `readings.U.convention.*`; `test_candidate_space_and_classes`,
  `test_separating_judgments_under_each_reading`,
  `test_invariance_under_permitted_renamings`; score C1-4;
  `test_c1_4_misses_when_u_separates_or_splits`.
- **Lean theorem**: `BoundarySeed.admitted_sides_differ`,
  `BoundarySeed.admitted_contents_placed`,
  `BoundarySeed.admitted_contents_other`,
  `BoundarySeed.admitted_candidates_unequal`,
  `BoundarySeed.reflect_admitted`, `BoundarySeed.candidates_related_U`,
  `BoundarySeed.invariant_judgment_does_not_separate`.
- **Axiom report**: propext, Quot.sound; propext, Quot.sound; propext,
  Quot.sound; propext; propext; propext; propext.
- **Falsifier**: equal U profiles after one admitted mark, different U
  keys for the two candidates, or a permitted-renaming-invariant judgment
  holding for one candidate and not the other.
- **Surviving boundary**: the Challenge 1 one-mark U regimes and the
  declared bounded domains; requires the admitted boundary.

### B1-CONVENTION-O

- **Statement**: Under O the inscription `<a|>` does not decide which
  admitted name the left of the bar carries; a presentation convention
  (left is side 0, named `near`) is declared as metatheory.  The two
  candidate regimes are unequal, related by no permitted renaming, and lie
  in two isomorphism classes; the mark's own judgment separates them and
  is invariant under every permitted renaming, there being none but the
  identity at one mark.  The regime under the other convention is the
  reflection of the designated one and is retained as a branch.
- **Status**: DEFINITION (the convention, the designation); PROVED
  (unequal; not related; separated; the other is the reflection);
  COMPUTED (two classes; the retained branch).
- **Dependencies**: definitions 2, 12, 16, 18, 23 to 27.
- **Assumptions**: reading O.
- **Python evidence**: receipt `readings.O.candidate_space`,
  `readings.O.convention.*`, `readings.O.retained_non_isomorphic_candidates`;
  `test_designated_current_is_by_the_declared_convention`,
  `test_conventions_are_the_two_bijections`; score C1-5;
  `test_c1_5_misses_when_o_collapses_or_loses_the_branch`.
- **Lean theorem**: `BoundarySeed.candidates_not_related_O`,
  `BoundarySeed.onSide_separates_candidates`,
  `BoundarySeed.admitted_candidates_unequal`,
  `BoundarySeed.reflect_admitted`.
- **Axiom report**: propext; propext, Quot.sound; propext; propext.
- **Falsifier**: a derivation of the O side of `a` from the inscription
  alone with no declared convention, equal O keys for the two candidates,
  or a designated regime whose reflection is not the other candidate.
- **Surviving boundary**: every O tower from this rung on depends on the
  declared convention; requires the admitted boundary.

### B1-REFLECT-COMMUTES

- **Statement**: The reflection commutes with a supply and carries a
  placement on a side to a placement on the other side.  Hence every
  continuation of the retained O branch is the reflection of a
  continuation of the designated one, and the branch is carried without a
  second tower.
- **Status**: PROVED.
- **Dependencies**: definitions 5, 6, 12.
- **Assumptions**: none.
- **Python evidence**: receipt `convention.other_is_reflection_of_designated`;
  `test_reflect_is_an_involution_and_swaps_sides`.
- **Lean theorem**: `BoundarySeed.reflect_step_supply`,
  `BoundarySeed.reflect_step_place`.
- **Axiom report**: none; propext.
- **Falsifier**: a history whose reflected replay is not the replay of the
  side-exchanged history.
- **Surviving boundary**: every regime and history of the grammar.

### B1-INERTIA

- **Statement**: No event follows from the supplied or admitted regime in
  the declared relation; every event and every history keeps the reading
  and the initial datum; Challenge 1 adds no event kind and no judgment
  form.
- **Status**: PROVED (relation empty; reading and datum kept); DEFINITION
  (no new form, by the unchanged grammars).
- **Dependencies**: definitions 3, 5 to 8.
- **Assumptions**: none.
- **Python evidence**: receipt `candidates[*].event_follows_relation_empty`,
  `initial_datum_unchanged`, `reading_unchanged`, `event_kinds`,
  `observation_vocabulary`; score C1-6;
  `test_c1_6_misses_on_a_following_event_or_a_new_form`.
- **Lean theorem**: `BoundarySeed.no_event_follows_admitted`,
  `BoundarySeed.step_reading`, `BoundarySeed.step_initialDatum`,
  `BoundarySeed.replay_reading`, `BoundarySeed.replay_initialDatum`.
- **Axiom report**: propext; none; none; none; none.
- **Falsifier**: an event in the relation on a Challenge 1 regime, or a
  result requiring a new event kind or judgment form.
- **Surviving boundary**: every regime; independent of the admitted
  boundary.

### B1-ONE-BOUNDARY

- **Statement**: Every Challenge 1 result is stated with the mark placed
  on a side of the one admitted boundary; every certified regime keeps the
  one initial datum and places one mark; no result required admitting the
  whole `<a|>` as a second datum or a second boundary.
- **Status**: DEFINITION-level modelling decision, scored on its
  mechanical part; OPEN as to whether a whole on a side is a datum, which
  Challenge 5 asks.
- **Dependencies**: definitions 1 to 3, 17, 24.
- **Assumptions**: the seed's phrase “the admitted boundary” names the one
  boundary of the initial datum.
- **Python evidence**: receipt `candidates[*].initial_datum_unchanged`,
  `marks`; score C1-7; `test_c1_7_misses_on_a_second_datum_or_mark`.
- **Lean theorem**: `BoundarySeed.replay_initialDatum` (the datum is kept);
  none for the modelling clause.
- **Axiom report**: none.
- **Falsifier**: a Challenge 1 fact that cannot be stated without a second
  datum or a second boundary in the regime.
- **Surviving boundary**: Challenges 0 and 1; reopened at Challenge 5.

### B1-ISO-SCOPE

- **Statement**: The implemented isomorphism relation is the existence of
  a permitted renaming (a mark permutation, and under U the reflection)
  carrying one regime onto another with tokens forgotten, found by
  unpruned search.  It agrees with canonical-key equality over every pair
  of regimes with at most three marks.  The Lean one-mark relatedness is
  sufficient at one mark only.
- **Status**: DEFINITION with bounded COMPUTED checks.
- **Dependencies**: definitions 13 to 16, 23, 27.
- **Assumptions**: validated regimes.
- **Python evidence**: `test_isomorphism_witness_and_relation`,
  `test_permitted_images_count_the_permitted_renamings`,
  `test_isomorphism_agrees_with_canonical_keys_to_three_marks`;
  receipt `convention.isomorphism_witness`.
- **Lean theorem**: `oneMarkRelated` definition; `candidates_related_U`,
  `candidates_not_related_O`.
- **Axiom report**: not applicable; propext; propext.
- **Falsifier**: a pair within the bound where the witness search and the
  canonical key disagree.
- **Surviving boundary**: zero through three marks.

### B1-CENSUS

- **Statement**: The Challenge 0 resolved-annotation census, run per
  module, finds no event-returning public function in the kernel; in the
  presentation module it names the two constructors (`supply_event`,
  `admission_event`); in the challenge module it names the bounded
  enumerator, the probes, and the two imported constructors.  None of
  these is applied to state by anything but `replay` of an explicit
  history.  The census fired live on the enumerator while it lived in the
  kernel; the enumerator moved.
- **Status**: COMPUTED (supplementary API census, not the semantic proof).
- **Dependencies**: B0-INERTIA's census; definition 21.
- **Assumptions**: the census reads module members as they are, imports
  included.
- **Python evidence**: receipt `state_event_generators`,
  `event_returning_functions_by_module`; `test_receipt_shape`,
  `test_no_state_event_generator_in_the_kernel`.
- **Lean theorem**: none; `no_event_follows` is the semantic statement.
- **Axiom report**: not applicable.
- **Falsifier**: an event-returning public function in the kernel, or a
  listed metatheory function that applies its result to state outside
  `replay`.
- **Surviving boundary**: the three modules as of Challenge 1.

### B1-BOUNDARY-DEPENDENCE

- **Statement**: Supply inertia, the admission discipline, the invariance
  of the initial datum and reading, and the empty event-follows relation
  do not require the admitted boundary.  The one new judgment, the
  profiles, the candidates, the convention, and the class counts require
  it and are not formulated after removing it; the side an admitted mark
  is retained on requires it while the retention discipline does not.
- **Status**: DEFINITION-level dependency classification.
- **Dependencies**: the seed's per-stage boundary-cost requirement.
- **Assumptions**: as B0-BOUNDARY-DEPENDENCE.
- **Python evidence**: receipt `boundary_dependence`; `test_receipt_shape`.
- **Lean theorem**: none.
- **Axiom report**: not applicable.
- **Falsifier**: as B0-BOUNDARY-DEPENDENCE.
- **Surviving boundary**: Challenge 1 dependency classification.

### B1-X

- **Statement**: When Challenge 2 supplies and retains `<a|>` and `<|a>`
  as two admitted marks on opposite sides: under U the regime is fixed by
  the reflection up to mark renaming, the two marks are exchanged by a
  permitted automorphism, and no permitted-renaming-invariant judgment of
  the closed grammar separates them; under O the side names separate them
  at the price of the O declaration already paid, with nothing new paid.
- **Status**: OPEN; the extrapolation of Challenge 1, scored by
  Challenge 2.
- **Dependencies**: Challenge 2's treatment of the shared glyph and of
  `Supply`, which carries the token only.
- **Assumptions**: none yet.
- **Python evidence**: none yet.
- **Lean theorem**: none yet.
- **Axiom report**: not applicable.
- **Falsifier**: as written in `challenge1/PREDICTIONS.md`.
- **Surviving boundary**: not yet.
