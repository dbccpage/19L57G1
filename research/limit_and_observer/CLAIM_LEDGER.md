# research/limit_and_observer — claim ledger

One row per claim: statement, status, dependencies, assumptions, Python
evidence, Lean theorem, axiom report, falsifier, surviving boundary.

**Evidence labels.** **CHECKED** means confirmed in the gated
`artifacts/lean_axioms.txt`. **CITED** means read from a pinned source, or a
research tree's manual receipt read by no gate. This tree's own Lean receipt
is CITED, never CHECKED: no CI gate runs this package's `verify_lean.py`.

AuthorityEffect: None.

---

## LO-01 — The sealed observation discards admission variation where covered

**Statement.** `derivable(r, inst) = inst[0] in r.rules or inst in r.insts` is
an *or* of a coverage bit, which does not depend on the datum plugged in, and
an admission bit, which does. At a fixed covered context the projected value
is constant despite variation in admission; at an uncovered context it reads
admission. The admitted state and its admission events retain the ingredients
separately. The projection's information loss is not evidence that these
state components or events were conflated, or that the discipline was broken.

**Status.** derived definition (a reading of a pinned source). Not a theorem.

**Dependencies.** `code/derivation/observe.py`, pinned at blob sha256
`78443d67…`, at **line 52**. Four files of this tree said line 56, which is
`profile`; the quoted body was always right, the blob pin always verified, and
only the anchor was wrong. `REQUIREMENTS.md` is frozen and its copy of the
wrong anchor stands, with the correction recorded in `STATUS.md`.

**Assumptions.** None beyond the pin.

**Python evidence.** `code/grammar.py` `coverage_bit`, `admission_bit`,
`sealed_derivable`; `tests/test_kernel_agreement.py`
`test_derivable_agrees_on_every_plugging`, which checks the re-implementation
against the sealed original at every plugging of every state of the
population.

**Lean.** `LimitObserver.sealed_is_blind_where_covered`,
`sealed_reads_admission_where_uncovered`.

**Axiom report.** Both axiom-free. CITED.

**Falsifier.** A context at which the sealed relation separates two data whose
coverage bit is present.

**Boundary.** This is a statement about the sealed *function*, not about the
paper's prose or about any intent. It does not establish that no other
repository interface reads the ingredients apart. The alternative reader
priced here is declared, not supplied by this projection alone.

---

## LO-02 — The reading axis has exactly four induced-separation behaviours

**Statement.** The sixteen readings of the bit pair collapse to eight
complement classes, seven of them non-constant, and — more sharply — to
exactly **four** induced-separation behaviours, because the coverage bit is
constant across data at a fixed context.

**Status.** proved theorem (the collapse) plus deterministic computation (the
counts).

**Dependencies.** LO-01.

**Assumptions.** None.

**Python evidence.** `code/census.py` `reading_axis_census`;
`tests/test_readers.py` `test_exactly_four_induced_separation_behaviours` and
`test_same_behaviour_gives_the_same_relation_at_every_state`, the latter over
the whole population.

**Lean.** `LimitObserver.behaviour_determines_separation`,
`separatesAt_eq_readsAt`.

**Axiom report.** `behaviour_determines_separation: [propext]`;
`separatesAt_eq_readsAt: [propext]`. CITED.  The second had **no** report
until the hand-written report list was replaced by a census read out of the
compiled environment; the list's own header claimed to cover every exported
theorem and did not.

**Falsifier.** Two readings with the same behaviour inducing different
relations at some state; or a fifth behaviour.

**Boundary.** The collapse is about the *induced relation*. The canonical key
of a stated state is deliberately finer than the induced relation, and both
counts are reported. The key retains the frozen complement class. The former
behavior-keyed implementation did not preserve OBS-4's full-reader transport
predicate and is withdrawn; `test_equal_behaviour_does_not_erase_the_frozen_reader_class`
records its concrete counterexample.

---

## LO-03 — The sealed observer is a point of this tree's reader space

**Statement.** The sealed observation relation is exactly the reader whose
selection is every context, whose behaviour reads the admission bit only where
coverage is absent, and whose aggregation is "at least one separating
context".

**Status.** deterministic computation, exhaustive over the declared
population.

**Dependencies.** LO-01, LO-02.

**Assumptions.** The population is the quotiented depth-3 population.

**Python evidence.** `code/census.py` `sealed_is_a_reader`: 85 states checked,
**0** mismatches. `tests/test_readers.py`
`test_sealed_relation_equals_the_full_uncovered_reader`.

**Lean.** `LimitObserver.sealed_behaviour` (the behaviour identity).

**Axiom report.** Axiom-free. CITED.

**Falsifier.** One state at which the two relations differ.

**Boundary.** Checked over the population, not proved for every regime. The
Lean theorem covers the behaviour, not the full-selection identity.

---

## LO-04 — The reader is admitted one item at a time

**Statement.** `NewReader` admits a reader with an **empty** selection and
`AddContext` adds exactly one context, so a reader's width equals the items
spent on it and `mu1` counts observational capacity correctly with no
redefinition of the sealed measure.

**Status.** admitted primitive (the two item kinds) plus deterministic
computation (the enforcement).

**Dependencies.** None.

**Assumptions.** `w_max = 3`, `max_readers = 2`, both declared and refused
rather than exceeded.

**Python evidence.** `code/items.py` `apply_delta`; `tests/test_guards.py`
`test_new_reader_admits_an_empty_selection`,
`test_a_readers_width_equals_the_items_spent_on_it`,
`test_width_beyond_the_bound_is_refused`,
`test_more_readers_than_the_bound_is_refused`.

**Lean.** None; this is a property of the item alphabet, not of `Bool`.

**Axiom report.** Not applicable.

**Falsifier.** A candidate whose reader has more contexts than the delta has
`AddContext` items.

**Boundary.** Were `NewReader` to carry its selection, a candidate would buy
unbounded observational capacity at unit price and every number on both sides
of the comparison would be wrong by an unbounded amount.

---

## LO-05 — Lawfulness is a decided precondition, and is not stable in the width

**Statement.** An admitted reader must be lawful in general, and exactly 4 of
the 8 aggregations with `a(0) = false` are lawful at width 3. The count is
width-dependent: 2 of 2 at width 1, 3 of 4 at width 2, 4 of 8 at width 3, 4 of
16 at width 4. Unlawful aggregations are counted and refused by name.

**Status.** deterministic computation.

**Dependencies.** None.

**Assumptions.** Lawfulness means transitivity of the induced non-separation
relation over the whole of `{0,1}^w`, not merely at one state.

**Python evidence.** `code/readers.py` `lawful`, `lawful_aggregations`,
`unlawful_aggregations`; `tests/test_guards.py`
`test_exactly_four_of_eight_are_lawful_at_width_three`,
`test_lawfulness_is_not_stable_in_the_width`,
`test_only_lawful_aggregations_are_offered_for_admission`.

**Lean.** None.

**Axiom report.** Not applicable.

**Falsifier.** A different lawful count at any width; or an unlawful
aggregation reaching admission.

**Boundary.** `DiffObs` carries its equivalence laws as fields, which is why
lawfulness is a precondition here rather than an assumption. Nothing is
claimed above width 4.

---

## LO-06 — Three sealed items are needed and enough to reach a rival-admitting state

**Statement.** The minimum number of sealed items reaching a state that admits
a raw-bit rival is exactly **3**, in both readings, with none at one or two
items. Every minimum prefix is a form, a uniform rule on it, and an explicit
instance: 6 raw minima in 3 isomorphism classes in reading L, 12 raw in 3
classes in reading F.

**Status.** deterministic computation, exhaustive within the declared bound.

**Dependencies.** LO-01.

**Assumptions.** The sealed `Bounds(2, 2)` item alphabet.

**Python evidence.** `run_price.py` `minimum_rival_prefix_census`, which
computes the raw counts **and** the isomorphism class counts into
`receipts/price.json` under `censuses.minimum_rival_prefix`; `code/census.py`
`admits_rival`; `tests/test_census.py`
`test_every_rival_state_has_the_forced_shape`.

The class counts were quoted in this row while being computed nowhere, and
P-14 — whose frozen text asserts them — was scored on the shape alone. Both
counts are now computed and both enter the score; the computed values are the
ones quoted above.

**Lean.** `LimitObserver.rival_separates_where_sealed_identifies` exhibits the
rival at a covered context; it does not prove the minimality of 3.

**Axiom report.** Axiom-free. CITED.

**Falsifier.** A rival-admitting state at one or two sealed items; or a
minimum prefix of another shape.

**Boundary.** The minimality of 3 is a bounded computation over the declared
alphabet, not a theorem over every item grammar. It is what licenses widening
above the sealed two-item bound.

---

## LO-07 — The second observer costs 5

**Statement.** OBS-3, an admitted reader separating a pair the sealed observer
identifies, has minimum `mu1 = 5` at both sealed genesis bases: three sealed
items, one `NewReader`, one `AddContext`. Outcome **PRICE**.

**Status.** deterministic computation at fully completed successful/lower levels,
with `cost_below_minimum_all_fail` decided by exhaustion — computed by
`code/price.py` `below_minimum_exhausted` from the item counts the walk
exhausted. It was a hard-coded `True` in both branches of the assembly,
correct only by the accident that the walk ascends and unfalsifiable by any
test; the value is unchanged and the way it is reached is not.

**Dependencies.** LO-01, LO-04, LO-06.

**Assumptions.** `max_items = 8`, sealed prefix at most 4, reader suffix at
most 4, `max_arity = 2`, `w_max = 3`, `max_readers = 2`, population depth 3.

**Python evidence.** `receipts/price.json` under `prices`, keys
`OBS-3|L|mu1`, `OBS-3|F|mu1`, `OBS-3|L|mu2`, `OBS-3|F|mu2`.

**Lean.** None. The price is a computation and is reported as one.

**Axiom report.** Not applicable.

**Falsifier.** Any candidate answering OBS-3 at four items or fewer.

**Boundary.** Depth 3 only; a rival appears at 6 of the 85 states. Depth 4 is
OPEN. The reported class count is the canonical-key count; the number of
distinct induced relations bought is reported separately and is smaller.

---

## LO-08 — The degenerate answer is cheaper, and the ladder prices it

**Statement.** OBS-1 and OBS-2 are both answered at `mu1 = 3` by a blind
reader. OBS-4, which requires two readers each separating something and
disagreeing at the designated pair with neither a renaming of the other, costs
strictly more, and the two readings differ: **7 in reading L, 6 in reading F**.

**Status.** deterministic computation.

**Dependencies.** LO-04, LO-07.

**Assumptions.** As LO-07.

**Python evidence.** `receipts/price.json`, keys `OBS-1|*`, `OBS-2|*`,
`OBS-4|*`; `tests/test_guards.py` `test_obs4_refuses_a_renaming`,
`test_obs4_refuses_a_reader_that_separates_nothing`.

**Lean.** None.

**Axiom report.** Not applicable.

**Falsifier.** OBS-1 or OBS-2 above 3; OBS-4 at or below OBS-3; equal OBS-4
values across the readings.

**Boundary.** `PREDICTIONS.md` P-16 predicted 8 and 7 for OBS-4 and is
**refuted on those values** by this row. The prediction is not edited; the
miss is recorded in `STATUS.md` with its cause.

---

## LO-09 — Refinement without end is obstructed at the carrier

**Statement.** A lawful reader's induced partition has at least one block and
at most `n_data` blocks. For a **monotone** aggregation adding a context never
lowers the block count, so a chain of strict splits has length at most
`n_data - 1`. A chain longer than the carrier exists at no state of the
declared population, under no reading and no lawful aggregation. Outcome
**PROVED OBSTRUCTION** for the monotone aggregations; **bounded computation**
for the other two.

**Status.** proved theorem (monotone aggregations) plus deterministic
computation (the remaining two, over the declared population).

**Dependencies.** LO-05 (an unlawful aggregation induces no partition, so no
block count is defined for it).

**Assumptions.** The carrier is the admitted data. The demand's threshold is
stated relative to the carrier, by declaration.

**Python evidence.** `code/census.py` `chain_census`: ceiling **attained at 26
states**, **0** chains above it. `tests/test_obstructions.py`
`test_no_chain_exceeds_the_carrier_minus_one`,
`test_the_demand_is_unsatisfiable_at_every_state`,
`test_the_positive_control_the_ceiling_is_attained`.

**Lean.** `LimitObserver.chain_bounded`,
`LimitObserver.refinement_demand_unsatisfiable`, `LimitObserver.strict_ge`,
`LimitObserver.chain_bound_has_an_instance`.

**Axiom report.** `chain_bounded: [Quot.sound, propext]`;
`refinement_demand_unsatisfiable: [Quot.sound, propext]`;
`strict_ge: [Quot.sound, propext]`;
`chain_bound_has_an_instance: [Quot.sound, propext]`. CITED.

**Falsifier.** A lawful reader chain strictly longer than `n_data - 1` at any
state.

**Boundary, and a narrowing this row makes to its own first statement.** This
row first claimed that every strict split raises the block count for every
lawful reader. **That is false and this tree's own test caught it.** Exactly
2 of the 4 lawful aggregations at width 3 are block-count monotone; under the
parity aggregation the block count can **fall** when a context is added.
`tests/test_obstructions.py`
`test_a_non_monotone_aggregation_can_lower_the_block_count` carries the
countermodel, and `code/readers.py` `monotone_aggregations` decides the split.

Consequently the Lean theorem — which is about any block count that rises
strictly along the chain and is bounded by the carrier up to the chain's
length — applies through its hypothesis only to the monotone aggregations. For
the other two the bound is checked exhaustively
over the declared population (`test_the_chain_bound_still_holds_for_every_lawful_aggregation`,
0 chains above the ceiling) and is reported as a computation, not a theorem.
The positive control is what makes either half an obstruction rather than a
demand nothing finite could meet.

**A second narrowing, to the Lean statement itself.** `chain_bounded` first
asked strictness at *every* index while also bounding the block count at
*every* index. Those hypotheses are jointly unsatisfiable, so the theorem and
its two corollaries were **vacuous** and no chain instantiated them; the chain
length appeared in no hypothesis at all. That form is **WITHDRAWN**. The
hypotheses are now bounded by the chain — strictness below the chain's length,
boundedness up to it — and `chain_bound_has_an_instance` exhibits an instance
meeting all three. The axiom report could not have caught the vacuity, because
it says which axioms a proof used and never whether its hypotheses can be met;
that is the residual this row now carries rather than assumes away.

**The reach of the enumeration, separately from the proof.** A chain longer
than the carrier needs a width above the carrier, so at `w_max = 3` the width
bound alone leaves the demand open at **24** of the 85 states and closes it at
the other 61. At those 24 the chain census tests the reader obstruction;
at the rest the width alone rules out the demand. That population census is
separate from the one-step price search: L completes, while F is refused.
The proof and the chain census cover all 85; this is not a complete F price census, and
`receipts/price.json` records the count under
`obstructions.LIM-R.reach_of_the_declared_space`.

---

## LO-10 — No finite delta over the six item kinds lifts LO-09

**Statement.** The demand's threshold is carrier-relative and the ceiling
tracks the carrier exactly, so admitting data raises both together. No finite
delta over the declared alphabet lifts the refinement obstruction, under
LO-09's chain hypotheses. Any escape must leave that declared contract.
No sufficient extension or smallest lifting item has been constructed.

**Status.** conditional proved theorem; extension feasibility and minimality OPEN.

**Dependencies.** LO-09.

**Assumptions.** As LO-09.

**Python evidence.** `tests/test_obstructions.py`
`test_growth_does_not_lift_it`, which checks up to **two** growth items on one
exhibited regime; `code/census.py` `chain_census`, which checks the bound at
every carrier the population reaches (2 to 6); `receipts/price.json` under
`obstructions.LIM-R.escape`, where `price_in_items` is `null` and
`liftable_by_a_finite_delta_over_the_six_kinds` is computed from the census
and the enumeration rather than written as a literal; it is null when the
full finite search is refused. The conditional Lean statement is separate.

**Lean.** `LimitObserver.refinement_obstruction_survives_growth`.

**Axiom report.** `[Quot.sound, propext]`. CITED.

**Falsifier.** A delta over the six kinds after which LIM-R is satisfiable.

**Boundary.** Neither a price nor a smallest extension is established. The
former 'smallest seventh item kind' wording is withdrawn. The frozen P-10
remains unchanged; its finite-delta clause and untested extension clause are
recorded separately in the receipt.

**Boundary, and what "any number of them" rests on.** The Lean theorem is what
covers *any* number of growth items, and it carried the vacuous hypotheses
withdrawn in LO-09 until they were bounded by the chain; before that repair
this row's "proved theorem" status had no instance behind it. The Python
evidence is narrower than the theorem and is reported as such above: two
growth items on one regime, plus the census over carriers 2 to 6. Neither is a
check at every number of growth items, and neither is presented as one.

---

## LO-11 — Growth without end is obstructed at a derived width threshold

**Statement.** Two data with equal signatures have a separating count of zero,
and `a(0)` is false for every admitted aggregation, so the non-separation
relation of any fixed-selection reader of width `w` is coarser than signature
equality and has at most `2 ** w` blocks. Once the carrier exceeds `2 ** w`
some pair is identified, for every selection, behaviour and lawful
aggregation. The threshold `2 ** w_max = 8` is derived from the width and does
not depend on the carrier. This capacity evidence is separate from the full
search result, now **OPEN: CandidateBudgetRefused**.

**Status.** proved theorem for growth by uninstantiated data (Lean); the
sharper `2 ** w` threshold is a deterministic computation, exhaustive at
widths 1 to 3, with the Lean obligation **OPEN**.

**Dependencies.** LO-04, LO-05.

**Assumptions.** The reader's selection is fixed at stage 0, asserted
structurally on the delta.

**Python evidence.** `code/census.py` `capacity_census`;
`tests/test_obstructions.py` `test_equal_signatures_are_never_separated`,
`test_blocks_never_exceed_two_to_the_width`,
`test_a_carrier_above_the_threshold_identifies_some_pair` (an exhibited
carrier of 9 with every fixed reader failing),
`test_the_positive_control_a_separating_reader_exists_below_it`.

**Lean.** `LimitObserver.fresh_data_are_never_separated`,
`LimitObserver.growth_defeats_every_reader`, `LimitObserver.diffCount_self`.

**Axiom report.** All three `[Quot.sound, propext]`. CITED.

**Falsifier.** A fixed-selection admitted reader separating every pair at a
carrier larger than `2 ** w`.

**Boundary, stated exactly.** **Lean proves the obstruction only for growth by
data carrying no instance**, with an explicit witness and no counting. The
`2 ** w` threshold, which holds even when growth carries content, needs a
pigeonhole over signatures that core Lean without Mathlib does not supply. It
is **checked in Python and recorded OPEN in Lean**, and is not claimed as a
theorem.

**Boundary, and what the empty price row does NOT show.** The demand needs a
carrier above `2 ** w_max = 8`. `max_sealed_items` is 4 and the genesis
carriers are 2 and 3, so the largest carrier any candidate in the declared
space reaches is **6** in reading L and **7** in reading F: every LIM-G
candidate is rejected at the carrier test before a reader property is
examined. The completed L empty minimum set and its exhaustion flag carry
**no information about readers**. F's refused search has no certified empty
minimum set or exhaustion pass; the carrier bound does not complete its
enumeration. This row's evidence is the signature argument, `capacity_census`,
and a carrier-9 exhibit built from **eight** sealed items — outside the
declared space, named as such in `receipts/price.json` under
`obstructions.LIM-G.positive_control.carrier_above_the_threshold_exhibited_out_of_space`,
and metatheory that is never admitted. It is **not** the enumeration.
Pricing LIM-G inside a space that reaches its threshold is OPEN.

---

## LO-12 — Necessary width is not a priced escape

**Statement.** A reader needs at least `ceil(log2(n))` contexts for full
separation, but that condition is not sufficient. With no explicit instances,
all admission signatures coincide and additional contexts separate nothing.
The previously asserted one-item escape is withdrawn. Its minimum price is OPEN.

**Status.** countermodel to the width-only escape; open minimum escape price.

**Dependencies.** LO-11.

**Assumptions.** As LO-11.

**Python evidence.** `receipts/price.json` under
`obstructions.LIM-G.escape`, where both price fields are `null`, and
`width_only_countermodel`; `tests/test_review_guards.py`
`test_more_width_cannot_repair_equal_raw_signatures`.

**Lean.** None.

**Axiom report.** Not applicable.

**Falsifier.** A selection separating data whose raw signatures agree everywhere.

**Boundary.** The necessary width bound is not a construction, a sufficient
rate, or evidence of a minimum purchase.

---

## LO-13 — The family-determined verdict is obstructed within the grammar

**Statement.** No item of the declared alphabet carries a stage index, an
earlier regime, or its own earlier verdict, so every admitted reader's stage
verdict is a function of that stage's regime alone. A novel family verdict
differs from every stage verdict and so is the value of no stage-local reader.
The full search result is **OPEN: CandidateBudgetRefused**; the family
controls and stage-locality evidence are retained separately.

**Status.** proved theorem (that novelty forces a constant sequence) plus
deterministic computation (the exhaustiveness check over the alphabet).

**Dependencies.** LO-04.

**Assumptions.** The verdict is two-valued. `H = 15`, window start 12.

**Python evidence.** `code/demands.py` `reads_only_the_stage`;
`tests/test_obstructions.py` `test_no_admitted_item_reads_beyond_its_stage`,
`test_the_demand_is_unsatisfiable`, `test_the_positive_control_passes`,
`test_novelty_is_satisfiable_exactly_on_a_constant_sequence`.

**Lean.** `LimitObserver.novel_forces_constant`,
`LimitObserver.no_novel_verdict_on_a_mixed_sequence`,
`LimitObserver.stage_local_verdict_is_not_novel`.

**Axiom report.** First two `[propext]`, third axiom-free. CITED.

**Falsifier.** An admitted delta whose reader passes both the stability and
the novelty test; or an item sequence producing a reader whose stage verdict
reads the stage index, an earlier regime, or its own earlier verdict.

**Boundary, stated exactly.** **The implication that stage-local readers
agreeing at every stage have equal family verdicts is DEFINITION-LEVEL** and
carries no content by itself. The content is the exhaustiveness check, which
is a real property of the enumeration and fails the moment an item kind grows
a field. The positive control is metatheory and is never admitted.

---

## LO-14 — Different obstruction bounds, open escape comparison

**Statement.** Refinement's ceiling tracks the carrier; growth's signature
ceiling tracks width. The complete minimum censuses remain uncomputed after
the resource refusal; they are not certified empty sets.
P-12's stronger claim that width alone supplies an escape is refuted. No
comparison of minimum escape prices has been established.

**Status.** deterministic computation over the two obstruction records.

**Dependencies.** LO-09, LO-10, LO-11, LO-12.

**Assumptions.** As those rows.

**Python evidence.** `run_price.py` `score_predictions` P-12;
`receipts/price.json` under `obstructions`.

**Lean.** None; the sharper growth threshold remains an OPEN Lean obligation.

**Axiom report.** Not applicable.

**Falsifier.** A reader separating the equal-raw-signature countermodel by
adding selected contexts alone.

**Boundary.** Different bounds do not imply different computed prices.

---

## LO-15 — The decisive price comparison remains OPEN

**Statement.** The observer has a completed price certificate. The refused
limit searches do not establish complete empty minima, so the former
'decisively cheaper' comparison is withdrawn. Independent conditional
theorems and bounded censuses are recorded under their own scopes.

**Status.** OPEN for the full comparison; completed observer prices retained.

**Dependencies.** LO-07, LO-09, LO-11, LO-13.

**Assumptions.** As those rows.

**Python evidence.** `receipts/price.json` under `comparison.table`.

**Lean.** None.

**Axiom report.** Not applicable.

**Falsifier.** Any limit direction returning a finite one-step price; or
OBS-3 returning an obstruction.

**Boundary.** `mu1` counts items. "The rival costs 5" is a statement about how
many admitted items it requires and nothing else — not difficulty, not
importance, not order of payment.

---

## LO-16 — Direct purchase checks retained; minimum-set comparisons OPEN

**Statement.** For the completed observer minima, direct predicate checks show
**no observer demand purchases a limit demand**: 30 purchase rows, none true,
and 15 containment rows were executed for completed L observer/limit pairs.
F's corresponding 15 pairs are omitted as OPEN. Missing
minimum sets are unknown, not empty. Joint-minimality pairs involving a
refused minimum census are also omitted, not answered negatively.

**What was not run.** A refused limit search supplies no certified minimum to
feed the other predicate or complete key set to compare, so `comparison.purchase` holds **no** row
with a limit demand as the first and
`comparison.containment_of_canonical_key_sets` holds **no** limit-against-limit
row. "The reverse" therefore names a test that produced nothing, not a test
that returned false. An earlier version of this row said "or the reverse"
without that qualification, and `FINDINGS.md` went further and asserted
"refinement purchases growth" as a holding containment; both are corrected
here, and the receipt records
`P-18-refinement-purchases-growth-UNTESTED` as false.

**Status.** deterministic computation.

**Dependencies.** LO-07, LO-09, LO-11, LO-13.

**Assumptions.** The declared combination set and the declared evidence-arity
labels.

**Python evidence.** `code/price.py` `satisfies_at`; `receipts/price.json`
under `comparison.purchase`, `comparison.containment_of_canonical_key_sets`
and `comparison.joint_minimality`.

**Lean.** None.

**Axiom report.** Not applicable.

**Falsifier.** Any purchase test returning true in an unexpected direction; or
a delta jointly minimal across evidence arities.

**Boundary.** Equality of `mu1` is **never** taken as evidence of purchase,
containment or joint minimality. Each is decided by running the test — and
where there was nothing to run, that is reported instead of an answer.

---

## LO-17 — The rival is inside, and is not the reader the estate's open bridge names

**Statement.** The rival's relation is a total function of the admitted
regime; it costs no oracle and reads strictly less than the sealed observer
already computes. It is therefore not an outside reader, and the estate's
named irreducible obligation is inherited unchanged.

**Whether it is *derived* is not uniform.** At the minimum rival state of
reading L (carrier 2) the rival's relation is the complement of the sealed
relation and the rival is **DERIVED**. At the minimum rival state of reading F
(carrier 3) it is outside the declared combination set entirely and the rival
is **ADMITTED**.

**Status.** deterministic computation (OBS-5, per state) plus an inherited
open obligation.

**Dependencies.** LO-01, LO-07.

**Assumptions.** The declared seven-element combination set.

**Python evidence.** `code/demands.py` `obs5_derivability`,
`combination_values`; `code/census.py` `rival_derivability_census`;
`tests/test_census.py`
`test_derived_at_two_data_admitted_at_three`; `receipts/price.json` under
`censuses.rival_derivability` and keys `OBS-5|*`.

**Lean.** None.

**Axiom report.** Not applicable.

**Falsifier.** The verdict changing at either exhibited state.

**What this row does NOT claim.** That the admitted verdict at three data
makes the rival an *outside* reader. It does not: its relation is a function
of the admitted regime and it reads only through the judgment grammar. The
admitted verdict says it is not reachable from the sealed relation by one
application of the declared operations, which is a statement about the
declared operations.

**Boundary, and a narrowing of an inherited premise.** The estate does **not**
hold a theorem that the system is not self-certifying. It holds that
certification is panel-relative (`cert_not_correspondence`,
`cert_panel_relative`, both CHECKED in `artifacts/lean_axioms.txt`), an
explicit refusal to define a self-evaluation interface, and the named
irreducible obligation in `OPEN_BRIDGES`. This tree inherits that as an
**open obligation** and does not discharge it.

---

## LO-18 — The calibration gates every other receipt

**Statement.** Restricting this tree's space to the four sealed item kinds
with no readers, and running this tree's own pricing routine with the sealed
separation demand at the two sealed bases, reproduces
`artifacts/challenges.json` `challenge3` field by field.

**Status.** deterministic computation.

**Dependencies.** Every kernel row.

**Assumptions.** The sealed artifact at its pinned blob sha256
`d5ddc3f8…`.

**Python evidence.** `code/calibration.py` `calibration_report`;
`tests/test_kernel_agreement.py`
`test_calibration_reproduces_the_sealed_answer` and
`test_transcribed_sealed_answer_matches_the_pinned_artifact`, the second of
which checks the transcription against the committed artifact so it cannot
drift into a convenient number.

**Lean.** None.

**Axiom report.** Not applicable.

**Falsifier.** Any field differing from the committed sealed artifact.

**Boundary.** A failure here **voids the tree**: this tree re-implements the
sealed kernel rather than importing it, and agreement here is the only thing
standing between a re-implementation and a lookalike.
