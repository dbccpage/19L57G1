# CLAIM LEDGER: rung six -- succession through the element count

`AuthorityEffect: None`.  Every row carries an evidence class.  A row at
the level of a definition is marked so and is never counted as content.
Per-theorem classification is NOT this file's job: it is
`FWDEF_CENSUS.json`'s, which is total over all thirty-four theorems of
this rung's package and is checked in both directions by
`test_census.py`.  Counts in this file are dated 2026-09-25.

Classes used: DEFINITION (true by unfolding, by `rfl`, by a projection,
by one rewrite, by kernel computation over a concrete history, or by pure
case exhaustion), PROVED_THEOREM, RECONSTRUCTION (the sealed estate's
theorem, reproduced verbatim under a pin, with no credit claimed here),
COUNTERMODEL, FINITE_COMPUTATION, OPEN, PREDICTION, RECORDED.

Library axioms, recorded exactly: of the thirty-four theorems, three
depend on no axiom, eighteen on `propext` alone, and thirteen on
`propext` and `Quot.sound`; none depends on `Classical.choice` or on any
other axiom.  The committed log is `receipts/lean_axioms.txt`, checked
against a fresh clean build by `verify_lean.py`.

---

## The leftover this rung takes, quoted by pin

Rung five's own leftover list names this rung's question.  It is quoted
verbatim from the span pinned in `SOURCE_MANIFEST.json` as
`research/second_symmetry/STATUS.md` lines 194-198, and is not edited:

> - **Z-4, succession through the element count.**  `size_counts_changes`
>   reads the number of CHANGING rounds off a regime and its base; whether
>   that decides the census row for succession of accepted rounds -- which
>   rounds are accepted, and whether the base must be named -- is not
>   claimed here.  Price: small; the theorem is in place.

**What this rung did with it.**  It declared three readings of an
accepted round -- EVERY event, every ADMITTING event, every CHANGING
event -- and decided, for each, whether the count of accepted rounds of a
history is carried by the regime it reaches.  Under CHANGING it is,
given the base, for every history of the sealed step; from the sealed
empty regime no base need be named; across bases the regime alone does
not carry it.  Under EVERY and under ADMITTING no function of base and
regime gives the count.  Taken up to the implemented isomorphism, the
answer is a finite computation on the rectangle and open beyond it.

---

## Stage one: the reconstruction

| id | claim | class | evidence |
|---|---|---|---|
| SUC-1 | The sealed kernel slice -- regime, well-formedness, contexts, derivability, collapse, separability, the six event kinds, the step, the replay, replay compositionality, the empty regime and the two sealed reading regimes with their recorded histories -- is reproduced verbatim under two blob pins and three span pins. | RECONSTRUCTION | `lean/SecondSuccession/Kernel.lean`; pins on `lean4/Derivation/Basic.lean` and `Inertia.lean`; `test_every_shared_declaration_is_identical` |
| SUC-2 | Thirty-seven declarations are shared between the reconstruction and its two pinned sources, and every one is identical after comments and namespace lines are stripped and whitespace is normalized; the four omitted declarations are pinned by name and mentioned nowhere in the reconstruction. | FINITE_COMPUTATION | `test_every_shared_declaration_is_identical`; `test_the_omitted_declarations_are_recorded_not_judged` |

## Stage two: the three readings, in Lean

| id | claim | class | evidence |
|---|---|---|---|
| SUC-3 | The element count of a regime is its data plus its forms plus its instances, rules and requirements, each counted as listed, as rung five defined it; it is zero at the empty regime.  The CHANGING count of a history replayed from a base counts the events after which the regime differs, and stops at an ill-formed event as replay does; the ADMITTING count counts the events other than supplies; the EVERY count is the length. | DEFINITION | `size_genesis`; the definitions `size`, `changes`, `weight`, `admitting` in `Count.lean` |
| SUC-4 | A supply is never a CHANGING round. | DEFINITION | `supply_uncounted`, `replayE_cons` |
| SUC-5 | Every event of the sealed step leaves the regime unchanged or raises its element count by exactly one.  The statement is rung five's `size_step`, proved again here so that the package imports nothing; it is not new to the run. | PROVED_THEOREM | `step_grows`, `insertNew_grows` |
| SUC-6 | For every base and every history that replays from it, the element count of the regime reached is the base's count plus the CHANGING count.  The statement is rung five's `size_counts_changes`, proved again here; it is not new to the run. | PROVED_THEOREM | `changes_counted`; prediction M-1, HIT |
| SUC-7 | Hence two histories from one base reaching one regime carry one CHANGING count, and a function of the base and the regime -- the element count of the regime less that of the base -- gives it.  No decidability hypothesis and no hypothesis beyond the replay. | PROVED_THEOREM | `changes_path_free`, `changes_given_base`; `test_m1_the_changing_count_is_read_off_base_and_regime`; prediction M-1, HIT |
| SUC-8 | From the sealed empty regime the CHANGING count of any history is the element count of the regime it reaches: no base is named. | PROVED_THEOREM | `changes_from_genesis`, `size_genesis`; prediction M-2, HIT |
| SUC-9 | Under EVERY the count is not a function of base and regime: from the empty regime the empty history and one supply reach one regime with counts zero and one.  So no function of base and regime gives it. | COUNTERMODEL | `every_splits` (kernel computation), `every_not_given_base`; prediction M-3, HIT |
| SUC-10 | Under ADMITTING the count is not a function of base and regime: from the empty regime a form of arity one with its uniform rule admitted once, and with the rule admitted twice, reach one regime with counts two and three.  So no function of base and regime gives it. | COUNTERMODEL | `admitting_splits` (kernel computation), `admitting_not_given_base`; prediction M-3, HIT |
| SUC-11 | Under CHANGING the count is not a function of the regime alone: the sealed reading-L regime is reached from the empty regime by the sealed reading-L history with count three, and from itself by the empty history with count zero.  So no function of the regime alone gives it, and the base must be named unless it is the empty regime. | COUNTERMODEL | `base_matters` (kernel computation through the sealed `historyL_replays`), `changing_not_of_regime`; prediction M-4, HIT |
| SUC-12 | For every base and every history, replayed or not, the CHANGING count is at most the ADMITTING count, which is at most the EVERY count. | PROVED_THEOREM | `changes_le_admitting`, `admitting_le_every`; prediction M-5, HIT |
| SUC-13 | That the CHANGING count is a function of the CLASS of a regime under the sealed isomorphism is NOT proved here; no native module of this package names the isomorphism.  Rung five's leftover Z-1, the element count across the isomorphism, is the named obstacle. | OPEN | `test_m6_no_theorem_mentions_the_isomorphism`; prediction M-6, HIT |

## Stage three: the finite cross-check

Over rung three's rectangle, unchanged: three bases, every sequence of at
most four declared events, 577, 3928 and 14293 sequences reaching 75, 523
and 1718 distinct regimes.  Counts are taken by stepping the sealed
Python step.

| id | claim | class | evidence |
|---|---|---|---|
| SUC-14 | Every node replays from its base; the sequence and regime counts are rung four's. | FINITE_COMPUTATION | `receipts/succession.json` `bases`, `replay_mismatches`; `test_the_rectangle_is_rung_three_s`; prediction M-8, HIT |
| SUC-15 | Under CHANGING, at every base: no regime is reached with two counts; on every sequence the count is the element count of the regime reached less that of the base; and counted from the sealed empty regime through the base's sealed genesis history followed by the sequence, it is the element count of the regime reached.  Zero violations of each. | FINITE_COMPUTATION | `bases.*.readings.CHANGING`, `changing_law_violations`, `changing_from_empty_violations`; `test_the_changing_reading_never_splits`; `test_a_forged_changing_count_violates_both_laws`; prediction M-9, HIT |
| SUC-16 | Under EVERY, 33, 118 and 276 regimes are reached with two counts at EMPTY, L and F, and the shortest splitting sequence at each base is one supply.  Under ADMITTING, 15, 100 and 259; the shortest splitting sequence has three events at EMPTY (a form of arity one, then its rule twice) and two at L and at F (one requirement imposed twice).  More regimes split under EVERY than under ADMITTING at every base. | FINITE_COMPUTATION | `bases.*.readings.EVERY`, `bases.*.readings.ADMITTING`; predictions M-10 and M-11, HIT |
| SUC-17 | Taken up to the implemented isomorphism, over 402 classes: no class is reached with two CHANGING counts within one base.  86 classes are reached from more than one base -- fourteen from EMPTY and L only, sixty-seven from L and F only, five from all three.  For every one of them the base-relative counts differ between its bases, and the counts from the sealed empty regime agree. | FINITE_COMPUTATION | `classes`; `test_agreeing_counts_at_two_bases_are_counted`; prediction M-12, HIT |
| SUC-18 | The element counts of the three bases are zero, two and three.  The sealed genesis histories carry, under EVERY, ADMITTING and CHANGING, six, two and two (L) and seven, three and three (F). | FINITE_COMPUTATION | `bases.*.base_element_count`, `bases.*.genesis_counts`; prediction M-13, HIT |
| SUC-19 | Each of the three Lean countermodels, written in the sealed Python grammar, replays with both sides reaching one regime and the counts differing as claimed.  The reading-L history there is the sealed Python genesis followed by the requirement the sealed Lean reading-L regime carries. | FINITE_COMPUTATION | `lean_witnesses`; `test_the_lean_witnesses_replay` |

## Stage four: the census row this rung decides

| id | claim | class | evidence |
|---|---|---|---|
| CENSUS-succession | Succession of accepted rounds, under three declared readings over histories of the sealed step.  CHANGING: DEFINABLE as a function of the base and the regime, the element count of the regime less that of the base, for every history (`changes_given_base`); DEFINABLE as a function of the regime alone when rounds are counted from the sealed empty regime (`changes_from_genesis`); NOT a function of the regime alone across bases (`changing_not_of_regime`).  EVERY and ADMITTING: NOT DEFINABLE from the base and the regime (`every_not_given_base`, `admitting_not_given_base`).  The trace the state counts its rounds through is the element count.  Up to the implemented isomorphism: a finite computation on the rectangle (SUC-17) and OPEN beyond it, behind rung five's Z-1.  FORCED in the seed's sense is conditional on an engine whose accepted rounds are the changing events of the sealed step; no such engine is declared yet.  Rung three's and rung four's readings stand: they read succession as the index of the first demand, which counts no rounds, and neither is revised here. | PROVED_THEOREM with COUNTERMODEL, FINITE_COMPUTATION and OPEN | SUC-6 to SUC-17; prediction M-14, HIT |

## Recorded

| id | claim | class | evidence |
|---|---|---|---|
| SUC-INPUTS | This rung neither reduces the count of declared inputs nor proves it at a floor; the value stays two, with no proof of a floor. | RECORDED | `receipts/succession.json` `input_count_claim`; prediction M-15, HIT |
| SUC-PREDICTIONS | Of the frozen predictions, the six computational rows score six hits and no miss; the FW-DEF prediction names seventeen targets and scores seventeen hits and no miss, with no native theorem it did not name.  Most rows were labelled FORCED before the run, and a hit on a FORCED row evidences the order of the work, not insight. | PREDICTION | `receipts/succession.json` `predictions_scored`; `test_the_scored_verdicts_are_the_dated_ones`; `test_the_prediction_is_scored_at_the_dated_values` |
