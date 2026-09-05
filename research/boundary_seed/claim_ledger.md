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
- **Status**: DEFINITION.  The Lean presence theorems `genesis_initial_datum`
  and `genesis_placement_nil` are `rfl` and DEFINITION-level; an earlier
  version called them PROVED, which the rule adopted at the Challenge 1
  review repair, one theorem one label, contradicts; corrected.
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
- **Status**: PROVED (both name judgments hold and the two O profiles differ
  at genesis: `O_name_judgment_at_genesis`, `sides_distinct_at_genesis_O`,
  neither by unfolding); DEFINITION (that the difference is the two admitted
  names and nothing else: `side_names_distinct`, closed by `decide` on two
  constructors).  An earlier version carried one unsplit DEFINITION over all
  three theorems, two of which this run's own labelling rule places in the
  content group and which two sibling entries label PROVED; split here, one
  clause one label, with no result changing.
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
- **Status**: DEFINITION (one supply changes no state, `supply_no_op`, `rfl`;
  a state-changing event is a placement, `step_changes_only_by_place`, a
  case split onto `rfl`; equal histories replay equally,
  `replay_deterministic`, by substitution; the declared relation is empty,
  `no_event_follows`, by unfolding `EventFollows := False`; the Python
  replay precondition); PROVED (a history of supplies replays to its base,
  `replay_supply_inert`, by induction); COMPUTED (the supplementary API
  census).  An earlier version labelled the four unfolding theorems PROVED
  while B1-INERTIA labelled the same relation-empty clause DEFINITION; one
  theorem carries one label, so corrected here.
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
- **Status**: PROVED (involution, `reflect_reflect` through the induction
  `map_not_not`); DEFINITION (permitted, `reflection_permitted_U`, by
  unfolding; fixes genesis, `reflect_genesis`, `rfl`).  An earlier version
  labelled `reflect_genesis` PROVED; corrected.
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
- **Status**: DEFINITION (not permitted, `reflection_not_permitted_O`, by
  unfolding; fixes genesis as raw data, `reflect_genesis`, `rfl`); PROVED
  (moves any placed mark, `reflect_moves_a_mark`).  An earlier version left
  `reflect_genesis` under PROVED by omission; corrected.
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
  `n = 1` row is now realized by certified, not current, candidates
  (B1-SIDES-U, B1-CONVENTION-O, B1-CURRENT-STATE).

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
- **Status**: SCORED at Challenge 1: HIT in both halves.  U half: PROVED
  for the profile clause (collapsed at genesis, `sides_collapsed_at_genesis_U`;
  distinct in every candidate, `admitted_sides_differ`); DEFINITION for the
  history shape (the candidate history is declared as one supply and one
  placement, `admitted_eq` is `rfl`); COMPUTED for “no augmentation beyond
  the admission”, which is the unchanged grammars: a comparison of the
  receipt's `event_kinds`, `observation_vocabulary`, and the candidates'
  `history` kinds against the Challenge 0 declarations in `score_c0x`, not
  a Lean theorem.  O half: PROVED for the profile and judgment clauses
  (distinct before, `sides_distinct_at_genesis_O`; distinct after,
  `admitted_sides_differ`; the only new holding judgment is the mark's own
  side, `admitted_onSide_true_iff`, with the name judgments as at genesis,
  `admitted_O_sideNamed`); COMPUTED for the receipt comparison of
  `new_observations` and `name_observations_unchanged` over every
  candidate.  An earlier version labelled each half PROVED as a whole,
  carrying the grammar clause on a receipt comparison and leaving the O
  “distinct before” theorem uncited; corrected, no result changing.
- **Dependencies**: the admission grammar Challenge 1 declares (definitions
  19, 21, 24).
- **Assumptions**: the prediction is conditional on the mark being
  admitted, so it is scored against every certified candidate; both score
  identically; no candidate is current (B1-CURRENT-STATE).
- **Python evidence**: receipt `receipts/challenge1.json` `scores.C0-X`;
  `test_scores`, `test_c0_x_halves_miss_independently`.
- **Lean theorem**: `BoundarySeed.admitted_sides_differ`,
  `BoundarySeed.sides_collapsed_at_genesis_U`,
  `BoundarySeed.sides_distinct_at_genesis_O`,
  `BoundarySeed.admitted_onSide_true_iff`,
  `BoundarySeed.admitted_O_sideNamed`, `BoundarySeed.admitted_eq`
  (DEFINITION-level); none for the grammar clause.
- **Axiom report**: propext, Quot.sound; propext, Quot.sound; propext,
  Quot.sound; propext, Quot.sound; propext; none.
- **Falsifier**: as written in `challenge0/PREDICTIONS.md`; neither fired.
- **Surviving boundary**: the Challenge 1 one-mark regimes.

### B1-SUPPLY-PRESENTATION

- **Statement**: Under both readings the supply of `<a|>` is a new external
  presentation event and nothing else: the regime after `Supply(a)` equals
  genesis, the supply-only history certifies genesis, and every judgment
  of the closed grammar holds after the supply exactly when it held
  before.
- **Status**: DEFINITION (one supply changes no state and no judgment, by
  unfolding `step`: `supply_no_op`, `supply_preserves_holds` are `rfl`);
  PROVED (a history of supplies replays to its base, by induction:
  `replay_supply_inert`); COMPUTED (the certified supply-only history).
  An earlier version labelled the two `rfl` theorems PROVED, which the
  paper's own DEFINITION-level list contradicted; corrected.
- **Dependencies**: definitions 5, 6, 9, 17, 19.
- **Assumptions**: the read whole's token is what the supply presents; the
  presented side is not carried by the event.
- **Python evidence**: receipt `readings.*.supply`;
  `test_supply_is_presentation_only_under_both_readings`; score C1-1
  (HIT, DEFINITION-level, not counted as content: every clause of the
  frozen text rests on the `rfl` facts above, `scores.C1-1.result_basis`,
  `tally.hit_definition_level`;
  `test_tally_counts_definition_level_hits_apart_from_content`);
  `test_c1_1_misses_when_supply_changes_state`.
- **Lean theorem**: `BoundarySeed.supply_no_op`,
  `BoundarySeed.supply_preserves_holds` (both DEFINITION-level);
  `BoundarySeed.replay_supply_inert`.
- **Axiom report**: none; propext; none.
- **Falsifier**: a judgment whose holding changes across a supply, or a
  supply-only history certifying a regime other than genesis.
- **Surviving boundary**: every regime; independent of the admitted
  boundary.

### B1-CURRENT-STATE

- **Statement**: The current state after a challenge is the replay of the
  caller's history and of no event the caller's history does not contain.
  At Challenge 1 the caller supplies and does not retain, so under each
  reading the current state is the replay of `[Supply(a)]`, which
  certifies and equals genesis; that `a` is supplied is a fact of that
  history, and a regime carries no supplied component.  No admission
  event is in the caller's history at this challenge; the
  two one-step admission candidates are certified candidate histories,
  every isomorphism class of them is kept as a certified branch (one under
  U, two under O), keeping admits nothing, and none is current.  The
  declared convention selects which candidate the presented side licenses
  if admission is later called for, and admits nothing.
- **Status**: DEFINITION (the designation rule and the convention's
  selection; the supply-only history `[Supply(a)]` replays to genesis by
  unfolding `step`, the n = 1 instance of `replay_supply_inert`, which is
  `rfl`); COMPUTED (the certified histories and classes).  An earlier
  version labelled that one-supply instance PROVED while
  B1-SUPPLY-PRESENTATION labelled the same fact DEFINITION; corrected,
  PROVED being reserved for the history-of-supplies theorem.
  An earlier version designated the convention's admitted candidate as
  current with no admission event from the caller; that conflated supply
  with admission, turned a model proposal into an admitted state change,
  and is WITHDRAWN.  A later version described the current state as
  “genesis with `a` presented” and called the kept candidate classes
  retained; the first read the supply into a regime that carries no such
  component, the second used retained in a sense other than the placement
  tuple of B1-ADMISSION-RETENTION, and both are WITHDRAWN (paper section 1
  and definition 25).  A third version wrote the rule and its falsifier
  with “supply” in a second, undeclared sense, the caller providing any
  event including an admission, which is not the `Supply` event of
  definition 5; reworded, the word now naming that event and the seed's
  quoted “supplies” only.
- **Dependencies**: definitions 5, 6, 18, 21, 24, 25.
- **Assumptions**: “supplies” at Challenge 1 licenses no admission; what
  “retains” licenses at Challenge 2, and who pays, is Challenge 2's first
  decision.
- **Python evidence**: receipt `readings.*.current_state`,
  `readings.*.candidate_classes`, `readings.*.convention.candidate_event`,
  `readings.*.convention.selection_is_by`;
  `test_current_state_is_the_replay_of_the_supplied_only_history`,
  `test_convention_selects_a_candidate_and_admits_nothing`,
  `test_candidate_space_and_classes`,
  `test_candidate_classes_group_by_canonical_key`.
- **Lean theorem**: `BoundarySeed.replay_supply_inert` at n = 1 (the state
  clause, DEFINITION-level); none for the designation rule, which is a
  declaration.
- **Axiom report**: none.
- **Falsifier**: a current state after Challenge 1 whose history contains
  an event the caller's history does not contain — an admission event in
  particular, none being in the caller's history at this challenge — or a
  candidate class dropped without a proof eliminating it.
- **Surviving boundary**: every challenge; independent of the admitted
  boundary.

### B1-ADMISSION-RETENTION

- **Statement**: The mark enters the admitted state only through the
  separately declared admission event, which no history of the caller's
  contains at Challenge 1; certifying replay refuses it without the prior
  supply and accepts it after.  In a certified candidate, once admitted
  the mark's judgment holds after every later event and every later
  history of the Lean grammar (a supply, a new placement); in the Python
  kernel a re-admission of the token on its own side is a no-op and a
  re-admission naming the other side is refused because it would move the
  mark; a hypothetical second admission of another token leaves the
  judgment holding.
- **Status**: DEFINITION (the replay precondition; the same-side no-op and
  the moving-admission refusal, Python-only because the Lean events carry
  no token); PROVED (retention under every event and history of the Lean
  grammar).  An earlier version called the same-side no-op a designation,
  absorbed a re-admission naming the other side as a no-op with its side
  discarded, so that the falsifier “an event that moves the admitted mark”
  could not fire by construction, and cited the Lean retention theorems
  for that Python-only behaviour; all three are WITHDRAWN.  The frozen
  C1-2 parenthetical predicted that absorption; under the repaired kernel
  it is false as written, and a later version labelled it SHARPENED from
  the overall score with no clause fact, which is WITHDRAWN too: the
  clause is a literal miss, recorded next to its value, and C1-2 is
  PARTIAL by the rule that scored C1-4.
- **Dependencies**: definitions 5, 6, 9, 21, 24.
- **Assumptions**: the Challenge 1 event grammar; the second admission of
  the retention probe is hypothetical and its token was never supplied by
  the caller.
- **Python evidence**: receipt `readings.*.candidates[*].certified`,
  `unsupplied_admission_refused`, `retention.*` (in particular
  `moving_admission_refused`, `moving_admission_refusal`,
  `moving_admission_accepted_and_inert`,
  `regime_unchanged_by_supply_and_readmission`);
  `test_each_candidate_adds_exactly_its_own_judgment`,
  `test_readmission_on_its_side_is_a_no_op`,
  `test_moving_admission_is_refused_by_name`,
  `test_refusal_names_the_refused_history_and_is_silent_otherwise`,
  `test_moving_admission_fact_reads_accepted_and_inert_only_when_the_kernel_absorbs`;
  score C1-2 (PARTIAL: `facts_status: HIT`,
  `either_side_readmission_clause_status: MISSED`; see
  `challenge1/STATUS.md`);
  `test_c1_2_misses_on_unsupplied_admission_or_lost_retention`,
  `test_c1_2_misses_when_a_moving_admission_is_accepted_and_moves_the_mark`,
  `test_c1_2_either_side_clause_hits_only_when_every_moving_admission_is_accepted_and_inert`.
- **Lean theorem**: `BoundarySeed.replay_preserves_onSide`,
  `BoundarySeed.step_preserves_onSide`, `BoundarySeed.getD_append_left`
  (supplies and new placements only).
- **Axiom report**: propext; propext; propext.
- **Falsifier**: a supply-only history reaching a placed mark, or an
  accepted later event of the grammar that removes or moves an admitted
  mark; the moving admission is now refused rather than absorbed, so the
  second falsifier is testable and does not fire.
- **Surviving boundary**: the event grammar as declared; the side the mark
  is retained on requires the admitted boundary, the discipline does not.

### B1-ONE-JUDGMENT

- **Statement**: After admission, under both readings, exactly one
  judgment holds that did not hold before: `OnSide(0, s)` for the placed
  side; `OnSide(0, s')` for the other side does not hold; every side-name
  judgment holds after every event and history exactly as before (none
  under U, both under O).  The mark's profile is that one judgment.  A
  supply adds no holding judgment.
- **Status**: PROVED (the one new judgment and its evaluation at the
  candidates: `admitted_onSide_true_iff`, `place_new_judgment`,
  `place_other_side_false`, `admitted_U_no_sideNamed`,
  `admitted_O_sideNamed`; every history keeps every side-name judgment:
  `replay_preserves_sideNamed`); DEFINITION (one event keeps a side-name
  judgment, `step_preserves_sideNamed`, by unfolding; the mark-profile
  clause; **a supply adds no holding judgment**, `supply_preserves_holds`,
  which is `rfl`, so the clause is true by unfolding `step` and is not
  counted as content).  An earlier version counted `step_preserves_sideNamed`
  as content; corrected.  An earlier version also left the supply clause of
  the statement with no status in this field and no theorem in the Lean list,
  against the rule that every clause of a ledger statement carries a status;
  added here, with no result changing.
- **Dependencies**: definitions 8, 9, 22, 24.
- **Assumptions**: the closed judgment grammar, unchanged.
- **Python evidence**: receipt `candidates[*].new_observations`,
  `mark_profile`, `other_side_judgment_holds`,
  `name_observations_unchanged`, `holding_judgments`; score C1-3 (HIT,
  counted as content: its one-judgment clauses rest on
  `admitted_onSide_true_iff`, `place_new_judgment`, and
  `place_other_side_false`; its name clause, read per event as the frozen
  text has it, is `step_preserves_sideNamed`, DEFINITION-level, exactly as
  C1-6's parallel clause was scored, the induction
  `replay_preserves_sideNamed` being this rung's addition; its supply
  clause alone is DEFINITION-level; `scores.C1-3.result_basis`,
  `tally.hit_as_content`; an earlier basis attributed the name clause to
  the induction and is corrected, no status changing);
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
  `BoundarySeed.getD_append_singleton`,
  `BoundarySeed.supply_preserves_holds` (the supply clause, DEFINITION-level).
- **Axiom report**: propext, Quot.sound; propext, Quot.sound; propext;
  propext; propext; propext; propext; propext; propext.
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
  them.  “The mark lies on exactly one side” is a metatheoretic statement
  about the closed grammar, PROVED: in each candidate exactly one `OnSide`
  judgment holds, mark 0 on the placed side (`admitted_onSide_true_iff`),
  where none held at genesis (`no_observation_at_genesis`), and it holds
  at both candidates, so the reflection does not disturb it; the closed
  grammar has no judgment expressing “exactly one side”, so it is a U fact
  of the metatheory and not an internal judgment.  “Which side” is not a
  U fact.
- **Status**: PROVED (profiles differ; candidates unequal;
  the exactly-one-side clause as a metatheoretic statement,
  `admitted_onSide_true_iff` with `no_observation_at_genesis`, which an
  earlier version carried with no status, evidence, or theorem; a
  judgment invariant under the reflection at every regime of the reading
  with at most one mark holds equally at the two candidates,
  `bounded_invariant_judgment_does_not_separate`, whose hypothesis is
  definition 26's bounded invariance under U because at one mark the
  permitted renamings are the identity and the reflection — that
  identification is by inspection of `permitted_images`, not a Lean
  theorem; the global-hypothesis `invariant_judgment_does_not_separate` is
  kept and closes less); DEFINITION (`candidates_related_U` as a whole:
  its permission half is `reflectionPermitted .U := True` and its
  reflection half is `reflect_admitted`, which is `rfl`, both sides
  reducing to the one-element placement; an earlier version called
  `reflect_admitted` the theorem's content and proved it by `simp`, whose
  `propext` it then carried); COMPUTED (one class and the empty
  invariant-separating list over the eight-judgment domain).  An earlier
  version rested the bounded-domain clause on the global-hypothesis
  theorem alone: a judgment such as `OnSide(1, s)` is invariant on the
  one-mark domain without being invariant everywhere, so that theorem said
  nothing about it and only the computation did; corrected by the bounded
  theorem.
- **Dependencies**: definitions 10 to 12, 16, 23, 24, 26, 27.
- **Assumptions**: reading U; the judgment domain names marks below two
  and the regime domain has at most one mark.
- **Python evidence**: receipt `readings.U.candidate_space`,
  `readings.U.candidate_classes`, `readings.U.convention.*`;
  `test_candidate_space_and_classes`,
  `test_separating_judgments_under_each_reading`,
  `test_invariance_under_permitted_renamings`; score C1-4 (PARTIAL: its
  “only event in the history” clause is scored literally, see
  `challenge1/STATUS.md`); `test_c1_4_misses_when_u_separates_or_splits`,
  `test_c1_4_only_event_clause_is_scored_literally`.
- **Lean theorem**: `BoundarySeed.admitted_sides_differ`,
  `BoundarySeed.admitted_contents_placed`,
  `BoundarySeed.admitted_contents_other`,
  `BoundarySeed.admitted_candidates_unequal`,
  `BoundarySeed.reflect_admitted`, `BoundarySeed.candidates_related_U`,
  `BoundarySeed.invariant_judgment_does_not_separate`,
  `BoundarySeed.bounded_invariant_judgment_does_not_separate`,
  `BoundarySeed.admitted_onSide_true_iff`,
  `BoundarySeed.no_observation_at_genesis`.
- **Axiom report**: propext, Quot.sound; propext, Quot.sound; propext,
  Quot.sound; propext; none; none; propext; propext; propext,
  Quot.sound; propext.
- **Falsifier**: equal U profiles after one admitted mark, different U
  keys for the two candidates, or a permitted-renaming-invariant judgment
  holding for one candidate and not the other.
- **Surviving boundary**: the Challenge 1 one-mark U regimes and the
  declared bounded domains; requires the admitted boundary.

### B1-CONVENTION-O

- **Statement**: Under O the inscription `<a|>` does not decide which
  admitted name the left of the bar carries; a presentation convention
  (left is side 0, named `near`) is declared as metatheory, selects the
  candidate admission the presented side licenses, and admits nothing.
  The two candidate regimes are unequal, related by no permitted renaming,
  and lie in two isomorphism classes; the mark's own judgment separates
  them and is invariant under every permitted renaming, there being none
  but the identity at one mark.  The candidate under the other convention
  is the reflection of the convention's candidate; both classes are
  kept as certified branches, and neither is current.  The frozen clause's
  bare word designation is read as this selection, as the paper's section 1
  declares; the run reserves designation for current-state designation in
  its own prose, and the two readings are stated together so that one word
  does not carry two undeclared senses.
- **Status**: DEFINITION (the convention and its selection; the other
  candidate is the reflection of it, `reflect_admitted`, which is `rfl`,
  relabelled from PROVED); PROVED (unequal,
  `admitted_candidates_unequal`; the one-mark relation does not relate them,
  `candidates_not_related_O`, whose permission half is by unfolding
  `reflectionPermitted .O := False` so that under O the relation is raw
  inequality; the mark's own judgment separates them as raw data,
  `onSide_separates_candidates`); COMPUTED (related by no permitted
  renaming in the general relation with mark permutations, over the
  unpruned `permitted_images` search: `isomorphic_under_reading = false`,
  `isomorphism_witness = null`; two classes; both kept; the judgment's
  invariance on the bounded domain).  An earlier version labelled “related
  by no permitted renaming” PROVED on `candidates_not_related_O`, whose
  adequacy for the general relation is prose plus a Python test; split as
  above.
- **Dependencies**: definitions 2, 12, 16, 18, 23 to 27.
- **Assumptions**: reading O.
- **Python evidence**: receipt `readings.O.candidate_space`,
  `readings.O.candidate_classes`, `readings.O.convention.*`;
  `test_convention_selects_a_candidate_and_admits_nothing`,
  `test_candidate_space_and_classes`,
  `test_conventions_are_the_two_bijections`,
  `test_permitted_images_count_the_permitted_renamings`,
  `test_isomorphism_witness_and_relation`; score C1-5 (HIT, counted as
  content: `facts_status`; `convention_clause_status`, which pins the
  frozen convention literally — `declared`, its left side, the candidate
  event's side, and `side_0_name_under_O` — so that the other convention
  scores it MISSED; and `designation_clause_status`, scored on the frozen
  words from `selection_is_by` and `other_is_reflection_of_candidate`;
  `scores.C1-5.result_basis`, `tally.hit_as_content`; an earlier version
  scored a clause “current-state designation of the admitted candidate”
  MISSED and reported PARTIAL, words the frozen text does not contain,
  WITHDRAWN, see `challenge1/STATUS.md`);
  `test_c1_5_misses_when_o_collapses_or_loses_the_branch`,
  `test_c1_5_designation_clause_is_scored_on_the_frozen_words`,
  `test_c1_5_convention_clause_misses_under_the_other_convention`.
- **Lean theorem**: `BoundarySeed.candidates_not_related_O`,
  `BoundarySeed.onSide_separates_candidates`,
  `BoundarySeed.admitted_candidates_unequal`,
  `BoundarySeed.reflect_admitted`.
- **Axiom report**: propext; propext, Quot.sound; propext; none.
- **Falsifier**: a derivation of the O side of `a` from the inscription
  alone with no declared convention, equal O keys for the two candidates,
  a permitted renaming found by the unpruned search, or a convention's
  candidate whose reflection is not the other candidate.
- **Surviving boundary**: every O tower from this rung on depends on the
  declared convention; requires the admitted boundary.

### B1-REFLECT-COMMUTES

- **Statement**: The reflection commutes with a supply and carries a
  placement on a side to a placement on the other side; by induction over
  histories, the reflection of a replayed history is the replay of the
  side-exchanged history from the reflected base.  Hence every
  continuation of the second O candidate class is the reflection of a
  continuation of the first, and that class is carried without a second
  tower.
- **Status**: PROVED (`reflect_replay`, by induction, and its corollaries
  `continuation_reflects` and `other_continuation_is_a_reflection`;
  `reflect_step_place`, by `simp` with the map of a placement over an
  append, carrying `propext`; `reflect_step`, a case split whose place
  branch is `reflect_step_place`; `exchangeSide_exchangeSide` and
  `map_exchangeSide_map_exchangeSide`, the involution lemmas);
  DEFINITION (the step lemma `reflect_step_supply`, `rfl`).  An earlier
  version was PROVED on the two step lemmas alone, with the history-level
  “hence” a prose step and a Python test that checked only an involution;
  the replay-level theorem and a replay-commutation test now carry it.  A
  later version listed `reflect_step` as DEFINITION and left
  `reflect_step_place` and the two involution lemmas with no label;
  corrected, no result changing.
- **Dependencies**: definitions 5, 6, 12, 24, 28.
- **Assumptions**: none.
- **Python evidence**: receipt `convention.other_is_reflection_of_candidate`;
  `test_reflect_commutes_with_replay` (every history of up to three events
  over two tokens from genesis under both readings: 86 accepted histories
  commute, and every refused history is refused side-exchanged);
  `test_reflect_is_an_involution_and_swaps_sides`.
- **Lean theorem**: `BoundarySeed.reflect_replay`,
  `BoundarySeed.continuation_reflects`,
  `BoundarySeed.other_continuation_is_a_reflection`,
  `BoundarySeed.reflect_step`, `BoundarySeed.reflect_step_place`,
  `BoundarySeed.reflect_step_supply`,
  `BoundarySeed.exchangeSide_exchangeSide`,
  `BoundarySeed.map_exchangeSide_map_exchangeSide`.
- **Axiom report**: propext; propext; propext; propext; propext; none;
  propext; propext.
- **Falsifier**: a history whose reflected replay is not the replay of the
  side-exchanged history.
- **Surviving boundary**: every regime and history of the Lean grammar;
  in Python, every accepted history within the tested bound.

### B1-INERTIA

- **Statement**: No event follows from the supplied or candidate regime in
  the declared relation; every event and every history keeps the reading
  and the initial datum; Challenge 1 adds no event kind and no judgment
  form.
- **Status**: DEFINITION (the relation is empty by unfolding
  `EventFollows := False`, and `no_event_follows_admitted` is a bare
  instantiation of `no_event_follows`; one event keeps the reading and
  datum, `step_reading` and `step_initialDatum`, by unfolding; no new
  form, by the unchanged grammars); PROVED (every history keeps the
  reading and datum: `replay_reading`, `replay_initialDatum`, by
  induction).  An earlier version labelled the relation-empty and step
  clauses PROVED; corrected.
- **Dependencies**: definitions 3, 5 to 8.
- **Assumptions**: none.
- **Python evidence**: receipt `candidates[*].event_follows_relation_empty`,
  `initial_datum_unchanged`, `reading_unchanged`, `event_kinds`,
  `observation_vocabulary`; score C1-6 (HIT, DEFINITION-level, not
  counted as content: the frozen text's relation clause is the empty
  relation by unfolding, its “unchanged by every event” clause is the
  step lemmas by unfolding, and its grammar clause is the census of the
  run's own declarations, a modelling decision as C1-7's;
  `scores.C1-6.result_basis`, `tally.hit_definition_level`);
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
  on a side of the one admitted boundary; every certified candidate regime
  keeps the one initial datum and places one mark; no result required
  admitting the whole `<a|>` as a second datum or a second boundary.  An
  earlier version wrote “every certified regime”, which is false of the
  current state: it is certified and places none, the scorer reading only
  the candidates; narrowed.
- **Status**: DEFINITION-level modelling decision, scored on its
  mechanical part, which holds by construction: the `Regime` type
  represents neither a second datum nor a second boundary, so
  `initial_datum_unchanged` cannot be reported false, and `marks == 1` is a
  proxy reading “the mark placed on a side” as exactly one placed mark,
  which the frozen text does not name.  C1-7 is therefore HIT by
  construction and not counted as content in the tally; an earlier version
  counted it among the hits.  OPEN as to whether a whole on a side is a
  datum, which Challenge 5 asks.
- **Dependencies**: definitions 1 to 3, 17, 24.
- **Assumptions**: the seed's phrase “the admitted boundary” names the one
  boundary of the initial datum.
- **Python evidence**: receipt `candidates[*].initial_datum_unchanged`
  (fixed by the type), `marks` (the proxy); score C1-7 (`result_basis`,
  `mechanical_part`); `test_c1_7_misses_on_a_second_datum_or_mark`.
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
  intended for one mark only; that adequacy is prose, and under O the
  relation reduces to raw inequality by unfolding, so no Lean theorem
  about it is a theorem about the general relation.
- **Status**: DEFINITION with bounded COMPUTED checks.
- **Dependencies**: definitions 13 to 16, 23, 27.
- **Assumptions**: validated regimes.
- **Python evidence**: `test_isomorphism_witness_and_relation`,
  `test_permitted_images_count_the_permitted_renamings`,
  `test_isomorphism_agrees_with_canonical_keys_to_three_marks`;
  receipt `convention.isomorphism_witness`.
- **Lean theorem**: `oneMarkRelated` definition; `candidates_related_U`,
  `candidates_not_related_O`.
- **Axiom report**: not applicable; none; propext.
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

- **Statement**: Supply inertia, the admission discipline, the rule that
  the current state is the replay of the caller's history, the invariance
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
- **Status**: SCORED at Challenge 2: PARTIAL.  U half HIT, and PROVED or
  COMPUTED clause by clause: the retained regime is fixed by the reflection
  up to mark renaming (COMPUTED, `fixed_by_reflection_up_to_mark_renaming`),
  a permitted automorphism exchanges the two marks (COMPUTED over the
  unpruned search; the composite itself is `exchangeMarks_reflect_retained`,
  DEFINITION-level, and what it carries is `retained_exchange_transports`,
  PROVED), and no permitted-renaming-invariant mark form separates them
  (COMPUTED over the bounded domain).  O half PARTIAL: the names clause HIT
  (COMPUTED that the only O automorphism is the identity, with the raw
  separation PROVED by `retained_marks_separated_by_a_side`); the clause
  “the price is the O declaration paid at genesis, and nothing new is paid
  at Challenge 2” MISSED, and its own falsifier, “under O a price beyond the
  names”, fired: the occurrence identity of B2-IDENTITY-POLICY is a new
  declaration paid at this rung, under both readings.  The frozen condition,
  that Challenge 2 admits two internal identities for the two wholes despite
  the shared visible mark, was met.  Recorded next to its value here and in
  `challenge2/STATUS.md`; the frozen file is untouched.
- **Dependencies**: Challenge 2's treatment of the shared visible mark
  (B2-IDENTITY-POLICY) and of `Supply`, which carries the token only.
- **Assumptions**: the clauses are scored on the frozen words; the price
  clause is scored against the receipt's `price.nothing_new_paid_at_challenge_2`.
- **Python evidence**: receipt `receipts/challenge2.json` `scores.C1-X`;
  `test_scores`, `test_c1_x_halves_and_clauses_score_independently`.
- **Lean theorem**: `BoundarySeed.retained_exchange_transports`,
  `BoundarySeed.retained_marks_separated_by_a_side`,
  `BoundarySeed.exchangeMarks_reflect_retained` (DEFINITION-level); none for
  the automorphism counts or the price, which are computations and
  declarations.
- **Axiom report**: propext; propext; propext.
- **Falsifier**: as written in `challenge1/PREDICTIONS.md`; the O price
  falsifier fired.
- **Surviving boundary**: the Challenge 2 retained regime.

### B2-RETENTION

- **Statement**: The caller's “retains” at Challenge 2 is read as the
  admission of both wholes: the caller's history contains, for each whole,
  a `Supply` and an admission, and the current state under each reading is
  the replay of that history, a regime with two marks on opposite sides
  under the declared convention.  The two supplies are the same event value
  twice, separated only by their position, and change nothing.  This is the
  first rung at which the caller's history contains an admission.
- **Status**: DEFINITION (the reading of the word, definition 30, and the
  placement that follows from the declared convention and the declared
  identity policy); COMPUTED (the certified history and its replay from
  genesis).  Not counted as content: score C2-1 is HIT by construction
  (`scores.C2-1.result_basis`, `tally.hit_definition_level`).
- **Dependencies**: definitions 5, 6, 18, 19, 25, 30, 31.
- **Assumptions**: the run could instead have refused the challenge and
  recorded it OPEN; that alternative is stated in the paper's 5.5 and is
  not taken.
- **Python evidence**: receipt `readings.*.retained`;
  `test_the_retained_state`,
  `test_every_certified_history_replays_from_genesis`;
  `test_c2_1_misses_on_a_state_with_fewer_marks_or_a_shared_side`.
- **Lean theorem**: `BoundarySeed.retained_eq`,
  `BoundarySeed.retained_placement_length`,
  `BoundarySeed.retained_without_supplies` (all DEFINITION-level, `rfl`).
- **Axiom report**: none; none; none.
- **Falsifier**: a current state after Challenge 2 with fewer than two
  admitted marks, a state change with no admission event in the caller's
  history, or two marks on the same side under the declared convention.
- **Surviving boundary**: Challenge 2 onward; the side each mark is
  retained on requires the admitted boundary, the reading of the word does
  not.

### B2-SHARED-MARK-REFUSED

- **Statement**: With the Challenge 1 token-keyed admission event, the
  caller's Challenge 2 history is refused by certifying replay, under both
  readings and under both conventions, by the moving-admission refusal
  naming the side the mark is admitted on: that event keys the admitted
  mark by its presentation token, so the second whole names the first mark
  and asks for it on the other side.
- **Status**: DEFINITION (the Challenge 1 declaration replayed on a
  declared history; four histories, all refused); not counted as content,
  score C2-2 being HIT by construction, although the declaration was made
  at Challenge 1 and before this question arose.
- **Dependencies**: definitions 3, 6, 18, 30, 31; B1-ADMISSION-RETENTION.
- **Assumptions**: the caller's history is formed by the declared reader
  and one of the two declared conventions.
- **Python evidence**: receipt `readings.*.identity_policies.rows`;
  `test_the_declared_policy_is_the_only_one_that_retains_both`,
  `test_the_two_identity_policies_disagree_on_the_callers_history`,
  `test_c2_2_misses_when_the_shared_policy_is_accepted_or_refused_otherwise`.
- **Lean theorem**: none; the Lean events carry no token, so this refusal
  is not formulable there.
- **Axiom report**: not applicable.
- **Falsifier**: that history certifying a two-mark regime; a refusal for
  some other reason; or the refusal depending on the reading or the
  convention.
- **Surviving boundary**: the token-keyed admission event, wherever it is
  offered a history that names an admitted token on the other side.

### B2-IDENTITY-POLICY

- **Statement**: The declared space of identity policies has exactly two
  members — the second admission names the mark already admitted, or it
  admits a fresh one — and it is exhaustive over the caller's two wholes
  because the second admission's target either is or is not already
  admitted.  Exactly one member lets the caller retain both wholes.  The
  run declares that one, the occurrence identity, at the price of one new
  admission event, `AdmitOccurrence`, and the withdrawal of definition 3's
  repeated-label rule, and with it the withdrawal of the identification of
  presentation identity with internal identity.  The price is paid by the
  run, not by the boundary and not by the caller, and is the same under
  both readings.  It buys that the caller's two wholes are two marks at
  all.
- **Status**: DEFINITION (the space, its exhaustiveness over that question,
  the declared policy, and the price); COMPUTED (that exactly one member
  admits both wholes, over the four policy-and-convention histories).  Not
  counted as content, score C2-3 being HIT by construction.  The
  uniqueness is **scoped to the declared space** and is not a claim that no
  other treatment of the shared visible mark exists; a policy that changed
  the event grammar further is outside it.
- **Dependencies**: definitions 3, 5, 6, 31; B2-SHARED-MARK-REFUSED.
- **Assumptions**: a policy decides only what the second admission admits.
- **Python evidence**: receipt `readings.*.identity_policies`,
  `readings.*.price`;
  `test_the_declared_policy_is_the_only_one_that_retains_both`,
  `test_the_price_is_one_new_declaration_paid_by_the_run`,
  `test_policy_event_and_caller_history`,
  `test_c2_3_misses_on_a_third_policy_or_a_free_retention`;
  kernel: `test_occurrence_admission_admits_a_fresh_mark_whatever_the_label`,
  `test_a_repeated_label_is_a_valid_regime_from_challenge_2`,
  `test_token_keyed_admission_refuses_a_repeated_label_by_name`,
  `test_occurrence_admission_refuses_an_unsupplied_token_by_name`.
- **Lean theorem**: none; the Lean `place` was already occurrence-keyed,
  because its events carry no token, so the policy question does not arise
  there and no Lean theorem is evidence for it.
- **Axiom report**: not applicable.
- **Falsifier**: a third policy inside the declared space; the caller's
  retention expressible with no new declaration; a price differing between
  the readings; or the boundary rather than the run paying it.
- **Surviving boundary**: Challenge 2 onward; every later rung inherits the
  occurrence identity and the withdrawn repeated-label rule.

### B2-TWO-JUDGMENTS

- **Statement**: The two admissions add exactly two holding judgments,
  `OnSide(0, s)` and `OnSide(1, s')` with `s` and `s'` the two sides, and
  change no name judgment, no initial datum, and no reading; the count of
  holding judgments goes 0 to 2 under U and 2 to 4 under O; each mark's
  profile is its own side and nothing else; no new judgment form is needed;
  and each retained mark's judgment survives every later event and history
  of the Lean grammar.
- **Status**: PROVED (which judgments hold: `retained_onSide_true_iff` with
  `retained_onSide_zero`, `retained_onSide_one`, `retained_onSide_beyond`);
  DEFINITION (retention: `retained_judgments_survive`, an instantiation of
  the Challenge 1 induction, which is itself PROVED as B1-ADMISSION-RETENTION
  records; the names as at genesis: `retained_sideNamed`, likewise an
  instantiation); COMPUTED (the counts, the profiles, and the growth probe).
  Counted as content: score C2-4.
- **Dependencies**: definitions 8, 9, 22, 30, 31.
- **Assumptions**: the closed judgment grammar, unchanged at this rung.
- **Python evidence**: receipt `readings.*.retained.new_observations`,
  `holding_judgments_*`, `later_events`,
  `readings.*.separation.mark_profiles`; `test_the_retained_state`,
  `test_c2_4_misses_on_a_third_judgment_or_a_changed_name`.
- **Lean theorem**: `BoundarySeed.retained_onSide_true_iff`,
  `BoundarySeed.retained_onSide_zero`, `BoundarySeed.retained_onSide_one`,
  `BoundarySeed.retained_onSide_beyond`,
  `BoundarySeed.retained_judgments_survive`,
  `BoundarySeed.retained_sideNamed`.
- **Axiom report**: propext, Quot.sound; propext; propext; propext;
  propext; propext.
- **Falsifier**: a third new holding judgment, a changed name judgment, a
  changed datum or reading, or a Challenge 2 fact needing a new judgment
  form.
- **Surviving boundary**: the retained two-mark regime; the judgments
  themselves require the admitted boundary.

### B2-MARKS-U

- **Statement**: Under U the retained regime has exactly two permitted
  automorphisms, the identity and the reflection followed by the exchange
  of the two marks; that non-identity one carries mark 0 to mark 1, and it
  is the same renaming that exchanges the two sides.  Neither mark form is
  invariant under the permitted renamings of U on the bounded domain, so no
  invariant mark form separates the two retained wholes, and by definition
  33 they are not internally separable under U.  The Challenge 0 profile
  comparison `sides_collapsed` is false at that regime and is not the
  internal fact, because it reads internal identities that a permitted
  renaming permutes; the two sides, unequal after Challenge 1's one mark,
  are exchanged by a permitted automorphism once both wholes are retained.
- **Status**: COMPUTED (the automorphism count, the exchanging witness, the
  side-exchanging witness, and the invariance census over the bounded
  domain, all over the unpruned `permitted_images` enumeration); PROVED
  (what the composite carries: `retained_exchange_transports`; that neither
  half fixes the regime alone: `reflect_retained_ne`,
  `exchangeMarks_retained_ne`); DEFINITION (that the composite fixes the
  regime: `exchangeMarks_reflect_retained`, which is `rfl`; and its
  permission under U: `retained_composite_permitted_U`).  Counted as
  content: scores C2-5 and C2-8.  **Lean does not close the automorphism
  count**; it exhibits the composite and the two non-fixings, which is
  weaker.
- **Dependencies**: definitions 12, 13, 16, 23, 29, 32, 33, 34, 36.
- **Assumptions**: reading U; the regime domain has at most two marks.
- **Python evidence**: receipt `readings.U.automorphisms`,
  `readings.U.separation`, `readings.U.retained.sides_collapsed`;
  `test_automorphisms_and_separation_under_each_reading`,
  `test_the_one_non_identity_U_automorphism_does_both_exchanges`,
  `test_automorphisms_match_an_unpruned_filter_of_the_images`,
  `test_mark_form_invariance_is_a_census_over_the_declared_domain`,
  `test_marks_are_separable_under_O_and_exchanged_under_U`,
  `test_side_exchanging_automorphism_only_under_U`,
  `test_c2_5_misses_when_U_separates_or_the_counts_move`,
  `test_c2_8_misses_when_the_sides_separate_or_the_order_shows`.
- **Lean theorem**: `BoundarySeed.exchangeMarks_reflect_retained`,
  `BoundarySeed.retained_composite_permitted_U`,
  `BoundarySeed.retained_exchange_transports`,
  `BoundarySeed.reflect_retained_ne`,
  `BoundarySeed.exchangeMarks_retained_ne`,
  `BoundarySeed.exchangeFirstTwo_involutive`,
  `BoundarySeed.exchangeMarks_involutive`.
- **Axiom report**: propext; propext; propext; propext; propext; none;
  propext.
- **Falsifier**: a different automorphism count under U; no automorphism
  exchanging the marks; a permitted-renaming-invariant mark form holding of
  one U mark and not the other; or `sides_collapsed` true at the retained
  regime.
- **Surviving boundary**: the retained two-mark U regime and the declared
  bounded domains; requires the admitted boundary.

### B2-MARKS-O

- **Statement**: Under O the only permitted automorphism of the retained
  regime is the identity; both mark forms are invariant under the permitted
  renamings of O on the bounded domain and both separate the two retained
  marks, one lying on `near` and the other on `far`; the two name judgments
  hold as at genesis.  So the two wholes are internally separable under O in
  the sense of definition 33.  The separation uses the admitted boundary,
  the O reading of that declaration, and the Challenge 2 occurrence
  identity, and nothing else; the presentation convention fixes which
  presented whole is which mark and not that they are separated, the other
  convention's regime lying in the same isomorphism class under both
  readings.
- **Status**: COMPUTED (the single automorphism, the absence of an
  exchanging one, the invariance census, and the one-class convention
  comparison, all over the unpruned search); PROVED (the raw separation:
  `retained_marks_separated_by_a_side`); DEFINITION (the names as at
  genesis, `retained_sideNamed`, an instantiation; the capability list,
  which is a classification; and the convention itself).  Counted as
  content: score C2-6.
- **Dependencies**: definitions 2, 10, 16, 18, 23, 29, 32, 33, 34.
- **Assumptions**: reading O.
- **Python evidence**: receipt `readings.O.automorphisms`,
  `readings.O.separation`, `readings.*.convention`, `readings.O.price`;
  `test_automorphisms_and_separation_under_each_reading`,
  `test_order_label_and_convention_are_not_internally_available`,
  `test_the_price_is_one_new_declaration_paid_by_the_run`,
  `test_c2_6_misses_when_O_collapses_or_the_convention_splits`.
- **Lean theorem**: `BoundarySeed.retained_marks_separated_by_a_side`,
  `BoundarySeed.retained_sideNamed`, `BoundarySeed.retained_sides_differ`.
- **Axiom report**: propext; propext; propext, Quot.sound.
- **Falsifier**: a permitted automorphism of the O regime exchanging the
  marks; equal mark side-profiles under O; a separation that survives
  removing the names; or the other convention's regime lying in a different
  class.
- **Surviving boundary**: the retained two-mark O regime; requires the
  admitted boundary and the O reading of it.

### B2-DIFFERENT-SIDES

- **Statement**: The property that no two admitted marks lie on the same
  side is invariant under every permitted renaming of both readings, over
  every hypothetical placement of at most three marks and every permitted
  image of each — 177 images — and it holds of the retained regime.  So it
  is an internal fact under both readings, and it is what the admitted
  boundary alone buys about the two retained wholes; under U it buys
  nothing further about them, and under O it buys, in addition, which of
  them lies on which named side.
- **Status**: COMPUTED, bound three marks; PROVED for the concrete retained
  regime (`retained_marks_differ_in_side`).  Counted as content: score
  C2-7.  No unbounded theorem is claimed.
- **Dependencies**: definitions 23, 29, 35.
- **Assumptions**: the census enumerates hypothetical placements; nothing
  in it is admitted.
- **Python evidence**: receipt `different_sides_census`,
  `readings.*.retained.marks_on_different_sides`;
  `test_the_different_sides_census`,
  `test_different_sides_is_invariant_under_every_permitted_renaming`,
  `test_the_census_reports_a_property_that_is_not_invariant`,
  `test_mark_side_and_different_sides`,
  `test_c2_7_misses_when_the_census_fails_or_U_gains_an_invariant`.
- **Lean theorem**: `BoundarySeed.retained_marks_differ_in_side`.
- **Axiom report**: propext.
- **Falsifier**: a permitted renaming after which two marks share a side;
  the property failing at the retained regime; or a further invariant U
  fact separating the two wholes.
- **Surviving boundary**: placements of at most three marks; requires the
  admitted boundary.

### B2-ORDER-AND-LABEL

- **Statement**: Neither the order in which the caller retained the two
  wholes nor the visible mark they share is an internal fact under either
  reading.  Retaining them in the other order gives a regime that is
  unequal as raw data and isomorphic under both readings, by the mark
  exchange; a regime with the same placement and a different label is
  likewise unequal and isomorphic.  Python `Regime` equality compares the
  labels and the Lean `Regime` has none to compare, and this is the rung at
  which those two equalities part.
- **Status**: COMPUTED (both isomorphism witnesses, over the unpruned
  search, with the canonical keys agreeing); PROVED (the two orders give
  different raw regimes: `retainedOtherOrder_ne_retained`); DEFINITION (the
  other order is the mark exchange of the first:
  `retainedOtherOrder_is_exchange`, `rfl`).  Counted as content: score
  C2-8.
- **Dependencies**: definitions 3, 13, 14, 15, 23, 29, 36.
- **Assumptions**: the isomorphism relation of definition 23 is the
  quotient the run sanctions; the label is presentation.
- **Python evidence**: receipt `readings.*.order`, `readings.*.label`;
  `test_order_label_and_convention_are_not_internally_available`,
  `test_c2_8_misses_when_the_sides_separate_or_the_order_shows`.
- **Lean theorem**: `BoundarySeed.retainedOtherOrder_eq`,
  `BoundarySeed.retainedOtherOrder_is_exchange`,
  `BoundarySeed.retainedOtherOrder_ne_retained`.
- **Axiom report**: none; propext; propext.
- **Falsifier**: an order or a label that a permitted renaming cannot carry
  away, or a canonical key that separates the two orders.
- **Surviving boundary**: the retained two-mark regimes; the order clause
  restates that definition 3's index is a metatheoretic name.

### B2-AUDIT-TOTALITY

- **Statement**: Every theorem declared under `lean/BoundarySeed/` carries
  a `#print axioms` line in the root module.  `verify_lean.py` enumerates
  the declared theorems from the source text, with block and line comments
  stripped first, and fails by name on any that carries no line.  The two
  populations agree in both directions, 84 and 84.
- **Status**: COMPUTED (the two populations and their comparison), proved
  by injection with its counterfactual observed on the same tree.
  LIMITATION: the check reads source text, not the compiled environment, so
  a theorem the text scan cannot see would escape it.
- **Dependencies**: the paper's section 7 totality sentence, which was
  pinned by nothing before this rung.
- **Assumptions**: theorem declarations begin a line, possibly indented and
  possibly preceded by a visibility modifier; namespaces open and close on
  their own lines.
- **Python evidence**: `test_every_declared_theorem_carries_a_report_line`,
  `test_comments_are_stripped_before_the_population_is_read`;
  `MANUAL.md` injection rows.
- **Lean theorem**: none; the check is apparatus.
- **Axiom report**: not applicable.
- **Falsifier**: a declared theorem with no report line that the check does
  not name, or a name it reports that no module declares.
- **Surviving boundary**: the tree's own Lean package.

### B2-BOUNDARY-DEPENDENCE

- **Statement**: The identity policy space, the refusal of the shared
  policy, the price, supply inertia, the rule that the current state is the
  replay of the caller's history, the invariance of the initial datum and
  reading, and the empty event-follows relation do not require the admitted
  boundary.  The two new judgments, the sides the marks are retained on,
  the automorphisms, the separation, and the different-sides fact require
  it and are not formulated after removing it.
- **Status**: DEFINITION-level dependency classification.
- **Dependencies**: the seed's per-stage boundary-cost requirement.
- **Assumptions**: as B0-BOUNDARY-DEPENDENCE.
- **Python evidence**: receipt `boundary_dependence`; `test_receipt_shape`.
- **Lean theorem**: none.
- **Axiom report**: not applicable.
- **Falsifier**: as B0-BOUNDARY-DEPENDENCE.
- **Surviving boundary**: Challenge 2 dependency classification.

### B2-X

- **Statement**: Challenge 3 will declare its sense of internal
  separability to be definition 33's — no permitted automorphism carries
  one mark to the other — and will find the requirement already met under O
  by the declaration of the reading, with no augmentation, and unmet under
  U; under U no augmentation that only adds a judgment to the closed
  grammar can meet it, so every minimum one-step augmentation will either
  name a side or admit a further datum, and at least two tied
  non-isomorphic minima will survive, so uniqueness will not be provable.
- **Status**: OPEN; the extrapolation of Challenge 2, scored by
  Challenge 3.
- **Dependencies**: Challenge 3's declared sense, candidate space, and cost
  measures.
- **Assumptions**: none yet.
- **Python evidence**: none yet.
- **Lean theorem**: none yet.
- **Axiom report**: not applicable.
- **Falsifier**: as written in `challenge2/PREDICTIONS.md`.
- **Surviving boundary**: not yet.
