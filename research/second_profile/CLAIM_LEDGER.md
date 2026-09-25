# CLAIM LEDGER: rung nine -- two-ness and the observational classes

`AuthorityEffect: None`.  Every row carries an evidence class.  A row at
the level of a definition is marked so and is never counted as content.
Per-theorem classification is NOT this file's job: it is
`FWDEF_CENSUS.json`'s, which is total over all fifty theorems of this
rung's package and is checked in both directions by `test_census.py`.
Counts in this file are dated 2026-09-25.

Classes used: DEFINITION (true by unfolding, by `rfl`, by a projection,
by one rewrite, by kernel computation over concrete regimes, or by pure
case exhaustion), PROVED_THEOREM, RECONSTRUCTION (the sealed estate's
theorem, reproduced verbatim under a pin, with no credit claimed here),
COUNTERMODEL, FINITE_COMPUTATION, OPEN, PREDICTION, RECORDED.

Library axioms, recorded exactly: of the fifty theorems, three depend on
no axiom, twenty on `propext` alone, and twenty-seven on `propext` and
`Quot.sound`; none depends on `Classical.choice` or on any other axiom.
The committed log is `receipts/lean_axioms.txt`, checked against a fresh
clean build by `verify_lean.py`.  The first complete build had seven
theorems reaching `Classical.choice`; the cause was the `omega` tactic
closing a goal that was a conjunction, or a goal that was not arithmetic
at all, and each such use was rewritten to close one arithmetic goal at
a time.  `STATUS.md` records it.

---

## The leftover this rung takes, quoted by pin

Rung three's leftover list names X-6, and rung eight's application of
the seed's next-rung rule selects it.  Rung three's text is quoted
verbatim from the span pinned in `SOURCE_MANIFEST.json` as
`research/second_index/STATUS.md` lines 165-168, and is not edited:

> - **X-6, the other eleven rows of the challenge-five census.**  Two-ness,
>   observational classes, duration, adjacency, reach, invariants,
>   irreversibility, symmetry, branching, exhaustion and recurrence.  This
>   rung decides one row and claims nothing about the rest.

As rung eight carries it, quoted from the span pinned as
`research/second_class/STATUS.md` lines 213-216:

> - Carried from rung three, unchanged: X-1, X-2, X-4, X-5, and X-6 less
>   symmetry, invariants, irreversibility, succession, duration and
>   recurrence: two-ness, observational classes, adjacency, reach,
>   branching and exhaustion.

**The reading this rung applied, recorded in `PROMPT.md` before its
predictions were frozen.**  Rung eight left open whether a rung taking
X-6 decides all six rows or some, and which first.  This rung took the
rows in the order rung three named them and decided the first two, which
are both read off the profile of an admitted datum and need no
response; the next row, adjacency, is declared by the seed through a
response, and no responder is declared in this run.  The reading binds
no later rung.

**What this rung did with it.**  It declared holding two -- some two
admitted data separable -- as the reading of two-ness, and representative
lists as the reading of the observational classes, and proved that the
sealed isomorphism carries separability, collapse, holding two and
representative lists with no hypothesis on either regime.  It proved
what holding two needs -- two data, a form and an instance -- and that
from the sealed empty regime no history shorter than four events reaches
it, and from each sealed reading regime none shorter than two; both
bounds are attained.  It proved that four of the six event kinds keep
every separable pair separable, and exhibited the other two ending
holding two.  The class count as a number stays a finite computation.

---

## Stage one: the reconstruction

| id | claim | class | evidence |
|---|---|---|---|
| PRF-1 | The sealed kernel slice -- regime, well-formedness, contexts, derivability, collapse, separability, the six event kinds, the step, the replay, replay compositionality, the empty regime and the two sealed reading regimes with their recorded histories -- and the sealed isomorphism structure with its requirement ordering, its identity instance and the swap of the first two data, are reproduced verbatim under three blob pins and four span pins. | RECONSTRUCTION | `lean/SecondProfile/Kernel.lean`, `lean/SecondProfile/IsoKernel.lean`; pins on `lean4/Derivation/Basic.lean`, `Inertia.lean` and `Minimality.lean`; `test_every_shared_declaration_is_identical` |
| PRF-2 | Forty-one declarations are shared between the reconstructions and their three pinned sources, and every one is identical after comments and namespace lines are stripped and whitespace is normalized; the omitted declarations are pinned by name and mentioned nowhere in the reconstructions. | FINITE_COMPUTATION | `test_every_shared_declaration_is_identical`; `test_the_omitted_declarations_are_recorded_not_judged` |

## Stage two: observation across the isomorphism, in Lean

| id | claim | class | evidence |
|---|---|---|---|
| PRF-3 | A context carried along an inhabitant of the sealed isomorphism -- its form by the form map, every filled slot by the data map, every hole kept a hole -- and plugged with the image of a datum gives the carried plugging; a well-formed context of the source is carried to a well-formed context of the target; every argument of the plugging of an admitted datum into a well-formed context is admitted. | PROVED_THEOREM | `mapCtx`; `plug_mapCtx` (at the level of a definition), `wfCtx_mapCtx`, `plug_args_lt`, `map_inv` |
| PRF-4 | For a well-formed context of the source and an admitted datum, the plugging is derivable in the source exactly when the carried plugging is derivable in the target, with no hypothesis on either regime. | PROVED_THEOREM | `derivable_fwd` (at the level of a definition), `derivable_bwd`, `derivable_mapCtx` |
| PRF-5 | For every two regimes, every inhabitant of the sealed isomorphism between them and every two data admitted in the source, separability of the two is carried to their images, and so is collapse; neither needs well-formedness or the absence of a repeated entry, of either regime.  Collapse is carried by pulling every context of the target back along the exchanged structure, which repeats rung eight's `isoSymm`. | PROVED_THEOREM | `separable_iso`, `collapsed_iso`; `test_q1_observation_is_carried_with_admitted_data_only`; prediction Q-1, HIT |
| PRF-6 | Collapse is reflexive, symmetric and transitive, so the observational classes of a regime are classes. | PROVED_THEOREM (at the level of a definition) | `collapsed_refl`, `collapsed_symm`, `collapsed_trans`; `test_q3_collapse_is_reflexive_symmetric_and_transitive`; prediction Q-3, HIT |
| PRF-7 | A regime holds two exactly when an isomorphic regime does; a representative list of the source, carried by the data map, is a representative list of the target, of the same length; neither needs a hypothesis on either regime. | PROVED_THEOREM | `HoldsTwo`, `Reps`; `holdsTwo_iso`, `reps_iso`; `test_q2_holding_two_and_representatives_need_no_hypothesis`; prediction Q-2, HIT |
| PRF-8 | A representative list with two entries witnesses holding two; with no instance, the first datum alone represents every admitted datum, and no regime holds two. | PROVED_THEOREM | `holdsTwo_of_reps`, `reps_of_no_insts`, `no_twoness_without_insts` |
| PRF-9 | Whether any two representative lists of one regime have one length -- the class count as a NUMBER in Lean -- is NOT proved here.  Collapse quantifies over every context and no decision procedure for it is built in this run. | OPEN | leftover T-1; rung three's X-1 |

## Stage three: what holding two needs, and when it is first reached, in Lean

| id | claim | class | evidence |
|---|---|---|---|
| PRF-10 | A regime that holds two has at least two data, at least one form and at least one instance, with no hypothesis on the regime. | PROVED_THEOREM | `holdsTwo_parts`; prediction Q-4, HIT |
| PRF-11 | Every event the sealed step accepts raises the number of data plus the lengths of the lists of forms and of instances by at most one, and lowers no number of data; so every history reaches a regime whose count of those is at most the base's plus the length of the history, with at least the base's data. | PROVED_THEOREM | `insertNew_le` (at the level of a definition), `step_parts_le`, `replay_parts_le` |
| PRF-12 | Every history from the sealed empty regime reaching a regime that holds two has at least four events; from each sealed Lean reading regime, at least two. | PROVED_THEOREM | `twoness_needs_four`, `twoness_needs_two_L`, `twoness_needs_two_F`; `test_q4_the_bounds_and_their_witnesses`; prediction Q-4, HIT |
| PRF-13 | The bounds are attained: a datum, a datum, a form of arity one and the instance of that form at the first datum, from the sealed empty regime, reach a regime that holds two, whose two data form a representative list; the last two of those events do the same from each sealed Lean reading regime.  The sealed Lean reading regimes hold a requirement the Python bases do not; requirements do not enter derivability, and the same witnesses hold in the Python grammar (PRF-19). | DEFINITION | `twoness_at_four`, `twoness_at_two_L`, `twoness_at_two_F`, `two_classes_at_four` (each by kernel computation); prediction Q-4, HIT |

## Stage four: which events keep holding two and which end it, in Lean

| id | claim | class | evidence |
|---|---|---|---|
| PRF-14 | For every regime, every pair of data and every accepted event that is neither an instance admission nor a rule admission -- a supply, a datum, a form or a requirement -- a separable pair stays separable; so those four kinds keep holding two.  No hypothesis on the regime.  The form case reads the arity of an old form through the lengthened list, which repeats rung five's `getD_append_lt`, proved again at rung eight and here. | PROVED_THEOREM | `getD_append_lt`, `separable_step_keep`, `holdsTwo_step_keep`; `test_q5_four_kinds_keep_separability_with_no_hypothesis`; prediction Q-5, HIT |
| PRF-15 | The other two kinds can end holding two: a well-formed regime of two data, one form of arity one and its instance at the first datum holds two, and after the instance at the second datum, or after the uniform rule of the form, no two admitted data are separable.  The first needs an argument over every context -- each well-formed context of the regime reached is the one-hole context of its only form -- and is not a kernel computation. | COUNTERMODEL | `twoness_lost_by_inst`, `twoness_lost_by_rule`; `test_q6_two_kinds_can_end_it`; prediction Q-6, HIT |

## Stage five: the finite cross-check

Over rung three's rectangle, unchanged: three bases, every sequence of at
most four declared events, 577, 3928 and 14293 sequences reaching 75,
523 and 1718 distinct regimes, 2316 in all.  Holding two is read by the
sealed `separable`, the class count by the sealed `profiles`; classes of
regimes are the sealed key procedure's.

| id | claim | class | evidence |
|---|---|---|---|
| PRF-16 | Every node replays from its base; there are 54, 174 and 265 classes of regimes within EMPTY, L and F and 402 over all three; the key partition and the brute-force partition agree at every one of the 2316 regimes. | FINITE_COMPUTATION | `receipts/profile.json`; `test_the_rectangle_is_rung_three_s`; prediction Q-8, HIT |
| PRF-17 | The least length of a sequence reaching a regime that holds two is four at EMPTY and two at L and at F; at EMPTY exactly 22 sequences hold two, reaching 6 regimes in 3 classes; at L 2036 sequences, 315 regimes, 82 classes; at F 8676 sequences, 1240 regimes, 156 classes.  At every regime, it holds two exactly when its class count is at least two. | FINITE_COMPUTATION | `test_the_holding_two_counts_are_the_dated_ones`; predictions Q-9 and Q-10, HIT |
| PRF-18 | The largest class count is two at EMPTY, three at L and four at F; no regime has more classes than data, or more than its named data plus one.  The class counts over the distinct regimes are, at EMPTY, 21 regimes with none, 48 with one, 6 with two; at L, 208, 225 and 90 with one, two and three; at F, 478, 356, 824 and 60 with one to four. | FINITE_COMPUTATION | `test_the_class_count_histograms_are_the_dated_ones`; prediction Q-11, HIT |
| PRF-19 | No class of regimes, within a base or over all three, carries two values of holding two or of the class count.  The Lean witnesses hold in the Python grammar: the four-event history holds two with class count two, and one instance or one rule after it ends holding two with class count one. | FINITE_COMPUTATION | `lumping`, `lean_witnesses`; `test_a_lumping_partition_is_counted_everywhere`; `test_the_lean_witnesses_in_the_python_grammar`; prediction Q-12, HIT |
| PRF-20 | No transition at EMPTY ends holding two; at L, 28 transitions by an instance and 126 by a rule end it, and at F, 6 and 370; no other kind ends it.  Over all three bases the class count changes by zero under a supply, a requirement and a form; by zero or one under a datum; by minus two, minus one or zero under a rule; and by minus one, zero, one or two under an instance, never by minus two. | FINITE_COMPUTATION | `base_report`; `test_no_instance_admission_lowered_the_count_by_two`; predictions Q-13 and Q-14, HIT |

## Stage six: the census rows this rung decides

| id | claim | class | evidence |
|---|---|---|---|
| CENSUS-twoness | Two-ness, read as HOLDING TWO -- some two admitted data separable in the sealed sense -- is DEFINABLE: a property of the regime's own observables, carried by the sealed isomorphism with no hypothesis on either regime (`holdsTwo_iso`, through `separable_iso`).  Its first stage is four events from the sealed empty regime and two from each sealed reading regime, proved as a lower bound for every history (`holdsTwo_parts`, `twoness_needs_four`, `twoness_needs_two_L`, `twoness_needs_two_F`) and attained (`twoness_at_four` and its two companions).  It is not kept by every event: a supply, a datum, a form and a requirement keep it (`separable_step_keep`), and an instance or a rule can end it (`twoness_lost_by_inst`, `twoness_lost_by_rule`).  Deciding it at a given regime in Lean needs a decision procedure for separability, which is rung three's X-1; the Python decides it by the sealed finite enumeration.  USEFUL REALIZATION: none is declared, because none is needed for definability.  FORCED in the seed's sense is conditional on an engine, and no engine is declared yet.  No earlier rung decided this row. | PROVED_THEOREM with COUNTERMODEL and FINITE_COMPUTATION | PRF-5, PRF-7, PRF-10 to PRF-15, PRF-17; prediction Q-15, HIT |
| CENSUS-classes | The observational classes are the classes of collapse among admitted data, which is reflexive, symmetric and transitive (`collapsed_refl`, `collapsed_symm`, `collapsed_trans`); they are DEFINABLE as a relation, carried both ways by the sealed isomorphism with no hypothesis (`collapsed_iso`, `separable_iso`), and as representative lists, carried with their length (`reps_iso`).  The count of observational classes as a NUMBER is a finite computation on the rectangle, where it is one value per class of regimes and is two at most at EMPTY, three at L and four at F (PRF-18, PRF-19); in Lean it is OPEN, behind a decision procedure for collapse (rung three's X-1) and the uniqueness of the length of a representative list (leftover T-1).  FORCED in the seed's sense is conditional on an engine, and no engine is declared yet.  No earlier rung decided this row. | PROVED_THEOREM with FINITE_COMPUTATION and OPEN | PRF-5 to PRF-9, PRF-18, PRF-19; prediction Q-16, HIT |

## Recorded

| id | claim | class | evidence |
|---|---|---|---|
| PRF-INPUTS | This rung neither reduces the count of declared inputs nor proves it at a floor; the value stays two, with no proof of a floor. | RECORDED | `receipts/profile.json` `input_count_claim`; prediction Q-17, HIT |
| PRF-PREDICTIONS | Of the frozen predictions, the seven computational rows score seven hits.  The FW-DEF prediction names thirty-three targets and scores twenty-nine hits and four misses, every one a demotion from CONTENT to THIN of a statement that turned out to be an assembly of its neighbours: `derivable_mapCtx`, `collapsed_iso`, `reps_iso` and `replay_parts_le`; no native theorem was added beyond the prediction.  Five rows were labelled FORCED before the run (Q-3, Q-8, Q-10, Q-17, Q-18), and a hit on a FORCED row evidences the order of the work, not insight. | PREDICTION | `receipts/profile.json` `predictions_scored`; `test_the_scored_verdicts_are_the_dated_ones`; `test_the_prediction_is_scored_at_the_dated_values`; `test_every_miss_is_the_dated_one` |
