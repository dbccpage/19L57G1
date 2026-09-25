# CLAIM LEDGER: rung five -- the automorphisms of a regime along a history

`AuthorityEffect: None`.  Every row carries an evidence class.  A row at
the level of a definition is marked so and is never counted as content.
Per-theorem classification is NOT this file's job: it is
`FWDEF_CENSUS.json`'s, which is total over all sixty-four theorems of
this rung's package and is checked in both directions by
`test_census.py`.  Counts in this file are dated 2026-09-25.

Classes used: DEFINITION (true by unfolding, by `rfl`, by a projection,
by one rewrite, by kernel computation over a concrete regime, or by
assembling neighbours), THIN (one genuine step, or a direct corollary of
a neighbour), PROVED_THEOREM, RECONSTRUCTION (the sealed estate's
theorem, reproduced verbatim under a pin, with no credit claimed here),
COUNTERMODEL, FINITE_COMPUTATION, OPEN, METATHEORY, PREDICTION, RECORDED.

Library axioms, recorded exactly: of the sixty-four theorems, five
depend on no axiom, twenty-four on `propext` alone, and thirty-five on
`propext` and `Quot.sound`; none depends on `Classical.choice` or on any
other axiom.  The committed log is `receipts/lean_axioms.txt`, checked
against a fresh clean build by `verify_lean.py`.

---

## The leftover this rung takes, quoted by pin

Rung four's own leftover list names this rung's question.  It is quoted
verbatim from the span pinned in `SOURCE_MANIFEST.json` as
`research/second_iso/STATUS.md` lines 185-189, and is not edited:

> - **Y-3, symmetry along a history.**  This rung decides the symmetry
>   row as definable at every regime reached.  Whether the size of the
>   automorphism group is preserved or monotone along the events of a
>   history, and at which event kinds it moves, is not measured.  Price:
>   small; the rectangle and the automorphism counts are in place.

**What this rung did with it.**  It separated WHICH automorphisms survive
an event from HOW MANY there are.  Which: proved, for every regime, at
every event kind -- a supply keeps all; a datum or a form loses none; an
instance, a rule or a requirement keeps exactly the automorphisms that
fix the element it adds, and the automorphisms after that are common to
both sides are exactly those that fix it too.  How many: computed on the
rectangle, never proved -- the size is neither preserved nor monotone,
each of the three adding kinds moves it in both directions, and the
admission of a datum or a form only ever multiplies it, by a factor the
untouched indices fix.

---

## Stage one: the reconstructions

| id | claim | class | evidence |
|---|---|---|---|
| SYM-1 | The sealed kernel slice -- regime, well-formedness, contexts, derivability, collapse, separability, the six event kinds, the step, the replay, replay compositionality, and the two sealed reading regimes -- is reproduced verbatim under a blob pin and three span pins. | RECONSTRUCTION | `lean/SecondSymmetry/Kernel.lean`; pins on `lean4/Derivation/Basic.lean` and `Inertia.lean`; `test_every_shared_declaration_is_identical` |
| SYM-2 | The sealed isomorphism structure, its identity instance, the requirement ordering and the swap of the first two data are reproduced verbatim from one sealed module under a blob pin and a span pin.  An automorphism in this rung is an instance of that structure from a regime to itself; no field is added or weakened. | RECONSTRUCTION | `lean/SecondSymmetry/IsoKernel.lean`; pins on `lean4/Derivation/Minimality.lean`; `test_every_shared_declaration_is_identical` |
| SYM-3 | Forty-one declarations are shared between the two reconstruction modules and their three pinned sources, and every one is identical after comments and namespace lines are stripped and whitespace is normalized; the omitted declarations are pinned by name and mentioned nowhere in the reconstructions. | FINITE_COMPUTATION | `test_every_shared_declaration_is_identical`; `test_the_omitted_declarations_are_recorded_not_judged` |

## Stage two: which automorphisms survive one event

| id | claim | class | evidence |
|---|---|---|---|
| SYM-4 | A supply leaves the regime, and so every automorphism, in place. | DEFINITION | `supply_keeps`; prediction K-3, HIT |
| SYM-5 | The five admitting events reach the regimes this rung names, under the sealed step's own side conditions. | DEFINITION | `stepE_inst`, `stepE_rule`, `stepE_req`, `stepE_datum`, `stepE_form` |
| SYM-6 | In the sealed grammar reconstructed here, for an instance that is well-formed and not already admitted: a pair of maps that is an automorphism before its admission and an automorphism after it FIXES the instance; an automorphism before that fixes it is, with the same maps, one after; and, for a well-formed regime before, an automorphism after that fixes it is, with the same maps, one before.  No decidability hypothesis. | PROVED_THEOREM | `inst_fixed_of_survives`, `inst_survives_of_fixed`, `inst_descends_of_fixed`, `inst_meet`, `inst_meet_after`; prediction K-1, HIT |
| SYM-7 | The same three facts for a uniform rule on an admitted form not already ruled, with fixing read as the form bijection fixing the form. | PROVED_THEOREM | `rule_fixed_of_survives`, `rule_survives_of_fixed`, `rule_descends_of_fixed`, `rule_meet`, `rule_meet_after`; prediction K-1, HIT |
| SYM-8 | The same three facts for a requirement on two admitted data in order, not already imposed, with its image re-ordered as the sealed structure orders requirements. | PROVED_THEOREM | `req_fixed_of_survives`, `req_survives_of_fixed`, `req_descends_of_fixed`, `req_meet`, `req_meet_after`; `sortPair_round`; prediction K-1, HIT |
| SYM-9 | Hence, at each of the three adding kinds, the pairs of maps common to the automorphisms before and after are exactly the fixers of the added element before, and exactly its fixers after.  This is a statement about which pairs survive and never about how many: no theorem of this package counts an automorphism set. | PROVED_THEOREM | SYM-6 to SYM-8; `test_k5_no_theorem_counts_an_automorphism_set`; prediction K-5, HIT |
| SYM-10 | Every automorphism of a well-formed regime extends, fixing the new index, to an automorphism after admitting a datum, and after admitting a form.  No automorphism is lost at either kind. | PROVED_THEOREM | `datum_lift`, `form_lift`; prediction K-2, HIT |
| SYM-11 | At each of the three adding kinds there is a regime where an automorphism is LOST and a regime where one is GAINED: two data and one form of arity one for an instance; no data and two forms of arity one for a rule; three data and no form for a requirement.  Each is closed through the fixing theorems, by exhibiting maps that move the added element. | COUNTERMODEL | `inst_loss`, `inst_gain`, `rule_loss`, `rule_gain`, `req_loss`, `req_gain`, `kinds_move_both_ways`; `test_the_lean_witnesses_replay`; prediction K-4, HIT |

## Stage three: a quantity that only grows

| id | claim | class | evidence |
|---|---|---|---|
| SYM-12 | With the element count of a regime defined as its data plus its forms plus its instances, rules and requirements, each counted as listed: every event either leaves the regime unchanged or raises the count by exactly one. | PROVED_THEOREM | `size_step`, `insertNew_cases`; prediction K-6, HIT |
| SYM-13 | The element count of the regime a history reaches from a base equals the base's count plus the number of the history's events that change the regime; so along any replayed history it never falls, and no history returns to a regime it left by a changing event. | PROVED_THEOREM | `size_counts_changes`, `size_replay_mono`, `no_return`; predictions K-6 and K-7, HIT |
| SYM-14 | That two regimes the sealed isomorphism relates have one element count is NOT proved here; no theorem statement of this package mentions both an isomorphism and the element count. | OPEN | `test_k8_no_theorem_carries_the_count_across_an_isomorphism`; prediction K-8, HIT |

## Stage four: the finite cross-check

Over rung three's rectangle, unchanged: three bases, every sequence of at
most four declared events, 577, 3928 and 14293 sequences, 18795 edges.

| id | claim | class | evidence |
|---|---|---|---|
| SYM-15 | Every node replays from its base; at every one of 2316 regimes reached, the sealed automorphism set equals a brute-force set over every bijection pair, and its size equals rung four's brute-force count.  Sizes run from one to two hundred and forty. | FINITE_COMPUTATION | `receipts/symmetry.json` `automorphisms`; `test_the_rectangle_is_rung_three_s`; predictions K-10 and K-17, HIT |
| SYM-16 | By kind, over the changing edges: a datum raises the size on 987 edges and keeps it on 359; a form raises it on 304 and keeps it on 1896; an instance raises it on 678, keeps it on 2344 and lowers it on 4476; a rule raises it on 18, keeps it on 1064 and lowers it on 132; a requirement raises it on 318, keeps it on 1384 and lowers it on 1886.  All 1376 supply edges and all 1573 other edges that change nothing keep it. | FINITE_COMPUTATION | `receipts/symmetry.json` `edges.by_kind`; `test_the_three_adding_kinds_move_both_ways`; prediction K-11, HIT |
| SYM-17 | On every one of 1346 changing datum edges the size after is the size before times one more than the count of untouched data before; on every one of 2200 form edges, times one more than the count of untouched forms of the new form's arity.  Zero violations. | FINITE_COMPUTATION | `edges.datum_law`, `edges.form_law`; `test_a_forged_datum_edge_violates_the_datum_law`; prediction K-12, HIT |
| SYM-18 | On every one of 12300 changing edges of the three adding kinds, the pairs common to the two sealed automorphism sets are exactly the fixers of the added element before and after, and the size before times the count of the element's images after equals the size after times the count of its images before.  Zero violations. | FINITE_COMPUTATION | `edges.meet_law`; `test_a_forged_adding_edge_violates_the_meet_law`; prediction K-13, HIT |
| SYM-19 | The largest ratio by which one edge raises the size is five, attained only by datum edges.  The largest ratio by which one edge lowers it is TWENTY-FOUR, attained only by instance edges -- an instance of arity two on two data of four, with two untouched forms of arity two, so that its images number twenty-four. | FINITE_COMPUTATION | `edges.largest_rise`, `edges.largest_fall`; prediction K-14, MISSED (predicted twenty) |
| SYM-20 | Of the sequences, classed by the sizes along their prefixes: at EMPTY 343 constant, 157 rising, no falling, 77 mixed; at L 498, 365, 1106, 1959; at F 135, 278, 6996, 6884.  The shortest mixed sequence has two events: from F, admit a datum, then impose a requirement. | FINITE_COMPUTATION | `sequences.classes_by_base`, `sequences.shortest_mixed`; prediction K-15, HIT |
| SYM-21 | On every changing edge the element count rises by exactly one and on every other it stays; no sequence reaches, after a changing event, a regime in the class of one an earlier prefix reached. | FINITE_COMPUTATION | `edges.element_count_violations`, `sequences.class_revisits_after_a_changing_event`; prediction K-16, HIT |
| SYM-22 | Each of the six Lean witnesses, reached from the empty regime by declared events, replays in Python with the exhibited pair on the side the Lean claims and not on the other. | FINITE_COMPUTATION | `lean_witnesses`; `test_the_lean_witnesses_replay` |

## Stage five: the census rows this rung decides

| id | claim | class | evidence |
|---|---|---|---|
| CENSUS-symmetry | Along a history, the size of the automorphism set is NEITHER preserved NOR monotone: definable at every regime (rung four), moved in both directions by each of the three adding kinds (`kinds_move_both_ways`, and the counts of SYM-16), never lowered by a datum or a form (`datum_lift`, `form_lift`), never moved by a supply (`supply_keeps`).  Whether any of this is FORCED in the seed's sense is conditional on an engine whose accepted rounds are sealed events; no such engine is declared yet. | PROVED_THEOREM with COUNTERMODEL and FINITE_COMPUTATION | SYM-4 to SYM-11, SYM-16; prediction K-18, HIT |
| CENSUS-invariant | Two quantities: the element count, which never falls and rises by exactly one at each changing event, for every history of the sealed step (`size_step`, `size_counts_changes`); and the set of fixers of the element an adding event admits, which is the same set before and after (`inst_meet`, `inst_meet_after` and their rule and requirement twins).  The NUMERIC form of the second -- the size over the count of images, kept by the event -- is a finite computation on the rectangle and is not proved.  FORCED is conditional on an engine whose accepted rounds are sealed events. | PROVED_THEOREM with FINITE_COMPUTATION | SYM-9, SYM-12, SYM-13, SYM-18; prediction K-18, HIT |
| CENSUS-irreversibility | No history returns to a REGIME it left by a changing event (`no_return`), proved for every history.  No sequence of the rectangle returns to a CLASS it left; beyond the rectangle that is OPEN, because the element count is not proved invariant under the isomorphism (SYM-14).  FORCED is conditional on an engine whose accepted rounds are sealed events. | PROVED_THEOREM with FINITE_COMPUTATION and OPEN | SYM-13, SYM-14, SYM-21; prediction K-18, HIT |

## Recorded

| id | claim | class | evidence |
|---|---|---|---|
| SYM-INPUTS | This rung neither reduces the count of declared inputs nor proves it at a floor; the value stays two, with no proof of a floor. | RECORDED | `receipts/symmetry.json` `input_count_claim`; prediction K-19, HIT |
| SYM-SUCCESSION | By SYM-13, the element count of a regime minus its base's count is the number of changing events of any history reaching it from that base.  This reads the number of CHANGING rounds off the state and the base; supplies and repeated admissions are invisible to it.  Whether this decides the census row for succession is not claimed here; the row stays as rung four left it. | RECORDED | `size_counts_changes` |
| SYM-PREDICTIONS | Of the frozen predictions, the nine computational rows score eight hits and one miss (K-14); the FW-DEF prediction names thirty-five targets and scores twenty-seven hits and eight misses, every miss a demotion, with twelve native theorems it did not name. | PREDICTION | `receipts/symmetry.json` `predictions_scored`; `test_the_prediction_is_scored_at_the_dated_values` |
