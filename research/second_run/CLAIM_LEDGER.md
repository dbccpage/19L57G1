# CLAIM LEDGER: continuation two -- run forward

`AuthorityEffect: None`.  Every row carries an evidence class.  A row at
the level of a definition is marked so and is never counted as content.
Per-theorem classification is NOT this file's job: it is
`FWDEF_CENSUS.json`'s, which is total over all thirty-two theorems of this
tree's package and is checked in both directions by `test_census.py`.
Counts in this file are dated 2026-09-28.

Classes used: DEFINITION, PROVED_THEOREM, RECONSTRUCTION (the sealed
estate's theorem, reproduced verbatim under a pin, with no credit
claimed here), COUNTERMODEL (an executable witness: a path of a run
graph, every node of which replays from genesis), FINITE_COMPUTATION
(a value computed over the declared class at the declared bounds, and
true at those bounds only), DECLARED_POLICY, OPEN, PREDICTION, RECORDED.

Library axioms, recorded exactly: of the thirty-two theorems, two depend
on no axiom, seventeen on `propext` alone, and thirteen on `propext` and
`Quot.sound`; none depends on `Classical.choice` or on any other axiom.
The committed log is `receipts/lean_axioms.txt`, checked against a fresh
clean build by `verify_lean.py`.  Proofs use `omega` and
`Decidable.em` on the derived decidable equality of regimes; the fresh
axiom census is what shows that neither reaches `Classical.choice`.

The declared bounds of every FINITE_COMPUTATION row: the sealed
candidate space at the sealed bounds (at most two items, arities at
most two), unpruned, with rung one's no-op filter; growth below four
data; fifteen rounds; a node guard of two hundred and fifty per run,
checked before each expansion; the sealed permutation budget of one
hundred thousand for the key procedure, and rung two's observable
budget as rung two declared it.

---

## The leftovers this attempt takes, and the ruling that authorizes it

Continuation one named them, quoted verbatim from the spans pinned in
`SOURCE_MANIFEST.json` as `research/second_engine/STATUS.md` lines
234-242 and 255-256, and not edited:

> - **G-1, run every member forward.**  Challenge four, the second
>   authorized attempt: every member of the class, from both readings, to
>   declared bounds, with the census rows' FORCED columns read off the
>   runs.  The probe partitions the 144 members into ten classes, by label
>   signature and by exact content alike; nothing says the partition holds
>   deeper.  Price: the second attempt.
> - **G-2, whether a member without the stream carries the grammar
>   forward.**  The thirty-two of INPUT-COUNT; the question the seed's
>   required question one turns on.  Price: inside G-1.

> - **G-7, the probe beyond level two.**  Probe-isomorphism is decided to
>   level two only.  Price: inside G-1.

The author's ruling of 2026-09-25, pinned as `research/second/MANUAL.md`
lines 764-815, authorizes at most two further research attempts, first
challenge three and then challenge four with its engine-dependent census
evaluations.  This tree is the second and last.  It is a protocol
intervention by the author, not a result of the seed's next-rung rule,
and `SEED.md` is unchanged.

---

## Stage one: what no run can undo, in Lean

| id | claim | class | evidence |
|---|---|---|---|
| RUN-1 | The sealed kernel slice (regimes, contexts, derivability, collapse, separability, the six event kinds, step, replay, genesis and the two Lean reading regimes) is reproduced verbatim under two blob pins and three span pins, produced from continuation one's copy by changing only the outer namespace; thirty-seven shared declarations are identical after comments and namespace lines are stripped. | RECONSTRUCTION | `lean/SecondRun/Kernel.lean`; `test_every_shared_declaration_is_identical`; prediction R-4, HIT |
| RUN-2 | No sealed step lowers the element count (data plus the lengths of the four lists), and a sealed step that changes the regime raises it.  The same holds of every engine event, the switch marker keeping the regime; two switch markers return the state.  Each with no hypothesis beyond the step's success. | PROVED_THEOREM | `stepE_elems_le`, `stepE_elems_lt_of_ne`, `estep_elems_le`, `estep_elems_lt_of_ne`, `switch_keeps_regime`, `switch_switch`; `test_r1_the_step_statements`; prediction R-1, HIT |
| RUN-3 | For EVERY history of sealed events and switch markers, whoever chose it: the element count never falls; a history that leaves it unchanged leaves the regime unchanged; a history that changes the regime raises it; after a history that changes the regime, no further history reaches a state holding the first regime (`no_return`); on a history that returns to its starting state, the state reached part of the way holds the starting regime (`cycle_regime_const`).  So in every run of every engine of the class, and at every bound, the element count is monotone, no run returns to a regime it has left, and every cycle of states is made of steps that keep the regime.  The Lean mirror does not reconstruct the responder or the generators; it speaks of every history of the same events, which the runs are. | PROVED_THEOREM | `ereplay_elems_le`, `ereplay_regime_eq_of_elems_eq`, `ereplay_elems_lt_of_ne`, `no_return`, `cycle_regime_const`; `test_r2_the_history_statements`; prediction R-2, HIT |

## Stage two: the runs

Two hundred and eighty-eight runs, one per engine and sealed genesis
reading: 25,932 nodes, 69,490 edges, 43,846 merges.  Terminal nodes:
370 FIXPOINT, 758 REFUSAL, 368 BOUND, 11,266 GUARD.  One hundred and
twenty-eight runs TERMINATE, forty-four CYCLE, one hundred and sixteen
are NOT CLOSED.  Sixty-eight distinct run contents.

| id | claim | class | evidence |
|---|---|---|---|
| RUN-4 | Every node's history replays by the engine's replay rule to its representative, and every edge's events replay from its parent's representative to a state of its child node: zero mismatches.  At every merge the sealed isomorphism witness carries the generator's label of every pair onto the label of its image: zero quotient defects over the 43,818 merges checked.  Twenty-eight merges were NOT checked -- seven in each of the runs of E-four with `mu2`, HALT or growth alone, and either member, at reading F -- because rung two's observable budget refused the regimes they reach; they are recorded by name in the receipt and not repaired.  The sealed key partition agrees with the brute-force minimum on the 5,386 distinct regimes reached whose datum and form bijections number at most one thousand four hundred and forty (2,159 classes); 482 regimes above that count were not compared. | FINITE_COMPUTATION | `replay_mismatches`; `receipts/forward.json` `totals`, `key_crosscheck`; `test_replay_mismatches_are_named`; `test_a_merge_whose_labels_disagree_is_a_named_defect`; `test_a_merge_the_budget_leaves_unchecked_is_recorded`; prediction R-6, MISSED on the twenty-eight unchecked merges |
| RUN-5 | The QUIET engines are the eighty that hold no response edge at either reading: every E-seven and E-eight member, and every E-one, E-two, E-three, E-five, E-six and E-nine member without switch.  The other sixty-four, which hold a response edge at both readings, are exactly continuation one's LIVE members.  The quiet runs: with HALT one FIXPOINT; with growth alone three nodes at L and two at F, ending in a FIXPOINT at four data; with switch alone two nodes and a cycle of switch edges; with growth and switch six nodes and ten edges at L, four and six at F, cycling.  Every quiet run is closed. | FINITE_COMPUTATION | `receipts/forward.json` `runs`; `test_a_halting_quiet_engine_is_one_fixpoint`; `test_a_quiet_engine_with_both_rules_cycles`; predictions R-7 and R-8, HIT |
| RUN-6 | Beyond level two, reasoned by hand before the run and computed after: at reading L, E-four with HALT under `mu2` runs to twenty-three nodes and thirty edges, with seven FIXPOINT nodes and one BOUND node at stage fifteen; under `mu1`, fifty-three nodes and seventy-six edges, twenty-one FIXPOINT and three BOUND.  The run is a chain that separates the two data by a fresh form and collapses them again, each collapse by a new instance continuing the chain and each by a uniform rule ending it at a fixpoint. | FINITE_COMPUTATION | `test_the_deep_run_of_e4_under_mu2_at_l`; predictions R-9 and R-10, HIT |
| RUN-7 | Closure.  No run of an E-four member is closed, and no run of an E-one, E-two, E-three, E-five or E-nine member holding switch is closed; every run of an E-six member with switch alone is closed and cycles, at both readings, as do the E-six members with growth and switch under `mu2`; under `mu1` those two are not closed.  Under `mu1` at reading F every E-four run meets the node guard.  Eighty-eight runs meet the node guard; twenty-eight reach stage fifteen. | FINITE_COMPUTATION | `receipts/forward.json` `runs`; predictions R-11 and R-12, HIT |
| RUN-8 | No response edge of any run carries a datum: within two items, the stream is never part of a response here. | FINITE_COMPUTATION | `receipts/forward.json` `totals.datum_responses`; prediction R-14, HIT |
| RUN-9 | REFUSAL nodes occur under E-four (502), E-three (234) and E-five (22) only.  Of the refused demands, counted wherever they occur, 772 are of kind apart and 970 of kind same.  Every refused apart demand, all 772, has one shape, and it is structural, not a bound: a third datum is collapsed with both members of the pair, and both of its pairs with them are labelled same, so no-regress keeps both collapsed, and a pair collapsed with a common third datum is not separable in any regime (`not_separable_through`), so no delta of any size can separate the pair.  The first such refusal on the witness of CEN-5 is node 19 of E-three with `mu1`, member one, growth and switch, at reading L.  The 970 refused same demands are counted and not classified: whether each is refused by the two-item bound or by structure is OPEN. | FINITE_COMPUTATION; PROVED_THEOREM for the shape; COUNTERMODEL for the witness | `collapsed_through`, `not_separable_through`; `test_the_refusal_shape_statements`; `refusal_shapes`; `receipts/forward.json` `totals.refusal_shapes`; `test_the_refusal_shapes_are_counted`; `test_a_refused_demand_is_a_refusal` |
| RUN-10 | Run-isomorphism.  The class holds thirty-five run-isomorphism classes.  The run partition refines continuation one's ten probe classes, splitting six of them, and meets no two.  Every member-one engine is run-isomorphic to its member-two twin, seventy-two of seventy-two.  E-one and E-five with `mu2` and switch alone are run-isomorphic at both readings, which the prediction did not expect.  The decision agrees with the exhaustive search over node bijections on all 6,807 pairs of runs of at most eight nodes compared. | FINITE_COMPUTATION | `run_signature`, `brute_run_isomorphic`; `receipts/forward.json` `run_classes`; `test_the_decision_and_the_search_agree`; `test_the_search_sees_an_edge_label`; prediction R-15, HIT; prediction R-16, MISSED at thirty-five |

## Stage three: the census's FORCED column

Every verdict is over the named set of engines, at both sealed readings,
at the declared bounds.  A NOT FORCED verdict is a countermodel: the
first failing engine in class order and a path of its run, both in the
receipt.  A FORCED verdict of a run reading that HOLDS in every run holds
beyond the bounds as well, because HOLDS means every run path meets the
property before any bound or guard node.  FORCED AT BOUND is a finite
computation at the bounds.

| id | claim | class | evidence |
|---|---|---|---|
| CEN-1 | Two-ness.  Stage reading over the class: FORCED at round zero with the value false, NOT FORCED at every round from one to fifteen.  Run reading ("every run comes to hold two"): NOT FORCED over the class, first failing at E-one with `mu1`, member one and HALT, at L; FORCED over the sixty-four LIVE members, over the thirty-two streamless LIVE members and over the sixteen TWO-KINDED: every run path of every such run holds two before any bound or guard node. | FINITE_COMPUTATION; COUNTERMODEL for the class | `receipts/forward.json` `stage`, `run_verdicts`; `test_fails_at_a_fixpoint_with_its_path`; predictions R-17 and R-18, HIT for these rows |
| CEN-2 | The count of observational classes.  Stage reading: FORCED at round zero with the value one, NOT FORCED from round one.  Run reading ("no edge lowers it"): NOT FORCED, first failing at E-one with `mu1`, member one and switch alone, at L.  It is never lowered in eighty-two engines: the eighty quiet ones and the two E-six members with `mu2` and switch alone. | FINITE_COMPUTATION; COUNTERMODEL | `receipts/forward.json` `candidates.classes`; predictions R-17, R-18 and R-22, HIT for these rows |
| CEN-3 | Succession of accepted rounds.  Under EVERY and under CHANGING: NOT FORCED.  One countermodel serves both: node 86 of E-one with `mu1`, member one and switch alone, at reading F, holds three data, two unary forms each carrying a uniform rule, and instances on the first form at data zero and one and on the second at datum zero.  One path reaches it in five rounds, four of them changing, the last admitting both rules at once; another in six rounds, five of them changing, admitting the rules one at a time.  So within a run the number of rounds is not a function of the state.  Over 288 runs, CHANGING FAILS in forty-eight, HOLDS in one hundred and twenty-eight, HOLDS AT BOUND in sixty-eight, and is UNDECIDED in forty-four closed runs with cycles of switch edges only, on each of which the supplementary pass finds one value per node. | COUNTERMODEL | `receipts/forward.json` `run_verdicts.class.three_changing`, `supplementary`; `test_two_short_paths_fail`; prediction R-18, MISSED on this row |
| CEN-4 | Duration, as rest rounds since the last datum round.  NOT FORCED, with the same countermodel as CEN-3: no datum round lies on either path, so the two paths bring four and five rest rounds. | COUNTERMODEL | `receipts/forward.json` `run_verdicts.class.four_duration`; prediction R-18, MISSED on this row |
| CEN-5 | Adjacency, a response moving two pairs together, and reach, a response moving a pair through a third datum.  NOT FORCED over the class, first failing at E-one with `mu1`, member one and HALT, at L.  Over the LIVE members NOT FORCED, first failing at E-three with `mu1`, member one, growth and switch, at L, on the structural refusal of RUN-9; at reading F both HOLD in every LIVE run. | COUNTERMODEL | `receipts/forward.json` `run_verdicts.live`, `live_by_reading`; prediction R-20, MISSED on the first failing member |
| CEN-6 | An invariant.  The element count is never lowered on any edge of any run: FORCED AT BOUND as a finite computation, and, by RUN-3, proved for every history of every engine, so FORCED beyond the bounds.  The numbers of data, forms, instances and uniform rules are never lowered in any run either; the profile class count, the automorphism count, the number of demands and the number of honoured labelled pairs are each lowered in some run. | PROVED_THEOREM and FINITE_COMPUTATION | `ereplay_elems_le`; `receipts/forward.json` `run_verdicts.class.seven_invariant`, `candidates`; predictions R-19 and R-22, HIT |
| CEN-7 | Irreversibility.  No changing edge of any run lies on a cycle: FORCED AT BOUND as a finite computation, and FORCED beyond the bounds by RUN-3.  Every cycle of every run is made of switch edges only. | PROVED_THEOREM and FINITE_COMPUTATION | `no_return`, `cycle_regime_const`; `receipts/forward.json` `totals.cyclic_non_switch`; prediction R-19, HIT |
| CEN-8 | Symmetry, the number of sealed automorphisms.  FORCED at round zero (two at L, six at F), NOT FORCED from round one. | FINITE_COMPUTATION | `receipts/forward.json` `stage`; prediction R-17, HIT for this row |
| CEN-9 | Branching, the number of distinct successors of a node.  NOT FORCED at every round from zero to fifteen. | FINITE_COMPUTATION | `receipts/forward.json` `stage`; prediction R-17, HIT for this row |
| CEN-10 | Exhaustion, the number of exhausted forms.  FORCED at rounds zero and one with the value zero, NOT FORCED from round two. | FINITE_COMPUTATION | `receipts/forward.json` `stage`; prediction R-17, HIT for this row |
| CEN-11 | Recurrence, a run reaching a node on a cycle.  NOT FORCED over the class, first failing at E-one with `mu1`, member one and HALT, at L; NOT FORCED over the LIVE members, first failing at E-three with `mu1`, member one and switch alone, at F. | COUNTERMODEL | `receipts/forward.json` `run_verdicts`; prediction R-18, HIT for the class row |
| CEN-12 | Within a single engine, every stage reading is forced at every complete round for seventy-four engines: the seventy-two quiet engines other than the E-seven and E-eight members with growth and switch, and the two E-six members with `mu2` and switch alone, whose runs are single chains closing in a cycle of switch edges. | FINITE_COMPUTATION | `receipts/forward.json` `per_engine_forced`; prediction R-21, HIT |
| CEN-13 | The DEFINABLE and USEFUL REALIZATION columns, as the prompt's rule records them: two-ness, the class count, the element count, symmetry and exhaustion are read off the representative's regime and are DEFINABLE at every stage; adjacency, reach and branching read the responder, which every engine declares, and are DEFINABLE relative to the engine's declaration, the declaration rung ten priced as a realization; succession and duration are functions of the state within a run exactly when their run reading does not FAIL, recorded per run; irreversibility and recurrence are read off the run graph. | DECLARED_POLICY | `receipts/forward.json` `definable` |

## Stage four: the seed's required questions and the input count

| id | claim | class | evidence |
|---|---|---|---|
| INPUT-COUNT | Required question one, within the declared bounds and under the literal reading of carrying forward (not closed, every frontier node reached with no switch marker in its history): eight engines carry forward at both readings, the E-four members with HALT or growth alone, and four of them are streamless, the E-four members with HALT.  Under the input tally each of those four declares the stake and not the stream.  So at these bounds, under these readings, two is not the floor: an engine with one of the seed's two named inputs carries the grammar forward.  This is a FINITE COMPUTATION at the declared bounds: it is not a floor proof, and it is not a reduction of the seed's count of declared inputs outside those bounds -- whether those runs carry forward past fifteen rounds or two hundred and fifty nodes is OPEN, and the engines declare six or seven capabilities each. | FINITE_COMPUTATION | `receipts/forward.json` `carrying`; `test_the_deep_run_of_e4_under_mu2_at_l`; predictions R-13 and R-23, HIT |
| Q2 | Required question two: no response edge of any run carries a datum, at two items (RUN-8).  The three-item bound of challenge one is not computed here. | FINITE_COMPUTATION | RUN-8 |
| Q4 | Required questions four and ten, on the engines that carry forward: count-minimal and inclusion-minimal are E-four with `mu1`, member one, HALT and E-four with `mu2`, member one, HALT, at count six under both readings of growth; they are not run-isomorphic, so the minimum is not unique up to run-isomorphism; no member is initial under inclusions of declarations.  The universal property is refused for this reading of morphism only. | FINITE_COMPUTATION and COUNTERMODEL | `receipts/forward.json` `carrying`, `run_classes`; prediction R-13, HIT |
| Q5 | Required question five: the element count is monotone across every accepted round of every run of every engine, raised by every changing round -- an invariant of the engines, proved (RUN-3), not of the bounds.  Other candidates hold in the runs of particular engines only; each such fact is an invariant of the engine where its runs are closed and of the bounds where they are not, and the receipt says which. | PROVED_THEOREM and FINITE_COMPUTATION | CEN-6 |
| Q6 | Required question six: succession and duration are not functions of the state in general (CEN-3, CEN-4); they are within the runs where the reading HOLDS, through the trace of changing rounds. | COUNTERMODEL | CEN-3, CEN-4 |
| Q7 | Required question seven: adjacency is exhibited (CEN-5); no distance on it was declared or computed by this attempt. | OPEN | CEN-5 |
| Q8 | Required question eight: every run has an arrow -- no run returns to a regime it has left by a changing round, proved for every history (RUN-3); a run revisits a state only through switch markers, and every cycle of every run is made of them. | PROVED_THEOREM | `no_return`, `cycle_regime_const`; CEN-7 |
| Q9 | Required question nine, at the bounds: the element count recurs in every engine as an invariant (proved); one refusal shape recurs under E-three and E-four, the transitivity shape of RUN-9, and is every refused apart demand; the member-one and member-two twins share every run; E-one and E-five under `mu2` with switch alone share one run; and the run partition refines the probe partition. | PROVED_THEOREM and FINITE_COMPUTATION | RUN-3, RUN-9, RUN-10, CEN-6 |
| RUN-PREDICTIONS | Of the frozen predictions, nineteen computational rows are scored in the receipt: fifteen HIT and four MISSED (R-6 on twenty-eight unchecked merges, R-16 at thirty-five classes, R-18 on succession under CHANGING and duration, R-20 on the first failing LIVE member).  The first full run also scored R-13 MISSED because the scorer compared a list in class order with a sorted one; the values were the predicted ones, the comparison was corrected, and the correction is recorded in `STATUS.md`.  The FW-DEF prediction names thirteen native targets and scores thirteen hits; two native theorems were added after it and are unpredicted work (`collapsed_through`, `not_separable_through`).  Three rows were labelled FORCED (R-5, R-19, R-24), and a hit on them evidences the order of the work, not insight. | PREDICTION | `receipts/forward.json` `predictions_scored`; `test_the_scores_are_recomputed_from_the_reports`; `test_the_scorer_can_say_missed`; `test_the_prediction_is_scored_at_the_dated_values` |
