# CLAIM LEDGER: rung three -- the first-demand index over an arbitrary run

`AuthorityEffect: None`.  Every row carries an evidence class.  A row at
the level of a definition is marked so and is never counted as content.
Per-theorem classification is NOT this file's job: it is
`FWDEF_CENSUS.json`'s, which is total over all eighty-seven theorems of
this rung's package and is checked in both directions by
`test_census.py`.  Counts in this file are dated 2026-09-23.

Classes used: DEFINITION (true by unfolding, by `rfl`, by a projection,
by one rewrite, by kernel computation over a concrete regime, or by
assembling neighbours), THIN (one genuine step, or a direct corollary of
a neighbour), PROVED_THEOREM, RECONSTRUCTION (a sibling's or the sealed
estate's theorem, reproduced verbatim under a pin, with no credit claimed
here), COUNTERMODEL, FINITE_COMPUTATION, OPEN, METATHEORY, PREDICTION,
RECORDED.

---

## The leftover this rung takes, quoted by pin

The sibling rung's own leftover list names this rung's question.  It is
quoted verbatim from the span pinned in `SOURCE_MANIFEST.json` as
`research/second_nofirst/STATUS.md` lines 391-396, and is not edited:

> - **L-2, the first-demand index over an arbitrary run.**  `Run.lean` proves
>   no demand is ever first under a run of INERT events.  The other three
>   kinds do change demand sets, so locating the first demand of a general
>   run needs an index over histories.  Price: a moderate rung; the
>   definitions are in place and the induction shape is the one `Run.lean`
>   already uses.

**What this rung did with it.**  It defined the index over histories,
proved it unique, bounded it from below at the empty base, proved what
the event it counts last cannot be, and gave two countermodels: the index
is not a function of the regime a prefix reaches, and a demand can cease.
It did NOT prove that an index exists: existence is conditional on a
decision for the demand predicate, which this rung does not build and
names as a leftover.  The sibling's own statements are unchanged, and
this rung reports no change to them.

**The plan's item four, and why this rung is not it.**  The execution
list of `research/second/PLAN.md`, pinned here as a span, assigns the
engine of the seed's challenge three to this ordinal.  The seed's
next-rung rule -- the smallest named leftover that either reduces the
count of declared inputs or extends the census of challenge five, and on
a tie the one named first -- selects L-2 instead, because L-2 extends the
census row for succession and the parallel track recorded the
declared-input count at two with no reduction proved.  The sibling's own
statement of that rule and of its outcome is pinned as the second
`STATUS.md` span.  The engine is undone and is named as a leftover in
`STATUS.md`; it is executed nowhere here.

---

## Stage one: the reconstructions

| id | claim | class | evidence |
|---|---|---|---|
| IX-1 | The sealed kernel slice -- regime, contexts, derivability, collapse, separability, the six event kinds, the step, the replay, replay compositionality, and the two sealed reading regimes -- is reproduced verbatim under a blob pin and three span pins. | RECONSTRUCTION | `lean/SecondIndex/Kernel.lean`; pins on `lean4/Derivation/Basic.lean` and `Inertia.lean`; `verify_pins.py`; `test_reconstruction.py` |
| IX-2 | The sibling rung's two-sided stake, honour, demand predicate, four demand results, transport lemma, form-admission inertia, and inert-run results are reproduced verbatim under a blob pin and six span pins. | RECONSTRUCTION | `lean/SecondIndex/Inherited.lean`; six spans of the sibling package |
| IX-3 | Seventy-five declarations are shared between the reconstructions and their pinned sources, and every one of them is identical after comments, namespace lines and `open` lines are stripped and whitespace is normalized. | FINITE_COMPUTATION | `test_every_shared_declaration_is_identical` |
| IX-4 | The reconstructions add no declaration absent from their pinned sources. | FINITE_COMPUTATION | `test_reconstruction_modules_add_no_unattributed_declaration` |
| IX-5 | Seventeen declarations of the pinned sources are omitted, named exactly, and mentioned nowhere in the reconstructions. Whether omitting them is SAFE is read by hand. | OPEN, named | `test_the_omitted_declarations_are_recorded_not_judged`; leftover X-4 in `STATUS.md` |
| IX-6 | `replayE_append` -- that a history extended by one event replays by stepping the replayed prefix -- is the SEALED estate's own theorem, not this rung's. The frozen prediction took it for this rung's content; that is a census miss, recorded. | RECONSTRUCTION | `Sealed.replayE_append`; `test_the_one_reconstruction_the_prediction_took_for_native` |

## Stage two: the index

| id | claim | class | evidence |
|---|---|---|---|
| IX-7 | The regime a prefix of length `k` reaches from a base is `replayE (h.take k) base`; a prefix carrying an admission the grammar refuses reaches none, and the definition carries that case explicitly (`stateAt`). | DEFINITION | `lean/SecondIndex/Index.lean` |
| IX-8 | The count zero names the base itself (`stateAt_zero`). | DEFINITION -- `rfl` | `lean_axioms.txt` |
| IX-9 | A count one larger reaches what the smaller count reaches, stepped by the one event it consumes last (`stateAt_succ`), for every history and every count below its length. | PROVED_THEOREM | `lean_axioms.txt`; through the reconstructed `replayE_append` |
| IX-10 | Carrying a demand is some ordered pair of held data being a demand (`HasDemand`); being a first count is carrying one with no shorter prefix carrying one (`IsFirstDemand`). Both are propositions, not functions. | DEFINITION | `lean/SecondIndex/Index.lean` |
| IX-11 | For one base, one history and one stake, at most one count is a first count (`first_demand_unique`), with no decidability hypothesis and no hypothesis on the events. | PROVED_THEOREM | `lean_axioms.txt` |
| IX-12 | The count zero is a first count exactly when the base itself carries a demand (`first_demand_zero_iff_base_carries_one`). | THIN | `lean_axioms.txt` |
| IX-13 | Under the stake that labels every pair free, no count is a first count at any base along any history (`free_stake_has_no_index`). | DEFINITION -- through the reconstructed `free_stake_no_demand` | `lean_axioms.txt`; `index.json` earliest index `null` for the free stake at all three bases |
| IX-14 | All six event kinds carry a well-formed regime to a well-formed regime whenever the grammar admits the step (`wf_step_any`); hence every prefix of every history from a well-formed base reaches a well-formed regime (`wf_replayE`, `wf_stateAt`). | PROVED_THEOREM | `lean_axioms.txt` |
| IX-15 | From a well-formed base, when a first count is a successor, the event that count consumes last is NOT one of the three kinds the sibling rung proved demand-inert (`first_demand_follows_a_changing_event`). | PROVED_THEOREM | `lean_axioms.txt` |
| IX-16 | IX-15 does not say the event CAUSED the demand, and does not name the kind positively. A demand is read off the state; the theorem orders two prefixes and says no more. | RECORDED | the disclaimer at the theorem in `Index.lean` |
| IX-17 | Over the whole rectangle -- three bases, seven stakes, every sequence of at most four events -- no first count that is a successor consumes an inert event last: the violation count is zero, and the counter is shown able to fire. | FINITE_COMPUTATION | `index.json` `inert_last_event_violations`; `test_declaring_an_admission_inert_is_counted_as_a_violation` |
| IX-18 | One event admits at most one datum (`data_of_step`, `data_le_step`), so a prefix of length `k` reaches a regime holding at most `k` data more than its base (`data_le_replay`, `data_le_stateAt`). | PROVED_THEOREM | `lean_axioms.txt` |
| IX-19 | From the regime with nothing admitted, no count below two is a first count, for any stake and any history whatever (`no_index_below_two_from_the_empty_base`). | THIN -- a corollary of IX-18 and `demand_needs_two_data` | `lean_axioms.txt`; `index.json` earliest index two at the empty base |
| IX-20 | From a well-formed base carrying no demand, a run built only from the three inert kinds has no first count (`inert_run_carries_no_index`). | THIN -- the sibling's run theorem restated in the index vocabulary | `lean_axioms.txt` |

## Stage three: existence, and the decision it needs

| id | claim | class | evidence |
|---|---|---|---|
| IX-21 | A decidable predicate on the numbers with a witness has a least witness (`least_witness_from`, `least_witness`), by bounded upward search, with no classical extraction. | PROVED_THEOREM | `lean_axioms.txt`; the whitelist holds at `propext` and `Quot.sound` |
| IX-22 | If some prefix reaches a regime carrying a demand AND carrying a demand is decidable at a regime, then a first count exists (`first_demand_exists_when_a_demand_is_decidable`). | PROVED_THEOREM, CONDITIONAL on its hypothesis | `lean_axioms.txt` |
| IX-23 | The decidability hypothesis of IX-22 is NOT discharged here. Whether a regime carries a demand is a statement over the sealed context type; the well-formed contexts of a fixed regime are finitely many, so a decision procedure exists in principle, and this rung builds none. | OPEN, named and priced | leftover X-1 in `STATUS.md`; `test_the_existence_theorem_carries_a_decidability_hypothesis`; `test_no_decision_procedure_for_separability_is_declared` |
| IX-24 | Over the rectangle the first count IS computed, because every regime there is concrete and its profiles are finite. That computation is not evidence for IX-22's hypothesis in Lean, and no row here treats it as such. | FINITE_COMPUTATION, kept apart | `index.py`; the note at the head of that file |

## Stage four: the two countermodels

| id | claim | class | evidence |
|---|---|---|---|
| IX-25 | Two histories from the empty base -- two datum admissions, and a supply followed by the same two -- reach one and the same regime with first counts two and three (`index_is_not_a_function_of_the_reached_regime`). | COUNTERMODEL | `lean_axioms.txt`; `index.json` collision witness at the empty base |
| IX-26 | Hence there is NO function from regimes to numbers returning the first count of every history reaching that regime from the empty base under the apart-labelling stake (`no_state_function_gives_the_index`). | COUNTERMODEL, stated negatively | `lean_axioms.txt` |
| IX-27 | The same two histories are exhibited on the Python side, with the same two counts, and the two sides are compared as text rather than assumed to agree. | FINITE_COMPUTATION | `test_the_two_sides_name_the_same_three_histories`; `test_the_two_sides_report_the_same_two_counts` |
| IX-28 | A demand standing at one prefix need not stand at a longer one: a four-event history carries a demand at the prefix of length two and none at the prefix of length four (`demand_can_cease`). | COUNTERMODEL | `lean_axioms.txt`; `test_a_demand_can_cease` |
| IX-29 | What ends it is not a withdrawal of the stake, which is declared once and never moves, but a change in what the regime observes: the admitted instance separates the pair, and separability honours an apart label. | RECORDED | the note at `demand_can_cease` |
| IX-30 | Over the whole rectangle the event kinds at which a standing demand ceases are exactly two: the admission of a judgment instance and the admission of a uniform rule. | FINITE_COMPUTATION | `index.json` `cessation_kinds`; prediction I-18, HIT |
| IX-31 | The first count of the ceasing history is still two: a first count is a first occurrence and not a threshold. | FINITE_COMPUTATION and DEFINITION | `index_of_ceaseHistory`; `test_the_count_of_the_ceasing_history_is_still_two` |
| IX-32 | The six-clause assembly `first_demand_index` adds nothing beyond its conjuncts and is never counted as content. | DEFINITION -- an assembly | `lean_axioms.txt`; `FWDEF_CENSUS.json` |

## Stage five: the rectangle

| id | claim | class | evidence |
|---|---|---|---|
| IX-33 | The rectangle holds 577 sequences from the empty base, 3928 from reading L, and 14293 from reading F, at a bound of four events over the declared alphabet. The last two replay the sibling receipt's counts. | FINITE_COMPUTATION | `index.json`; prediction I-12 and I-13, both HIT |
| IX-34 | Every node of the rectangle replays from its base to the regime recorded for it; the mismatch count is zero, and the counter is shown able to fire. | FINITE_COMPUTATION | `index.json` `replay_mismatches`; `test_a_tampered_node_is_counted_as_a_replay_mismatch` |
| IX-35 | The first count computed by walking forward and the first count computed by the independently written second procedure agree at every base, stake and sequence; the disagreement count is zero, and the counter is shown able to fire. | FINITE_COMPUTATION | `index.json` `procedure_disagreements`; `test_a_blinded_second_procedure_is_counted_as_a_disagreement` |
| IX-36 | The earliest first count is two at the empty base for five of the seven stakes, four for the same-labelling stake, and absent for the free stake; it is zero at both sealed readings for those five, two for the same-labelling stake, and absent for the free stake. | FINITE_COMPUTATION | `index.json`; predictions I-14 and I-15, both HIT |
| IX-37 | From the empty base under the apart-labelling stake the first counts taken over the rectangle are exactly two, three and four, and 21 regimes are reached with more than one first count. | FINITE_COMPUTATION | `index.json`; predictions I-19 and I-20, both HIT |
| IX-38 | The independently written second enumerator reaches exactly the regimes the first reaches, on the declared cross-check family at depth three, at all three bases. | FINITE_COMPUTATION | `index.json` `crosscheck`; `test_a_disagreeing_second_enumerator_is_reported` |
| IX-39 | The receipt regenerates byte-identically and carries no timestamp and no environment value. | FINITE_COMPUTATION | `run_index.py --check`; `test_the_committed_receipt_matches_a_fresh_run` |

## The census of the seed's challenge five

| id | claim | class | evidence |
|---|---|---|---|
| CENSUS-succession | Succession, read as the count of accepted events a prefix consumes, is NOT DEFINABLE from the state's own observables at the stage reached: no function of the regime returns the first-demand index, by `no_state_function_gives_the_index`. The scope is this grammar, the empty base, the apart-labelling stake, and the reading of the index fixed in `Index.lean`; a different reading of succession is a different row and is not decided here. | COUNTERMODEL | `lean_axioms.txt`; `CLAIM_LEDGER.md` IX-25 and IX-26; prediction I-23 |

**No other census row is decided.**  Two-ness, observational classes,
duration, adjacency, reach, invariants, irreversibility, symmetry,
branching, exhaustion and recurrence are untouched here, and this rung
claims nothing about them in either direction.

## What this rung does not claim

| id | claim | class | evidence |
|---|---|---|---|
| IX-40 | This rung neither reduces the count of declared inputs below two nor proves it at a floor. Its receipt records the claim as absent in those words. | RECORDED | `index.json` `input_count_claim: none` |
| IX-41 | Nothing here is a claim about the sealed estate's standing obstructions, which this rung leaves exactly where it found them. | RECORDED | `test_no_file_reports_the_obstruction_as_discharged` |
| IX-42 | Nothing here is a claim about a grammar other than the sealed one reconstructed in `Kernel.lean` extended by a declared two-sided stake. | RECORDED | the scope sentence carried by every theorem statement |
| IX-43 | The pins prove that the sources did not move. They prove nothing about the mathematics, and a green gate proves nothing that its injection has not shown it can fail on. | METATHEORY | `research/second/MANUAL.md` injection record |
