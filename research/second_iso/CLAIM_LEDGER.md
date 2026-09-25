# CLAIM LEDGER: rung four -- the first-demand index up to the implemented isomorphism

`AuthorityEffect: None`.  Every row carries an evidence class.  A row at
the level of a definition is marked so and is never counted as content.
Per-theorem classification is NOT this file's job: it is
`FWDEF_CENSUS.json`'s, which is total over all eighty-four theorems of
this rung's package and is checked in both directions by
`test_census.py`.  Counts in this file are dated 2026-09-24.

Classes used: DEFINITION (true by unfolding, by `rfl`, by a projection,
by one rewrite, by kernel computation over a concrete regime, or by
assembling neighbours), THIN (one genuine step, or a direct corollary of
a neighbour), PROVED_THEOREM, RECONSTRUCTION (a sibling's or the sealed
estate's theorem, reproduced verbatim under a pin, with no credit claimed
here), COUNTERMODEL, FINITE_COMPUTATION, OPEN, METATHEORY, PREDICTION,
RECORDED.

Library axioms, recorded exactly: of the eighty-four theorems, four
depend on no axiom, thirty-four on `propext` alone, and forty-six on
`propext` and `Quot.sound`; none depends on `Classical.choice` or on any
other axiom.  The committed log is `receipts/lean_axioms.txt`, checked
against a fresh clean build by `verify_lean.py`.

---

## The leftover this rung takes, quoted by pin

Rung three's own leftover list names this rung's question.  It is quoted
verbatim from the span pinned in `SOURCE_MANIFEST.json` as
`research/second_index/STATUS.md` lines 152-156, and is not edited:

> - **X-3, the index up to the implemented isomorphism.**  The rectangle
>   counts sequences, not classes: two histories that differ by a renaming
>   of presentation tokens are two nodes.  Whether the first count is an
>   invariant of the isomorphism class is neither proved nor computed here.
>   Price: small, and the sealed `iso.py` is the tool.

**What this rung did with it.**  It separated three readings of "an
invariant of the isomorphism class" and answered each.  Of the class of
the regime a history reaches: no, inherited from rung three and measured
again here.  Of the classes of every prefix -- class-matched histories:
yes under a uniform stake, proved; no under each of the three declared
stakes that are not uniform, by exhibited countermodels at eight and
eleven events, beyond the rectangle's bound of four, inside which no
class-matched pair differs under any stake.  Of a renaming of
presentation tokens: yes, proved for the tokens the Lean events carry and
computed for every token of the rectangle.

---

## Stage one: the reconstructions

| id | claim | class | evidence |
|---|---|---|---|
| ISO-1 | The sealed kernel slice -- regime, contexts, derivability, collapse, separability, the six event kinds, the step, the replay, replay compositionality, and the two sealed reading regimes -- is reproduced verbatim under a blob pin and three span pins. | RECONSTRUCTION | `lean/SecondIso/Kernel.lean`; pins on `lean4/Derivation/Basic.lean` and `Inertia.lean`; `test_every_shared_declaration_is_identical` |
| ISO-2 | The sealed isomorphism structure, its identity instance, the swap of the first two data, the inverse isomorphism, the images of an instance and of a context, and the transport of collapse across an isomorphism are reproduced verbatim from two sealed modules, one of them parked, under blob and span pins. | RECONSTRUCTION | `lean/SecondIso/IsoKernel.lean`; pins on `lean4/Derivation/Minimality.lean` and `IsoCollapse.lean`; `test_every_shared_declaration_is_identical` |
| ISO-3 | The track-one sibling's label, stake, three constant stakes, honour, demand predicate, and the two constructive readings of collapse against separability are reproduced verbatim. | RECONSTRUCTION | `lean/SecondIso/Inherited.lean`; pins on `Stake.lean` and `NoFirst.lean` of `research/second_nofirst/lean/` |
| ISO-4 | Rung three's prefix reading, carrying a demand, being a first count, quiet before the index, and uniqueness of the first count are reproduced verbatim. | RECONSTRUCTION | `lean/SecondIso/IndexSlice.lean`; pins on `research/second_index/lean/SecondIndex/Index.lean` |
| ISO-5 | Seventy-three declarations are shared between the four reconstruction modules and their seven pinned sources, and every one is identical after comments, namespace and `open` lines are stripped and whitespace is normalized; the omitted declarations are pinned by name and mentioned nowhere in the reconstructions. | FINITE_COMPUTATION | `test_every_shared_declaration_is_identical`; `test_the_omitted_declarations_are_recorded_not_judged` |

## Stage two: a demand transported across the isomorphism

| id | claim | class | evidence |
|---|---|---|---|
| ISO-6 | In the sealed grammar reconstructed here, separability of two admitted data transports along the datum bijection of a sealed isomorphism in both directions, by carrying the witnessing context; no decision of collapse or separability is made. | PROVED_THEOREM | `separable_fwd`, `separable_transport`; prediction J-1, HIT |
| ISO-7 | Honour of each of the three labels is symmetric in the pair and transports across a sealed isomorphism. | PROVED_THEOREM | `honour_symm`, `honour_transport` |
| ISO-8 | In the sealed grammar reconstructed here, extended by a declared two-sided stake: a demand at a regime is carried to a demand at any isomorphic regime whenever the isomorphism preserves the stake's labels on the held pairs. | PROVED_THEOREM | `demand_transport`, `uniform_preserved` |
| ISO-9 | Under a UNIFORM stake -- one label on every pair of distinct indices -- carrying a demand is invariant under the sealed isomorphism, at every pair of regimes it relates, reachable or not, with no decidability hypothesis. | PROVED_THEOREM | `hasDemand_iff_of_uniform`; prediction J-2, HIT |
| ISO-10 | The free stake, the stake labelling every distinct pair apart, and the stake labelling every distinct pair same are uniform. | DEFINITION | `uniform_freeStake`, `uniform_allApart`, `uniform_allSame`; prediction J-3, HIT |
| ISO-NECESSITY | Whether a stake that is not uniform can still make carrying a demand invariant under the isomorphism is OPEN.  The candidate named, and not proved: a stake labelling one pair of three indices apart and the two pairs that meet it same, which no regime of three or more data honours, so that every such regime carries a demand; proving that invariance needs a decision of collapse, which is rung three's leftover X-1. | OPEN | `test_j4_no_theorem_derives_uniformity`; prediction J-4, HIT |

## Stage three: countermodels for the stakes that are not uniform

| id | claim | class | evidence |
|---|---|---|---|
| ISO-11 | `parity`, `chain` and `residueThree`, declared here with the labels the sibling Python rules give, are each not uniform. That the Lean formulas are the Python rules is checked by transcription on every pair of distinct indices below twelve, not proved. | DEFINITION | `parity_not_uniform`, `chain_not_uniform`, `residue_not_uniform`; `test_the_lean_stake_formulas_are_the_sibling_rules` |
| ISO-12 | Under each of the three, two regimes the sealed isomorphism relates carry a demand and carry none: three data and one form of arity one for `parity` and `chain`, four data and two forms of arity one for `residueThree`. | COUNTERMODEL | `demand_not_class_invariant`; `test_the_lean_regime_pairs_carry_what_the_lean_says`; prediction J-5, HIT |
| ISO-13 | When every admitted form has arity one, a well-formed context has one slot and it is a hole; collapse of two data follows from form-by-form agreement on the one-slot instance, modulo uniform rules. | PROVED_THEOREM | `unary_ctx_slots`, `collapsed_of_unary` |
| ISO-14 | Boolean checks for honour, dishonour, carrying no demand and carrying one are proved SOUND: a check returning true implies the proposition it names. None is proved to return true whenever the proposition holds; none is a decision procedure, and a false return proves nothing. | PROVED_THEOREM | `sepB_sound`, `colB_sound`, `honourCheck_sound`, `dishonourCheck_sound`, `noDemandCheck_sound`, `demandCheck_sound`; `test_no_decision_procedure_for_separability_is_declared` |
| ISO-15 | Under a uniform stake, two class-matched histories, from any two bases, have exactly the same first counts, with no decidability hypothesis and no hypothesis on the bases or the events. | PROVED_THEOREM | `first_demand_transport`, `first_demand_matched_of_uniform`; prediction J-6, HIT |
| ISO-16 | Two class-matched histories of eight events from the empty base, with two forms of arity one and three data, differing only in their one uniform-rule admission, have first count eight and no first count at all, under `parity` and under `chain` alike. | COUNTERMODEL | `matched_P`, `index_P2_parity`, `quiet_P1_parity`, `index_P2_chain`, `quiet_P1_chain`; `test_the_first_counts_by_both_rung_three_procedures`; prediction J-7, HIT |
| ISO-17 | Two class-matched histories of eleven events from the empty base, with three forms of arity one and four data, differing only in their one uniform-rule admission, have first count eleven and no first count at all under `residueThree`. | COUNTERMODEL | `matched_Q`, `index_Q2_residue`, `quiet_Q1_residue`; prediction J-7, HIT |
| ISO-SHORTEST | Whether a shorter class-matched pair with differing first counts exists is OPEN at lengths five to seven for `parity` and `chain`, and at lengths five to ten for `residue_three`. The rectangle settles lengths up to four, where no pair differs; nothing between is enumerated. | OPEN | `test_the_shorter_witness_lengths_are_open`; prediction J-8, HIT |
| ISO-18 | Renaming the token every supply of a history carries moves no first count, under any declared stake; the Lean datum admission carries no token at all. | THIN | `first_demand_renameSupply`; prediction J-9, HIT |
| ISO-19 | The headline: invariance under uniform stakes at the level of regimes and of class-matched histories, the countermodels for the three other stakes at both levels, and the supply renaming, in one statement. | DEFINITION | `iso_index`, `first_count_not_trajectory_invariant` |

## Stage four: the finite cross-check

| id | claim | class | evidence |
|---|---|---|---|
| ISO-20 | The rectangle is rung three's: 577 sequences from the empty base, 3928 from reading L, 14293 from reading F; every node replays from its base. | FINITE_COMPUTATION | `iso_index.json` `bases`; `test_the_rung_three_counts_replay`; prediction J-10, HIT |
| ISO-21 | The 2316 distinct regimes the rectangle reaches fall into 402 classes, and the sealed key procedure and the brute-force minimum give the same partition, with zero disagreements; 357 classes hold at least two reached regimes. | FINITE_COMPUTATION | `iso_index.json` `key_partition_disagreements`, `class_split`; `test_a_blinded_brute_force_key_is_counted`; prediction J-11, HIT |
| ISO-22 | The sealed automorphism list and a brute-force count over every bijection pair agree at all 2316 regimes. The sizes taken are one, two, three, four, six, eight, twelve, twenty-four, forty-eight, one hundred and twenty and two hundred and forty. The frozen prediction said the largest would be twenty-four; it is two hundred and forty, at five collapsed data and two forms of one arity, because the sealed Python readings carry no imposed requirement. The miss is recorded and the prediction is not edited. | FINITE_COMPUTATION | `iso_index.json` `automorphisms`; `test_the_automorphism_counts_agree_and_a_wrong_one_is_counted`; prediction J-12, MISSED |
| ISO-23 | Under the four uniform-labelled stakes no class, taken as its reached members or as all 6128 presentations formed from its representatives, holds a regime carrying a demand and one carrying none. | FINITE_COMPUTATION | `iso_index.json` `reached_split_classes`, `orbit_split_classes`; prediction J-13, HIT |
| ISO-24 | Under `parity`, `chain` and `residue_three`, 47, 61 and 13 classes respectively hold a reached regime carrying a demand and a reached one carrying none, and the same counts hold when every presentation is taken; the witnesses replay from their bases. | FINITE_COMPUTATION | `iso_index.json` `class_split`; `test_the_witness_of_a_split_class_replays`; prediction J-14, HIT |
| ISO-25 | The 18798 sequences fall into 4368 trajectory classes, 3042 with at least two members and the largest with 72; under every one of the seven stakes the first count is constant on every trajectory class. For the three stakes that are not uniform this is a property of the bound, by ISO-16 and ISO-17, and not of the stake. | FINITE_COMPUTATION | `iso_index.json` `trajectory`; `test_a_tampered_count_in_a_shared_trajectory_is_counted`; prediction J-15, HIT |
| ISO-26 | Quotiented by the class of the regime the whole sequence reaches -- 402 classes -- the first count takes two different values on 19 classes under each of `total_apart`, `one_sided_total`, `parity`, `residue_three` and `chain`, on 226 under `total_same`, and on none under the free stake. | FINITE_COMPUTATION | `iso_index.json` `final_classes_with_two_counts`; prediction J-16, HIT |
| ISO-27 | The declared token renaming changes the presentation of 7849 sequences' final regimes and moves no first count and no prefix class, at any sequence. | FINITE_COMPUTATION | `iso_index.json` `tokens`; `test_a_collapsing_renaming_is_counted`; prediction J-17, HIT |
| ISO-28 | The four exhibited histories replay through the sealed step, their prefixes are pairwise in one class by both key procedures, and both of rung three's first-count procedures give the counts the Lean theorems state. | FINITE_COMPUTATION | `iso_index.json` `exhibited`; `test_the_pairs_are_class_matched_by_both_key_procedures`; `test_the_python_histories_are_the_lean_ones`; prediction J-18, HIT |
| ISO-29 | The receipt regenerates byte-identically, carries no timestamp and no environment value, and is 10316 bytes. | FINITE_COMPUTATION | `run_iso_index.py --check`; `test_the_committed_receipt_matches_a_fresh_run`; prediction J-19, HIT |

## The census of the seed's challenge five

| id | claim | class | evidence |
|---|---|---|---|
| CENSUS-succession | A second reading of succession, as the first count along a history taken up to the isomorphism. It is NOT a function of the class of the regime reached, since rung three's countermodel reaches one regime with two counts. It IS an invariant of class-matched trajectories under a uniform stake, by `first_demand_matched_of_uniform`; under the three declared stakes that are not uniform it is NOT, by `first_count_not_trajectory_invariant`. Within the rectangle no stake shows the difference. The scope is this grammar extended by the seven declared stakes. | PROVED_THEOREM | `lean_axioms.txt`; ISO-15 to ISO-17 and ISO-25; prediction J-21 |
| CENSUS-symmetry | Symmetry, as the size of the automorphism group of the state, is DEFINABLE at every stage the rectangle reaches: the sealed `automorphisms` computes it from the regime's own structure, and a brute-force count over every bijection pair agrees at all 2316 regimes. It is a function of the regime and not of the history reaching it. Whether it is preserved or monotone along any run is not decided here. | FINITE_COMPUTATION | `iso_index.json` `automorphisms`; ISO-22; prediction J-21 |

**No other census row is decided.**  Two-ness, observational classes,
duration, adjacency, reach, invariants, irreversibility, branching,
exhaustion and recurrence are untouched here, and this rung claims
nothing about them in either direction.

## What this rung does not claim

| id | claim | class | evidence |
|---|---|---|---|
| ISO-30 | This rung neither reduces the count of declared inputs below two nor proves it at a floor. Its receipt records the claim as absent in those words. | RECORDED | `iso_index.json` `input_count_claim: none`; `test_the_input_count_claim_is_absent` |
| ISO-31 | Nothing here is a claim about the sealed estate's standing obstructions, which this rung leaves exactly where it found them. | RECORDED | `test_no_file_reports_the_obstruction_as_discharged` |
| ISO-32 | Nothing here is a claim about a grammar other than the sealed one reconstructed in `Kernel.lean` extended by a declared two-sided stake, nor about a stake other than the seven declared. | RECORDED | the scope sentence carried by every theorem statement |
| ISO-33 | Rung three's frozen extrapolation stays PENDING; this rung declares no responder. | RECORDED | `research/second_index/receipts/index.json` |
| ISO-34 | The pins prove that the sources did not move. They prove nothing about the mathematics, and a green gate proves nothing that its injection has not shown it can fail on. | METATHEORY | `research/second/MANUAL.md` injection record |
