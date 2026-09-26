# CLAIM LEDGER: continuation one -- the engine

`AuthorityEffect: None`.  Every row carries an evidence class.  A row at
the level of a definition is marked so and is never counted as content.
Per-theorem classification is NOT this file's job: it is
`FWDEF_CENSUS.json`'s, which is total over all sixty-seven theorems of
this tree's package and is checked in both directions by
`test_census.py`.  Counts in this file are dated 2026-09-25.

Classes used: DEFINITION (true by unfolding, by `rfl`, by a projection,
by one rewrite, by kernel computation over concrete objects, or by pure
case exhaustion, including exhaustion over the declared finite class),
PROVED_THEOREM, RECONSTRUCTION (the sealed estate's theorem, reproduced
verbatim under a pin, with no credit claimed here), RESTATED (an earlier
rung's statement, proved again here so that the package imports nothing,
credited to its rung), COUNTERMODEL, FINITE_COMPUTATION, DECLARED_POLICY,
OPEN, PREDICTION, RECORDED.

Library axioms, recorded exactly: of the sixty-seven theorems, sixteen
depend on no axiom, thirty-two on `propext` alone, and nineteen on
`propext` and `Quot.sound`; none depends on `Classical.choice` or on any
other axiom.  The committed log is `receipts/lean_axioms.txt`, checked
against a fresh clean build by `verify_lean.py`.  No proof of the
package uses the `omega` tactic.  Five census theorems close by
`decide +kernel`, which leaves the check to the kernel and adds no
axiom; the log says so of each.

---

## The leftover this attempt takes, and the ruling that authorizes it

Rung three named X-5, quoted verbatim from the span pinned in
`SOURCE_MANIFEST.json` as `research/second_index/STATUS.md` lines
162-164, and not edited:

> - **X-5, the engine of the seed's challenge three.**  The plan's item
>   four, and the sibling stake rung's own first leftover.  Not started
>   here in any direction.

Rung ten recorded it for the author, quoted from the span pinned as
`research/second_response/STATUS.md` lines 366-372:

> - X-5, the engine of the seed's challenge three, is the leftover that the
>   FORCED column of every row waits on -- S-5, T-3, V-2, W-3, Z-5 and X-2
>   among them -- and the seed's completion gate names every engine of the
>   declared class run to bounds, refuted, or OPEN.  Whether "extends the
>   census" covers deciding a FORCED column is a reading the seed leaves
>   open; rungs three to nine read it as no, and this rung does not change
>   that reading.

The author's ruling of 2026-09-25, pinned as `research/second/MANUAL.md`
lines 764-815, makes X-5 eligible as a named prerequisite of the census
and authorizes at most two further research attempts, first challenge
three and then challenge four.  This tree is the first.  It is a protocol
intervention by the author, not a result of the seed's next-rung rule,
and `SEED.md` is unchanged.

---

## Stage one: the declaration

| id | claim | class | evidence |
|---|---|---|---|
| ENG-1 | An ENGINE is a declaration of four parts: a generator reading demands off the state, a responder answering a demand by a response, a continuation fired at a demand-free state, and a replay rule applying a history.  A history is NAMED at a state when it is a response to one of the state's demands, or the state is demand-free and the history is an enabled continuation; a step applies a named history and a run chains steps.  So every history of every run is named by the declaration at the state it is taken from, and a step from a state with a demand is a response.  At the level of a definition, and recorded so. | DEFINITION | `Engine`, `Named`, `Step`, `Run`; `run_named`, `step_at_demand_is_response`, `fixpoint_of_halt`; `test_c1_the_engine_statements`; prediction C-1, HIT |
| ENG-2 | The DECLARED CLASS: nine generators (rung two's rules E-one to E-nine), two measures (the sealed ones), two validity members (challenge one's), and four continuations (the subsets of growth and switch; the empty one is named HALT and is this tree's declaration).  One hundred and forty-four members; one hundred and eight hold a continuation rule, the seed-literal subclass. | DECLARED_POLICY and DEFINITION | `engine_class`, `literal_class`; `class_size`, `literal_size`; `test_the_class_and_its_literal_subclass`; prediction C-6, HIT; prediction C-8, HIT |
| ENG-3 | The switch of the identification tree is read here as a flip of the generator's labels, apart and same exchanged and free kept, at a demand-free state; no requirement is retracted because an engine imposes none.  Validity member two, declared by rung one for an index commitment, is read for a rule that reads the state as: every labelled pair involving a datum the response introduces is honoured afterwards, its label read afterwards in the same mode.  Both readings are this tree's and bind no later attempt. | DECLARED_POLICY | `moded_rule`, `introduced_clause`; `test_the_flip_exchanges_apart_and_same_and_keeps_free`; `test_member_two_drops_a_delta_member_one_keeps` |
| ENG-4 | The CAPABILITY COUNT of a member is the size of its capability list: three skeleton capabilities, the observables of its rule as rung two counts them, its measure, one or two validity clauses, and its continuation rules.  Every count lies between six and ten; the histogram is sixteen at six, fifty at seven, fifty-four at eight, twenty-two at nine and two at ten. | DEFINITION and FINITE_COMPUTATION | `Decl.caps`, `Decl.count`; `count_ge_six`; `receipts/engine.json` `class`; prediction C-8, HIT |
| ENG-5 | No member of the class is one declaration: every count is at least six.  A label calling any member one declaration is refused by name, with every capability listed; all one hundred and forty-four members refuse it.  The two-sided tree's "one declaration" names its stake alone, one index commitment, and calls no engine one declaration. | PROVED_THEOREM and FINITE_COMPUTATION | `no_one_declaration`; `check_declaration_label`; `test_a_label_calling_a_bundle_one_declaration_is_refused`; `test_every_member_refuses_the_label`; prediction C-10, HIT |
| ENG-6 | A count cannot tell two rules reading one observable apart: the members reading E-three and E-four, alike elsewhere, declare one capability list, and so do those reading E-two and E-seven; thirty-two unordered pairs of distinct members, at each of the sixteen settings of measure, validity and continuation. | PROVED_THEOREM and FINITE_COMPUTATION | `same_caps_e3_e4`; `shared_capability_pairs`; `test_the_shared_capability_pairs`; prediction C-9, HIT |

## Stage two: the stakes, in Lean

| id | claim | class | evidence |
|---|---|---|---|
| ENG-7 | The sealed kernel slice and the sealed isomorphism structure are reproduced verbatim under three blob pins and four span pins, produced from rung ten's copies by changing only the outer namespace; forty-one shared declarations are identical after comments and namespace lines are stripped. | RECONSTRUCTION | `lean/SecondEngine/Kernel.lean`, `lean/SecondEngine/IsoKernel.lean`; `test_every_shared_declaration_is_identical` |
| ENG-8 | Rung nine's pieces for carrying observation along the sealed isomorphism, and rung eight's `isoSymm`, are stated and proved again unedited but for the namespace: `map_inv`, `plug_mapCtx`, `plug_args_lt`, `wfCtx_mapCtx`, `derivable_fwd`, `derivable_bwd`, `derivable_mapCtx`, `separable_iso`, `collapsed_iso`. | RESTATED | `lean/SecondEngine/Carry.lean`; `test_the_credited_statements_say_whose_they_are` |
| ENG-9 | Three of rung two's observables are carried, forward and back, by every inhabitant of the sealed isomorphism between any two regimes, with the only hypothesis that the two data are admitted in the source: equal sealed profiles (as collapse and separability), one orbit, and requirement membership.  The orbit statement conjugates an automorphism of the source by the isomorphism, through the composite `isoTrans`, whose field proofs are the work; the theorem itself is an assembly and is classed THIN. | PROVED_THEOREM | `isoTrans`; `oneOrbit_iso`, `reqMember_iso`, `separable_iso_iff`, `collapsed_iso_iff`, `sortPair_map`, `sortPair_swap`; `test_c2_the_observables_are_carried_with_admission_only`; prediction C-2, HIT |
| ENG-10 | The four rules that read only those observables -- E-one, E-three, E-four, E-eight -- are mirrored as readings, and each is carried, in both modes, as are its demands.  So the labels and demands of E-three and E-four are invariant under renaming, for every regime, in the Lean mirror; rung two left that OPEN at transport replay for E-three, E-four and E-six.  E-six, which also reads profile size, stays OPEN, and rung two's receipt is not revised. | PROVED_THEOREM | `demand_carried`, `carried_flip`, `e1_carried`, `e3_carried`, `e4_carried`, `e8_carried`; `test_c3_every_mirrored_reading_is_carried`; prediction C-3, HIT |
| ENG-11 | E-one gives no demand at any regime, in plain mode; its flip demands every collapsed and every separable pair.  E-three and E-four are one another's flip, by `rfl`.  A regime holding no requirement gives E-eight and its flip no demand, and no member of the class imposes one.  An engine whose generator reads E-one has no demand at any plain state, and with HALT has no step there. | PROVED_THEOREM | `e1_never_demands`, `e1_flip_demands`, `e3_flip_eq_e4`, `e4_flip_eq_e3`, `flip_flip`, `e8_quiet_without_reqs`, `e1_engine_quiet`, `e1_halt_no_step`; `test_c4_the_quiet_rules_and_the_flips`; predictions C-1 and C-4, HIT |
| ENG-12 | At the genesis of reading L -- two data and nothing else, which the genesis history replays to -- the two data are collapsed and in one orbit; E-four has a demand there, E-three and E-one have none, and the flip of E-one has one. | DEFINITION | `genL_replays`, `genL_one_orbit`, `genL_collapsed`, `e4_demands_at_genL`, `e3_quiet_at_genL`, `e1_flip_demands_at_genL`, `minima_differ_at_genL`; `test_c5_the_genesis_of_reading_l`; prediction C-5, HIT |

## Stage three: the probe

The probe of `PROMPT.md`, at the sealed bounds (two items, arity two),
unpruned, growth below four data, to level two, at both sealed genesis
readings: two hundred and eighty-eight probes, seven hundred and
twenty-eight nodes, six hundred and eight edges, twenty distinct probe
contents over the two readings.  By label signature, and by exact
content alike, the probe puts the one hundred and forty-four members in
ten classes.

| id | claim | class | evidence |
|---|---|---|---|
| ENG-13 | In plain mode at both genesis regimes E-four is the only rule with a demand -- one at L, three at F, every one apart; in flipped mode E-one, E-two, E-three, E-five, E-six and E-nine demand every held pair apart, and E-four, E-seven and E-eight none.  Every growth state of the probe is demand-free. | FINITE_COMPUTATION | `receipts/engine.json` `probe`; `test_the_four_root_terminals`; `test_the_probe_puts_the_members_in_ten_classes`; prediction C-11, HIT |
| ENG-14 | Every demand of the probe is answered at two items, under both measures and both members, which give the same minima there: six tied minima under `mu1` and two under `mu2` at L, ten and two at F; every minimum is one form admission and one instance admission; no demand is refused. | FINITE_COMPUTATION | `test_the_genesis_ties`; prediction C-12, HIT |
| ENG-15 | Every state an E-four response reaches reads a demand of kind same: at L exactly one, at F two or three.  So the E-four rule relabels the pair it has just separated. | FINITE_COMPUTATION | `demand_census`; `test_the_demand_census_names_an_odd_state_at_l`; prediction C-13, HIT |
| ENG-16 | Sixty-four members are LIVE -- an answered demand in the probe at both readings: the sixteen reading E-four, and the forty-eight reading E-one, E-two, E-three, E-five, E-six or E-nine with switch in their continuation.  The sixteen reading E-four, and only they, are TWO-KINDED. | FINITE_COMPUTATION | `receipts/engine.json` `live`, `two_kinded`; prediction C-14, HIT |
| ENG-17 | Every node of the probe replays from its genesis by the engine's replay rule, and every edge holds exactly the events of its capability: zero mismatches, zero violations.  An edge holding a requirement is refused by name, and so is every other misattribution. | FINITE_COMPUTATION | `replay_mismatches`, `attribution_violations`; `test_every_node_replays_and_every_edge_is_attributed`; `test_an_edge_carrying_a_requirement_is_named`; `test_every_other_misattribution_is_named`; prediction C-18, HIT |
| ENG-18 | Cross-checks: fifty-six responder situations reduce to four distinct situations of member one; on each, under each measure, this tree's responder agrees with rung two's minimum responses, and every situation agrees with its representative.  The sealed key procedure and the brute-force minimum give one partition of the twenty-two probe regimes, nine classes.  The probe-isomorphism decided by labels agrees with the exhaustive search in all twelve hundred and thirty-two comparisons, four hundred and twenty of them isomorphic and eight hundred and twelve not.  Each check reports a disagreement when one is injected. | FINITE_COMPUTATION | `responder_crosscheck`, `key_brute_disagreements`, `brute_isomorphic`; `test_the_responder_agrees_with_rung_two`; `test_labels_and_the_exhaustive_search_agree_and_both_say_no`; `test_an_isomorphism_disagreement_is_reported`; `test_a_responder_disagreement_with_rung_two_is_reported`; `test_a_representative_and_a_member_disagreement_are_reported`; prediction C-19, HIT |

## Stage four: the minima, and the seed's required questions four and ten

Growth counted as one capability and, in brackets, as two.

| id | claim | class | evidence |
|---|---|---|---|
| ENG-19 | Count-minimal members.  Of the class: sixteen at count six -- every rule but E-six, each measure, member one, HALT [the same sixteen].  Of the seed-literal subclass: thirty-two at seven -- the same eight rules, each measure, member one, growth alone or switch alone [sixteen, switch alone].  Of the LIVE members of the class: the two reading E-four with member one and HALT [the same].  Of the LIVE seed-literal members: fourteen -- E-four with growth alone or switch alone, and E-one, E-two, E-three, E-five, E-nine with switch alone, each measure, member one [twelve].  Of the TWO-KINDED: two in the class, four in the seed-literal subclass [two].  In the class and the seed-literal subclass the inclusion-minimal members are exactly the count-minimal ones. | FINITE_COMPUTATION with DEFINITION | `count_minimal`, `inclusion_minimal`; `count_six_members`, `literal_count_seven_members`, `literal_count2_seven_members`, `literal_count_ge_seven`; `test_the_count_minima_are_the_declared_sets`; predictions C-8, C-9 and C-15, HIT |

| id | claim | class | evidence |
|---|---|---|---|
| Q4-EXISTS | A minimal member exists in every subclass named in ENG-19: the class is finite and each subclass is nonempty. | DEFINITION | ENG-19; `count_minimal` |
| Q4-UNIQUE | No minimum set of ENG-19 is unique up to probe-isomorphism.  The numbers of probe-isomorphism classes are three for the class minima, six [five] for the seed-literal minima, two and four [four] for the LIVE minima, and two for each TWO-KINDED set.  For the class minima the countermodel is in Lean too: two members alike but for reading E-four or E-one part at the root of reading L, one with a demand and one without (`minima_differ_at_genL`).  Every other split is between the two measures or between a member that answers at the root and one that answers after a switch. | COUNTERMODEL | `probe_signature`, `brute_isomorphic`; `minima_differ_at_genL`; `receipts/engine.json` `minima`; prediction C-16, HIT |
| Q4-INITIAL | No member is initial in the class under the declared morphisms, inclusions of declarations (`no_initial`), and none in any subclass holding members of both measures (`no_initial_of_two_measures`); every minimum set of ENG-19 holds both.  So the universal property is refused for this reading of morphism, and the refusal is scoped to it; another reading of morphism is G-5. | PROVED_THEOREM | `no_initial`, `no_initial_of_two_measures`; `initial_members`; `test_inclusion_and_initial_members`; predictions C-17 and C-20, HIT |
| Q10 | The seed's question ten asks the same of the surviving engine among engines meeting the same challenges: within this declared class and probe, the answer is Q4-EXISTS, Q4-UNIQUE and Q4-INITIAL for the LIVE and TWO-KINDED members, read as the members meeting challenge two's filters within the probe.  No engine is called the surviving one here. | COUNTERMODEL and PROVED_THEOREM | Q4-EXISTS, Q4-UNIQUE, Q4-INITIAL; prediction C-20, HIT |

## Recorded

| id | claim | class | evidence |
|---|---|---|---|
| CENSUS-NONE | No row of the challenge-five census is decided here, in any column.  Every FORCED column stays conditional on running the engines, which is the second attempt's. | RECORDED | prediction C-21, HIT |
| INPUT-COUNT | The input tally records thirty-two LIVE members whose declaration carries the stake and not the stream: the eight reading E-four with HALT or switch alone, and the twenty-four reading E-one, E-two, E-three, E-five, E-six or E-nine with switch alone.  Each answers a demand within the probe with no stream.  Whether any of them carries the grammar forward beyond the probe is G-2, named for the second attempt.  This attempt neither reduces the count of declared inputs nor proves it at a floor; the count stays at the value two. | RECORDED and FINITE_COMPUTATION | `input_tally`; `receipts/engine.json` `streamless_live`, `input_count_claim`; prediction C-22, HIT |
| ENG-PREDICTIONS | Of the frozen predictions, the thirteen computational rows score thirteen hits; the ten others are scored where their evidence lives.  The FW-DEF prediction names fifty targets and scores forty-eight hits and two misses: `oneOrbit_iso` predicted CONTENT and recorded THIN, a demotion, and `sortPair_swap` predicted DEFINITION and recorded THIN, a promotion; no native theorem was added beyond the prediction.  No theorem of the package is CONTENT.  Four rows were labelled FORCED before the run (C-8, C-9, C-10 and C-23), and a hit on a FORCED row evidences the order of the work, not insight. | PREDICTION | `receipts/engine.json` `predictions_scored`; `test_every_computed_prediction_is_a_hit`; `test_the_scorer_can_say_missed`; `test_the_prediction_is_scored_at_the_dated_values`; `test_every_miss_is_the_dated_one` |
