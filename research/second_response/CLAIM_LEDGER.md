# CLAIM LEDGER: rung ten -- adjacency, reach, branching and exhaustion

`AuthorityEffect: None`.  Every row carries an evidence class.  A row at
the level of a definition is marked so and is never counted as content.
Per-theorem classification is NOT this file's job: it is
`FWDEF_CENSUS.json`'s, which is total over all fifty-six theorems of
this rung's package and is checked in both directions by
`test_census.py`.  Counts in this file are dated 2026-09-25.

Classes used: DEFINITION (true by unfolding, by `rfl`, by a projection,
by one rewrite, by kernel computation over concrete regimes, or by pure
case exhaustion), PROVED_THEOREM, RECONSTRUCTION (the sealed estate's
theorem, reproduced verbatim under a pin, with no credit claimed here),
RESTATED (an earlier rung's statement, proved again here so that the
package imports nothing, credited to its rung), COUNTERMODEL,
FINITE_COMPUTATION, OPEN, PREDICTION, RECORDED.

Library axioms, recorded exactly: of the fifty-six theorems, three
depend on no axiom, twenty-seven on `propext` alone, and twenty-six on
`propext` and `Quot.sound`; none depends on `Classical.choice` or on any
other axiom.  The committed log is `receipts/lean_axioms.txt`, checked
against a fresh clean build by `verify_lean.py`.  Every use of the
`omega` tactic closes one arithmetic goal inside `absurd`, the shape
rung nine's handoff names; the first complete build was already within
the whitelist.

---

## The leftover this rung takes, quoted by pin

Rung three's leftover list names X-6, and rung nine's application of the
seed's next-rung rule selects it.  Rung three's text is quoted verbatim
from the span pinned in `SOURCE_MANIFEST.json` as
`research/second_index/STATUS.md` lines 165-168, and is not edited:

> - **X-6, the other eleven rows of the challenge-five census.**  Two-ness,
>   observational classes, duration, adjacency, reach, invariants,
>   irreversibility, symmetry, branching, exhaustion and recurrence.  This
>   rung decides one row and claims nothing about the rest.

As rung nine carries it, quoted from the span pinned as
`research/second_profile/STATUS.md` lines 212-215:

> - Carried from rung three, unchanged: X-1, X-2, X-4, X-5, and X-6 less
>   symmetry, invariants, irreversibility, succession, duration,
>   recurrence, two-ness and observational classes: adjacency, reach,
>   branching and exhaustion.

**The readings this rung applied, recorded in `PROMPT.md` before its
predictions were frozen.**  It takes all four remaining rows, because
the seed's rung budget is nearly spent.  And, answering rung nine's
remark (pinned as lines 217-224 of the same file), it reads the
response of the adjacency, reach and branching rows as the SEALED
RESPONDER: the sealed demand read off the state, the sealed candidate
space at the sealed bounds, the sealed validity rule and each sealed
cost measure in turn, consumed unchanged; the sealed responder refuses a
regime holding a uniform rule, and this rung does not widen it.  Both
readings bind no later rung.

---

## Stage one: the reconstruction and the restatements

| id | claim | class | evidence |
|---|---|---|---|
| RSP-1 | The sealed kernel slice and the sealed isomorphism structure are reproduced verbatim under three blob pins and four span pins, produced from rung nine's copies by changing only the outer namespace. | RECONSTRUCTION | `lean/SecondResponse/Kernel.lean`, `lean/SecondResponse/IsoKernel.lean`; `test_every_shared_declaration_is_identical` |
| RSP-2 | Forty-one declarations are shared between the reconstructions and their three pinned sources, and every one is identical after comments and namespace lines are stripped and whitespace is normalized; the omitted declarations are pinned by name. | FINITE_COMPUTATION | `test_every_shared_declaration_is_identical`; `test_the_omitted_declarations_are_recorded_not_judged` |
| RSP-3 | Rung nine's pieces for carrying a context along the sealed isomorphism, and rung eight's `isoSymm`, are stated and proved again unedited but for the namespace: `map_inv`, `plug_mapCtx`, `plug_args_lt`, `wfCtx_mapCtx`, `derivable_fwd`, `derivable_bwd`, `derivable_mapCtx`.  Rung nine's `HoldsTwo`, rung nine's `separable_step_keep`, rung five's `getD_append_lt` and rung three's `wf_step_any` (here `step_wf`) are stated again and proved here. | RESTATED | `lean/SecondResponse/Carry.lean`; `test_the_credited_statements_say_whose_they_are` |

## Stage two: exhaustion, in Lean

| id | claim | class | evidence |
|---|---|---|---|
| RSP-4 | A form is EXHAUSTED when every well-formed context on it reads every two admitted data alike, and DISTINGUISHES when some well-formed context on it tells two admitted data apart.  A form is exhausted exactly when it does not distinguish, constructively, and a regime holds two exactly when some form distinguishes; neither needs a hypothesis on the regime. | PROVED_THEOREM | `Exhausted`, `Distinguishes`; `exhausted_iff_not_distinguishes`; `holdsTwo_iff_distinguishes` (at the level of a definition); `test_r2_exhaustion_and_holding_two_need_no_hypothesis`; prediction R-2, HIT |
| RSP-5 | A form carrying a uniform rule, a form on which no held instance lies, and every form of a regime holding at most one datum, are exhausted, with no well-formedness hypothesis; a form admission to a well-formed regime adds an exhausted form. | PROVED_THEOREM | `exhausted_of_rule` (at the level of a definition), `exhausted_of_no_inst`, `exhausted_of_le_one`, `fresh_form_exhausted` |
| RSP-6 | For every two regimes and every inhabitant of the sealed isomorphism between them, a form admitted in the source is exhausted exactly when its image is; no well-formedness of either regime is needed. | PROVED_THEOREM | `exhausted_iso`; `test_r1_exhaustion_is_carried_with_an_admitted_form_only`; prediction R-1, HIT |
| RSP-7 | A supply, a requirement, a form admission and a rule admission keep every exhausted admitted form exhausted, on every regime; a supply, a requirement, a form admission and a datum admission keep every distinguishing form distinguishing, on every regime.  Both rest on one statement: those kinds keep every well-formed context well formed and leave derivability as it was, apart from the rule admission, whose own form becomes exhausted. | PROVED_THEOREM | `ctx_step_keep`, `exhausted_step_keep`, `distinguishes_step_keep`, `separable_step_keep`, `step_data_le`; `test_r3_the_keeping_kinds_and_the_four_exhibits`; prediction R-3, HIT |
| RSP-8 | The four other changes each happen, on an exhibited well-formed regime and one accepted event: an instance admission and a rule admission each begin the exhaustion of a form, and a datum admission and an instance admission each end it.  The instance case that begins it needs an argument over every context and is not a kernel computation.  So, besides a form admission adding a fresh exhausted form, exhaustion is begun only by instance and rule admissions and ended only by datum and instance admissions. | COUNTERMODEL | `exhaustion_begun_by_inst`, `exhaustion_begun_by_rule`, `exhaustion_ended_by_datum`, `exhaustion_ended_by_inst`; prediction R-3, HIT |
| RSP-9 | The sealed empty regime has no exhausted form; the history of one form admission of arity one reaches a regime that has one. | DEFINITION | `no_exhausted_at_genesis`, `exhaustion_at_one`; `test_r4_the_first_stage_of_exhaustion`; prediction R-4, HIT |

## Stage three: which events move a pair, in Lean

A pair of data is MOVED when it is separable on one side and collapsed on
the other.  Nothing in this stage is about a minimum, a cost or a tie:
every statement is about events and histories, whatever responder chose
them.

| id | claim | class | evidence |
|---|---|---|---|
| RSP-10 | An accepted instance admission whose arguments mention neither datum of a pair leaves the pair's separability and its collapse as they were, with no hypothesis on the regime: the datum plugged into a context with a hole is an argument of the plugging. | PROVED_THEOREM | `mem_plug_of_hole` (at the level of a definition), `derivable_inst_unmentioned`, `separable_inst_unmentioned`, `collapsed_inst_unmentioned`; `test_r5_which_kinds_keep_a_pair_and_what_each_needs`; prediction R-5, HIT |
| RSP-11 | On a WELL-FORMED regime every accepted event other than an instance admission keeps every collapsed pair collapsed; well-formedness is used, for the datum and form admissions, to show that a context reading the new datum or the new form holds no admitted instance.  Every accepted event keeps a regime well formed. | PROVED_THEOREM | `slots_ok_of_plug_mem`, `collapsed_step_keep`, `step_wf`; prediction R-5, HIT |
| RSP-12 | For a well-formed base and every history the sealed replay accepts from it, a pair collapsed before and separable after is mentioned by the arguments of some instance admission of the history; so every such history holds an instance admission.  A pair separable before and collapsed after is so mentioned, or the history holds a rule admission, with no hypothesis on the base.  So for a history holding no rule admission, every pair it moves meets the arguments of its instance admissions: which pairs one history can move together is bounded by what it mentions. | PROVED_THEOREM | `separation_needs_mention`, `collapse_needs_mention_or_rule`, `moved_pairs_meet_mentions`, `separation_needs_inst`; `test_r6_a_moved_pair_is_mentioned`; prediction R-6, HIT |
| RSP-13 | One instance admission, on an exhibited well-formed regime of three collapsed data and one form of arity one, moves two pairs apart at once; on another, it moves a collapsed pair apart and a separable pair together. | COUNTERMODEL | `one_inst_moves_two_pairs` (at the level of a definition), `response_collapses_a_pair`; `test_r7_the_two_moving_exhibits`; `test_the_lean_exhibits_in_the_python_grammar`; prediction R-7, HIT |

## Stage four: the finite cross-check

Over rung three's rectangle, unchanged: three bases, every sequence of at
most four declared events, 577, 3928 and 14293 sequences reaching 75,
523 and 1718 distinct regimes, 2316 in all, in 402 classes of the sealed
key procedure with zero disagreements against the brute-force minimum.
The responder is the sealed `min_responses` at two items and arity two.

| id | claim | class | evidence |
|---|---|---|---|
| RSP-14 | The responder's domain: 47, 402 and 1441 distinct regimes at EMPTY, L and F lie inside it, and 28, 121 and 277 outside; the sealed responder refuses to run on exactly the regimes holding a uniform rule. | FINITE_COMPUTATION | `in_domain`; `test_the_domain_counts_are_the_dated_ones`; prediction R-10, HIT |
| RSP-15 | There are 34, 597 and 2479 demands at EMPTY, L and F inside the domain, and NONE is refused within two items, under either measure.  At EMPTY 14 are answered at one item and 20 at two; at L 315 and 282; at F 1514 and 965; the two measures answer every demand at the same item count.  The frozen prediction of a refusal at L and at F MISSED: the refusal this session expected before the run, several requirements on collapsed data, are answered at two items by a new form of arity two and one instance, which tells three data apart at once.  A refusal exists beside the rectangle: four data with a requirement on every pair. | FINITE_COMPUTATION | `measure_report`; `test_the_miss_is_recorded_with_its_value`; `test_a_refused_demand`; prediction R-11, MISSED |
| RSP-16 | Under both measures, at every base: no response holds a rule item; every response holds an instance item mentioning a demanded datum; no response moves a pair that none of its instance items mentions; every response moves its demand apart.  Responses that move some pair together number 0, 114 and 1152 at EMPTY, L and F, under each measure. | FINITE_COMPUTATION | `test_the_response_counts_are_the_dated_ones`; predictions R-12 and R-13, HIT |
| RSP-17 | Reach: a response has a nonempty reach exactly when it moves at least two pairs; every datum collapsed with the demanded pair before the response is in its reach; the largest reach is two at EMPTY and three at L and at F; every base has responses of empty and of nonempty reach. | FINITE_COMPUTATION | `measure_report`; prediction R-14, HIT |
| RSP-18 | Adjacency and distance: the least length of a sequence reaching a regime whose adjacency graph has an edge is three at EMPTY, one at L and zero at F, under both measures.  The largest finite distance is one at EMPTY under `mu1` and two everywhere else; no graph of the rectangle has a finite distance above two.  The measure changes the graph: at EMPTY, `mu2` reaches distance two where `mu1` does not. | FINITE_COMPUTATION | `adjacency`; `test_a_path_of_two_edges_has_distance_two`; `test_no_distance_above_two_within_the_bound`; prediction R-15, HIT |
| RSP-19 | Branching: the least length reaching a demand with two tie classes is two, zero and zero at EMPTY, L and F under `mu1`, and three, one and one under `mu2`; every `mu2` response is a `mu1` response; demands with one response number 0, 42 and 192 under `mu1` and 6, 174 and 456 under `mu2`.  The largest tie-class count is five, eight and sixteen under `mu1` and four, eight and sixteen under `mu2`. | FINITE_COMPUTATION | `test_the_two_measures_part_at_two_items`; `test_the_response_counts_are_the_dated_ones`; prediction R-16, HIT |
| RSP-20 | No class of regimes, within a base or over all three, carries two values of the exhausted count, or of the response signature under either measure; so on the rectangle every quantity above is a function of the class. | FINITE_COMPUTATION | `lumping`; `test_a_lumping_partition_is_counted_everywhere`; prediction R-17, HIT |
| RSP-21 | Exhaustion on the rectangle: a regime holds two exactly when its exhausted count is below its number of forms; every ruled form is exhausted; the exhausted count changes by zero under a supply and a requirement, by one under a form admission, by zero or one under a rule, by minus one or zero under a datum, and by minus one, zero or one under an instance.  The least length reaching an exhausted form is one at every base; reaching one beside holding two, three at L and F, and never within the EMPTY rectangle. | FINITE_COMPUTATION | `exhaustion_report`; `test_a_small_exhaustion_report_by_hand`; predictions R-18 and R-19, HIT |
| RSP-22 | On the declared family, the 47 rule-free regimes of the EMPTY rectangle, the sealed responder agrees with the minimum of the sealed unpruned enumeration under the sealed reference validity, in responses and in refusals, at all 68 demand-and-measure situations, and the key partition of the tie classes agrees with the brute-force partition; every response of the whole population passes the sealed reference validity. | FINITE_COMPUTATION | `crosscheck`, `unpruned`; `test_the_unpruned_minimum_agrees_by_hand`; prediction R-20, HIT |

## Stage five: the census rows this rung decides

| id | claim | class | evidence |
|---|---|---|---|
| CENSUS-adjacency | Adjacency, read as which pairs one response moves together, is a USEFUL REALIZATION under a named additional declaration: that the row's response is the sealed responder's minimum response to a demand read off the state, under ONE chosen measure.  It is priced at two declared capabilities beyond the supplied grammar -- the reading that the sealed responder is the response, and the choice of a measure, which changes the graph (RSP-18) -- and limited to the responder's domain, the regimes holding no rule.  Its event-level statement is PROVED for every well-formed regime and history, whatever responder is declared: a history holding no rule moves only pairs its instances mention (`separation_needs_mention`, `collapse_needs_mention_or_rule`, `moved_pairs_meet_mentions`), and one instance can move two pairs at once (`one_inst_moves_two_pairs`).  Its numbers are FINITE COMPUTATION on the rectangle, a function of the class there; the first stage with an edge is three events from the empty regime, one from L and zero from F.  The distance is derived from adjacency with no further declaration, and within the bound it never exceeds two.  FORCED in the seed's sense is conditional on an engine, and none is declared. | PROVED_THEOREM with COUNTERMODEL and FINITE_COMPUTATION | RSP-10 to RSP-13, RSP-16, RSP-18, RSP-20; prediction R-22, HIT |
| CENSUS-reach | Reach, read as the data outside the demanded pair that a response moves a pair of, is a USEFUL REALIZATION under the same named declaration as adjacency -- the sealed responder under one chosen measure -- priced the same, at two declared capabilities.  PROVED for every history: every moved pair meets the arguments of an instance of the history, unless the history holds a rule (`separation_needs_mention`, `collapse_needs_mention_or_rule`); a single instance reaches a third datum (`one_inst_moves_two_pairs`) and can move a separable pair together (`response_collapses_a_pair`).  FINITE COMPUTATION on the rectangle: the reach is nonempty exactly when two pairs move, always holds every datum collapsed with the demand, and is at most three.  FORCED in the seed's sense is conditional on an engine, and none is declared. | PROVED_THEOREM with COUNTERMODEL and FINITE_COMPUTATION | RSP-12, RSP-13, RSP-17; prediction R-22, HIT |
| CENSUS-branching | Branching, read as the tie count and the tie-class count of a demand, is a USEFUL REALIZATION under the same named declaration -- the sealed responder under one chosen measure -- priced the same, at two declared capabilities; the choice of measure changes it (RSP-19).  There is no Lean statement about a tie count: the sealed candidate space is not reconstructed in Lean.  FINITE COMPUTATION on the rectangle: the first stage with two tie classes is two events from the empty regime under `mu1` and three under `mu2`; a function of the class there.  FORCED in the seed's sense is conditional on an engine, and none is declared. | FINITE_COMPUTATION | RSP-19, RSP-20, RSP-22; prediction R-22, HIT |
| CENSUS-exhaustion | Exhaustion, read as a form that distinguishes nobody, is DEFINABLE: read off the regime's own contexts and derivability, carried by the sealed isomorphism with no hypothesis on either regime (`exhausted_iso`), and exactly the complement of a distinguishing form (`exhausted_iff_not_distinguishes`), so a regime holds two exactly when not every form is exhausted (`holdsTwo_iff_distinguishes`).  Its first stage is one event from the empty regime (`no_exhausted_at_genesis`, `exhaustion_at_one`).  A supply, a requirement, a form and a rule keep it and a supply, a requirement, a form and a datum keep its negation (`exhausted_step_keep`, `distinguishes_step_keep`); an instance or a rule can begin it and a datum or an instance can end it (`exhaustion_begun_by_inst`, `exhaustion_begun_by_rule`, `exhaustion_ended_by_datum`, `exhaustion_ended_by_inst`).  Deciding it at a regime in Lean needs a decision procedure over contexts, rung three's X-1; the Python decides it by the sealed enumeration.  FORCED in the seed's sense is conditional on an engine, and none is declared. | PROVED_THEOREM with COUNTERMODEL and FINITE_COMPUTATION | RSP-4 to RSP-9, RSP-20, RSP-21; prediction R-21, HIT |

## Recorded

| id | claim | class | evidence |
|---|---|---|---|
| RSP-INPUTS | This rung neither reduces the count of declared inputs nor proves it at a floor; the value stays two, with no proof of a floor. | RECORDED | `receipts/response.json` `input_count_claim`; prediction R-23, HIT |
| RSP-PREDICTIONS | Of the frozen predictions, the twelve computational rows score eleven hits and one miss, R-11.  The FW-DEF prediction names thirty-nine targets and scores thirty-seven hits and two misses, both demotions from THIN to DEFINITION: `holdsTwo_iff_distinguishes` and `mem_plug_of_hole`; no native theorem was added beyond the prediction.  Three rows were labelled FORCED before the run (R-9, R-23, R-24), and a hit on a FORCED row evidences the order of the work, not insight. | PREDICTION | `receipts/response.json` `predictions_scored`; `test_the_scored_verdicts_are_the_dated_ones`; `test_the_prediction_is_scored_at_the_dated_values`; `test_every_miss_is_the_dated_one` |
