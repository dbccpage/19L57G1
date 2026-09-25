# CLAIM LEDGER: rung seven -- duration under the CHANGING reading

`AuthorityEffect: None`.  Every row carries an evidence class.  A row at
the level of a definition is marked so and is never counted as content.
Per-theorem classification is NOT this file's job: it is
`FWDEF_CENSUS.json`'s, which is total over all thirty-three theorems of
this rung's package and is checked in both directions by
`test_census.py`.  Counts in this file are dated 2026-09-25.

Classes used: DEFINITION (true by unfolding, by `rfl`, by a projection,
by one rewrite, by kernel computation over a concrete history, or by pure
case exhaustion), PROVED_THEOREM, RECONSTRUCTION (the sealed estate's
theorem, reproduced verbatim under a pin, with no credit claimed here),
COUNTERMODEL, FINITE_COMPUTATION, OPEN, PREDICTION, RECORDED.

Library axioms, recorded exactly: of the thirty-three theorems, two
depend on no axiom, sixteen on `propext` alone, and fifteen on `propext`
and `Quot.sound`; none depends on `Classical.choice` or on any other
axiom.  The committed log is `receipts/lean_axioms.txt`, checked against
a fresh clean build by `verify_lean.py`.

---

## The leftover this rung takes, quoted by pin

Rung six's own leftover list names this rung's question.  It is quoted
verbatim from the span pinned in `SOURCE_MANIFEST.json` as
`research/second_succession/STATUS.md` lines 161-167, and is not edited:

> - **W-1, duration under the CHANGING reading.**  The seed's census row
>   for duration reads it as rounds between growths.  Under CHANGING the
>   regime carries the total number of rounds and, separately, the number
>   of growths (its data); whether it carries the number of changing rounds
>   between two growths -- or only bounds on it, through which data the
>   admitted instances and requirements name -- is not decided.  Price:
>   small; the counts and the rectangle are in place.

**What this rung did with it.**  It declared a growth (a round that adds
a datum), a rest round (any other round), and the duration vector of a
history (its rest rounds counted by the number of growths before them),
and decided which of it the regime a history reaches carries.  Given the
base, the regime carries the number of segments and their sum, for every
history; it does not carry any single segment, and it does not carry a
duration between two growths even when every history starts at the
sealed empty regime.  It carries lower bounds: the instances and
requirements naming a datum or a later one are at most the rest rounds
taken after that datum exists; and when every new element names the
newest datum, the vector is fixed.  On the rectangle, the vectors
reached at each regime are exactly the tuples those lower bounds allow;
beyond it, that is open.

---

## Stage one: the reconstruction

| id | claim | class | evidence |
|---|---|---|---|
| DUR-1 | The sealed kernel slice -- regime, well-formedness, contexts, derivability, collapse, separability, the six event kinds, the step, the replay, replay compositionality, the empty regime and the two sealed reading regimes with their recorded histories -- is reproduced verbatim under two blob pins and three span pins. | RECONSTRUCTION | `lean/SecondDuration/Kernel.lean`; pins on `lean4/Derivation/Basic.lean` and `Inertia.lean`; `test_every_shared_declaration_is_identical` |
| DUR-2 | Thirty-seven declarations are shared between the reconstruction and its two pinned sources, and every one is identical after comments and namespace lines are stripped and whitespace is normalized; the four omitted declarations are pinned by name and mentioned nowhere in the reconstruction. | FINITE_COMPUTATION | `test_every_shared_declaration_is_identical`; `test_the_omitted_declarations_are_recorded_not_judged` |

## Stage two: the duration vector, in Lean

| id | claim | class | evidence |
|---|---|---|---|
| DUR-3 | A growth of a history replayed from a base is an event after which the regime has other data than before; a rest round is an event after which the regime differs and has the same data.  `during n` counts the rest rounds taken while the regime has exactly `n` data, so that segment `i` of the vector from a base with `k` data is `during (k + i)`; `after t` counts those taken while it has more than `t` data; `naming t` counts the instances and requirements naming a datum index at or above `t`.  Each count stops at an ill-formed event, as replay does. | DEFINITION | the definitions `size`, `growths`, `rest`, `during`, `after`, `naming` in `Rounds.lean`; `replayE_cons` |
| DUR-4 | Every event of the sealed step leaves the regime unchanged, or adds one datum and one element, or keeps the data and adds one element. | PROVED_THEOREM | `step_parts`, `insertNew_grows` (rung six's lemma, proved again here; its statement is not new to the run) |
| DUR-5 | For every base and every history that replays from it, the regime reached has the base's data plus the growths, and its element count is the base's plus the growths plus the rest rounds.  No decidability hypothesis, no well-formedness hypothesis, and none beyond the replay. | PROVED_THEOREM | `growths_counted`, `rest_counted`; `test_n1_growths_and_rest_rounds_are_read_off_base_and_regime`; prediction N-1, HIT |
| DUR-6 | Hence a function of the base and the regime gives the number of growths -- one less than the number of segments -- and the number of rest rounds, the sum of the vector: the data of the regime less the base's, and the element count of the regime less the base's less that difference. | PROVED_THEOREM | `growths_given_base`, `rest_given_base`; prediction N-1, HIT |
| DUR-7 | No function of a position, a base and a regime gives the rest rounds taken at that position: from the sealed empty regime a form of arity one then a datum, and a datum then the form, reach one regime with segment zero one and zero. | COUNTERMODEL | `lead_splits` (kernel computation), `segment_not_given_base`; `test_n2_a_segment_is_refused_given_the_base`; prediction N-2, HIT |
| DUR-8 | No function of the regime alone gives the duration between the first and the second growth, even over histories from the sealed empty regime: a datum, a form of arity one, a datum; and a datum, a datum, the form, reach one regime with that duration one and zero. | COUNTERMODEL | `gap_splits` (kernel computation), `gap_not_from_genesis`; `test_n3_a_duration_between_growths_is_refused_from_the_empty_regime`; prediction N-3, HIT |
| DUR-9 | For every base, every history that replays from it and every `t`, the instances and requirements of the regime reached that name `t` or later are at most those of the base plus the rest rounds taken after the regime has more than `t` data.  No well-formedness hypothesis on the base.  For every history, replayed or not, the rest rounds after `t` are among the rest rounds. | PROVED_THEOREM | `naming_step`, `naming_bounded`, `after_le_rest`; `test_n4_the_lower_bound_needs_no_well_formed_base`; prediction N-4, HIT |
| DUR-10 | When the base names nothing at or above `t` and the regime reached has as many instances and requirements naming `t` or later as the history has rest rounds, every rest round is taken after the regime has more than `t` data.  In particular every history from the sealed empty regime reaching the regime of two data and the one requirement between them takes one rest round, after the second growth: its vector is fixed. | PROVED_THEOREM | `tail_forced`, `pinned_by_requirement`; `test_n5_the_tail_is_forced_when_everything_names_late`; prediction N-5, HIT |
| DUR-11 | That every tuple the lower bounds allow is the vector of some history -- attainment of the envelope -- is NOT proved here, and nothing is carried across the sealed isomorphism; no native module names either. | OPEN | `test_n6_no_theorem_mentions_the_isomorphism_or_attainment`; prediction N-6, HIT |

## Stage three: the finite cross-check

Over rung three's rectangle, unchanged: three bases, every sequence of at
most four declared events, 577, 3928 and 14293 sequences reaching 75, 523
and 1718 distinct regimes.  Vectors are taken by stepping the sealed
Python step; envelopes are enumerated by exhaustion over tuples.

| id | claim | class | evidence |
|---|---|---|---|
| DUR-12 | Every node replays from its base; the sequence and regime counts are rung four's. | FINITE_COMPUTATION | `receipts/duration.json` `bases`, `replay_mismatches`; `test_the_rectangle_is_rung_three_s`; prediction N-8, HIT |
| DUR-13 | On every sequence of every base the vector has one entry more than the regime reached has new data, and sums to the number of new elements other than data.  Zero violations of each. | FINITE_COMPUTATION | `length_violations`, `sum_violations`; `test_a_forged_vector_violates_the_shape_laws_and_the_envelope`; prediction N-9, HIT |
| DUR-14 | At every base every vector reached lies in its envelope, and at every regime reached the set of vectors reached is exactly its envelope; so a regime is reached with one vector exactly when its envelope has one tuple -- 28, 263 and 1121 regimes at EMPTY, L and F. | FINITE_COMPUTATION | `vectors_outside_envelope`, `regimes_with_unreached_or_extra_tuples`, `one_tuple_iff_one_vector_violations`; `test_the_envelope_is_reached_exactly`; `test_a_vector_below_the_bound_is_outside_the_envelope`; prediction N-10, HIT |
| DUR-15 | 47, 260 and 597 regimes are reached with two vectors at EMPTY, L and F, and 19, 63 and 103 with two tuples of durations between growths.  The shortest vector-splitting sequence at every base is a datum then a form of arity one (two events); the shortest gap-splitting sequence is two data then the form (three events). | FINITE_COMPUTATION | `vector_split_regimes`, `gap_split_regimes`, the two shortest-sequence records; `test_the_split_counts_are_the_dated_ones`; prediction N-11, HIT |
| DUR-16 | 3, 13 and 17 regimes with at least one growth and at least one rest round have an envelope of one tuple, whose rest rounds all lie in the tail. | FINITE_COMPUTATION | `tail_only_regimes`; `test_the_tail_only_census`; prediction N-12, HIT |
| DUR-17 | Taken up to the implemented isomorphism, within each base, over 54, 174 and 265 classes at EMPTY, L and F: 34, 69 and 73 classes are reached with two vectors; none with two vector sums; and 3, 45 and 50 carry two regimes with different envelopes -- the envelope is not carried by the class, because renaming data moves levels. | FINITE_COMPUTATION | `classes`; `test_isomorphic_regimes_with_two_envelopes_are_counted`; prediction N-13, HIT |
| DUR-18 | Each of the Lean countermodels, written in the sealed Python grammar, replays with both sides reaching one regime and the segments one and zero as claimed; the regime of `pinned_by_requirement` has the one-tuple envelope (0, 0, 1). | FINITE_COMPUTATION | `lean_witnesses`; `test_the_lean_witnesses_replay`; prediction N-14, HIT |

## Stage four: the census row this rung decides

| id | claim | class | evidence |
|---|---|---|---|
| CENSUS-duration | Duration, as rest rounds between growths, under the CHANGING reading over histories of the sealed step.  The durations between growths are NOT DEFINABLE from the base and the regime, nor from the regime over histories from the sealed empty regime (`gap_not_from_genesis`); no single segment is (`segment_not_given_base`).  DEFINABLE from the base and the regime: the number of segments and the sum of the vector (`growths_given_base`, `rest_given_base`), and lower bounds on every sum of later segments through the data the instances and requirements name (`naming_bounded`); the whole vector when every new element names the newest datum (`tail_forced`).  That the vectors reached are exactly the tuples those bounds allow: a finite computation on the rectangle (DUR-14) and OPEN beyond it, leftover V-1.  Up to the implemented isomorphism: the envelope is not a class invariant on the rectangle (DUR-17), and whether the sum is is OPEN beyond it, behind rung five's Z-1.  FORCED in the seed's sense is conditional on an engine whose rounds are the changing events of the sealed step; no such engine is declared yet.  No earlier rung decided this row. | PROVED_THEOREM with COUNTERMODEL, FINITE_COMPUTATION and OPEN | DUR-5 to DUR-17; prediction N-15, HIT |

## Recorded

| id | claim | class | evidence |
|---|---|---|---|
| DUR-INPUTS | This rung neither reduces the count of declared inputs nor proves it at a floor; the value stays two, with no proof of a floor. | RECORDED | `receipts/duration.json` `input_count_claim`; prediction N-16, HIT |
| DUR-PREDICTIONS | Of the frozen predictions, the seven computational rows score seven hits and no miss.  The FW-DEF prediction names sixteen targets and scores thirteen hits and three misses, with no native theorem it did not name: `growths_counted` and `naming_step` promoted from THIN to CONTENT, `naming_bounded` demoted from CONTENT to THIN.  Six rows were labelled FORCED before the run, and a hit on a FORCED row evidences the order of the work, not insight. | PREDICTION | `receipts/duration.json` `predictions_scored`; `test_the_scored_verdicts_are_the_dated_ones`; `test_the_prediction_is_scored_at_the_dated_values`; `test_every_miss_is_the_dated_one` |
