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
  caller's Challenge 2 history is refused under both readings and under both
  conventions by the moving-admission refusal — raised by low-level `step`
  and surfaced by certifying `replay`, which calls it, as section 1 of the
  paper says and as this entry did not when it was written
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
  `BoundarySeed.retained_sideNamed`, `BoundarySeed.retained_reading`,
  `BoundarySeed.retained_initialDatum`.
- **Axiom report**: propext, Quot.sound; propext; propext; propext;
  propext; propext; none; none.
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
  identity, and nothing else.  **Narrowed at Challenge 3, in place**: what
  the O reading contributes is the WITHDRAWAL of the side exchange and not
  the two names.  The counterfactual square computes that the separation
  holds in exactly the cells where the side exchange is not permitted,
  whether or not the names are admitted, so this entry's frozen falsifier
  "a separation that survives removing the names" FIRED at Challenge 3 and
  the reading of the middle capability is corrected accordingly.  Nothing
  computed here moves: the automorphism counts, the invariance census, and
  the convention comparison stand as this rung measured them, and the
  attribution is what is narrowed.  The paper's C2-6 row carries the same
  note; the presentation convention fixes which
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
  boundary alone buys about the two retained wholes; under O it buys, in
  addition, which of them lies on which named side.  An earlier version
  added “under U it buys nothing further about them”.  That is a totality
  this rung does not compute — only one census property and the two declared
  mark forms are checked, and the frozen falsifier scopes the clause to
  facts that separate the two wholes — so it is **narrowed** to what is
  computed: no declared mark form invariant under the permitted renamings of
  U separates the two retained wholes, and no invariant fact separating them
  was found.  Challenge 3 goes further in one direction only, and it is
  recorded there rather than here: over its declared space of 48 points, no
  candidate that changes the judgment grammar alone separates them, and no
  property invariant under the composite can (Lean
  `no_invariant_mark_property_separates_retained`).  That is still not a
  totality over everything the boundary might buy.
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

### B3-REQUIREMENT

- **Statement**: The Challenge 3 requirement, in the sense the run declares:
  the two retained marks meet it under a reading exactly when no permitted
  automorphism of the regime carries one to the other.  A second reading is
  declared beside it — some property of a mark that forgets whatever the
  candidate's declared serialization forgets, and that is invariant under
  every permitted renaming, holds of one and not of the other.  The witness
  declared for it is membership in the first mark's orbit, invariant by
  construction, and what the receipt computes at all 48 points of the
  declared space under each reading is the first reading against that
  witness — not against the existential over every such property.
- **Status**: DEFINITION (the sense, definition 38, and the half of the
  agreement definition 39 gives, which is by unfolding); COMPUTED (that the
  first reading and the declared witness agree at every enumerated point, and
  that the sense agrees with the Challenge 2 notion at the current regime).
  Not counted as content: score C3-1 is HIT by construction.  Two things are
  neither computed nor proved here and are narrowed into the statement above:
  the direction back from an arbitrary property of the second reading's kind
  to the first reading, which is definition 33's justifying sentence and is
  prose; and the premise definition 39's "by construction" rests on, that a
  candidate's permitted renamings are closed under composition and inverse.
  An earlier version of this entry said the two readings agree at all 48
  points; that is WITHDRAWN in favour of what the key computes.
- **Dependencies**: definitions 23, 29, 32, 33, 37, 38, 39.
- **Assumptions**: the caller's demand is read as a demand about the two
  retained marks and not about the two supplied wholes as presentations; a
  different sense was available and is not explored.
- **Python evidence**: receipt `requirement`,
  `readings.*.requirement_readings_agree_at_every_point`,
  `readings.*.requirement_matches_the_challenge_2_notion`;
  `test_the_orbit_witness_agrees_with_the_requirement_at_every_point`,
  `test_the_orbit_is_the_separation_test`,
  `test_c3_1_misses_when_the_two_readings_part`.
- **Lean theorem**: none; the sense quantifies over the implemented renaming
  relation, which is Python.
- **Axiom report**: not applicable.
- **Falsifier**: a point of the declared space at which the first reading and
  the declared witness disagree; or the declared sense disagreeing with the
  Challenge 2 notion at the current regime.
- **Surviving boundary**: Challenge 3 onward; the sense itself does not
  require the admitted boundary.

### B3-O-ALREADY-MET

- **Statement**: Under O the current regime already meets the requirement,
  and what meets it is the withdrawal of the side exchange from the
  permitted renamings, which the O reading of the one admitted primitive
  carries.  The two admitted names are **not** used: over the four-cell
  counterfactual (names admitted or not) by (side exchange permitted or
  not), the requirement is met in exactly the two cells where the exchange
  is not permitted, under both readings.  The satisfaction uses the admitted
  boundary, that withdrawal, and the Challenge 2 occurrence identity, and
  nothing is paid at this rung: the minimum capability count under O is
  zero, attained by the null augmentation alone.
- **Status**: COMPUTED on the side-exchange coordinate (each cell is an
  automorphism search over the unpruned enumeration, and both values are
  attained); DEFINITION on the names coordinate (definition 16 makes
  permission a declaration and not a consequence of the judgment grammar, so
  the names cannot enter the computation, and the square exhibits that
  rather than discovering it).  Counted as content: score C3-2.  The
  attribution of the satisfaction to those three capabilities, and of the two
  names to the idle list, is a declaration this run writes and no run moves;
  the receipt names it as one under `price.fields_declared_not_computed`, and
  what carries the claim that the names are idle is the square.
- **Dependencies**: definitions 2, 16, 23, 32, 37, 38, 46; B2-MARKS-O.
- **Assumptions**: reading O; the retained regime of Challenge 2.
- **Python evidence**: receipt `readings.*.counterfactual_square`,
  `readings.O.price`, `readings.O.minima_by_mu1`;
  `test_the_counterfactual_square_turns_on_the_exchange_alone`,
  `test_the_minimum_under_O_is_the_null_augmentation_alone`,
  `test_c3_2_misses_when_a_cell_of_the_square_turns`,
  `test_the_declared_price_fields_do_not_move_with_the_enumeration`.
- **Lean theorem**: none; the Lean model carries no candidate renaming set.
- **Axiom report**: not applicable.
- **Falsifier**: the O regime failing the requirement; the U regime meeting
  it; any cell of the square coming out the other way; or a minimum
  capability count under O other than zero.
- **Surviving boundary**: the retained two-mark regime under O.  It narrows
  B2-MARKS-O, whose statement listed the side names among the capabilities
  the O separation uses and whose falsifier named exactly the fact that
  fired; the narrowing is now written into that entry, and what the
  Challenge 2 receipt's price field records is the pre-narrowing
  attribution, carried because repairing it would regenerate a closed
  rung's receipt.  An earlier version of this line attributed the price to
  the ledger entry rather than to that receipt field.

### B3-NO-JUDGMENT-ADDITION

- **Statement**: Under U, while the composite of the side exchange with the
  exchange of the two marks remains a permitted renaming, no addition of
  judgment forms meets the requirement, whatever the forms: every property
  of a mark that the composite leaves alone takes the same value at the two
  retained marks.  Neither of the two mark forms is such a property, which
  is why both separate the two marks as raw data and neither separates them
  internally.
- **Status**: PROVED, and quantified over an ARBITRARY property of a
  `(Regime, Nat)` pair, so it is not a census over the declared space:
  `no_invariant_mark_property_separates_retained`.  The countermodel that
  keeps its hypothesis from being vacuous is
  `mark_form_is_not_invariant_under_the_composite`.  COMPUTED beside them:
  the concrete `admit_names` candidate fails, and no point of the declared
  space that changes only the judgment grammar meets the requirement.
  Counted as content: score C3-3.  This closes the Challenge 2 leftover that
  recorded the statement as an argument and not a theorem.
- **Dependencies**: definitions 8, 16, 29, 32, 33, 36, 38; B2-MARKS-U.
- **Assumptions**: reading U at the retained regime; the composite is the
  Challenge 2 one.
- **Python evidence**: receipt
  `readings.U.points_satisfying_with_grammar_change_only`,
  `readings.U.one_step_detail`, `readings.U.base.invariant_mark_properties`;
  `test_the_two_failing_one_step_candidates`,
  `test_c3_3_misses_when_a_grammar_change_alone_would_satisfy`.
- **Lean theorem**: `BoundarySeed.no_invariant_mark_property_separates_retained`,
  `BoundarySeed.mark_form_is_not_invariant_under_the_composite`,
  `BoundarySeed.composite_retained`,
  `BoundarySeed.retained_U_requirement_fails`.
- **Axiom report**: propext; propext, Quot.sound; propext; propext.
- **Falsifier**: an addition of judgment forms that meets the requirement
  with the composite still permitted; either mark form turning out invariant
  under the composite; or a point of the declared space that meets it by a
  grammar change alone.
- **Surviving boundary**: every regime the composite carries onto itself,
  which at this rung is the retained two-mark U regime.  The Lean statement
  is about that regime; nothing is claimed for regimes the composite moves.

### B3-CANDIDATE-SPACE

- **Statement**: The declared candidate space has five coordinates —
  withdraw the side exchange; withdraw the mark permutations; admit the two
  side names; keep the presentation labels in the serialization; admit one
  further mark, on side 0 or on side 1 — and 48 points under each reading.
  A candidate is one step exactly when it moves one coordinate, which is
  exactly when the number of undeclared capabilities it uses is one; a
  candidate of count two or more bundles capabilities and is refused as a
  one-step augmentation.  Forty-one of the 48 points are so refused, the
  candidate that adopts reading O under U among them, at count two.
- **Status**: DEFINITION (the coordinates, their values, the capability
  named for each, and therefore the point count and the identity of one-step
  with count one).  Not counted as content: score C3-4 is HIT by
  construction.  The exhaustiveness is **over those five coordinates and
  nothing wider**: an augmentation that changed the event grammar again,
  that admitted more than one further mark in one step, that supplied a
  datum the caller never presented, or that derived the permitted renamings
  from the judgment grammar is outside the space, and every minimality
  statement of this rung is scoped accordingly.
- **Dependencies**: definitions 5, 8, 13, 14, 16, 37, 40, 41.
- **Assumptions**: that one moved coordinate is one step is the run's
  declaration and not a discovered notion.
- **Python evidence**: receipt `candidate_space`,
  `readings.*.one_step_iff_capability_count_one`,
  `readings.*.bundles_refused_count`, `readings.*.reading_O_bundle`;
  `test_the_space_is_the_product_of_its_declared_coordinates`,
  `test_one_step_is_exactly_capability_count_one`,
  `test_the_reading_O_bundle_is_refused_as_two_capabilities`,
  `test_side_zero_is_a_moved_coordinate`,
  `test_the_bundles_are_refused_and_counted`,
  `test_c3_4_misses_on_a_different_space_or_a_free_bundle`.
- **Lean theorem**: none; the candidate space is Python-only.
- **Axiom report**: not applicable.
- **Falsifier**: a point count other than 48; a one-step candidate whose
  capability count is not one; the reading-O candidate costing other than
  two; or a point the count and the one-step test classify differently.
- **Surviving boundary**: Challenge 3 only.  A later rung that wants a wider
  space must declare it and re-run the enumeration.

### B3-THREE-MINIMA

- **Statement**: Under U exactly four one-step points of the declared space
  meet the requirement — withdraw the side exchange, withdraw the mark
  permutations, and admit one further mark on either side — and under the
  implemented class key they fall into exactly **three** classes, the two
  further-mark points being one class because their canonical keys under
  their own permitted renamings agree — the side exchange composed with a
  renaming of the marks carries one regime to the other, and the side
  exchange alone does not.  An earlier version of this sentence attributed
  the merge to the side exchange alone, which does not carry one regime to
  the other; the class key is what decides it, and the correction changes
  no count.  The minimum capability count
  is one, all three classes attain it, all three are retained, and
  uniqueness is refuted.  Under O the minimum is zero and the null
  augmentation is the only class attaining it.
- **Status**: COMPUTED, by exhaustive enumeration over the declared finite
  candidate space: which points meet the requirement is a witness search at
  each candidate's own renamings, and the class count is the implemented
  quotient of definition 42.  Counted as content: score C3-5.  **The
  non-uniqueness is scoped to the declared space** (B3-CANDIDATE-SPACE); it
  is a refutation of uniqueness there and not a claim about every possible
  augmentation.
- **Dependencies**: definitions 15, 23, 32, 37, 38, 40, 41, 42.
- **Assumptions**: reading U for the three; the class key is the effective
  structure with the canonical key of the regime under that structure's own
  renamings.
- **Python evidence**: receipt `readings.U.satisfying_one_step_points`,
  `readings.U.minima_by_mu1`, `readings.O.minima_by_mu1`;
  `test_the_minima_under_U_are_three_tied_classes`,
  `test_the_minimum_under_O_is_the_null_augmentation_alone`,
  `test_the_class_key_is_the_structure_with_the_canonical_regime`,
  `test_c3_5_misses_when_a_minimum_is_lost_or_uniqueness_appears`.
- **Lean theorem**: none for the enumeration.  The third minimum's mechanism
  is PROVED unboundedly as B3-COUNT-ARGUMENT.
- **Axiom report**: not applicable.
- **Falsifier**: a different set of satisfying one-step points; a different
  class count; a proof that the minimum is unique inside the declared space;
  or a minimum capability count other than one under U or zero under O.
- **Surviving boundary**: the declared space at the retained two-mark
  regime, under each reading separately.

### B3-THREE-MECHANISMS

- **Statement**: The three retained minima separate the two marks in three
  different ways.  Withdrawing the side exchange makes both side properties
  invariant and separating and leaves the two index properties
  non-invariant; withdrawing the mark permutations does the reverse; and
  admitting one further mark leaves none of the five declared mark
  properties both invariant and separating, its witness being the orbit
  property alone.  The property that reads the supplied label is invariant
  under every candidate's renamings and separates nothing, both retained
  marks carrying the same label.  **The second of the three meets the
  requirement by unfolding**: with the mark permutations withdrawn no
  permitted renaming moves an index at all.
- **Status**: COMPUTED on the first and third mechanisms (the invariance of
  each property is a census over the declared bounded domain at the
  candidate's renamings, and the third minimum's empty row is what makes the
  orbit witness necessary); **DEFINITION-level on the second**, which the
  receipt reports separately as `no_permitted_renaming_moves_an_index`.
  Counted as content: score C3-7, on the first and third rows.
- **Dependencies**: definitions 34, 37, 39, 43; B3-THREE-MINIMA.
- **Assumptions**: the five declared mark properties and the bounded domain
  of at most three marks over two labels; a property outside that list could
  behave differently and none is offered.
- **Python evidence**: receipt `readings.U.one_step_detail`,
  `mark_properties`, `property_domain_max_marks`;
  `test_the_three_mechanisms`,
  `test_property_invariance_is_a_census_and_reports_a_false`,
  `test_property_separation_reads_the_two_retained_marks`,
  `test_c3_7_misses_when_a_mechanism_row_moves`.
- **Lean theorem**: `BoundarySeed.mark_form_is_not_invariant_under_the_composite`
  for why neither side property is invariant at the base.
- **Axiom report**: propext, Quot.sound.
- **Falsifier**: any of the three mechanism rows differing; a declared
  property turning out invariant and separating where the receipt says it is
  not; or the second minimum's satisfaction resting on a computation rather
  than on unfolding.
- **Surviving boundary**: the declared property list and the declared bounded
  domain.

### B3-COUNT-ARGUMENT

- **Statement**: A renaming of the marks preserves how many marks lie on
  each side, and the side exchange exchanges those two counts; so at a
  placement whose two sides carry different numbers of marks, no renaming of
  the marks returns the reflected placement to the original.  After one
  further mark the retained placement is such a placement.  At the retained
  regime itself the two counts are equal, so the argument says nothing
  there.
- **Status**: PROVED, and unbounded in the renaming: the statement
  quantifies over every permutation of the placement rather than over a
  bounded enumeration.  It closes, in one direction and for this shape of
  placement, half of the equal-count law the Challenge 0 census recorded as
  a computation; the converse direction is not proved.
- **Dependencies**: definitions 12, 13, 37; B3-THREE-MINIMA.
- **Assumptions**: a renaming of the marks acts on the placement as a
  permutation of that list.  That identification is the correspondence
  between the Lean model and the Python `rename_marks`, and it is prose, not
  a theorem: no Lean statement says that the Python relation and this one
  agree.
- **Python evidence**: receipt `readings.U.one_step_detail` rows
  `extra_mark_0` and `extra_mark_1`;
  `test_withdrawing_a_generator_shrinks_the_enumeration`.
- **Lean theorem**: `BoundarySeed.countOn_map_not`,
  `BoundarySeed.countOn_perm`, `BoundarySeed.reflect_not_undone_by_renaming`,
  `BoundarySeed.retainedPlus_counts_differ`,
  `BoundarySeed.retainedPlus_reflection_is_not_an_automorphism`,
  `BoundarySeed.retained_counts_equal`.
- **Axiom report**: none; none; none; none; none; none.
- **Falsifier**: a permutation of a placement that changes a count; a
  placement with unequal counts whose reflection some permutation returns;
  or the retained placement having unequal counts.
- **Surviving boundary**: every placement, for the general lemmas; the
  three-mark placement `[false, true, s]` for the instance.

### B3-TWO-MEASURES

- **Statement**: The second declared cost measure, the collateral count, is
  the number of five declared facts about the retained configuration that a
  candidate makes internally available and the same reading's base did not.
  It is one at each of the three U minima, so under U both declared measures
  select the same three classes at a minimum of one; **under O they do not**,
  the collateral count's minimum of zero being attained by five points in
  three classes while the capability count's is the null augmentation alone.
  Under both readings the two measures differ in value at points of the
  space, so neither is the other.  The required separation is not one of the
  five facts, but the first of them is that separation said of the two SIDES
  rather than of the two MARKS, and the enumeration computes that it takes
  the requirement's value at every point of the declared space under each
  reading; so the "one" at each of the three U minima is that fact and
  nothing else, and to that extent the measure re-counts the requirement
  rather than excluding it.
- **Status**: COMPUTED (each collateral fact is an automorphism or
  isomorphism-witness search at the candidate's own renamings, and the
  difference of the two measures, the agreement of the minima, and the
  side-fact coincidence are censuses over the 48 points).  Counted as
  content: score C3-6, whose clauses are read under U alone.  **The measure
  is over five declared facts**, not over everything a candidate makes
  available, and one of the five is the requirement under another
  description.
- **Dependencies**: definitions 37, 40, 41, 44; B3-THREE-MINIMA.
- **Assumptions**: the five declared facts; a sixth could break the tie and
  none is offered.  The declared list is left as it stands: revising it after
  the enumeration would fit the declaration to the answer.
- **Python evidence**: receipt `measures`, `collateral_facts`,
  `readings.*.minima_by_mu2`, `readings.U.measures_agree_on_minima` (true)
  and `readings.O.measures_agree_on_minima` (false),
  `readings.*.measures_differ_somewhere`,
  `readings.*.sides_fact_agrees_with_the_requirement_at_every_point`;
  `test_the_collateral_measure_counts_only_what_the_base_lacked`,
  `test_the_two_measures_are_not_the_same_measure`,
  `test_the_measures_select_the_same_minima_under_U_and_not_under_O`,
  `test_the_sides_fact_agrees_with_the_requirement_at_every_point`,
  `test_the_sides_fact_agreement_reads_false_when_one_point_parts`,
  `test_c3_6_misses_when_the_measures_part_or_coincide`.
- **Lean theorem**: none; the measures are Python-only.
- **Axiom report**: not applicable.
- **Falsifier**: a U minimum whose collateral count is not one; the two
  measures selecting different minimum sets under U; the two agreeing at
  every point of the space; or a point at which the side-separability fact
  and the required separation part.
- **Surviving boundary**: the declared fact list and the declared space.

### B3-PROCESS-ADMISSION

- **Statement**: The further-mark candidate needs no supply of its own: the
  token it admits is the one the caller already presented, and certifying
  replay accepts the extended history, while a token the caller never
  presented is refused by name.  Its one capability is therefore that the
  process, and not only the caller, issues an event — which definition 25
  does not license, the current state being the replay of the caller's
  history.  No such event is in any history the receipt reports as current.
- **Status**: COMPUTED (the acceptance and the refusal are runs of
  certifying replay); DEFINITION (that the issuing of the event is the
  capability, and that it costs one).
- **Dependencies**: definitions 5, 6, 20, 25, 40, 45.
- **Assumptions**: that a further mark carrying a token the caller never
  presented would cost two capabilities rather than one is stated and not
  enumerated: no such point is in the declared space.
- **Python evidence**: receipt `readings.*.process_admission`;
  `test_the_process_admission_needs_no_new_supply`,
  `test_the_process_admission_facts`.
- **Lean theorem**: none; the Lean model carries no token and no issuer, so
  `retainedPlus` records only what follows once the mark is placed.
- **Axiom report**: not applicable.
- **Falsifier**: the extended history being refused; a token the caller
  never presented being accepted; or a receipt history that contains a
  process-issued event and is reported as current.
- **Surviving boundary**: the further-mark coordinate; every later rung that
  would let the process issue an event inherits this price.

### B3-PLACEMENT-CHECK

- **Statement**: Every candidate regime's placement equals the placement the
  declared convention and the candidate's own side predict, computed from
  the presented sides and the convention alone.  This is the one statement
  about a candidate regime in the receipt that is not a comparison of a
  replay with itself.
- **Status**: COMPUTED.  It exists because review found that the receipt
  keys `certified` and `replays_from_genesis`, cited at the previous rung as
  evidence for the certified-and-replayed claim, are tautologies of their
  own construction and cannot be false.  Those keys are kept, because a
  reader wants to see them, and this key is added beside them; the other
  non-tautological check is the test, which rebuilds the events from the
  rendered receipt and replays them.
- **Dependencies**: definitions 18, 19, 25, 40, 45.
- **Assumptions**: the reader and the convention are the declared ones.
- **Python evidence**: receipt
  `readings.*.base.placement_matches_the_declared_convention` and the same
  key on every one-step row;
  `test_the_placement_is_checked_against_the_declared_convention`,
  `test_the_placement_key_reads_false_when_the_prediction_parts` for the
  negative direction, and `test_every_candidate_history_replays_from_genesis`.
  The key is proved by injection in `MANUAL.md`: with the further mark's
  admission moved to the other side, the check named `extra_mark_0`.
- **Lean theorem**: none; the convention is Python-only.
- **Axiom report**: not applicable.
- **Falsifier**: a candidate regime whose placement differs from the one the
  convention predicts.
- **Surviving boundary**: the candidate regimes of this rung.

### B3-BOUNDARY-DEPENDENCE

- **Statement**: At Challenge 3 the declared sense and its second reading,
  the identity of the candidate space, the capability counts, the one-step
  rule, the refusal of bundles, the two index mark properties, and the
  withdrawal of the mark permutations do not require the admitted boundary.
  The side exchange, its withdrawal, the two side mark properties, the
  counterfactual square, the further-mark minimum, and every separation
  result of the rung require it and are not formulated after removing it.
- **Status**: LIMITATION, a dependency classification of the run.  It is
  reported in the receipt and is not computed by anything.
- **Dependencies**: the seed's requirement to classify at every stage.
- **Assumptions**: removing the boundary is a counterfactual classification
  and not a third reading added to the model.
- **Python evidence**: receipt `boundary_dependence`; `test_receipt_shape`.
- **Lean theorem**: none.
- **Axiom report**: not applicable.
- **Falsifier**: as B0-BOUNDARY-DEPENDENCE.
- **Surviving boundary**: Challenge 3 dependency classification.

### B3-X

- **Statement**: At Challenge 4 the declared reader bound of at most one
  mark per whole will have to be widened to one mark on each side of the
  bar, and that widening will be a new declaration priced like this rung's,
  paid by the run.  The two wholes will become four admitted marks with
  placement `(0, 1, 0, 1)` under the declared convention, so the two sides
  will carry equally many marks and the composite of the side exchange with
  a mark renaming will again be a permitted automorphism under U; the
  requirement will fail again under U, with the same minimum count of one,
  and hold again under O with no new declaration.  What the boundary
  contributes will be the side each mark lies on, and what it cannot
  contribute is the matching of a visible mark across the boundary.
- **Status**: OPEN; the extrapolation of Challenge 3, scored by Challenge 4.
- **Dependencies**: Challenge 4's reader bound, retained placement, and
  declared space.
- **Assumptions**: none yet.
- **Python evidence**: none yet.
- **Lean theorem**: none yet.
- **Axiom report**: not applicable.
- **Falsifier**: as written in `challenge3/PREDICTIONS.md`.
- **Surviving boundary**: not yet.

### B4-READER-WIDENING

- **Statement**: The Challenge 1 reader admits at most one mark in a whole and
  refuses **both** Challenge 4 inscriptions by name, so the caller's challenge
  cannot be read under it.  The run declares the widened reader — at most one
  mark on each side of the bar, and nothing further — and a within-whole
  admission order beside it; both are declarations of the metatheory, paid by
  the run at this rung, and the narrower reader is left refusing.  The widened
  reader refuses a nested whole by name.
- **Status**: DEFINITION (the widened bound and the order are declarations);
  COMPUTED (that the Challenge 1 reader refuses both inscriptions, and that the
  widened one refuses the nested whole).  Counted as content: no.  Score C4-1
  is HIT by construction.
- **Dependencies**: definitions 17, 18, 47, 48.
- **Assumptions**: that the caller's inscriptions are to be read at all; the
  run could instead have refused the challenge and recorded it OPEN, as it
  could have at Challenge 2.
- **Python evidence**: receipt `reader`; `test_the_challenge_1_reader_refuses_both_inscriptions`,
  `test_the_widened_reader_reads_a_mark_on_each_side`,
  `test_the_widened_reader_refuses_what_is_beyond_its_bound`,
  `test_the_within_whole_order_is_a_declaration_with_another_value`,
  `test_c4_1_misses_when_the_reader_or_the_retention_moves`.
- **Lean theorem**: none; the reader is Python-only, the Lean events carrying
  no token.
- **Axiom report**: not applicable.
- **Falsifier**: the Challenge 1 reader accepting either inscription; the
  widened reader accepting two marks on one side or a nested whole.
- **Surviving boundary**: Challenge 4 onward.  The widening is about how many
  marks a whole may carry and does not require the admitted boundary, though
  what it reads is a presented side.

### B4-RETENTION

- **Statement**: Under definition 30's reading of "retains" and the Challenge 2
  occurrence identity, the caller's Challenge 4 history is a `Supply` for each
  mark of each whole in presented order and an `AdmitOccurrence` for each in
  the declared within-whole order — eight events — and the current state under
  each reading is its replay: four admitted marks, placement `(0, 1, 0, 1)`,
  labels `("a", "b", "b", "a")`, certified and replayed from genesis, with the
  placement equal to the one the convention and the order predict.  The other
  within-whole order gives an isomorphic configuration under both readings, so
  that order is not internally available.
- **Status**: DEFINITION (the history follows from the declared reader,
  convention, order, and policy); COMPUTED (the replay, the placement check
  against the declarations, and the isomorphism of the other order).  Counted
  as content: no; score C4-1 is HIT by construction, and its one non-declared
  clause is reported separately.
- **Dependencies**: definitions 5, 6, 25, 30, 31, 47, 48, 49.
- **Assumptions**: the caller's "retains" is read as at Challenge 2; a whole is
  presented once and presents both its marks.
- **Python evidence**: receipt `readings.*.base`;
  `test_the_retention_history_and_its_grouping`,
  `test_every_candidate_history_replays_from_genesis`,
  `test_the_placement_is_checked_against_the_declarations`,
  `test_the_placement_key_reads_false_when_the_prediction_parts`.
- **Lean theorem**: `BoundarySeed.crossRetained_eq`,
  `BoundarySeed.crossRetained_placement_length`,
  `BoundarySeed.crossRetained_reading`,
  `BoundarySeed.crossRetained_initialDatum`.
- **Axiom report**: none for any of the four.
- **Falsifier**: a retained placement other than `(0, 1, 0, 1)`; a history that
  is not one supply and one admission per mark; a candidate regime whose
  placement differs from the one the declarations predict.
- **Surviving boundary**: the Challenge 4 retained configuration under each
  reading.

### B4-GROUPING-IS-METATHEORY

- **Statement**: A whole is a set of marks, and the regime carries no component
  that groups marks into wholes: the grouping is read off the caller's history.
  The Challenge 4 requirement and its declared witness are therefore statements
  about the automorphisms of the state together with a metatheoretic grouping,
  at every candidate that does not admit that grouping.
- **Status**: LIMITATION, and a narrowing of what internal separability can
  mean for a whole.  It is not computed; it is a fact about the declared
  `Regime` type, made visible by the `Configuration` type that keeps the two
  apart, and it is the reason the grouping is one of the declared coordinates.
- **Dependencies**: definitions 3, 50, 51, 52.
- **Assumptions**: none.
- **Python evidence**: `Configuration` in `code/boundary/model.py`; receipt
  `requirement.grouping_is_metatheory`;
  `test_a_configuration_needs_one_tag_per_mark`.
- **Lean theorem**: none; the Lean regime carries no grouping either, which is
  why a whole is named there by an index map.
- **Axiom report**: not applicable.
- **Falsifier**: a component of the regime that carries the grouping without a
  declared augmentation.
- **Surviving boundary**: every Challenge 4 result stated in the whole sense.

### B4-REQUIREMENT

- **Statement**: The Challenge 4 requirement, in the sense the run declares:
  the two retained wholes meet it under a reading exactly when no permitted
  automorphism of the configuration carries the mark-set of one onto the
  mark-set of the other.  A second reading is declared beside it — some
  property of a mark-set that forgets whatever the candidate's key forgets and
  is invariant under every permitted renaming holds of one whole's mark-set and
  not of the other's — and its declared witness is membership in the first
  whole's orbit.  The sense reduces to definition 38's at the Challenge 3
  configuration, where each whole is one mark, which the receipt computes under
  both readings.
- **Status**: DEFINITION (the sense; the half of the agreement the orbit
  witness gives by unfolding; and the reduction, which the receipt computes but
  which holds by unfolding where each whole is a single mark); COMPUTED (that
  the first reading and the declared witness agree at all 192 points under each
  reading).  Two things are neither computed nor proved and are narrowed into
  the statement: the direction back from an arbitrary property of the second
  reading's kind to the first, which is definition 33's justifying sentence and
  is prose; and the premise definition 54's "by construction" rests on, that a
  candidate's permitted renamings are closed under composition and inverse.
- **Dependencies**: definitions 23, 29, 33, 38, 50, 51, 52, 53, 54.
- **Assumptions**: the caller's demand is read as a demand about the two
  retained wholes and not about the four marks pairwise; the pointwise sense is
  declared beside it and computed, and it is a different requirement.
- **Python evidence**: receipt `requirement`,
  `readings.*.requirement_readings_agree_at_every_point`,
  `readings.*.reduction_to_challenge_3`;
  `test_the_orbit_witness_agrees_with_the_requirement_at_every_point`,
  `test_the_reduction_at_the_challenge_3_configuration`,
  `test_the_whole_orbit_carries_the_key_and_the_mark_set`.
- **Lean theorem**: none; the sense quantifies over the implemented renaming
  relation, which is Python.
- **Axiom report**: not applicable.
- **Falsifier**: a point at which the first reading and the declared witness
  disagree.  The frozen falsifier naming a disagreement of the two senses at
  the Challenge 3 configuration cannot fire, the reduction being by unfolding.
- **Surviving boundary**: Challenge 4 onward; the sense itself does not require
  the admitted boundary.

### B4-FAILS-UNDER-BOTH

- **Statement**: The retained configuration fails the requirement under **both**
  readings — the first rung at which reading O does not already meet it.  The
  obstruction is the exchange of the two wholes, the permutation carrying mark
  0 to mark 2 and mark 1 to mark 3, which carries the configuration onto itself
  **with no side exchange**, so the withdrawal that the O reading carries does
  not touch it.  Of the six pairs of distinct marks, under O exactly the four
  lying on different sides are separable and the two sharing a side are not;
  under U none is.  Under U there are eight permitted automorphisms and under O
  four.
- **Status**: COMPUTED (the automorphism counts, the whole-carrying witness,
  and the pair census, all over the unpruned enumeration); PROVED (that the
  exchange carries the retained regime onto itself, and that each of the two
  pairs of marks that share a side satisfies the same mark-on-side judgments,
  one theorem per pair).  Counted as content: score C4-2.
- **Dependencies**: definitions 16, 51, 52; B4-RETENTION.
- **Assumptions**: the declared sense, and the reading's own renamings.
- **Python evidence**: receipt `readings.*.base.satisfies`,
  `whole_exchange_witness`, `separable_mark_pairs`, `automorphism_count`;
  `test_the_requirement_fails_under_both_readings`,
  `test_the_pairs_of_marks_the_boundary_separates`,
  `test_c4_2_misses_when_a_reading_meets_the_requirement`.
- **Lean theorem**: `BoundarySeed.exchangeWholesRegime_crossRetained`,
  `BoundarySeed.exchangeWholes_carries_the_first_whole`,
  `BoundarySeed.crossRetained_marks_share_a_side`,
  `BoundarySeed.crossRetained_other_marks_share_a_side`,
  `BoundarySeed.reflect_crossRetained_ne`,
  `BoundarySeed.exchangeMarks_crossRetained_ne`.
- **Axiom report**: propext; none; propext; propext; propext; propext.
- **Falsifier**: the O regime meeting the requirement; a whole-carrying
  automorphism that uses the side exchange under O; a pair census other than
  four-and-two under O or empty under U.
- **Surviving boundary**: the Challenge 4 retained configuration under each
  reading.

### B4-NO-JUDGMENT-ADDITION

- **Statement**: While the exchange of the two wholes is a permitted renaming,
  no addition of judgment forms meets the requirement, whatever the forms:
  every property of a regime and an ordered pair of internal identities that
  the exchange leaves alone takes the same value at the two retained wholes,
  and the same holds for a property of a single mark at **marks 0 and 2**,
  which is what `no_invariant_mark_property_separates_the_paired_marks` states.
  An earlier version of this entry said "the two marks that share a side", a
  description that does not uniquely denote — marks 1 and 3 share a side too —
  and that wider reading is WITHDRAWN: the mark-level theorem covers the one
  named pair, and the same-side judgment equalities of B4-FAILS-UNDER-BOTH
  cover both pairs.  The hypothesis is a real restriction: the property that reads
  whether the first mark of a pair is the first admitted mark separates the two
  wholes and is therefore not invariant under the exchange.
- **Status**: PROVED, for an arbitrary property, with a countermodel.  Counted
  as content: it is the Lean half of scores C4-2 and C4-5.  The countermodel
  shows only that the hypothesis excludes that one property; it says nothing
  about what else lies outside it.
- **Dependencies**: definitions 8, 52; B4-FAILS-UNDER-BOTH.
- **Assumptions**: the property is a Boolean of a regime and one or two
  internal identities; the correspondence between `exchangeWholes` and the
  Python renaming of a configuration is prose.
- **Python evidence**: receipt `readings.*.base.witness_whole_properties`,
  which is empty under both readings; the concrete `admit_names` point does not
  meet the requirement.
- **Lean theorem**: `BoundarySeed.no_invariant_pair_property_separates_the_wholes`,
  `BoundarySeed.no_invariant_mark_property_separates_the_paired_marks`,
  `BoundarySeed.firstIsMarkZero_separates_the_wholes`,
  `BoundarySeed.firstIsMarkZero_is_not_invariant_under_the_whole_exchange`.
- **Axiom report**: propext for all four.
- **Falsifier**: an addition of judgment forms that meets the requirement with
  the whole exchange still permitted; the Lean statement not covering an
  arbitrary property; or the countermodel property turning out invariant.
- **Surviving boundary**: the Challenge 4 retained configuration, under both
  readings.

### B4-CONTINUATION

- **Statement**: No continuation removes the obstruction.  After every later
  history of the Lean grammar — any number of further supplies and placements —
  the exchange of the two wholes still carries the regime onto itself.  In
  particular one further mark on either side, which was one of the three minima
  at Challenge 3, does not meet the requirement here.  The Challenge 3 counting
  argument does not apply: the two sides of the retained placement carry equally
  many marks.
- **Status**: PROVED, over every history rather than over a bounded
  enumeration, through the induction that replaying a history appends to the
  placement.  Counted as content.  It is strictly stronger than the enumeration,
  which reaches one further mark.
- **Dependencies**: definitions 5, 6, 51, 52; B4-FAILS-UNDER-BOTH.
- **Assumptions**: the Lean grammar's events, which carry no token; a Python
  history that refuses an unsupplied admission is a subset of what this covers.
- **Python evidence**: receipt `readings.*.one_step_detail` rows
  `extra_mark_0` and `extra_mark_1`, neither of which meets the requirement;
  `test_the_coordinates_that_were_minima_at_the_previous_rung_are_not`.
- **Lean theorem**: `BoundarySeed.replay_placement_append`,
  `BoundarySeed.exchangeWholesRegime_of_prefix`,
  `BoundarySeed.whole_exchange_survives_every_continuation`,
  `BoundarySeed.whole_exchange_survives_a_further_mark`,
  `BoundarySeed.crossRetained_counts_equal`.
- **Axiom report**: propext; propext; propext; propext; none.
- **Falsifier**: a continuation after which the exchange does not carry the
  regime onto itself.
- **Surviving boundary**: every regime whose placement begins with the retained
  one, under both readings.

### B4-CANDIDATE-SPACE

- **Statement**: The declared Challenge 4 candidate space has seven
  coordinates — the five of definition 40 together with admitting the whole
  grouping and naming the two wholes — and 192 points under each reading.  A
  candidate is one step exactly when its capability count is one; every
  candidate of count two or more is refused as bundling, 183 of the 192; and
  naming the wholes without admitting the grouping changes nothing and
  collapses into the null point under the implemented quotient.
- **Status**: DEFINITION.  The coordinates, their values, the capability named
  for each, and therefore the point count and the identity of one step with
  count one are declarations of this rung.  Counted as content: no; score C4-4
  is HIT by construction.  **Every minimality statement of this rung is scoped
  to this space**, including the uniqueness of the U minimum.
- **Dependencies**: definitions 40, 41, 51, 56, 57.
- **Assumptions**: that the grouping and its naming are two coordinates and not
  one.  A run that declared them one would report a second minimum under both
  readings; they are two here because naming tags is the U-versus-O distinction
  one level up, and that is a declaration.
- **Python evidence**: receipt `candidate_space`, `readings.*.bundles_refused_count`,
  `one_step_iff_capability_count_one`, `name_wholes_collapses_into_the_base`;
  `test_the_space_is_the_product_of_its_declared_coordinates`,
  `test_one_step_is_exactly_capability_count_one`,
  `test_the_effective_structure_collapses_the_no_ops`,
  `test_c4_4_misses_on_a_different_space_or_a_live_no_op`.
- **Lean theorem**: none; the space is Python-only.
- **Axiom report**: not applicable.
- **Falsifier**: a point count other than 192; a one-step candidate whose
  capability count is not one; the name-wholes point not collapsing.
- **Surviving boundary**: Challenge 4's minimality statements and nothing
  wider.

### B4-MINIMUM-U

- **Statement**: Under U exactly one one-step point of the declared space meets
  the requirement — withdrawing the mark permutations — at a minimum capability
  count of one and in one class, so **uniqueness is not refuted inside the
  declared space**.  That minimum meets the requirement by unfolding: with the
  mark permutations withdrawn no permitted renaming moves an index at all, so
  it leaves the admitted boundary idle entirely.  The withdrawal of the side
  exchange, a minimum at Challenge 3, does not meet the requirement here, and
  neither does a further mark on either side.
- **Status**: COMPUTED, by exhaustive enumeration over the declared finite
  space: which points meet the requirement is a witness search at each
  candidate's own renamings, and the class count is the implemented quotient.
  Counted as content: score C4-5.  That the one minimum meets the requirement
  by unfolding is DEFINITION-level and the receipt reports it separately.  **The
  uniqueness is uniqueness inside the declared space** (B4-CANDIDATE-SPACE) and
  is the run's first uniqueness statement; it is not a claim about every
  augmentation.
- **Dependencies**: definitions 51, 52, 56, 57; B4-CANDIDATE-SPACE.
- **Assumptions**: reading U.
- **Python evidence**: receipt `readings.U.satisfying_one_step_points`,
  `readings.U.minima_by_mu1`, `readings.U.one_step_detail`;
  `test_the_minimum_under_U_is_one_class_and_uniqueness_is_not_refuted`,
  `test_the_coordinates_that_were_minima_at_the_previous_rung_are_not`,
  `test_c4_5_misses_when_a_second_minimum_appears_under_U`.
- **Lean theorem**: none for the enumeration; B4-CONTINUATION closes the
  further-mark coordinate unboundedly.
- **Axiom report**: not applicable.
- **Falsifier**: a second satisfying one-step point under U; a class count
  other than one; a minimum capability count other than one.
- **Surviving boundary**: the declared space at the retained configuration
  under U.

### B4-MINIMA-O

- **Statement**: Under O exactly two one-step points meet the requirement —
  withdrawing the mark permutations, and keeping the presentation labels — in
  two classes tied at capability count one, both retained, so uniqueness is
  refuted under O.  Keeping the labels meets the requirement under O and fails
  under U, because the two retained wholes are each other's reflection and
  under U the side exchange is a renaming the object language cannot see; under
  O the pair of a label with a side is what the witness property reads.
- **Status**: COMPUTED, by the same enumeration and quotient.  Counted as
  content: score C4-6.
- **Dependencies**: definitions 51, 52, 55, 56, 57; B4-CANDIDATE-SPACE.
- **Assumptions**: reading O for the two minima; the label-keeping witness is
  one of the five declared whole properties and the list is declared, not a
  survey.
- **Python evidence**: receipt `readings.O.satisfying_one_step_points`,
  `readings.O.minima_by_mu1`, `readings.*.one_step_detail`;
  `test_the_minima_under_O_are_two_tied_classes`,
  `test_the_witness_of_each_satisfying_one_step_point`,
  `test_c4_6_misses_when_the_O_minima_move`.
- **Lean theorem**: none; the Lean model carries no presentation label.
- **Axiom report**: not applicable.
- **Falsifier**: a different set of satisfying one-step points under O; a
  different class count; the label-keeping candidate meeting the requirement
  under U or failing under O.
- **Surviving boundary**: the declared space at the retained configuration
  under O.

### B4-GROUPING-BUNDLE

- **Statement**: The augmentation that gives the caller internal wholes is a
  bundle and is refused as one step.  Admitting the whole grouping alone does
  not meet the requirement: with the two tags admitted and unnamed, their
  exchange is a renaming the object language cannot see, and composed with the
  permutation that exchanges the two wholes it carries the configuration onto
  itself.  Naming the two wholes without admitting the grouping names tags no
  mark carries and collapses into the null point.  The two together meet the
  requirement under both readings, at a capability count of two, so neither
  half is a minimum.  The four-cell grouping square is met in one cell under
  each reading.
- **Status**: COMPUTED (each cell is an automorphism search with both values
  attained, and the collapse is the implemented quotient); DEFINITION on the
  capability count, which is the declared measure.  Counted as content: score
  C4-7.
- **Dependencies**: definitions 50, 51, 52, 56, 57; B4-CANDIDATE-SPACE.
- **Assumptions**: that the tag exchange is a permitted renaming exactly when
  the grouping is admitted and the wholes are unnamed, which is this rung's
  declaration and the tag-level counterpart of the side exchange under U.
- **Python evidence**: receipt `readings.*.grouping_square`, `grouping_bundle`,
  `name_wholes_collapses_into_the_base`;
  `test_the_grouping_square_turns_on_both_coordinates`,
  `test_the_grouping_bundle_costs_two_and_neither_half_is_one`,
  `test_c4_7_misses_when_a_half_of_the_bundle_would_do`.
- **Lean theorem**: none; the Lean regime carries no grouping.
- **Axiom report**: not applicable.
- **Falsifier**: the grouping alone meeting the requirement; the pair costing
  other than two; the pair failing to meet it under either reading; the
  name-wholes point not collapsing.
- **Surviving boundary**: the declared space at the retained configuration
  under each reading.

### B4-TWO-SENSES

- **Statement**: The pointwise sense — every pair of distinct admitted marks
  separable — implies the declared whole sense at every point of the declared
  space under both readings, and the converse fails inside it: at 18 points
  under U and 16 under O the two wholes are separable while some pair of marks
  is not.  The grouping-with-names point is among them **under U only**: under
  O that point satisfies the pointwise sense as well and is therefore not one
  of the 16.  An earlier version of this entry named it under both readings,
  which is WITHDRAWN.  At the Challenge 3
  configuration, where each whole is one mark, the two senses agree.
- **Status**: COMPUTED, a census over the 192 points under each reading.
  Counted as content: score C4-8, on the census and the parting points.  The
  reduction at the Challenge 3 configuration is computed rather than asserted
  but is **DEFINITION-level** and is no part of that content: with each whole a
  single mark the whole sense's set test unfolds to the pointwise sense's mark
  test over the same list of automorphisms, so the two senses cannot disagree
  there and the falsifier below that names that disagreement cannot fire.
  The implication is computed over the space and is not proved in general.
- **Dependencies**: definitions 33, 52, 53.
- **Assumptions**: the two wholes are disjoint and non-empty, which the kernel
  enforces by refusing a whole that groups no mark.
- **Python evidence**: receipt `readings.*.pointwise_implies_whole_at_every_point`,
  `points_where_the_two_senses_part`,
  `at_every_parting_point_the_wholes_separate_and_the_marks_do_not`,
  `reduction_to_challenge_3`; `test_the_two_senses_of_separability_part`,
  `test_c4_8_misses_when_the_two_senses_coincide_or_invert`.
- **Lean theorem**: none; both senses quantify over the implemented renaming
  relation.
- **Axiom report**: not applicable.
- **Falsifier**: a point at which the pointwise sense holds and the whole sense
  fails; or the two senses agreeing at every point.  The frozen third
  falsifier, the two senses disagreeing at the Challenge 3 configuration,
  cannot fire, for the reason given under Status.
- **Surviving boundary**: the declared space at the retained configuration.

### B4-WITNESS-CLAUSE

- **Statement**: A declared whole property witnesses the separation only if it
  is BOTH invariant under the candidate's permitted renamings on the declared
  domain AND determined by the candidate's key.  The second conjunct is
  definition 29's token-forgetting clause generalized, and it is load-bearing:
  the property that reads the group tag is invariant under every permitted
  renaming at the base and separates the two wholes there, so a census of
  invariance alone reports a witness at the very point where the requirement
  fails.  With both conjuncts the witness list is empty at the base and at
  every one-step point that fails the requirement, and names exactly one
  property at each satisfying one-step point: the index property under both
  readings, and the label-and-side property under O.  Those nine rows per
  reading are the whole population the census is run over: the 192 point rows
  carry no witness column, so nothing is claimed about the bundled points.
- **Status**: COMPUTED, two censuses over the declared domain of 768
  configurations per reading.  Counted as content: it carries score C4-3's
  content and the mechanism halves of C4-5 and C4-6.  **The defect was live**:
  the rung's first census carried the invariance conjunct only and reported the
  tag property as a witness at the base.  It is recorded in `MANUAL.md` with
  the injection that reproduces it.
- **Dependencies**: definitions 29, 43, 51, 55.
- **Assumptions**: the five declared properties are a declared list and not a
  survey; the domain carries three groupings because a property that reads the
  tag must be tested against configurations whose grouping differs while their
  key does not.
- **Python evidence**: receipt `readings.*.base.invariant_whole_properties`,
  `key_determined_whole_properties`, `witness_whole_properties`,
  `whole_properties`; `test_the_tag_property_is_invariant_and_not_determined_by_the_key`,
  `test_the_key_determination_census_reads_both_ways`,
  `test_property_invariance_is_a_census_and_reports_both_values`,
  `test_the_witness_of_each_satisfying_one_step_point`.
- **Lean theorem**: none; the Lean model carries no key.
- **Axiom report**: not applicable.
- **Falsifier**: a property reported as a witness at a point that fails the
  requirement; or a satisfying one-step point with no witness where one of the
  five is both invariant, key-determined, and separating.
- **Surviving boundary**: the Challenge 4 census.  It does not repair the
  Challenge 3 census, which carried the first conjunct only and whose one
  anomalous property was reported there as invariant and separating nothing.

### B4-BOUNDARY-CONTRIBUTION

- **Statement**: At Challenge 4 the admitted boundary contributes what it
  contributed at Challenge 3 — the side each mark lies on, each mark's profile
  being its side and nothing else — and that now sorts four marks into two
  classes of two and no finer.  Neither side-reading whole property separates
  the two wholes under either reading.  What it cannot contribute is which mark
  within a side is which, the grouping of marks into wholes, and the matching
  of a visible mark across the boundary: the configuration in which the second
  whole's copy of the first token is a token the caller never presented is
  reached by a permitted renaming under both readings.
- **Status**: COMPUTED (the property census, the mark profiles, and the
  matching comparison); PROVED (that each of the two pairs of marks that share
  a side satisfies the same mark-on-side judgments).  Counted as content: score
  C4-3, which is **PARTIAL**: its clause that both side-reading properties are
  invariant under both readings is false under U, where the side exchange moves
  a mark's side, and the miss is recorded next to its value.
- **Dependencies**: definitions 22, 34, 55, 58; B4-FAILS-UNDER-BOTH.
- **Assumptions**: the classification of a contribution is the run's.
- **Python evidence**: receipt `readings.*.base.separating_whole_properties`,
  `mark_profiles`, `collateral_facts.cross_boundary_matching_internally_available`,
  `scores.C4-3`; `test_the_recorded_miss_of_this_rung`,
  `test_the_matching_variant_replaces_one_token_and_refuses_none`,
  `test_c4_3_moves_between_partial_and_hit_on_its_own_clauses`.
- **Lean theorem**: `BoundarySeed.crossRetained_marks_share_a_side`,
  `BoundarySeed.crossRetained_other_marks_share_a_side`.
- **Axiom report**: propext; propext.
- **Falsifier**: a side-reading whole property that separates the two wholes;
  the cross-boundary matching being internally available at the retained
  configuration under either reading.
- **Surviving boundary**: the Challenge 4 retained configuration.

### B4-TWO-MEASURES

- **Statement**: The second declared measure at Challenge 4 counts how many of
  eight declared collateral facts a candidate makes available that the same
  reading's base did not.  Neither of the two facts nearest the requirement —
  the same separation said of the two sides, and the Challenge 3 separation
  said pointwise of the four marks — takes the requirement's value at every
  point, so the measure does not re-count the requirement as Challenge 3's did.
  The two measures are not the same function on the space, and under both
  readings they select the same minima.
- **Status**: COMPUTED.  Counted as content: the collateral facts are witness
  searches and the two agreement keys are censuses over the 192 points.  The
  declared list of eight is a declaration, not a survey, and it was declared
  before the enumeration ran.
- **Dependencies**: definitions 44, 51, 58; B4-CANDIDATE-SPACE.
- **Assumptions**: the eight facts are the declared ones; a different list
  would give a different measure.
- **Python evidence**: receipt `readings.*.sides_fact_agrees_with_the_requirement_at_every_point`,
  `pairwise_fact_agrees_with_the_requirement_at_every_point`,
  `measures_differ_somewhere`, `measures_agree_on_minima`, `minima_by_mu2`;
  `test_neither_near_fact_re_counts_the_requirement`,
  `test_the_fact_agreement_check_reads_both_ways`,
  `test_the_collateral_measure_counts_only_what_the_base_lacked`.
- **Lean theorem**: none.
- **Axiom report**: not applicable.
- **Falsifier**: either near fact agreeing with the requirement at every point;
  the two measures agreeing at every point of the space; or the two measures
  selecting different minimum sets.
- **Surviving boundary**: the declared space at the retained configuration.

### B4-BOUNDARY-DEPENDENCE

- **Statement**: At Challenge 4 the declared sense, its second reading, the
  pointwise sense, the identity of the candidate space, the capability counts,
  the one-step rule, the refusal of bundles, the whole grouping with its two
  coordinates, the tag and index properties, and the withdrawal of the mark
  permutations do not require the admitted boundary.  The side exchange, its
  withdrawal, the two side-reading whole properties, the label-and-side
  property, the grouping square's cells, the further-mark coordinate, and every
  separation result of the rung except the index withdrawal require it and are
  not formulated after removing it.
- **Status**: LIMITATION, a dependency classification of the run.  It is
  reported in the receipt and is not computed by anything.
- **Dependencies**: the seed's requirement to classify at every stage.
- **Assumptions**: removing the boundary is a counterfactual classification and
  not a third reading added to the model.
- **Python evidence**: receipt `boundary_dependence`; `test_receipt_shape`.
- **Lean theorem**: none.
- **Axiom report**: not applicable.
- **Falsifier**: as B0-BOUNDARY-DEPENDENCE.
- **Surviving boundary**: Challenge 4 dependency classification.

### B4-X

- **Statement**: At Challenge 5 the widened reader of Challenge 4 will refuse
  `<<a|>|>` by name as well, its declared bound reading marks and not wholes,
  so the bound will have to be widened a second time and priced a second time,
  paid by the run.  Depth will not be an internally available count at the
  retained configuration under either reading, the regime recording one side
  per admitted mark and no depth, and the boundary within a side will not be
  visible without a new declaration.  The rung will have to decide what the
  inner whole is — a datum, a side, or something needing a new definition — and
  that decision will take the shape Challenge 2's did: a declared finite space
  of policies with exactly one member letting the caller retain the
  inscription, priced and paid by the run.
- **Status**: SCORED at Challenge 5: PARTIAL.  Six clauses HIT: the Challenge 4
  reader refuses the nested whole by name (`reader.inherited_readers`); the new
  bound is priced and paid by the run (`reader.paid_by`); the ordinal — "a
  second" widening — holds, the run having three reader bounds and two
  widenings (`reader.widenings_of_the_reader_bound`); depth is available at no
  policy of capability count one; the inner whole is a second initial datum
  under no policy; and the decision takes the form of a declared finite policy
  space.  **MISSED**, recorded next to its value: "a declared finite space of
  policies with exactly one member letting the caller retain the inscription".
  **Three** of the four declared policies admit the caller's inscription
  (`scores.C4-X.policies_admitting_the_inscription`); exactly one retains it so
  that the retained state tells it from the flat inscription, and that count is
  reported beside the clause rather than substituted for it.  The clause is
  scored on the first count, which is what its own words say.  The frozen file
  is untouched, and the same miss is recorded in `challenge5/STATUS.md`.  The
  first clause was already half computed when this entry was written, so that
  clause is weak evidence and is marked as such.
- **Dependencies**: Challenge 5's reader bound, its policy space, and its
  declared depth.
- **Assumptions**: the clauses are scored on the frozen words; "letting the
  caller retain the inscription" is read as admitting it, and the narrower
  count — retaining it so that the state tells it from the flat inscription —
  is reported beside the clause and does not rescue it.
- **Python evidence**: receipt `receipts/challenge5.json` `scores.C4-X`;
  `test_the_previous_extrapolation_is_scored_clause_by_clause`,
  `test_c4x_hits_only_if_one_policy_admits_the_inscription`,
  `test_the_one_widening_is_given_two_ordinals_and_both_are_scored`.
- **Lean theorem**: none; every clause is a computation or a declaration.
- **Axiom report**: not applicable.
- **Falsifier**: as written in `challenge4/PREDICTIONS.md`; the
  "exactly one member" falsifier fired.
- **Surviving boundary**: the Challenge 5 policy space and reader bound.

### B5-READER

- **Statement**: Both readers the run has refuse `<<a|>|>` by name — the
  Challenge 1 reader, whose declared bound is at most one mark in a whole, and
  the Challenge 4 reader, whose bound is at most one mark on each side of the
  bar — because neither reads an item on a side that is itself a whole.  The
  run declares a third reader in which an item is nothing, one mark, or one
  whole, to a declared depth of two, refusing a deeper item by name; both
  narrower readers are left refusing.  This is the run's **third reader bound
  and its second widening**: the Challenge 1 bound was declared and not
  widened.  Reading a nested item is not admitting one.
- **Status**: DEFINITION for the two refusals, which are earlier rungs' bounds
  replayed on the caller's text, for the new bound, which is this rung's
  declaration, and for the count of bounds and widenings, which is a census of
  the run's own readers.  Not counted as content: score C5-1, **PARTIAL**.  Its
  readers clause HITS; its ordinal clause, "the bound must be widened a third",
  **MISSES** — the census gives three bounds and two widenings, which is the
  ordinal the frozen C4-X gives the same event and which is scored HIT there.
  Recorded next to its value here and in `challenge5/STATUS.md`; the frozen
  file is untouched.
- **Dependencies**: definitions 17, 47, 59, 60.
- **Assumptions**: the depth bound is a declaration, not a limit; the same
  reader at a wider bound reads deeper wholes.  The ordinal is scored on the
  frozen words and on one census read by both scored files, so that the same
  event is not given two ordinals with neither read.
- **Python evidence**: receipt `reader`, `reader.reader_bounds_declared` (3)
  and `reader.widenings_of_the_reader_bound` (2);
  `test_both_inherited_readers_refuse_the_inscription`,
  `test_the_widened_reader_reads_a_whole_within_a_side`,
  `test_the_widened_reader_refuses_what_is_beyond_its_bound`,
  `test_a_deeper_bound_reads_what_the_declared_one_refuses`,
  `test_the_reader_reads_every_member_of_the_declared_domain`,
  `test_the_one_widening_is_given_two_ordinals_and_both_are_scored`,
  `test_c5_1_hits_only_where_the_run_has_widened_three_times`.
- **Lean theorem**: none; the Lean model has no reader.
- **Axiom report**: not applicable.
- **Falsifier**: either inherited reader accepting the inscription; the new
  reader accepting an item deeper than its declared bound; or the widening not
  being priced as a declaration of the run.  The frozen falsifier list does not
  cover the ordinal, so none of the three fired; the ordinal is read against the
  census instead, which names two widenings and not three.
- **Surviving boundary**: Challenge 5 onward, as the run's reader.

### B5-POLICY-SPACE

- **Statement**: What an admission does with an item that is itself a whole is
  not decided by the admitted boundary.  The run declares four policies —
  refuse it; admit it as one opaque mark on the outer side, its interior
  discarded; discard the inner boundary and admit its items on the outer side;
  record the crossing, admitting its items each carrying the sides crossed —
  over three declared capabilities, at counts `0`, `1`, `1`, `2`.  With the
  naming coordinate of B5-NAMING the space has eight points.  A candidate is
  one step exactly when its capability count is one, and a candidate of two or
  more bundles capabilities and is refused as one step.
- **Status**: DEFINITION.  The policies, the capabilities, the counts, and the
  one-step rule are declarations of this rung; a hit on them is by construction
  and is not counted as content: score C5-2.
- **Dependencies**: definitions 61, 62, 71; B5-READER.
- **Assumptions**: the four exhaust the run's own reading of what an admission
  can do with such an item — nothing, the whole without its interior, the
  interior without the boundary, the interior with it — and that reading is
  itself a declaration, stated in the receipt.  The opaque policy carries a
  second declaration with it, definition 71: one presentation token for every
  whole admitted as a mark.  It is listed in
  `reader.declared_at_challenge_5` and reported at `reader.whole_token`, and
  what rests on it is recorded in B5-MEASURES-PART.
- **Python evidence**: receipt `policy_space`, `readings.*.policies`;
  `test_the_declared_policy_counts`,
  `test_the_space_is_the_product_of_its_declared_coordinates`,
  `test_the_naming_coordinate_is_a_capability_of_its_own`.
- **Lean theorem**: none; the Lean model carries no policy.
- **Axiom report**: not applicable.
- **Falsifier**: a policy count other than `0, 1, 1, 2`; one step not
  coinciding with capability count one; or the recording policy having
  capability count one.
- **Surviving boundary**: Challenge 5's enumeration, and nothing wider.

### B5-ONE-STEP-PARTS

- **Statement**: At Challenge 5 the capability count and the number of
  coordinates a candidate moves are **different numbers**: the recording policy
  moves one coordinate and uses two capabilities.  The run keeps the capability
  reading, because the seed requires a candidate called one step not to bundle.
  Challenge 4's statement that a candidate is one step "exactly when it moves
  one coordinate, which is exactly when the count of undeclared capabilities it
  uses is one" is therefore a fact about that rung's space and not a general
  one, and is narrowed accordingly.
- **Status**: COMPUTED, over the eight points of the declared space, with both
  readings of "one step" reported at each.  Counted as content: it is part of
  score C5-2's basis and is the reason the space's own key
  `one_step_iff_one_coordinate_moved` is false.
- **Dependencies**: definition 62; B5-POLICY-SPACE; definition 56 as narrowed.
- **Assumptions**: none beyond the declared counts.
- **Python evidence**: receipt `readings.*.one_step_iff_capability_count_one`
  (true) and `one_step_iff_one_coordinate_moved` (false);
  `test_one_step_is_capability_count_one_and_not_coordinate_count`.
- **Lean theorem**: none.
- **Axiom report**: not applicable.
- **Falsifier**: the two counts agreeing at every point of this rung's space.
- **Surviving boundary**: the Challenge 5 space; the narrowing of Challenge 4's
  sentence stands for the whole run.

### B5-RETENTION

- **Statement**: Under each admitting policy the caller's history for `<<a|>|>`
  is one supply and one admission, and the state it retains under each reading
  is the replay of that history: one mark, at address `(0,)` under the two
  one-step policies and `(0, 0)` under the recording one.  Every retained state
  is certified and replays from genesis; the refusing policy retains nothing
  and its refusal is recorded by name.
- **Status**: COMPUTED (the replay and certification at every point), with the
  histories themselves DEFINITION-level, following from the declared reader,
  convention, order, and policy.
- **Dependencies**: definitions 30, 59, 61, 63, 64; B5-READER, B5-POLICY-SPACE.
- **Assumptions**: the caller's "retains" is read as at Challenge 2, as the
  admission of what is supplied; the within-whole order is extended to every
  level, which is a declaration.
- **Python evidence**: receipt `readings.*.point_detail.*.history`, `retained`,
  `certified`, `replays_from_genesis`;
  `test_every_retained_state_replays_from_genesis`,
  `test_the_four_policies_on_the_caller_inscription`,
  `test_the_supplies_precede_every_admission`.
- **Lean theorem**: `BoundarySeed.nestedRetained_eq`,
  `BoundarySeed.flatRetained_eq`, `BoundarySeed.nestedRetained_addresses`.
- **Axiom report**: none for any of the three.
- **Falsifier**: a retained state that does not replay from genesis; a history
  that is not one supply and one admission; or an address other than the one
  the declared convention gives.
- **Surviving boundary**: Challenge 5's candidates; none is current.

### B5-NESTING-INVISIBLE

- **Statement**: Under both readings and at each of the two one-step policies,
  what `<<a|>|>` retains is one mark whose address has length one, and it is
  isomorphic to what the Challenge 1 inscription `<a|>` retains under the same
  reading — under the discarding policy, equal to it.  **So the object language
  cannot see a boundary within a side at any policy of capability count one.**
  More generally, a state recording one side per mark is blind to every
  exchange below the outermost boundary, at every state and every such level,
  and no property whatever of the flattened state separates the caller's nested
  whole from the flat one.
- **Status**: COMPUTED (the isomorphism searches at each candidate's own
  renamings, and the equality); PROVED (that the two flatten alike; that
  flattening is blind to every inner exchange, for an arbitrary state and
  level; and that no property of the flattened state separates them, for an
  arbitrary property).  Counted as content: score C5-3.
- **Dependencies**: definitions 65, 67; B5-RETENTION.
- **Assumptions**: the isomorphism relation is the candidate's own declared
  renamings; the flat inscription is read under the same policy.
- **Python evidence**: receipt
  `readings.*.point_detail.{opaque,discard}.flat_inscription_isomorphic`,
  `flat_inscription_equal`, `inherited_grammar.flat_inscription_regime_isomorphic`,
  and `collateral_facts.nesting_internally_visible` false;
  `test_the_nesting_is_invisible_at_every_one_step_policy`,
  `test_the_discarding_policy_retains_the_flat_regime_exactly`,
  `test_the_recording_policy_tells_the_two_inscriptions_apart`.
- **Lean theorem**: `BoundarySeed.flatten_nested_eq_flat`,
  `BoundarySeed.flatten_nested_eq_admitted`,
  `BoundarySeed.flattenDeep_exchangeLevel_succ`,
  `BoundarySeed.no_flattened_property_separates_the_nesting`.
- **Axiom report**: `[propext]` for all four.
- **Falsifier**: a one-step policy retaining a state with a mark count other
  than one, or one not isomorphic to what `<a|>` retains under either reading.
- **Surviving boundary**: every policy of capability count one in the declared
  space, under both readings.

### B5-TWO-TIED-MINIMA

- **Statement**: The two one-step policies are not the same policy: over the
  declared 144-member domain they retain non-isomorphic states at 95
  inscriptions, and at none of those is it the caller's own.  So among the
  points that admit the caller's inscription the minimum capability count is
  one, exactly two non-isomorphic classes attain it, both are retained, and
  **uniqueness is refuted under both readings** — where at Challenge 4 it was
  not refuted under U.
- **Status**: COMPUTED, a census over the declared domain with the parting
  inscriptions named, and the implemented quotient of definition 69.  Counted
  as content: score C5-4.
- **Dependencies**: definitions 62, 69; B5-POLICY-SPACE, B5-NESTING-INVISIBLE.
- **Assumptions**: two policies are the same policy exactly when they retain
  isomorphic states at every member of the declared domain; a wider domain
  might separate policies this one identifies.
- **Python evidence**: receipt `readings.*.policy_separation`,
  `minima_by_mu1`; `test_the_two_one_step_policies_are_two`,
  `test_the_minima_are_two_tied_classes_under_both_readings`,
  `test_differing_inscriptions_is_bounded_and_ordered`.
- **Lean theorem**: none; Lean closes no census.
- **Axiom report**: not applicable.
- **Falsifier**: the two policies agreeing up to isomorphism at every member of
  the declared domain; a class count other than two at the minimum; a minimum
  count other than one; or the two parting at the caller's own inscription.
- **Surviving boundary**: the declared policy space and the declared domain.

### B5-CLASS-KEY

- **Statement**: The implemented class key of a candidate is its declared
  structure together with a digest of its canonical key at every member of the
  declared domain — read over the domain and **not** at the caller's one
  inscription.  A key read at that inscription alone reports ONE class where
  the enumeration finds two, because the two one-step policies retain
  isomorphic states there, and so understates a tie the seed requires to be
  retained.  The digest is a naming device and never evidence: every
  inscription at which two candidates part is enumerated and the first of them
  are named.
- **Status**: COMPUTED, with the defect the domain-wide key exists to catch
  demonstrated in both directions.  It is the first quotient the run takes over
  a FUNCTION rather than over a state.
- **Dependencies**: definition 69; B5-TWO-TIED-MINIMA.
- **Assumptions**: the domain is a declaration; the digest is deterministic and
  is compared, never inverted.
- **Python evidence**: receipt `readings.*.points.*.class_key`;
  `test_the_class_key_read_at_one_inscription_understates_the_tie`,
  `test_the_digest_moves_with_the_behaviour`; injection row in `MANUAL.md`.
- **Lean theorem**: none.
- **Axiom report**: not applicable.
- **Falsifier**: a key read over the domain that identifies the two one-step
  policies, or one read at the caller's inscription that separates them.
- **Surviving boundary**: the Challenge 5 quotient.

### B5-INNER-WHOLE

- **Statement**: Under no declared policy is the inner whole a second initial
  datum — the state carries exactly one and no admission event of any kind
  makes another — and under no policy is it a side, sides coming with a
  boundary and never being admitted.  It is a MARK under the opaque policy,
  NOTHING AT ALL under the discarding policy, which admits only its items, and
  a second BOUNDARY under the recording policy, which is a new definition.
  Treating the inner whole as the outer whole was treated means that its own
  two sides are places at which a further mark may be admitted, and that holds
  under the recording policy alone, which is not one step.
- **Status**: COMPUTED (the datum reading at every point, and the probe with
  both values attained); PROVED (that no deep
  history moves the initial datum).  The classification of what the inner whole
  IS under each policy is a declaration of the run and is labelled as such.
  Counted as content: score C5-5.
- **Dependencies**: definitions 61, 63, 64, 69; B5-POLICY-SPACE.
- **Assumptions**: the mechanical reading of "treated as the outer whole was
  treated" is the admissibility of a further mark inside it; a different
  reading is available.  What the probe reads is a **census and not the
  policy's name**: the deep grammar is policy-agnostic and records the
  requested length-two address under every admitting policy, which the receipt
  reports at `address`, so the deciding fact is
  `deepest_place_the_policy_names` — the longest address the policy's own
  admissions produce over the declared 144-member domain, one at the two
  one-step policies and two at the recording one.  The census is scoped to that
  domain, as every other census of this rung is.
- **Python evidence**: receipt `what_the_inner_whole_is`,
  `readings.*.point_detail.*.further_mark_within_the_inner_whole`,
  `initial_datum_unchanged`; `test_no_policy_makes_a_second_initial_datum`,
  `test_a_further_mark_within_the_inner_whole_needs_the_recording_policy`,
  `test_the_deepest_place_a_policy_names_is_read_off_the_domain`,
  `test_a_place_is_nameable_exactly_when_the_policy_names_one_that_deep`,
  `test_the_probe_reports_the_address_the_replay_kept_at_every_point`,
  `test_what_the_inner_whole_is_under_each_policy`.
- **Lean theorem**: `BoundarySeed.deepReplay_initialDatum`.
- **Axiom report**: none.
- **Falsifier**: a retained state carrying a second initial datum; a policy
  admitting the inner whole as a side; or a further mark admissible inside it
  under a policy of capability count one.
- **Surviving boundary**: the declared policy space.

### B5-DEPTH-TWO-SENSES

- **Statement**: Under every one-step policy every retained mark of the
  declared domain is one boundary in, so depth separates nothing there.  Under
  the recording policy the depth of a mark is invariant under every permitted
  renaming and is determined by the key, so it is internally available in the
  sense Challenge 3 declared and Challenge 4 generalized.  It is nevertheless
  **not expressible**: no form of the closed observation grammar reads it, the
  grammar having no counting form, and this rung adds none.  The two senses are
  kept apart and neither is unconditional.
- **Status**: COMPUTED (the key-determination census over the declared domain,
  and the depths a policy can hold); PROVED (that no level exchange moves any
  mark's depth).  The grammar clause is DEFINITION-level, the grammar being the
  declared sum of two forms, and is reported apart.  Counted as content: score
  C5-6, on the census.
- **Dependencies**: definitions 65, 66, 67, 70; B5-POLICY-SPACE.
- **Assumptions**: "internally available" is the run's declared sense —
  invariant under the permitted renamings and determined by the key — and
  "expressible" is membership in the closed grammar; the two are different
  questions and are answered separately.
- **Python evidence**: receipt `readings.*.point_detail.*.depths_over_the_domain`,
  `collateral_facts.depth_determined_by_the_key`,
  `depth_expressible_in_the_closed_grammar` false everywhere, and
  `closed_grammar_forms_reading_depth` empty;
  `test_depth_is_one_at_every_one_step_policy`,
  `test_depth_is_determined_by_the_key_where_a_state_is_retained`,
  `test_the_key_determination_check_reads_both_ways`,
  `test_no_form_of_the_closed_grammar_reads_depth`,
  `test_no_permitted_renaming_moves_a_mark_depth`.
- **Lean theorem**: `BoundarySeed.exchangeAt_length`,
  `BoundarySeed.depth_invariant_under_exchange`,
  `BoundarySeed.depth_is_invariant_where_the_inner_side_is_not`,
  `BoundarySeed.nested_depth_survives_every_continuation`.
- **Axiom report**: `[propext]` for all four.
- **Falsifier**: a permitted renaming that changes a mark's depth; two members
  of the declared domain with equal keys and different depth signatures; a form
  of the closed grammar whose value depends on depth; or a mark of depth other
  than one under a one-step policy.
- **Surviving boundary**: the declared domain and the declared grammar.

### B5-NAMING

- **Statement**: Whether the reading's naming of the two sides reaches the
  inner boundary is a further declaration the seed's one admitted exception
  does not make, and the run carries it as a coordinate.  **Under U it
  collapses at every policy**: U names nothing at any level, so both its values
  declare the same permitted renamings and the same key.  **Under O it
  collapses at three policies of four**, and not at the recording one: with the
  naming reaching inward no side exchange is permitted at either level and the
  retained mark's address orbit has one member; without it, the exchange of the
  inner boundary's two sides is a renaming the object language cannot see, the
  orbit has two members, and **which side of the inner boundary the mark lies
  on is not internally available under O either**.  Under U, at the same
  recording policy, the orbit has four members and neither boundary's side is
  available.  All three counts are read at the recording policy; at the two
  one-step policies the same key reads two under U and one under O, no address
  there being longer than one.
- **Status**: COMPUTED (the collapses, by the implemented quotient over the
  whole domain, and the three orbit sizes, over the unpruned enumeration);
  PROVED (that nothing invariant under the inner exchange separates the two
  inner sides, for an arbitrary property, with a countermodel).  Counted as
  content: score C5-7.
- **Dependencies**: definitions 66, 67, 68, 69; B5-POLICY-SPACE.
- **Assumptions**: a level whose sides carry no admitted name has an exchange
  the object language cannot see, and the exchanges of different levels are
  independent declarations; both are declarations of definition 67.
- **Python evidence**: receipt `readings.*.naming_coordinate_collapses_at`,
  `naming_coordinate_collapses_everywhere`,
  `point_detail.*.mark_address_orbit_size`,
  `collateral_facts.inner_side_internally_available`;
  `test_the_naming_coordinate_collapses_under_U_and_not_under_O`,
  `test_the_address_orbit_sizes_under_each_declaration`,
  `test_the_inner_side_is_unavailable_under_O_without_the_declaration`,
  `test_under_U_neither_side_of_either_boundary_is_available`.
- **Lean theorem**: `BoundarySeed.exchangeLevel_one_nestedRetained`,
  `BoundarySeed.no_invariant_property_separates_the_inner_sides`,
  `BoundarySeed.innerSideIsZero_separates`,
  `BoundarySeed.innerSideIsZero_is_not_invariant_under_the_inner_exchange`.
- **Axiom report**: `[propext]` for the first and the third, none for the
  second, `[propext, Quot.sound]` for the fourth.
- **Falsifier**: the coordinate not collapsing under U; the inner side being
  internally available under O without the further declaration; or an address
  orbit size other than four, one, and two respectively.
- **Surviving boundary**: two boundary levels; what happens at three is not
  computed.

### B5-MEASURES-PART

- **Statement**: The two declared cost measures select **different** minima at
  this rung: the capability count ties the two one-step policies at one, and
  the collateral count picks the discarding policy alone under both readings.
  This is the first rung at which they part under **both** readings; at
  Challenge 3 they parted under O alone (B3-TWO-MEASURES: "under O they do
  not") and at Challenge 4 they agreed under both (B4-TWO-MEASURES).  The one
  declared fact that parts them is the seventh,
  `inner_whole_presentation_admitted`, which is the presence of definition 71's
  whole token among the retained labels: it holds at the opaque policy and at
  no other minimum, so the choice between the two tied minima rests on that
  declaration.  The eight declared collateral facts are
  facts and not independent facts, and the receipt names the pairs that take
  the same value at every point of the space rather than re-weighting the
  measure.
- **Status**: COMPUTED, over the declared space under each reading.  That this
  is the first rung at which they part under both readings is read off the
  Challenge 3 and Challenge 4 receipts' own
  `readings.*.measures_agree_on_minima`, not asserted.
- **Dependencies**: definitions 62, 70, 71; B5-TWO-TIED-MINIMA; B3-TWO-MEASURES
  and B4-TWO-MEASURES for the comparison.
- **Assumptions**: a fact about a retained configuration is FALSE where nothing
  is retained; absence of a test is not turned into the fact holding.  The
  parting turns on definition 71, a declaration of this rung: a different token
  policy for an opaquely admitted whole would move the seventh fact and could
  remove the parting.
- **Python evidence**: receipt `readings.*.measures_agree_on_minima` false,
  `minima_by_mu2`, `collateral_facts_agreeing_everywhere`;
  `test_the_two_measures_select_different_minima`,
  `test_the_facts_that_agree_everywhere_are_named`,
  `test_the_agreement_check_reads_both_ways`,
  `test_a_fact_is_false_where_nothing_is_retained`,
  `test_the_collateral_measure_counts_only_what_the_base_lacked`.
- **Lean theorem**: none.
- **Axiom report**: not applicable.
- **Falsifier**: the two measures selecting the same minima under either
  reading; or a pair of facts reported as agreeing everywhere that differs at
  some point.
- **Surviving boundary**: the declared space at the caller's inscription.

### B5-INERTIA

- **Statement**: Nothing at Challenge 5 changes the initial datum, the reading,
  or the event-follows relation, which stays empty on every probe of both event
  grammars at every point; every admitting point's history is certified and
  replays from genesis and every refusing point retains nothing; no rule of an
  earlier rung is withdrawn; and one event kind, `AdmitAt`, is added, available
  only under the recording policy.  A mark's depth survives every continuation,
  however many further marks are admitted at whatever depth.
- **Status**: COMPUTED (the certification, the replay, and the probes at every
  point, with both values of the admission predicate attained); PROVED (that
  any deep history keeps the reading and the datum, that the deep event-follows
  relation is empty, and that an admitted address is read the same after any
  later history).  The empty relation is DEFINITION-level and is reported
  apart.  Counted as content: score C5-8.
- **Dependencies**: definitions 9, 63, 64; B5-RETENTION.
- **Assumptions**: the probe set offers every event kind of the deep grammar.
- **Python evidence**: receipt `readings.*.point_detail.*.event_follows_relation_empty`,
  `inherited_event_follows_relation_empty`, `initial_datum_unchanged`,
  `reading_unchanged`, `new_event_kinds_at_challenge_5`,
  `withdrawn_rules_at_challenge_5`;
  `test_the_probe_set_offers_every_event_kind_of_the_deep_grammar`,
  `test_an_admission_of_a_token_never_supplied_is_refused`,
  `test_deep_certify_reads_false_on_a_refused_history`.
- **Lean theorem**: `BoundarySeed.deep_no_event_follows`,
  `BoundarySeed.deepReplay_reading`,
  `BoundarySeed.deepReplay_preserves_address`,
  `BoundarySeed.no_event_follows_nestedRetained`.
- **Axiom report**: `[propext]` for the first, third and fourth; none for the
  second.
- **Falsifier**: a non-empty event-follows relation at any point; a retained
  state that does not replay from genesis; or an earlier event kind withdrawn.
- **Surviving boundary**: Challenge 5 and every later stage that adds no rule.

### B5-OUTSIDE

- **Statement**: The run formulates no address value denoting the outside of
  the outermost boundary.  An address is a sequence of sides crossed inward and
  the declared alphabet has two values, both of them sides of a boundary
  already crossed; so the outside is not formulable in the declared alphabet.
- **Status**: OPEN.  The question is named and not answered, and the run
  declines to declare a value for it, because a declaration made to answer the
  question would be fitting the model to the answer.
- **Dependencies**: definition 63; the seed's required question 11.
- **Assumptions**: none; the statement is about the declared alphabet only and
  makes no claim about what a different alphabet could formulate.
- **Python evidence**: receipt `outside_of_the_outermost_boundary`;
  `test_receipt_shape`.
- **Lean theorem**: none.
- **Axiom report**: not applicable.
- **Falsifier**: an address value in the declared alphabet denoting the
  outside.
- **Surviving boundary**: the declared address alphabet.

### B5-BOUNDARY-DEPENDENCE

- **Statement**: At Challenge 5 the identity of the policy space, the
  capability counts, the one-step rule, the refusal of bundles, and the two
  senses of an available depth do not require the admitted boundary.  The
  notion of depth, the address, the crossing, every level exchange, the
  invisibility of the nesting at every one-step policy, and the reader's own
  bound require it and are not formulated after removing it.  The outside of
  the outermost boundary requires it to be formulated at all, and is not
  formulated.
- **Status**: LIMITATION, a dependency classification of the run.  It is
  reported in the receipt and is not computed by anything.
- **Dependencies**: the seed's requirement to classify at every stage.
- **Assumptions**: removing the boundary is a counterfactual classification and
  not a third reading added to the model.
- **Python evidence**: receipt `boundary_dependence`; `test_receipt_shape`.
- **Lean theorem**: none.
- **Axiom report**: not applicable.
- **Falsifier**: as B0-BOUNDARY-DEPENDENCE.
- **Surviving boundary**: Challenge 5 dependency classification.

### B5-X

- **Statement**: At the autonomous continuation the first challenge the
  generator justifies from a surviving Challenge 5 branch will be a further
  MARK and not a deeper nesting — a further mark costing one capability at
  every rung that has priced it and deeper nesting costing two here, with the
  generator required to be the weakest justified.  The stage will not reach
  fifteen accepted augmentation rounds on any branch in one session; it will
  declare a smaller resource bound, export the exact frontier, and state what
  is complete within that bound and nothing wider.
- **Status**: OPEN; the extrapolation of Challenge 5, scored by the autonomous
  continuation.  Nothing of it is computed here.
- **Dependencies**: the continuation's declared generator, its resource bound,
  and its frontier export.
- **Assumptions**: none yet.
- **Python evidence**: none yet.
- **Lean theorem**: none yet.
- **Axiom report**: not applicable.
- **Falsifier**: as written in `challenge5/PREDICTIONS.md`.
- **Surviving boundary**: not yet.
