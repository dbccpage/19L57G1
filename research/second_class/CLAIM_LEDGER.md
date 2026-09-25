# CLAIM LEDGER: rung eight -- the element count across the isomorphism

`AuthorityEffect: None`.  Every row carries an evidence class.  A row at
the level of a definition is marked so and is never counted as content.
Per-theorem classification is NOT this file's job: it is
`FWDEF_CENSUS.json`'s, which is total over all fifty-eight theorems of
this rung's package and is checked in both directions by
`test_census.py`.  Counts in this file are dated 2026-09-25.

Classes used: DEFINITION (true by unfolding, by `rfl`, by a projection,
by one rewrite, by kernel computation over concrete regimes and maps, or
by pure case exhaustion), PROVED_THEOREM, RECONSTRUCTION (the sealed
estate's theorem, reproduced verbatim under a pin, with no credit claimed
here), COUNTERMODEL, FINITE_COMPUTATION, OPEN, PREDICTION, RECORDED.

Library axioms, recorded exactly: of the fifty-eight theorems, three
depend on no axiom, eighteen on `propext` alone, and thirty-seven on
`propext` and `Quot.sound`; none depends on `Classical.choice` or on any
other axiom.  The committed log is `receipts/lean_axioms.txt`, checked
against a fresh clean build by `verify_lean.py`.  Three library lemmas
the argument would naturally use -- removing one entry from a list, the
length after that removal, and the admitted range holding no index twice
-- reach `Classical.choice`, and none of them is used: the first two are
done by hand inside `length_le_of_nodup_sub`, and the third is proved
again as `range_nodup`.

---

## The leftover this rung takes, quoted by pin

Rung five's own leftover list names this rung's question, and rung
seven's application of the seed's next-rung rule selects it.  It is
quoted verbatim from the span pinned in `SOURCE_MANIFEST.json` as
`research/second_symmetry/STATUS.md` lines 178-188, and is not edited:

> - **Z-1, the element count across the isomorphism.**  Whether two
>   regimes the sealed isomorphism relates have one element count.  It
>   would carry `no_return` from regimes to classes beyond the rectangle,
>   deciding irreversibility up to the isomorphism and the census row for
>   recurrence, which asks for an isomorphic state revisited.  Obstacle
>   recorded: the Lean regime keeps its collections as lists and
>   `Regime.wf` does not forbid a repeated entry, so the count is an
>   invariant only of duplicate-free regimes; every regime reached from the
>   empty one by the sealed step is duplicate-free, which is itself to be
>   proved.  Price: moderate -- a counting argument on the two
>   half-bijections in core Lean, plus the duplicate-free invariant.

**What this rung did with it.**  It split the element count into its five
component counts and decided each across the sealed isomorphism: the data
and the forms are kept by every inhabitant of the structure, with no
hypothesis; the instances, the rules and the requirements are kept
between CLEAN regimes -- well formed and duplicate-free -- and for each of
the three, each hypothesis is shown necessary by a pair of regimes that
breaks it alone.  It proved that the sealed step keeps a regime clean and
that the empty regime and both reading regimes are clean.  From a clean
base, therefore, a history never returns to a class it left, revisits a
class only as the very regime it left through events that change
nothing, and carries its CHANGING count, its growths and its rest rounds
in the class of the regime reached; across two bases it does not.

---

## Stage one: the reconstruction

| id | claim | class | evidence |
|---|---|---|---|
| CLS-1 | The sealed kernel slice -- regime, well-formedness, contexts, derivability, collapse, separability, the six event kinds, the step, the replay, replay compositionality, the empty regime and the two sealed reading regimes with their recorded histories -- and the sealed isomorphism structure with its requirement ordering, its identity instance and the swap of the first two data, are reproduced verbatim under three blob pins and four span pins. | RECONSTRUCTION | `lean/SecondClass/Kernel.lean`, `lean/SecondClass/IsoKernel.lean`; pins on `lean4/Derivation/Basic.lean`, `Inertia.lean` and `Minimality.lean`; `test_every_shared_declaration_is_identical` |
| CLS-2 | Forty-one declarations are shared between the reconstructions and their three pinned sources, and every one is identical after comments and namespace lines are stripped and whitespace is normalized; the omitted declarations are pinned by name and mentioned nowhere in the reconstructions. | FINITE_COMPUTATION | `test_every_shared_declaration_is_identical`; `test_the_omitted_declarations_are_recorded_not_judged` |

## Stage two: the counts across the isomorphism, in Lean

| id | claim | class | evidence |
|---|---|---|---|
| CLS-3 | The counts of a history -- the CHANGING count, the growths and the rest rounds -- are the definitions of rungs six and seven, and the regime reached has the base's element count plus the CHANGING count, the base's data plus the growths, and the base's element count plus the growths plus the rest rounds.  The statements are rung six's and rung seven's, proved again here; they are credited, not counted as new to the run. | PROVED_THEOREM | `changes_counted`, `growths_counted`, `rest_counted`, `step_parts`, `insertNew_grows`, `replayE_cons` |
| CLS-4 | A history cut in two replays as its first part, then its second from the regime the first reaches; and a history with CHANGING count zero that replays reaches its base. | PROVED_THEOREM | `replayE_split` (at the level of a definition), `still_of_no_changes` |
| CLS-5 | A list without a repeated entry, every entry of which lies in a second list, is no longer than it, over decidable equality and with no classical step; so a list without a repeated entry carried into a second list by a map with a left inverse on it is no longer than the second.  The admitted range holds no index twice. | PROVED_THEOREM | `length_le_of_nodup_sub`, `nodup_map_of_inv`, `count_le_of_inv`, `range_nodup` |
| CLS-6 | For every two regimes and every inhabitant of the sealed isomorphism between them, the numbers of data are equal and the numbers of forms are equal, with NO hypothesis on either regime. | PROVED_THEOREM | `data_le`, `forms_le`, `iso_data`, `iso_forms`, through the exchanged structure `isoSymm`; `test_p1_data_and_forms_need_no_hypothesis`; prediction P-1, HIT |
| CLS-7 | For every inhabitant of the sealed isomorphism from a well-formed source, a list of instances, of uniform rules or of requirements of the source that holds no entry twice is no longer than the matching list of the target; nothing is assumed of the target.  So two clean regimes the structure relates have all five component counts equal and one element count. | PROVED_THEOREM | `insts_le`, `rules_le`, `reqs_le`, `sortPair_of_le`, `sortPair_map`, `components_iso`, `size_iso`; `test_p2_the_three_lists_need_hypotheses_on_the_source_only`; prediction P-2, HIT |
| CLS-8 | Neither hypothesis can be dropped, for any of the three lists: for each, two regimes the structure relates, both well formed and the target duplicate-free, with different lengths because the source holds one entry twice; and two regimes the structure relates, both duplicate-free and the target well formed, with different lengths because the source holds an instance or a rule naming an index outside its range, or a requirement in the wrong order, which the maps carry onto an entry the target already has. | COUNTERMODEL | `insts_need_nodup`, `insts_need_wf`, `rules_need_nodup`, `rules_need_wf`, `reqs_need_nodup`, `reqs_need_wf` (each by kernel computation, at the level of a definition); `test_p3_six_countermodels_one_hypothesis_broken_each`; prediction P-3, HIT |
| CLS-9 | Every event of the six sealed kinds that the sealed step accepts keeps a clean regime clean; so every regime a history reaches from a clean base is clean.  The sealed empty regime and the two sealed reading regimes are clean. | PROVED_THEOREM | `nodup_insertNew`, `getD_append_lt` (rung five's statement, credited), `clean_step`, `clean_replay`; `genesis_clean`, `R2L_clean`, `R2F_clean` (by kernel computation, at the level of a definition); `test_p4_cleanness_is_kept_by_every_event`; prediction P-4, HIT |
| CLS-10 | From a clean base, for every history that replays: if the first event changes the regime, no regime the rest of the history reaches is isomorphic to the base; and if the regime reached after the whole history is isomorphic to the regime reached after a first part of it, the two are EQUAL and the rest of the history has CHANGING count zero. | PROVED_THEOREM | `no_return_class`, `recurrence_is_stutter`; `test_p5_no_return_and_stutter_need_only_a_clean_base`; prediction P-5, HIT |
| CLS-11 | From one clean base, two histories reaching isomorphic regimes have one CHANGING count, one number of growths and one number of rest rounds; in particular from the sealed empty regime. | PROVED_THEOREM | `counts_of_class`, `counts_of_class_genesis`; `test_p6_the_counts_are_carried_by_the_class`; prediction P-6, HIT |
| CLS-12 | Across two bases the class does not carry the count: the empty history from the sealed Lean reading regime `R2L`, and a datum, a datum and the requirement between them from the sealed empty regime, reach one regime with CHANGING counts zero and three. | COUNTERMODEL | `counts_not_of_class` (by kernel computation, at the level of a definition); `test_p7_across_bases_the_count_moves`; prediction P-7, HIT |

## Stage three: the finite cross-check

Over rung three's rectangle, unchanged: three bases, every sequence of at
most four declared events, 577, 3928 and 14293 sequences reaching 75, 523
and 1718 distinct regimes, 2316 in all.  Counts are taken by stepping the
sealed Python step; classes are the sealed key procedure's.

| id | claim | class | evidence |
|---|---|---|---|
| CLS-13 | Every node replays from its base; the sequence and regime counts are rung four's; there are 54, 174 and 265 classes within EMPTY, L and F and 402 over all three; the key partition and the brute-force partition agree at every one of the 2316 regimes. | FINITE_COMPUTATION | `receipts/class_count.json`; `test_the_rectangle_is_rung_three_s`; prediction P-9, HIT |
| CLS-14 | No class, within any base or over all three, carries two values of any of the five component counts; no class within a base is reached with two CHANGING counts, two numbers of growths or two numbers of rest rounds.  The Python regime keeps sets, so this says nothing about repeated entries in the Lean lists. | FINITE_COMPUTATION | `classes_with_two_component_tuples`; `test_the_class_counts_are_the_dated_ones`; `test_a_lumping_partition_is_counted_everywhere`; prediction P-10, HIT |
| CLS-15 | At every base no sequence returns; a sequence recurs exactly when it holds an event that leaves the regime unchanged -- 339, 1597 and 4790 sequences at EMPTY, L and F -- and every recurrence is a stutter: 454, 1921 and 5583 of them, reached by a supply, a repeated instance, a repeated uniform rule and a repeated requirement at every base, and never by a datum or a form. | FINITE_COMPUTATION | `recurrence_report`; `test_the_recurrence_counts_are_the_dated_ones`; `test_a_forged_partition_shows_returns_and_mismatches`; prediction P-11, HIT |
| CLS-16 | 86 classes are reached at more than one base, 5 of them at all three, inside the range forty-six to ninety-one the receipts force; every one of the 86 is reached with two CHANGING counts. | FINITE_COMPUTATION | `classes_at_more_than_one_base`; `test_the_arithmetic_range_is_the_receipts`; prediction P-12, HIT |
| CLS-17 | The six hypothesis countermodels, written in the sealed Python grammar: each duplicate pair is one Python regime, and each ill-formed element is refused by the sealed Python step.  The across-bases witness is NOT one class in the Python grammar: the sealed Python reading regime L holds two data and no requirement, where the sealed Lean reading regime `R2L` holds the requirement between them, so the two sides have CHANGING counts zero and three as claimed but lie in two classes.  Written for the Python readings instead -- the empty history from L, and two data from the empty regime -- the two sides are one class with counts zero and two; that record was added after the miss and is not scored. | FINITE_COMPUTATION | `lean_witnesses`, `python_reading_witness`; `test_the_hypothesis_countermodels_hold_in_the_python_grammar`; `test_the_across_bases_witness_misses_in_the_python_grammar`; `test_the_python_reading_witness`; prediction P-13, MISSED |

## Stage four: the census rows this rung touches

| id | claim | class | evidence |
|---|---|---|---|
| CENSUS-recurrence | Recurrence, as an isomorphic state revisited along a history of the sealed step, decided for every history from a clean base -- well formed and duplicate-free, which the sealed empty regime and both sealed reading regimes are (`genesis_clean`, `R2L_clean`, `R2F_clean`) and which every event keeps (`clean_step`, `clean_replay`).  Across the sealed isomorphism such regimes keep their element count (`size_iso`), so a class is revisited only as a STUTTER: the regime reached is the very regime reached earlier and the events between change nothing (`recurrence_is_stutter`); after a changing event no class left is reached again (`no_return_class`).  DEFINABLE as a property of the history: it recurs exactly when it holds an unchanging event -- the direction from recurrence to unchanging events is `recurrence_is_stutter`, and the equivalence is a finite computation on the rectangle (CLS-15).  Without cleanness the element count is not carried (CLS-8), and recurrence from an unclean base is not decided here (leftover U-1).  FORCED in the seed's sense is conditional on an engine whose rounds are the changing events of the sealed step; no such engine is declared yet.  No earlier rung decided this row. | PROVED_THEOREM with COUNTERMODEL and FINITE_COMPUTATION | CLS-6 to CLS-11, CLS-15; prediction P-14, HIT |
| CENSUS-irreversibility | Added to rung five's row, which stands: for every history from a clean base, no class it left by a changing event is reached again (`no_return_class`), so irreversibility holds up to the sealed isomorphism beyond the rectangle; rung five's OPEN beyond the rectangle (its SYM-14) is closed for clean bases.  From an unclean base it is not decided (U-1).  FORCED is conditional on an engine whose rounds are the changing events of the sealed step. | PROVED_THEOREM | CLS-9, CLS-10; prediction P-14, HIT |
| CENSUS-succession | Added to rung six's row, which stands: under the CHANGING reading, the count is a function of the class of the regime reached, from the sealed empty regime and within any one clean base (`counts_of_class_genesis`, `counts_of_class`); rung six's OPEN beyond the rectangle (its SUC-17) is closed for clean bases.  Across two bases it is not a function of the class, nor of the regime (`counts_not_of_class`), and on the rectangle every one of the 86 classes reached at two bases has two counts (CLS-16).  FORCED is conditional on an engine whose rounds are the changing events of the sealed step. | PROVED_THEOREM with COUNTERMODEL and FINITE_COMPUTATION | CLS-11, CLS-12, CLS-16; prediction P-14, HIT |
| CENSUS-duration | Added to rung seven's row, which stands: the number of growths -- one less than the number of segments -- and the number of rest rounds -- the sum of the duration vector -- are functions of the class of the regime reached, from the sealed empty regime and within any one clean base (`counts_of_class`, `counts_of_class_genesis`); across two bases they are not (`counts_not_of_class`, on the CHANGING count they sum to).  The envelope is still not a class invariant (rung seven's DUR-17), and whether the multiset of envelopes of a class is stays rung seven's V-3.  FORCED is conditional on an engine whose rounds are the changing events of the sealed step. | PROVED_THEOREM with COUNTERMODEL | CLS-11, CLS-12; prediction P-14, HIT |

## Recorded

| id | claim | class | evidence |
|---|---|---|---|
| CLS-INPUTS | This rung neither reduces the count of declared inputs nor proves it at a floor; the value stays two, with no proof of a floor. | RECORDED | `receipts/class_count.json` `input_count_claim`; prediction P-15, HIT |
| CLS-PREDICTIONS | Of the frozen predictions, the five computational rows score four hits and one miss, P-13, recorded in CLS-17 and in `STATUS.md` next to its value.  P-12 is a hit on its falsifier, but the history its text gives for the class of L -- three events from EMPTY -- is the Lean reading's; in the Python rectangle that class is reached from EMPTY by two events.  The FW-DEF prediction names forty targets and scores forty hits and no miss, with one native theorem it did not name, `range_nodup`.  Six rows were labelled FORCED before the run, and a hit on a FORCED row evidences the order of the work, not insight. | PREDICTION | `receipts/class_count.json` `predictions_scored`; `test_the_scored_verdicts_are_the_dated_ones`; `test_the_prediction_is_scored_at_the_dated_values`; `test_the_unpredicted_native_declarations_are_counted` |
