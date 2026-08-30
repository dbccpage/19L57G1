# P1 -- S9.1, the axiom lattice (PROMPT.md steps 5-12; step 13 proposed)

AuthorityEffect: None.  This part proposes; it amends nothing sealed.
Every result in sections 0-12 is finite computation over carriers 1..4,
bounded by N = 4, and no Lean theorem carried any of it as of the Python
part (`LEAN_NOT_CARRIED` there).  The carrier-general statements the sweep
suggests are proposed under "Lean targets" (section 8) for the Lean stage.
Section 13, added by the Lean stage, records which targets are proved,
under which theorem names, and which cells they carry; the terminals of
section 7 are updated there, and the residuals it leaves are named there.
Sections 0-12 are the state after repair round 2; sections 11 and 12
record what the reviewers found in each round and what changed.

Governing prompt: `research/s9_obligations/PROMPT.md`, Git blob
`1642e3f6ac746002678e4997f738e0fabd1248c9`; snapshot commit
`db1d2b225b577d5212780ff02700efd693c8e446` (receipt key `header`).

S9.1 is the first bullet of section S9 of `paper/primitive_difference.md`;
the numbering is the prompt's, not the paper's (receipt key
`numbering_note`).

Receipt: `research/s9_obligations/receipts/axiom_lattice.json`, written by
`run_axiom_lattice.py`, SHA-256
`23f4c1b8547139dd1414a18b94ceba2ab473f4d90714f5b51fdec14d4741a363`
(445282 bytes, ASCII, LF; key `revision` names the repair rounds, the
last being the repair after full-run audit 1, section 14).  Every
number in this document is a value under the receipt key named beside it;
dotted keys are paths from the receipt root, `sweeps.N4.fragments.<F>`
abbreviated to `F.` where `F` is one of `PURE`, `EQ_BEARING`,
`MERGED_PURE_AND_EQ_BEARING`.

## 0. Declarations, fixed before anything was enumerated

These were written into `axiom_lattice.py` (module docstring and the
`DECLARED_BOUNDS`, `TRANSFER_*`, `ORDER_DECLARATION` constants) before the
first relation was enumerated; the receipt copies them.  Two of them were
revised in repair round 1 and are marked so; the original wording is
quoted in section 11 so the record of what was written first survives.

**Step 5, the axiom space** (key `axiom_space.declaration`).  Universally
quantified Horn clauses over one binary relation `r` in at most two
variables `x`, `y`.  Atoms `r x x`, `r x y`, `r y x`, `r y y`.  Head one
atom or falsum; body any subset of the atoms.  An axiom is a finite set of
clauses; its extent is the intersection of its clauses' extents.  Raw count
by arithmetic: 5 heads times 16 bodies = 80 (key
`declared_bounds.raw_clause_count_arithmetic`).  Clauses are quotiented by
the swap `x <-> y`; both counts are printed and both are in the receipt.
Head-in-body clauses (trivially valid) are KEPT in the enumeration and
counted, and DROPPED from the generating set, because their extent is the
top of the lattice, which is present anyway as the extent of the empty
axiom (key `axiom_space.PURE.head_in_body_policy`).  The count used
downstream is the number of non-trivial swap orbits (key
`axiom_space.PURE.used_downstream`).  *Revised in round 1:* a clause is
ONE-VARIABLE when the atoms it mentions, in body and head together, use at
most one of `x`, `y` (`-> falsum` mentions none and is counted among
them); `x = y` mentions both, so no EQ_BEARING clause is one-variable; the
raw count and the swap-orbit count are both reported and neither is used
downstream (key `axiom_space.one_variable_meaning`).

**Step 6, the EQ_BEARING fragment** (keys `eq_fragment`,
`axiom_space.EQ_BEARING`).  A fifth atom `x = y`, the metatheory's own
identity -- A3's bill per S1, not A1's.  A clause mentioning it in body or
head is EQ_BEARING; the fragment is enumerated separately under the same
bounds, gets its own lattice and transfer analysis, and is never merged
into the pure fragment's results except in the one object labelled
`MERGED_PURE_AND_EQ_BEARING`, which carries the sentence: *This object
MERGES the pure fragment's generators with the EQ_BEARING fragment's
generators; every count in it mixes A1's bill with A3's identity atom and
must be cited with this sentence* (key `MERGED_PURE_AND_EQ_BEARING.merge_sentence`).
Every terminal string of a merged cell now carries the same clause in the
same sentence (keys `terminals.transfer.MERGED_PURE_AND_EQ_BEARING.*`,
`terminals.f3.MERGED_PURE_AND_EQ_BEARING.*`).

**Step 7, soundness transfer, two definitions** (key
`transfer_definitions`), each displayed in one line:

    TRANSFER_ALL_CARRIERS:  phi transfers iff for every pointed structure
    (X, r, a, b) with |X| in 1..N, r a b and phi(r), the metatheory has
    a != b.

    TRANSFER_ABOVE_POINT:   phi transfers iff for every pointed structure
    (X, r, a, b) with |X| in 2..N, r a b and phi(r), the metatheory has
    a != b.

"phi entails irreflexivity" is fixed once, independently of either
definition (key `entails_irreflexivity`): every relation in ext(phi), over
carriers 1..N, is irreflexive, i.e. ext(phi) is contained in the extent of
`r x x -> falsum`.

*Can F3 fail under the default?*  Written before computing.  Under my
encoding, "phi transfers" under `TRANSFER_ALL_CARRIERS` unfolds to: no
relation in ext(phi) has a point `a` with `r a a`.  That is the same
statement as "ext(phi) is contained in the extent of `r x x -> falsum`",
which is the fixed meaning of "entails irreflexivity".  So the step-11 set
-- axioms that transfer but do not entail irreflexivity -- is empty by
construction under the default, the conjecture cannot fail, and the
default alone would be `F3_UNTESTED` (step 38).  Therefore a second
definition is named and computed side by side: `TRANSFER_ABOVE_POINT`.
Why this one: S7 lists two consequences of irreflexivity separately --
metatheoretic distinctness (`irrefl_witness_ne`) and the forced
two-element carrier (`no_witness_on_subsingleton`) -- and this definition
asks for the first without the second.  It is a weaker notion of soundness
than the paper's, because it discounts the one-point self-difference of
`selfdiff_consistent`; that caveat travels with every result computed under
it (key `transfer_definitions.TRANSFER_ABOVE_POINT.why`).

*Revised in round 1 -- what the second definition decides before the
sweep.*  Under EITHER definition "phi transfers" is a containment
`ext(phi) <= W` in one fixed extent W.  Under `TRANSFER_ALL_CARRIERS`, W is
irreflexivity's extent.  Under `TRANSFER_ABOVE_POINT`, W is the extent of
`r x x -> x = y`, which exceeds irreflexivity's extent by the one-point full
relation alone (key `F.transfer.TRANSFER_ABOVE_POINT.transfer_as_containment.W_minus_irreflexivity_extent`).
So the step-11 set under the second definition is decided by argument in
every fragment before anything is swept: it is NONEMPTY wherever the
lattice realizes an extent between the one-point full relation and W --
in the EQ_BEARING fragment `r x x -> x = y` is itself a generator, so its
extent is a member -- and it is EMPTY in the pure fragment, because no pure
clause separates the one-point full relation from the two-point full
relation (their realized `r`-atom patterns coincide), so every pure extent
admitting the former admits the latter and fails above the point -- that
lemma is checked at N = 4 and bounded by it, and its general form is Lean
target T7, not proved.  The sweep confirms both at N = 4 and lists the
members; it discovers neither.
The receipt carries the argument per cell, with every premise checked by
computation, under `F.transfer.<D>.f3_set.decided_before_the_sweep`, and
the terminals say it in the same sentence as the result.  The original
paragraph said the set "can be nonempty and F3 can fail"; that stated
possibility where necessity holds, and is superseded by this one.

**Step 8, bounds** (keys `declared_bounds`, `bounds_reached`; copied from
`PREFLIGHT.md` step 4).  N = 3 required; N = 4 attempted; N = 5 refused by
name: `check_carrier_bound` raises `RefusedCarrier` and `refusal_record(5)`
is in the receipt (key `bounds_reached.carrier_refused`, terminal
`REFUSED`).  Closure-size bound 65536 distinct extents; when hit, the
closure is marked truncated and the terminal is `S9_1_LATTICE_BOUNDED`.

**Step 9, representation.**  Extents are over all relations on carriers
1..N (unpointed; the pointing enters only in the transfer test).  An extent
is stored as the set of realized *pattern classes* it contains: two
relations are in one class when they have the same carrier size and
realize the same set of atom truth-patterns at pairs `(x, y)`; a clause's
truth on a relation depends only on that set.  Classes are nonempty and
pairwise disjoint, so equality and inclusion of class sets coincide with
equality and inclusion of the underlying relation sets.  This is checked,
not assumed: `RelationTable.expand` re-enumerates the relations of an
extent from the raw census and the test
`test_class_extents_expand_to_the_literal_extents` compares it, for all 62
generators, against `literal_extent`, which evaluates the quantifier
directly; and `test_bitset_verdicts_match_the_literal_definition_at_n3`
compares every transfer verdict against the definition evaluated literally
with the sealed enumerator `derivation.primdiff.enumerate_pointed`.

**Step 10, the order** (key `order`).  Extent inclusion: `e1 <= e2` iff
`e1` is a subset of `e2`.  A SMALLER extent is a STRONGER axiom, so
"stronger" points DOWN (key `order.stronger`; the runner prints it).  Meet
= intersection of extents = conjunction of axioms.  "Upward closed in the
strength direction" is reported as `closed_under_strengthening` (every
lattice extent contained in a transferring extent transfers, checked at N
over the closure's elements); `closed_under_weakening` (up in inclusion)
is reported for contrast and is expected to fail at the empty axiom; the
"unique minimum" of step 10 is the
unique weakest transferring extent, the one containing every other
transferring extent.  Because transfer is containment in a fixed W, the
transferring set is the principal down-set of W within the lattice:
closure under strengthening and under meet are then automatic, and W is
the unique weakest transferring extent whenever the lattice realizes it
(key `order.principal_downset`).  The three findings are computed and
reported anyway, with witnesses, and the receipt says next to them what is
automatic.

## 1. Step 5 -- the clause counts

| count | PURE (key `axiom_space.PURE.*`) | EQ_BEARING (key `axiom_space.EQ_BEARING.*`) |
|---|---|---|
| raw clauses, before the swap quotient (`raw_clause_count`) | 80 | 112 |
| swap orbits, after the quotient (`swap_orbit_count`) | 42 | 62 |
| of which swap-fixed (`swap_fixed_clause_count`) | 4 | 12 |
| head-in-body, trivially valid (`head_in_body_count`) | 32 | 48 |
| non-trivial clauses (`nontrivial_clause_count`) | 48 | 64 |
| non-trivial swap orbits, USED DOWNSTREAM (`nontrivial_swap_orbit_count`) | 26 | 36 |
| one-variable clauses, raw (`one_variable_clause_count_raw`) | 7 | 0 |
| one-variable swap orbits (`one_variable_swap_orbit_count`) | 4 | 0 |
| two-variable clauses, raw (`two_variable_clause_count_raw`) | 73 | 112 |

The seven one-variable pure clauses are listed under
`axiom_space.PURE.one_variable_clauses_raw`: `-> r x x`, `r x x -> r x x`,
`-> r y y`, `r y y -> r y y`, `-> falsum`, `r x x -> falsum`, `r y y ->
falsum` (four in `x` only, four in `y` only, `-> falsum` in both lists).
An earlier version of this row reported 4 and 8 under the key
`one_variable_clause_count`; that key counted clauses over `{r x x, x = y}`
with head in `{r x x, x = y, falsum}`, which is neither the label nor a
declared notion, and it is gone (section 11).

The orbit counts are (raw + fixed) / 2 in each column.  The merged object
sums the columns: 192 / 104 / 80 / 112 / 62, one-variable 7 / 4,
two-variable 185 (key `axiom_space.MERGED_PURE_AND_EQ_BEARING.*`, with the
merge sentence).  The swap fixes every extent:
`test_swap_fixes_every_extent` checks all 192 raw clauses at N = 3.  In the
pure fragment a clause is valid (extent = top) iff its head is in its body
(`test_pure_clause_is_valid_iff_head_in_body`; key
`PURE.generators.valid_by_extent_count` = 0).  In the EQ_BEARING fragment
14 further generators are valid by extent although their head is not in
their body (key `EQ_BEARING.generators.valid_by_extent_count` = 14, listed
under `valid_by_extent_clauses`): they have `x = y` in the body and an
`r`-atom head, and on the diagonal all four `r`-atoms coincide.  Those 14
are kept in the generating set and merge into the top class by extent
dedup; the count of generators is 26 / 36 / 62 (key `F.generators.count`).

## 2. Step 8 -- the sweep, and whether N = 4 completed

| key | N3 | N4 |
|---|---|---|
| `sweeps.N*.relation_census` | 1: 2, 2: 16, 3: 512 | 1: 2, 2: 16, 3: 512, 4: 65536 |
| `sweeps.N*.relation_total` | 530 | 66066 |
| `sweeps.N*.pattern_class_total` | 86 | 431 |
| `sweeps.N*.completed_inside_bound` | true | true |

N = 4 completed inside the declared bound: every clause extent and every
closure below was computed over all 66066 relations and no closure hit the
65536 bound (key `bounds_reached.carrier_completed_inside_bound` =
{3: true, 4: true}).  Observed wall time on the run machine for the whole
receipt, both N values and all three fragments: under one second; that
number is printed to stdout only and is not in the receipt.  N = 5 was not
attempted (key `bounds_reached.carrier_refused`: 33554432 relations would
be added; terminal `REFUSED`).

## 3. Step 9 -- the lattice of extents, not of syntax

| key (`F.`...) | PURE | EQ_BEARING | MERGED (with the merge sentence) |
|---|---|---|---|
| `generators.count` (syntax) | 26 | 36 | 62 |
| `single_clause_extents.syntax_class_count` | 26 | 36 | 62 |
| `single_clause_extents.extent_class_count` | 20 | 14 | 31 |
| `lattice.syntax_axiom_count` = 2^generators | 67108864 | 68719476736 | 4611686018427387904 |
| `lattice.closure_size` (extents) at N = 4 | 75 | 37 | 147 |
| `lattice.closure_size` at N = 3 (`sweeps.N3...`) | 75 | 37 | 147 |
| `lattice.closure_bound_hit` | false | false | false |
| `lattice.irreflexivity_extent_in_lattice` | true | true | true |
| `lattice.bottom_is_empty_extent` | true | true | true |

The closure is the set of all meets of subsets of the generating extents,
the empty meet being the top (the empty axiom, key
`lattice.top_is_empty_axiom`), computed by one pass per generator; the
tests check it contains top, bottom and every generator and is closed
under meet (`test_closure_contains_top_bottom_and_generators_and_is_meet_closed`),
and that a small bound truncates and says so
(`test_closure_bound_truncates_and_says_so`).  The extent of irreflexivity
has 1 / 4 / 64 / 4096 relations on carriers 1 / 2 / 3 / 4 (key
`PURE.lattice.irreflexivity_extent_size_by_carrier`).

The closure sizes at N = 3 and N = 4 coincide for all three fragments.
That two sizes agree does not by itself say the closures correspond, so
the correspondence is computed and recorded (key
`closure_restriction.<F>`, added in round 2): each of the 75 / 37 / 147
extents of the N = 4 closure, restricted to the relations on carriers
1..3, gives 75 / 37 / 147 distinct sets (`distinct_restrictions`;
`injective` = true in all three fragments), and the set of restrictions is
exactly the N = 3 closure (`image_equals_lower_closure` = true).  So no two
extents that are equal over carriers <= 3 separate at carrier 4, and every
N = 3 extent is the restriction of an N = 4 one.  Bounded: this is a
computed fact about the two bounds 3 and 4 (`bound_reached` = 4) and says
nothing about carrier 5, which is refused; the merged cell carries the
merge sentence.

Among the 20 pure single-clause extent classes, the class of `r x x ->
falsum` has 7 members (every falsum-headed orbit whose body contains `r x
x` or `r y y`; key `PURE.single_clause_extents.classes[*].members` for the
class with representative `r x x -> falsum`); the other three falsum-headed
extents are `-> falsum` (empty), `r x y -> falsum` (the empty relation on
each carrier) and `r x y, r y x -> falsum` (asymmetric: 1 / 3 / 27 / 729).
Every atom-headed orbit is its own extent class (16 classes).

## 4. Step 10 -- transfer as containment in W, and the three findings

Under either definition an extent transfers iff it is contained in W, the
extent of every relation with no reflexive point on a carrier the
definition ranges over.  The receipt flag
`F.transfer.<D>.transfer_as_containment.transferring_equals_lattice_extents_contained_in_W`
(= true in all six cells) checks `e & W == e` against the verdict on every
lattice element, but it is a consistency check of the bitset encoding and
cannot be false: `transfer_verdict` and `transfer_extent` read the same
two class masks.  The evidence that the verdicts match the displayed
definition is elsewhere: `test_bitset_verdicts_match_the_literal_definition_at_n3`
evaluates the definition literally with the sealed enumerator at N = 3,
and, added in round 2, key
`F.transfer.<D>.transfer_as_containment.W_recomputed_from_raw_census_equals_W`
(= true in all six cells) records that W was recomputed by a second path
-- every relation of the census re-enumerated, "has a reflexive point"
evaluated on the relation itself, each pattern class checked homogeneous
(`reflexive_classes_from_raw_census`), and the result compared with W; a
disagreement raises, so the key records that the cross-check ran
(`test_W_from_raw_census_matches_the_literal_definition_at_n3` compares
that W with the literal set at N = 3, and
`test_W_disagreement_between_the_two_paths_raises` injects a disagreement
and sees the raise).  W by definition (key
`F.transfer.<D>.transfer_as_containment.W_size_by_carrier`, carriers 1/2/3/4):

| definition | W | `W_equals_irreflexivity_extent` | `W_minus_irreflexivity_extent.relations` |
|---|---|---|---|
| TRANSFER_ALL_CARRIERS | 1 / 4 / 64 / 4096 | true | [] |
| TRANSFER_ABOVE_POINT | 2 / 4 / 64 / 4096 | false | [{carrier 1, relation [[0, 0]]}] -- the one-point full relation, alone |

Whether the lattice realizes W is the non-definitional content of step 10
in each cell (keys `W_in_lattice`, `W_realized_by_generators`,
`unique_weakest_equals_W` under `F.transfer.<D>`):

| fragment / definition | `W_in_lattice` | `W_realized_by_generators` (first) | `unique_weakest_equals_W` |
|---|---|---|---|
| PURE / ALL_CARRIERS | true | `r x x -> falsum` (7 generators) | true |
| PURE / ABOVE_POINT | false | none | false (the weakest is irreflexivity's extent, the largest pure lattice extent below W) |
| EQ_BEARING / ALL_CARRIERS | true | `r x x, x = y -> falsum` (9 generators) | true |
| EQ_BEARING / ABOVE_POINT | true | `r x x -> x = y` | true |
| MERGED / ALL_CARRIERS | true | `r x x -> falsum` (16 generators) | true |
| MERGED / ABOVE_POINT | true | `r x x -> x = y` | true |

The three step-10 findings, reported per fragment and per definition under
`F.transfer.<D>`, each with a witness when false.  `T` is the number of
transferring lattice extents (`transferring_count`); the lattice has
`lattice_size` extents.

| fragment / definition | T | `closed_under_strengthening` | `closed_under_weakening` | `closed_under_meet` | `unique_weakest` (representative axiom) | `unique_weakest_equals_irreflexivity_extent` | `generated_by_irreflexivity` |
|---|---|---|---|---|---|---|---|
| PURE / TRANSFER_ALL_CARRIERS | 5 of 75 | true | false | true | `r x x -> falsum` | true | true |
| PURE / TRANSFER_ABOVE_POINT | 5 of 75 | true | false | true | `r x x -> falsum` | true | true |
| EQ_BEARING / TRANSFER_ALL_CARRIERS | 5 of 37 | true | false | true | `r x x, x = y -> falsum` | true (same extent) | true |
| EQ_BEARING / TRANSFER_ABOVE_POINT | 10 of 37 | true | false | true | `r x x -> x = y` | false | false |
| MERGED / TRANSFER_ALL_CARRIERS | 6 of 147 | true | false | true | `r x x -> falsum` | true | true |
| MERGED / TRANSFER_ABOVE_POINT | 12 of 147 | true | false | true | `r x x -> x = y` | false | false |

What is automatic and what is not (key
`transfer_as_containment.automatic_once_W_is_fixed`).  Closure under
strengthening and under meet hold for every principal down-set, so the
`true` entries in those two columns are consequences of transfer being a
containment, not discoveries of the sweep; the same holds for the unique
weakest extent wherever `W_in_lattice` is true.  The `false` entries under
`closed_under_weakening` each carry a witness (key
`F.transfer.<D>.closed_under_weakening_witness`): the first transferring
extent in closure order is contained in the empty axiom's extent (the
top, `representative_axiom` = []), which does not transfer.  The recorded
witness differs by definition and by fragment, and an earlier version of
this paragraph wrongly said it was the same in all six cells:

| cell | `transferring.representative_axiom` | `failure` |
|---|---|---|
| PURE / ALL_CARRIERS | `-> falsum` | `{carrier 1, relation [[0, 0]], a = b = 0}`, the one-point full relation |
| EQ_BEARING / ALL_CARRIERS | `x = y -> falsum` | the one-point full relation |
| MERGED / ALL_CARRIERS | `-> falsum` | the one-point full relation |
| PURE / ABOVE_POINT | `-> falsum` | `{carrier 2, relation [[0, 0], [1, 1]], a = b = 0}`, the two-point diagonal relation |
| EQ_BEARING / ABOVE_POINT | `-> x = y` | the two-point diagonal relation |
| MERGED / ABOVE_POINT | `-> falsum` | the two-point diagonal relation |

Under `TRANSFER_ALL_CARRIERS` the failure is the structure of the sealed
`selfdiff_consistent` (the full relation on the one-point carrier), found
by the sweep.  Under `TRANSFER_ABOVE_POINT` the one-point carrier is
outside the definition's range, so the failure is a two-point relation
with a reflexive point; that is the same phenomenon on a two-point
carrier, and no sealed theorem exhibits that structure, so none is named
for it.  The one cell where the unique weakest extent is a
computed fact rather than W itself is PURE / TRANSFER_ABOVE_POINT: W is not
a pure extent, and the largest pure lattice extent below W is
irreflexivity's -- which is the same lemma as in section 5 (no pure clause
separates the one-point full relation from the two-point full relation),
bounded by N = 4.

`generated_by_irreflexivity` is set only when all three hold:
strengthening-closed, meet-closed, and a unique weakest extent equal to
irreflexivity's.  Under `TRANSFER_ALL_CARRIERS` it holds in every fragment
and is definitional (W is irreflexivity's extent), so its content is only
that irreflexivity's extent lies in the lattice as a single clause.  Under
`TRANSFER_ABOVE_POINT` it holds in the pure fragment (by the lemma) and
FAILS in the EQ_BEARING and merged lattices, where W is realized by the
generator `r x x -> x = y` -- 2 / 4 / 64 / 4096 relations on carriers 1 /
2 / 3 / 4 (key `EQ_BEARING.transfer.TRANSFER_ABOVE_POINT.unique_weakest`),
irreflexivity's extent plus the one-point full relation.  So, with the
identity atom admitted and the one-point carrier discounted, the
transferring axioms are generated by "a reflexive point makes the carrier a
singleton", not by irreflexivity.  Bounded by N = 4 (transfer above the
point is checked on carriers 2..4); the general fact is Lean target T6.
An earlier version of this part called the ABOVE_POINT findings "the
substantive" ones; under both definitions they are principal-down-set
facts, and the only non-definitional content is which fixed extent lies in
the lattice: irreflexivity's in every fragment, and `r x x -> x = y`'s
only where the identity atom is admitted.

Terminal per cell (key `terminals.transfer.<F>.<D>`):
`S9_1_TRANSFER_CHARACTERIZED` in all six cells, each bounded by N = 4, each
naming W, saying that closure is automatic, saying whether the lattice
realizes W and by which generator, saying whether the generator is
irreflexivity or `r x x -> x = y`, and ending "finite computation, no Lean
theorem carries it"; the merged cells carry the merge clause.

Also computed, as the syntactic side of the same characterization (key
`F.lattice.transferring_iff_representative_has_falsum_head` = true in all
three fragments): a lattice extent transfers under `TRANSFER_ALL_CARRIERS`
iff its recorded representative axiom contains a clause with head falsum.
Bounded by N = 4 and by the representatives recorded (a representative is
not unique, key `representative_is_unique` = false); the general statement
is Lean target T4.

## 5. Step 11 -- the set that transfers but does not entail irreflexivity

Printed even when empty, under `F.transfer.<D>.f3_set` with `count`,
`members`, `empty_by_definitional_identity`, `nonempty_by_construction`,
`flags_meaning`, and `decided_before_the_sweep` (verdict, reason, named
generator, and every premise checked at N); the runner prints the members
per cell, or `[]`.  The two flags use the verdict's vocabulary:
`empty_by_definitional_identity` is the definition-level flag (W is
irreflexivity's extent by the definition; key
`transfer_definitions.<D>.f3_set_empty_by_definitional_identity`) and
equals `verdict == empty_by_definitional_identity`, checked in code (a
disagreement raises; `test_definition_flag_disagreeing_with_the_verdict_raises`);
`nonempty_by_construction` equals `verdict == nonempty_by_named_generator`;
a lemma-decided emptiness (PURE / ABOVE_POINT) is neither flag and is read
from the verdict.  An earlier version named the first flag
`empty_by_construction`, which read as a contradiction next to a verdict of
`empty_by_lemma`; it is renamed.

| fragment / definition | `decided_before_the_sweep.verdict` | `count` | members (representative axiom; extent sizes on carriers 1/2/3/4) | terminal (`terminals.f3.<F>.<D>`) |
|---|---|---|---|---|
| PURE / ALL_CARRIERS | empty_by_definitional_identity | 0 | -- | `F3_UNTESTED` |
| EQ_BEARING / ALL_CARRIERS | empty_by_definitional_identity | 0 | -- | `F3_UNTESTED` |
| MERGED / ALL_CARRIERS | empty_by_definitional_identity | 0 | -- | `F3_UNTESTED` |
| PURE / ABOVE_POINT | empty_by_lemma | 0 | -- (empty by computation, and could not have come out otherwise) | `F3_SUPPORTED_BOUNDED` |
| EQ_BEARING / ABOVE_POINT | nonempty_by_named_generator (`r x x -> x = y`) | 5 | `-> x = y` (2/0/0/0); `x = y -> r x x, -> x = y` (1/0/0/0); `r x x -> x = y` (2/4/64/4096); `r x x -> x = y, r x y -> x = y` (2/1/1/1); `r x x -> x = y, r x y, r y x -> x = y` (2/3/27/729) | `F3_REFUTED` |
| MERGED / ABOVE_POINT | nonempty_by_named_generator (`r x x -> x = y`) | 6 | the five extents above (some with a different recorded representative, e.g. `-> r x x, -> x = y`) plus `r y x -> r x y, r x x -> x = y` (2/2/8/64) | `F3_REFUTED` |

The premises of each verdict are computed, not assumed (key
`f3_set.decided_before_the_sweep.premises_checked_at_N`, bounded by N = 4):
under the default, `W_equals_irreflexivity_extent` = true in every
fragment; under `TRANSFER_ABOVE_POINT`,
`one_point_full_implies_two_point_full_on_lattice` = true in PURE and false
in EQ_BEARING and MERGED, and `W_realized_by_generators` = [`r x x -> x =
y`] with `W_admits_one_point_full` = true and `W_transfers` = true in
EQ_BEARING and MERGED.  The code raises if a verdict and the sweep's count
ever disagree (`test_f3_decision_disagreeing_with_the_sweep_raises`
injects the disagreement and sees the raise).

Every member's `not_entailing_witness` is the one-point full relation
`{carrier 1, relation [[0, 0]], a = b = 0}`, and every member's
representative uses the identity atom: `uses_eq_atom` = true for all 5
EQ_BEARING members (key
`EQ_BEARING.transfer.TRANSFER_ABOVE_POINT.f3_set.count` = 5) and for all 6
members of the merged cell (key
`MERGED_PURE_AND_EQ_BEARING.transfer.TRANSFER_ABOVE_POINT.f3_set.count` =
6, with the merge sentence); the two cells are not summed, because no
receipt key holds their sum.  Two of the EQ_BEARING members (`-> x = y`,
and `x = y -> r x x` with `-> x = y`) transfer above the point vacuously:
they have no model on a carrier of size 2..4 at all.

What the refutation is, exactly.  Under `TRANSFER_ABOVE_POINT`, in the
EQ_BEARING fragment, the axiom `r x x -> x = y` makes every asserted pair
on carriers 2..4 metatheoretically distinct and yet admits the one-point
self-difference; so "every axiom that makes assertion sound contains
irreflexivity's content" (F3) fails for that reading of "sound".  It
fails by construction: that clause realizes W, so it transfers, and its
head is `x = y`, so it admits the one-point full relation (that is the
finite fact T2 records); the sweep adds the bounded listing of the other
members.  Under the paper's own reading (`TRANSFER_ALL_CARRIERS`), the same
axiom does not transfer, because the one-point self-difference is precisely
an unsound assertion; there F3 is untestable, not refuted.  The refutation
is exactly as strong as the decision to discount the one-point carrier,
and it lives entirely in A3's bill: F3 as written in the sealed paper
ranges over "one-relation axioms", which under A1's bill (S1) have no
identity relation of the object language, and S7 names
`selfdiff_consistent` as the soundness countermodel that
`TRANSFER_ABOVE_POINT` discounts; every member of the refuting set uses
the identity atom, so what is refuted is F3 extended to A3's bill under a
soundness weaker than S7's, not F3 as written.  Since round 2 the
`F3_REFUTED` terminal strings say this in the same sentence (keys
`terminals.f3.EQ_BEARING.TRANSFER_ABOVE_POINT`,
`terminals.f3.MERGED_PURE_AND_EQ_BEARING.TRANSFER_ABOVE_POINT`), computed
from the members' `uses_eq_atom` values rather than asserted.  In the pure
fragment the corresponding set is empty, and empty for a reason that does
not need the sweep -- no pure lattice extent that admits the one-point
full relation transfers above the point (key
`PURE.lean_target_evidence.T7_lattice_extents_admitting_one_point_full_and_transferring_above_point`
= 0), because none of them separates it from the two-point full relation,
checked at N = 4 and bounded by it.
Bounded: the "transfers above the point" half of every refuting witness,
and the lemma behind the pure emptiness, were checked on carriers up to 4
only; Lean targets T6 and T7 are the general statements.

The F3 content of the whole sweep, stated plainly (key `f3_sweep_scope`).
The sweep decides nothing about F3 that a one-line argument per cell does
not already decide: under `TRANSFER_ALL_CARRIERS` the conjecture is a
tautology of the encoding, and under `TRANSFER_ABOVE_POINT` it fails
exactly where the identity atom is admitted and holds in the pure
fragment.  F3's truth value is therefore set by whether the one-point
carrier counts; what the sweep adds is the bounded confirmation at N = 4
and the exact member listings.  The terminals below keep
`F3_SUPPORTED_BOUNDED` and `F3_REFUTED` for the ABOVE_POINT cells rather
than relabelling them `F3_UNTESTED`, for the reason recorded in section
11 (step 38's criterion is whether the run can fail F3, and under
`TRANSFER_ABOVE_POINT` the same test does fail it in EQ_BEARING); each of
those terminals carries the could-not-have-come-out-otherwise clause in the
same sentence.

## 6. Step 12 -- the classifier audit, under each definition, and its witnesses

Key `F.classifier_audit.<D>`: `defect` = false, `kind` = "mixed" in all
six cells, over the single-clause extent classes (`transferring_count` /
`non_transferring_count`; `row_count` = 20 / 14 / 31 is the number of rows
audited and `rows_are` says what they are -- an earlier version carried a
key `class_total` = 431, the pattern classes of the relation table, which
read as if the audit had 431 rows; it is gone):

| fragment | TRANSFER_ALL_CARRIERS | TRANSFER_ABOVE_POINT |
|---|---|---|
| PURE (20 classes) | 4 / 16 | 4 / 16 |
| EQ_BEARING (14 classes) | 2 / 12 | 4 / 10 |
| MERGED (31 classes) | 4 / 27 | 6 / 25 |

The two extra transferring classes above the point in EQ_BEARING are
`-> x = y` and `r x x -> x = y`, the two single-clause members of the
step-11 set.  The defect path is exercised in
`test_all_transfer_is_a_defect_naming_the_one_point_full_relation` (an
all-transfer table is flagged with the one-point full relation as the
witness, since the empty axiom admits it) and
`test_none_transfer_is_a_defect_naming_irreflexivity` (a none-transfer
table is flagged naming `r x x -> falsum` and its reported failure, which
would have to violate the clause it is claimed to satisfy);
`test_the_real_table_is_mixed_under_each_definition` pins the six cells.

Witness relations recorded in the receipt (key
`PURE.single_clause_extents.classes[*]`):

* transferring, `r x x -> falsum`: `failure_witness` = null under both
  definitions; `witnessed_model` = `{carrier 2, relation [[0, 1]], a 0, b
  1}` -- the oriented two-element structure `D2` of the sealed derivation.
* not transferring, the symmetry orbit `{r x y -> r y x, r y x -> r x y}`
  (representative `r y x -> r x y`): `failure_witness` under
  `TRANSFER_ALL_CARRIERS` = the one-point full relation, which is the
  structure of the sealed `symm_selfdiff_consistent` (the full relation on
  the one-point carrier, symmetric), found by the sweep; under
  `TRANSFER_ABOVE_POINT` = `{carrier 2, relation [[0, 0], [1, 1]], a = b =
  0}`, a symmetric relation with a reflexive point on a two-point carrier
  -- the same phenomenon, but not the structure any sealed theorem
  exhibits, so no theorem is named for it.
* not transferring, the empty axiom (top) and the full-forcing `-> r x y`:
  failure witness the one-point full relation.
* transferring vacuously, `-> falsum` (empty extent) and `r x y -> falsum`
  (only the empty relation): `witnessed_model` = null, i.e. no asserted
  pair anywhere in the extent.

Hand-checked in `test_axiom_lattice.py` (step 34): irreflexivity transfers
under both definitions; symmetry does not, with the witness above; the
empty axiom and the full-relation-forcing axiom do not; `-> falsum` and
`r x y -> falsum` transfer vacuously; asymmetry transfers with a witnessed
model; `r x x -> x = y` separates the two definitions; and
`test_transfer_is_containment_in_a_fixed_extent` checks, for all 62
generators and both definitions, that the verdict equals containment in W.

## 7. Terminals, each with scope

* `EQ_FRAGMENT_SEPARATED` -- clauses mentioning `x = y` are enumerated as
  `EQ_BEARING` under their own key with their own lattice and transfer
  analysis; the only object mixing them with the pure fragment is labelled
  `MERGED_PURE_AND_EQ_BEARING` and carries the merge sentence, and every
  merged terminal string carries it too (key `eq_fragment.terminal`).
* `S9_1_LATTICE_COMPLETE` -- the meet closure terminated below the closure
  bound 65536 for every fragment at N = 4 (75 / 37 / 147 extents), bounded
  by N = 4: complete only as the lattice of extents over carriers <= 4; an
  extent equality there is not an equality at larger carriers, and the map
  from the unbounded lattice onto this one need not be injective (key
  `terminals.lattice`).
* `S9_1_TRANSFER_CHARACTERIZED` -- six cells (key `terminals.transfer`),
  each bounded by N = 4: transfer is containment in the fixed extent W, so
  the transferring extents are exactly the lattice extents contained in W
  and closure under strengthening and meet is automatic; under
  `TRANSFER_ALL_CARRIERS` in every fragment W is irreflexivity's extent,
  realized by `r x x -> falsum` (or `r x x, x = y -> falsum` in
  EQ_BEARING), and the set is generated by irreflexivity; under
  `TRANSFER_ABOVE_POINT` in the pure fragment W is not in the lattice and
  the unique weakest is irreflexivity's extent, a computed fact; under
  `TRANSFER_ABOVE_POINT` in the EQ_BEARING and merged lattices W is
  realized by the generator `r x x -> x = y` and the set is NOT generated
  by irreflexivity.  Finite computation; no Lean theorem carries it.
* `F3_UNTESTED` -- under `TRANSFER_ALL_CARRIERS`, in each of the three
  fragments, carriers 1..4: the step-11 set is empty by construction
  because the transfer test and the entailment test are the same
  containment, so the conjecture could not fail and was not tested (key
  `terminals.f3.<F>.TRANSFER_ALL_CARRIERS`).
* `F3_SUPPORTED_BOUNDED` -- under `TRANSFER_ABOVE_POINT` in PURE: the
  step-11 set is empty by computation, bounded by N = 4, and could not
  have come out otherwise: transfer there is containment in the extent of
  `r x x -> x = y`, which exceeds irreflexivity's extent by the one-point
  full relation alone, and no pure clause separates that relation from the
  two-point full relation, so every pure lattice extent admitting it fails
  above the point; the sweep confirms that lemma at N = 4 (Lean target T7)
  rather than discovering it; no carrier-general claim (key
  `terminals.f3.PURE.TRANSFER_ABOVE_POINT`).
* `F3_REFUTED` -- under `TRANSFER_ABOVE_POINT` in EQ_BEARING (5 members)
  and in MERGED_PURE_AND_EQ_BEARING (6 members, all using the identity
  atom; the merge clause is in the string): each member admits the
  one-point self-difference, and the set is nonempty by construction --
  the generator `r x x -> x = y` realizes W and admits the one-point full
  relation because its head is `x = y`, so it is a member before any
  sweep; the sweep's contribution is the listing of all members, bounded
  by N = 4 (the transfer half of each witness is checked on carriers 2..4;
  Lean target T6); the refutation is exactly as strong as discounting the
  one-point carrier and does not touch F3 under `TRANSFER_ALL_CARRIERS`,
  where the same axioms do not transfer; F3 as written ranges over
  one-relation axioms under A1's bill (S1: no identity relation of the
  object language), and S7 names `selfdiff_consistent` as the soundness
  countermodel this definition discounts; every member uses A3's identity
  atom (`uses_eq_atom` = true), so this refutes F3 extended to A3's bill
  under a soundness weaker than S7's, not F3 as written (keys
  `terminals.f3.EQ_BEARING.TRANSFER_ABOVE_POINT`,
  `terminals.f3.MERGED_PURE_AND_EQ_BEARING.TRANSFER_ABOVE_POINT`).
* `REFUSED` -- carrier N = 5, by name; no relation, extent, or closure at
  that size was computed (key `bounds_reached.carrier_refused`).
* `LEAN_CARRIED` and `LEAN_NOT_CARRIED` (key `terminals.lean`, a pair
  since the repair after full-run audit 1, section 14) -- as of the
  Python part no Lean theorem carried any P1 claim, every result above
  was finite computation bounded by N = 4, and the key held one
  `LEAN_NOT_CARRIED` string naming the part split as what blocked the
  step-13 attempt (section 9).  The Lean stage has since carried the
  seven proposed targets; the per-cell `LEAN_CARRIED` terminals, with
  theorem names and scopes, and the residual `LEAN_NOT_CARRIED`
  terminals are in section 13.5, and the key now holds
  `terminals.lean.LEAN_CARRIED`, naming those theorems, and
  `terminals.lean.LEAN_NOT_CARRIED`, naming what stays finite
  computation bounded by N = 4 (the lattice as an object) and what was
  not attempted, in agreement with section 13.5.

Not in scope, not claimed: OB-1, S6.6, and the S9 last bullet are
untouched by this part.

## 8. Lean targets (step 13; proposal only, proved by nobody in the Python part)

This section is the Python part's proposal, kept as written; section 13
records the Lean stage's outcome for each target.  Encoding suggested for
the Lean stage: an inductive `Atom` with four
constructors (`xx`, `xy`, `yx`, `yy`; a fifth `eq` for the EQ_BEARING
version), a `Clause` as a list of body atoms plus a head that is an atom or
falsum, `Atom.eval r x y : Prop` reading the atom at a pair, `Clause.holds
r : Prop` as `forall x y, (all body atoms) -> head`, and `Axiom.holds` as
the conjunction over a list of clauses.  Finite evidence for each target is
the named receipt key under `F.lean_target_evidence`, all bounded by N = 4.
Each entry gives a proposed statement and, where useful, an expected route
naming only sealed theorem names and other targets; no argument steps are
written here, by step 13's rule.

* **T1 `atom_head_clause_holds_on_full`.**  Proposed statement: for every
  type `alpha` and every clause whose head is an atom, the full relation
  `fun _ _ => True` satisfies the clause.  Evidence:
  `T1_atom_headed_generators_admit_full_relation_on_carriers_1_to_N` = true
  in all three fragments (16 / 16 / 32 atom-headed generators), bounded by
  `bound_reached` = 4 beside it.  The key was renamed in round 2: its
  earlier name ended `on_every_carrier`, which a ledger row citing it by
  name would have read as the carrier-general claim.
* **T2 `non_falsum_axiom_admits_selfdiff`.**  Proposed statement: for every
  list of clauses with no falsum head (atom heads, or `x = y` heads in the
  EQ_BEARING version), the relation `fun _ _ => True` on `Unit` satisfies
  every clause and asserts `r () ()`.  This would generalize
  `selfdiff_consistent` from the empty axiom to every axiom without a
  falsum-headed clause.  Evidence:
  `T2_non_falsum_generators_admit_one_point_full` = true (16 / 26 / 42
  generators).
* **T3 `falsum_clause_entails_irrefl`.**  Proposed statement: for every
  body `B` (any subset of the atoms, `x = y` included in the EQ_BEARING
  version) and every `r`, `(forall x y, body B r x y -> False) -> Irrefl
  r`.  Evidence: `T3_falsum_headed_generators_entail_irreflexivity` = true
  (10 / 10 / 20 generators).
* **T4 `transfers_iff_has_falsum_clause`.**  Proposed statement: for every
  finite clause set `phi`: `(forall alpha (r : alpha -> alpha -> Prop) a b,
  phi.holds r -> r a b -> a != b) <-> exists c in phi, c.head = falsum`.
  Expected route: T3 with `irrefl_witness_ne` in one direction, T2 in the
  other.  If proved, this is the statement that would make the sweep more
  than a table: it would answer the prompt's step-13 question (whether a
  clause whose head is an atom can transfer at all) and characterize
  transfer under the default definition syntactically.  Evidence:
  `T4_lattice_transfers_iff_representative_has_falsum_head` = true in all
  three fragments at N = 4.
* **T6 `reflexive_point_forces_singleton_transfers_above_point`** and
  **`reflexive_point_forces_singleton_admits_selfdiff`.**  Proposed
  statements: for every `alpha` and `r`, `(forall x y, r x x -> x = y) ->
  (exists a b : alpha, a != b) -> Irrefl r`; and `fun _ _ => True : Unit ->
  Unit -> Prop` satisfies `forall x y, r x x -> x = y`.  Together they
  would carry the EQ_BEARING refutation under `TRANSFER_ABOVE_POINT` beyond
  N = 4.  Evidence:
  `EQ_BEARING.lean_target_evidence.T6_reflexive_point_forces_singleton`
  (transfers above the point: true; admits the one-point full relation:
  true; entails irreflexivity: false).
* **T7 `pure_transfer_above_point_iff_has_falsum_clause`.**  Proposed
  statement: for every finite clause set `phi` over the four `r`-atoms
  only: `(forall alpha, (exists u v : alpha, u != v) -> forall r a b,
  phi.holds r -> r a b -> a != b) <-> exists c in phi, c.head = falsum`.
  Expected route: through T1; the obstacle the left-to-right direction must
  clear is the two-point full relation, which the finite evidence shows is
  never separated from the one-point one by a pure clause.  If proved it
  would make `F3_SUPPORTED_BOUNDED` in the pure fragment carrier-general
  and say why the refutation needs the identity atom.  Evidence:
  `PURE.lean_target_evidence.T7_lattice_extents_admitting_one_point_full_and_transferring_above_point`
  = 0 (against 5 and 6 in the EQ_BEARING and merged lattices), and
  `PURE.transfer.TRANSFER_ABOVE_POINT.f3_set.decided_before_the_sweep.premises_checked_at_N.one_point_full_implies_two_point_full_on_lattice`
  = true.

Targets not proposed: nothing about the lattice's size or shape (75 / 37 /
147) is proposed for Lean; those are counts over carriers <= 4 and remain
finite computation.

## 9. What this part did not do

* It proved nothing in Lean; `S9Obligations/AxiomReport.lean` and
  `verify_lean.py`'s inventory are untouched by P1.  What blocked the
  step-13 attempt: the run's part split, not the mathematics.  Lean is
  available in this environment (`PREFLIGHT.md`: `lake build` exited 0 for
  the tree's Lake package), and the P1 brief assigns the proofs to the
  Lean stage and P1 only the statements; the seven targets above are the
  attempt's input, with their finite evidence (key `terminals.lean` said
  the same until the repair after full-run audit 1 replaced it by the
  Lean terminal pair, section 14).  Superseded by section 13: the Lean
  stage has attempted all seven, and the inventory now lists 23
  declarations.
* It did not compute a third definition of transfer.  One was considered
  and set aside: "non-vacuous transfer" (the default plus the existence of
  a witnessed model), under which the step-11 set is again empty by
  construction, so it would not have tested F3 either; its interest is
  that the transferring set would presumably fail closure under meet
  (conjoining symmetry-with-irreflexivity and asymmetry-with-irreflexivity
  leaves only empty relations), but that was not computed and is not
  claimed.
* The lattice elements are not listed individually in the receipt; each
  referenced element carries one recorded representative axiom (the first
  generator subset that produced it), which is not unique.
* The negative tests for steps 36, 37, 39 and 40 in `test_axiom_lattice.py`
  are scoped to P1's five files; the step-37 and step-40 checkers are
  heuristics (a sentence splitter and a marker list) and say so.  A
  tree-level walk belongs to the synthesis pass.

## 10. Receipts of this part (commands and results)

Run from `research/s9_obligations/` with `PYTHONPATH=../../code
PYTHONUTF8=1` unless stated.  The exact exit codes and key lines are in the
structured report of this round.

| command | exit | key line |
|---|---|---|
| `python run_axiom_lattice.py --out receipts` | 0 | `wrote receipts/axiom_lattice.json`; N4 `completed inside bound True`; every cell's `decided before the sweep` verdict printed with its members or `[]`; `closure restriction <F>: N4 -> N3: ... injective True, image equals lower closure True` for all three fragments; elapsed under one second, stdout only |
| `python run_axiom_lattice.py --out tmp_replay_a` then `--out tmp_replay_b`, `cmp` a b, `cmp` a `receipts/` | 0 | byte-identical both ways (step 33); the temp directories were deleted afterwards |
| `sha256sum receipts/axiom_lattice.json`, `wc -c` | 0 | `be72bb530aa0ab4cf01bd3a2d1c2cd92cf2a2a4820a81c13119c0b5480316f91`, 443687 bytes at that round; `23f4c1b8547139dd1414a18b94ceba2ab473f4d90714f5b51fdec14d4741a363`, 445282 bytes after the repair after full-run audit 1 (section 14) |
| `python -m unittest test_axiom_lattice` | 0 | `OK` (the count is in the structured report) |
| `python -m unittest discover -s . -p "test_*.py"` (whole tree) | see report | see the structured report; other parts' files are outside P1's ownership |
| `python -m mypy axiom_lattice.py run_axiom_lattice.py test_axiom_lattice.py common.py` | 0 | `Success: no issues found in 4 source files` |
| `python -m mypy` (whole tree) | see report | see the structured report |
| `python research/s9_obligations/verify_pins.py` (from the root) | 0 | `sealed prefixes clean: prompt paper code lean4/Derivation artifacts` |
| denylist scan of the five P1 files against the 102-identifier working denylist (also `test_step39_denylist_identifiers_absent_from_p1_files`) | 0 leaks | all five files ASCII, LF only |
| the widened step-37 heuristic over every key and string value of the receipt and every prose unit of this document (`test_step37_carrier_general_sentences_carry_a_bound_or_a_proposal`) | 0 units flagged | 8127 receipt strings walked |

## 11. Repair record, round 1

Three reviewers found the defects below; each was verified by
recomputation before anything changed.  None is rejected.

1. *F3 terminals under `TRANSFER_ABOVE_POINT` could not have come out
   otherwise, and only the default said so* (major).  Verified: W under
   `TRANSFER_ABOVE_POINT` equals `ext(r x x -> x = y)`, differs from
   irreflexivity's extent by the one-point full relation alone, the
   transferring set is the principal down-set of W in all six cells, and
   on the pure lattice every extent admitting the one-point full relation
   admits the two-point full relation.  Changed: the receipt carries
   `transfer_as_containment` per cell and
   `f3_set.decided_before_the_sweep` (verdict, reason, named generator,
   premises checked at N) plus `nonempty_by_construction`; the code raises
   if a verdict disagrees with the count; the ABOVE_POINT terminals carry
   the could-not-have-come-out-otherwise clause in the same sentence; the
   step-7 record and `transfer_definitions.TRANSFER_ABOVE_POINT.why` state
   necessity; the
   "substantive" wording is withdrawn (section 4); key `f3_sweep_scope`
   states plainly what the sweep decides about F3.  Decision on the
   reviewer's two options: the terminals are kept (`F3_SUPPORTED_BOUNDED`
   in PURE, `F3_REFUTED` in EQ_BEARING and MERGED) with the clause
   attached, rather than relabelled `F3_UNTESTED`, because step 38's
   criterion is whether the run can fail F3 and under `TRANSFER_ABOVE_POINT`
   the same test does fail it in EQ_BEARING; what the reviewer showed is
   that each cell's outcome also follows from a short argument, which the
   terminal now says.  The next round can judge that choice.
   Original wording, for the record: "the transfer test and the
   entailment test then differ exactly on the two one-point relations, so
   the step-11 set can be nonempty and F3 can fail".
2. *`one_variable_clause_count` mislabelled* (three reviewers, minor).
   Verified: the old key counted clauses over `{r x x, x = y}` with head in
   `{r x x, x = y, falsum}` (4 / 8); the declared notion gives 7 / 0 raw.
   Changed: the notion is declared (`axiom_space.one_variable_meaning`),
   the keys are `one_variable_clause_count_raw`, `one_variable_clauses_raw`,
   `one_variable_swap_orbit_count`, `two_variable_clause_count_raw`; the
   old key is gone; test and section 1 updated.
3. *Step 13 not attempted and no blocker named* (major).  Verified: the
   inventory is empty and the earlier findings named no blocker.  The
   attempt itself lies outside P1's five files (the brief assigns the
   proofs to the Lean stage), so only the reviewer's second option is
   applied: the blocker sentence is written in section 9 and in
   `terminals.lean`.  The attempt stays not done (structured report).
   (The key holds the Lean terminal pair since the repair after full-run
   audit 1, section 14; the blocker sentence stays in section 9.)
4. *F3 terminal strings did not name their fragment or the merge* (minor).
   Changed: `f3_terminal` takes the fragment; every F3 and transfer string
   of a merged cell carries the merge clause; `test_terminals` checks it.
5. *Lattice terminal lacked the word "bounded"* (minor).  Changed: "bounded
   by N = 4" is in the string and in section 7.
6. *Classifier audit run under the default only* (minor).  Changed:
   `classifier_audit` is keyed by definition (six cells), pinned by
   `test_the_real_table_is_mixed_under_each_definition`; section 6 updated.
7. *Prose proof sketches in the Lean targets* (two reviewers, minor).
   Changed: T3, T4 and T7 carry proposed statements and one-line expected
   routes naming only sealed theorem names and other targets; the earlier
   assertion that T4 answers the step-13 question on every carrier is
   reworded as a proposal ("would answer", "if proved").
8. *No negative tests for steps 36, 37, 39, 40* (minor).  Changed:
   `ForbiddenClosureTests` adds four, scoped to P1's five files, each shown
   to bite on an injected string built at runtime; the step-37 and step-40
   checkers are declared heuristics.  The tree-level walk is left to the
   synthesis pass.
9. *Runner stdout printed neither the "stronger" direction nor the
   step-11 members* (minor).  Changed: both are printed; the replay test
   checks the stdout.

## 12. Repair record, round 2

Three reviewers found the defects below against the round-1 state (receipt
SHA-256 `d94668e2...dac1faf`, 423264 bytes).  Each was verified against
that receipt, the code, and the sealed sources before anything changed;
none is rejected.  The receipt was regenerated once all changes were in;
its new hash and byte count are in the header.

1. *The `closed_under_weakening` witness sentence in section 4 was wrong in
   four of six cells* (one major, one minor; the same defect).  Verified by
   reading `F.transfer.<D>.closed_under_weakening_witness` in every cell:
   under `TRANSFER_ABOVE_POINT` the failure is the two-point diagonal
   relation on carrier 2 in all three fragments, and the EQ_BEARING
   transferring representative is `x = y -> falsum` (ALL_CARRIERS) or `->
   x = y` (ABOVE_POINT).  Changed: section 4 now tabulates the six
   witnesses per cell and drops "everywhere" and "the same witness shape";
   the receipt was right and is unchanged for this item; the three witness
   keys are added to `test_keys_cited_in_the_findings_exist`.
2. *A carrier-2 witness attributed to a sealed theorem stated on `Unit`*
   (minor).  Verified in `lean4/Derivation/PrimDiff.lean`:
   `selfdiff_consistent` and `symm_selfdiff_consistent` both exhibit the
   full relation on `Unit`.  Changed: sections 4 and 6 name the theorem
   only where the witness is literally the one-point full relation and
   call the carrier-2 witnesses "the same phenomenon on a two-point
   carrier", naming no theorem for them.
3. *`classifier_audit.<D>.class_total` = 431 named the table's pattern
   classes, not the audited rows* (minor).  Verified: rows are the 20 / 14
   / 31 single-clause extent classes.  Changed: the key is replaced by
   `row_count` (= the rows) and `rows_are` (what they are);
   `test_the_real_table_is_mixed_under_each_definition` pins `row_count`
   and the absence of `class_total`.
4. *The structured report's `counts` field for the merged syntax-axiom
   count was rounded to a double* (two reviewers, minor).  Verified: the
   receipt key `MERGED_PURE_AND_EQ_BEARING.lattice.syntax_axiom_count` and
   section 3 hold 4611686018427387904 = 2^62; only the report's number
   differed.  No file change; this round's report carries the value as a
   decimal string so no float conversion can touch it.
5. *`transferring_equals_lattice_extents_contained_in_W` was presented as
   evidence although it cannot be false* (minor).  Verified in code: the
   verdict and W read the same two class masks.  Changed: the receipt's
   `transfer_as_containment.meaning` and section 4 say the flag is a
   consistency check of the bitset encoding and name
   `test_bitset_verdicts_match_the_literal_definition_at_n3` as the
   evidence; and W is now also recomputed by a second path from the raw
   relation census (`reflexive_classes_from_raw_census`, which evaluates
   "has a reflexive point" on each relation and checks every pattern class
   is homogeneous), compared, and recorded under
   `W_recomputed_from_raw_census_equals_W`, with a raise on disagreement;
   three new tests cover the literal comparison at N = 3, the homogeneity
   guard, and the injected disagreement.
6. *"`uses_eq_atom` = true for all 11 rows" summed two differently
   labelled cells and matched no key* (minor).  Verified: no key holds 11.
   Changed: section 5 states 5 and 6 under their own keys and says why
   they are not summed.
7. *The inference from equal closure sizes to "no two extents separate at
   carrier 4" rested on an unrecorded argument* (minor).  Verified: only
   the two sizes were in the receipt.  Changed: `closure_restriction`
   (new function and top-level receipt key, per fragment) restricts every
   N = 4 closure element to carriers 1..3 and records
   `distinct_restrictions` (75 / 37 / 147), `injective` (true) and
   `image_equals_lower_closure` (true), bounded by 4; section 3 cites the
   key; the runner prints the three lines; two tests cover the mechanics
   (N = 3 onto N = 2, the argument-order refusal, `extent_keys`) and the
   receipt values.
8. *The pure-fragment lemma was stated as a general fact, with a prose
   reason and without a bound, in two receipt strings and the module
   docstring, and the step-37 test could not see those strings* (minor).
   Verified: `transfer_definitions.TRANSFER_ABOVE_POINT.why`,
   `f3_sweep_scope`, and the docstring's swap sentence; the test's
   population was this document plus eighteen terminals, and its phrase
   list matched none of the three.  Changed: every statement of the lemma
   in a receipt string (the two named, `F3_DECISION_MEANING`, the
   `empty_by_lemma` reason) now says "checked at N, bounded by N = 4; the
   general lemma is Lean target T7, not proved" in the same clause; the
   docstring's swap sentence cites the N = 3 computation instead of giving
   a reason; `test_step37` now walks every key and every string value of
   the receipt (8127 strings) and this document, and its phrase list is
   widened by "every lattice extent", "every pure extent", "every pure
   lattice extent", "no pure clause", "no clause of this fragment", with a
   word-bounded "at N" / "N = <digit>" accepted as a bound; the widened
   heuristic then flagged two `order.*` declaration strings and two prose
   units of this document, which were reworded to carry "checked at N",
   and it is shown to bite on the lemma stated bare.
9. *The `F3_REFUTED` strings did not say F3 as written ranges over A1's
   bill* (minor).  Verified in the sealed paper: F3 ranges over
   "one-relation axioms", A1's bill has "no identity relation of the object
   language", S7 bullet 1 names `selfdiff_consistent`.  Changed:
   `f3_terminal`'s `nonempty_by_named_generator` branch appends the clause,
   computed from the members' `uses_eq_atom` values (and says the opposite
   if a member ever used no identity atom, a branch the sweep never
   produces and a test exercises); section 7 carries it.
10. *The T1 evidence key's name ended `on_every_carrier`, which a ledger row
    citing it by name would read as if no bound applied* (minor).
    Changed: renamed `..._on_carriers_1_to_N`; test, section 8
    and the key list updated; the test also asserts no evidence key
    contains `every_carrier`.
11. *`f3_set.empty_by_construction` = false beside a verdict of
    `empty_by_lemma`* (minor).  Changed: the definition-level flag is
    `f3_set_empty_by_definitional_identity` on the definition and
    `empty_by_definitional_identity` in `f3_set` and under
    `transfer_definitions.<D>`, with `flags_meaning` beside it; code raises
    if the flag disagrees with the verdict, and a test injects the
    disagreement.
12. *Tree-wide `unittest` and `mypy` red at review time, attributed to P3's
    in-progress files and to other reviewers' scratch directories* (not a
    P1 defect).  Verified at the start of this round: only
    `tmp_p3_verify/` remained of the scratch directories listed, and P3's
    files carried timestamps after P1's report.  P1's own scratch directory
    for this round was deleted before the final gates; the tree-wide
    results at the close of this round are in the structured report,
    attributed by file.

The reviewer's judgement on the round-1 terminal choice under
`TRANSFER_ABOVE_POINT` (keep `F3_SUPPORTED_BOUNDED` / `F3_REFUTED` with
the could-not-have-come-out-otherwise clause rather than relabel
`F3_UNTESTED`) was "defensible, since a set nonempty by construction is a
refutation and not a confirmation-by-not-looking"; the residual named --
the missing A1/A3 clause -- is item 9.

## 13. Lean outcome (step 13, the Lean stage)

Written by the Lean stage after sections 0-12 were closed.  It edits only
this section and the three pointers to it above, and the following files:
`lean/S9Obligations/AxiomLattice.lean` (new), the root
`lean/S9Obligations.lean` (one import and the sentence naming it),
`lean/S9Obligations/AxiomReport.lean` (23 report lines), and
`verify_lean.py` (the same 23 names, in the same order, in
`AXIOM_REPORT_DECLARATIONS`).  No P1 Python file and no receipt was
changed; the receipt hash in the header stands.  AuthorityEffect: None.

### 13.1 Encoding, declared before proving

Namespace `S9Obligations.AxiomLattice`, importing the sealed
`Derivation.PrimDiff` and reusing `Irrefl` and `irrefl_witness_ne` by
their sealed names; nothing sealed is restated.

* `Atom`: `xx`, `xy`, `yx`, `yy`, `eq` -- the four `r`-atoms and the
  identity atom (index 4 of `axiom_lattice.py`).
* `Head`: `atom a` or `falsum`.  `Clause`: `body : List Atom`,
  `head : Head`; the body list is read as a conjunction, so it is a subset
  up to repetition.  `ClauseSet := List Clause`, read as a conjunction
  (P1's "finite set of clauses").  The type is not given the name section
  8 suggested, because that name, lowercased at the start of a wrapped
  line, is the token the plain-text scan of `verify_lean.py` forbids.
* `Atom.eval r x y` reads an atom at a pair; `Head.eval r x y` reads a
  head, falsum as `False`; `Clause.Holds r c` is
  `forall x y, (every body atom holds at (x, y)) -> head holds at (x, y)`;
  `ClauseSet.Holds r phi` is `forall c, c in phi -> c.Holds r`.
* `Clause.MentionsEq c` is `c.head = atom eq \/ eq in c.body` (P1's
  `mentions_eq`); `Clause.Pure c` is `not c.MentionsEq`;
  `ClauseSet.Pure phi` is `forall c, c in phi -> c.Pure`.  A theorem over
  the whole syntax covers the object `MERGED_PURE_AND_EQ_BEARING` and
  restricts to PURE and to EQ_BEARING; a theorem with a `Pure` hypothesis
  is about the PURE fragment only.  Where a merged cell is named below the
  merge sentence applies: that object MERGES the pure fragment's
  generators with the EQ_BEARING fragment's generators, and every claim
  about it mixes A1's bill with A3's identity atom.
* `ClauseSet.HasFalsumClause phi` is `exists c, c in phi /\ c.head =
  falsum`, with an explicit `Decidable` instance built from
  `DecidableEq Head` and decidable list membership, so that the one case
  split in the proofs below is on a decidable proposition and not on
  classical choice.
* `full alpha := fun _ _ => True`; on `Unit` it is the structure of the
  sealed `selfdiff_consistent`, on `Bool` the two-point full relation.
* Transfer, both definitions of step 7, with "carriers 1..N" replaced by
  every `alpha : Type` and "carriers 2..N" by every `alpha : Type` with
  two distinct points; and "entails irreflexivity" in the sealed sense:

      Transfers phi :=
        forall (alpha : Type) (r : alpha -> alpha -> Prop) (a b : alpha),
          ClauseSet.Holds r phi -> r a b -> a != b
      TransfersAbovePoint phi :=
        forall (alpha : Type) (r : alpha -> alpha -> Prop) (a b : alpha),
          (exists u v : alpha, u != v) -> ClauseSet.Holds r phi -> r a b -> a != b
      EntailsIrrefl phi :=
        forall (alpha : Type) (r : alpha -> alpha -> Prop),
          ClauseSet.Holds r phi -> Irrefl r

* Named clauses: `irreflClause := <[xx], falsum>` (`r x x -> falsum`) and
  `reflexivePointForcesSingleton := <[xx], atom eq>` (`r x x -> x = y`,
  P1's `REFLEXIVE_POINT_FORCES_SINGLETON`).

The phrase "on every carrier" in this section always sits beside the name
of the theorem whose statement quantifies over every `alpha : Type`; a
result without such a theorem says "bounded" and names its bound.

### 13.2 The seven targets: statement as written, outcome, cells carried

All names live in `S9Obligations.AxiomLattice`.  Statements are rendered
in ASCII from the Lean source; `alpha` is an implicit `Type` argument
unless shown.

| target | theorem | statement as written | outcome | cells carried |
|---|---|---|---|---|
| target T1 | `atom_head_clause_holds_on_full` | `(alpha : Type) (c : Clause) (a : Atom) (hh : c.head = .atom a) (ha : a != .eq) : c.Holds (full alpha)` | proved | key `T1_atom_headed_generators_admit_full_relation_on_carriers_1_to_N`, all three fragments; the `r`-atom heads exactly as P1's `atom_headed` counted them (an identity-atom head is excluded: `-> x = y` fails on `full Bool` and is covered on `Unit` by T2) |
| target T2 | `non_falsum_clause_set_admits_selfdiff` | `(phi : ClauseSet) (h : forall c, c in phi -> c.head != .falsum) : exists r : Unit -> Unit -> Prop, ClauseSet.Holds r phi /\ r () ()` | proved, under a name other than the proposed `non_falsum_axiom_admits_selfdiff` of section 8 (the statement is the proposed one; the proposed name embedded the type name section 8 suggested, and the theorem's name followed that type's rename to `ClauseSet`, recorded with its reason in section 13.1 and in the module docstring of `AxiomLattice.lean`; the docstring above the theorem cited the proposed name until the repair after full-run audit 1 made it cite the proved name, section 14; this note was added by the synthesis pass's repair round 1, which wrongly said the rename was unrecorded, and corrected by its repair round 2) | key `T2_non_falsum_generators_admit_one_point_full`, all three fragments; the empty clause set gives back the shape of `selfdiff_consistent` |
| target T3 | `falsum_clause_entails_irrefl` | `(c : Clause) (hhead : c.head = .falsum) (r : alpha -> alpha -> Prop) (h : c.Holds r) : Irrefl r` | proved; stated on a clause with a head hypothesis rather than on a bare body, which is the same statement for every body, identity atom included | key `T3_falsum_headed_generators_entail_irreflexivity`, all three fragments; lifted to clause sets as `has_falsum_clause_entails_irrefl` |
| target T4 | `transfers_iff_has_falsum_clause` | `(phi : ClauseSet) : Transfers phi <-> phi.HasFalsumClause` | proved | key `T4_lattice_transfers_iff_representative_has_falsum_head`, all three fragments, and the three `S9_1_TRANSFER_CHARACTERIZED` cells under `TRANSFER_ALL_CARRIERS` (section 13.5) |
| target T4, the prompt's step-13 question | `atom_head_clause_does_not_transfer` | `(c : Clause) (a : Atom) (hh : c.head = .atom a) : not Transfers [c]` | proved | a clause whose head is an atom, the identity atom included, does not transfer under the default definition, because the one-point full relation satisfies it and already hosts a self-difference |
| target T6, transfer half | `reflexive_point_forces_singleton_transfers_above_point` | `TransfersAbovePoint [reflexivePointForcesSingleton]` | proved | key `T6_reflexive_point_forces_singleton.transfers_above_point` (EQ_BEARING; MERGED with the merge sentence), which the sweep checked on carriers 2..4 only |
| target T6, non-entailment half | `reflexive_point_forces_singleton_admits_selfdiff` and `reflexive_point_forces_singleton_not_entails_irrefl` | `exists r : Unit -> Unit -> Prop, ClauseSet.Holds r [reflexivePointForcesSingleton] /\ r () ()` and `not EntailsIrrefl [reflexivePointForcesSingleton]` | proved | keys `T6_reflexive_point_forces_singleton.admits_one_point_full` (true) and `.entails_irreflexivity` (false) |
| target T7 | `pure_transfer_above_point_iff_has_falsum_clause` | `(phi : ClauseSet) (hp : phi.Pure) : TransfersAbovePoint phi <-> phi.HasFalsumClause` | proved | key `T7_lattice_extents_admitting_one_point_full_and_transferring_above_point` (= 0 in PURE), and the PURE cell of `S9_1_TRANSFER_CHARACTERIZED` under `TRANSFER_ABOVE_POINT` |

No target blocked and none was weakened.  The deviations from the
proposed wording are the three said in the table: T1 restricted to
`r`-atom heads (that is what P1's evidence key counts), T3 on a clause
with its head hypothesis, T6 stated on the syntactic clause with the raw
form P1 wrote proved beside it (`reflexivePointForcesSingleton_holds_iff`,
`reflexive_point_forces_singleton_irrefl_of_two_points`).

Beyond the seven targets, the following were proved because a cell needed
them or because they state what a target's proof turns on:

| beyond the targets | theorem | statement as written | what it carries |
|---|---|---|---|
| beyond the targets | `irreflClause_holds_iff` | `(r : alpha -> alpha -> Prop) : irreflClause.Holds r <-> Irrefl r` | ties P1's "irreflexivity's extent" to the sealed `Irrefl` on every carrier |
| beyond the targets | `transfers_iff_entails_irrefl` | `(phi : ClauseSet) : Transfers phi <-> EntailsIrrefl phi` | the three `F3_UNTESTED` cells: P1's "empty by definitional identity" is a theorem on every carrier, not an N = 4 observation |
| beyond the targets | `entails_irrefl_iff_has_falsum_clause` | `(phi : ClauseSet) : EntailsIrrefl phi <-> phi.HasFalsumClause` | with T4: transferring under the default, entailing irreflexivity, and containing a falsum head are one property on every carrier |
| beyond the targets | `transfers_above_point_iff` | `(phi : ClauseSet) : TransfersAbovePoint phi <-> forall (alpha : Type) (r : alpha -> alpha -> Prop), ClauseSet.Holds r phi -> (exists u v : alpha, u != v) -> Irrefl r` | the containment reading of `TRANSFER_ABOVE_POINT` on every carrier: W read as "irreflexive wherever two points differ" |
| beyond the targets | `reflexive_point_forces_singleton_f3_countermodel_above_point` | `reflexivePointForcesSingleton.MentionsEq /\ TransfersAbovePoint [c] /\ not EntailsIrrefl [c] /\ not Transfers [c]` for `c = reflexivePointForcesSingleton` | the two `F3_REFUTED` cells: the named member is a member on every carrier, uses the identity atom, and does not transfer under the default definition |
| beyond the targets | `pure_non_falsum_clause_set_holds_on_full`, `pure_one_point_full_implies_two_point_full` | `(phi : ClauseSet) (hp : phi.Pure) (h1 : phi.Holds (full Unit)) : phi.Holds (full Bool)` for the second | the lemma behind key `one_point_full_implies_two_point_full_on_lattice`, on every carrier's full relation, not only at N = 4 |
| beyond the targets | `pure_transfers_above_point_iff_entails_irrefl` | `(phi : ClauseSet) (hp : phi.Pure) : TransfersAbovePoint phi <-> EntailsIrrefl phi` | the `F3_SUPPORTED_BOUNDED` cell (PURE / `TRANSFER_ABOVE_POINT`): the step-11 set is empty for pure clause sets on every carrier |
| beyond the targets | `reflexivePointForcesSingleton_holds_iff_of_decidableEq` | `[DecidableEq alpha] (r : alpha -> alpha -> Prop) : reflexivePointForcesSingleton.Holds r <-> ((exists u v : alpha, u != v) -> Irrefl r)` | on a carrier with decidable identity the clause `r x x -> x = y` is exactly "irreflexive wherever two points differ" |
| beyond the targets | `transfers_above_point_of_entails_reflexive_point_forces_singleton` | `(phi : ClauseSet) (h : forall (alpha : Type) (r), ClauseSet.Holds r phi -> reflexivePointForcesSingleton.Holds r) : TransfersAbovePoint phi` | one half of P1's "W is the extent of `r x x -> x = y`" under `TRANSFER_ABOVE_POINT`, on every carrier |
| beyond the targets | `transfers_above_point_imp_entails_reflexive_point_forces_singleton` | `(phi : ClauseSet) (h : TransfersAbovePoint phi) (alpha : Type) [DecidableEq alpha] (r) (hphi : ClauseSet.Holds r phi) : reflexivePointForcesSingleton.Holds r` | the other half, on every carrier with decidable identity, which includes every finite carrier; the unrestricted form is not claimed (section 13.6) |

### 13.3 Report lines (a manual receipt)

Printed by `lake env lean S9Obligations/AxiomReport.lean` from
`research/s9_obligations/lean/`, and audited by `verify_lean.py`:

    'S9Obligations.AxiomLattice.irreflClause_holds_iff' depends on axioms: [propext]
    'S9Obligations.AxiomLattice.atom_head_clause_holds_on_full' does not depend on any axioms
    'S9Obligations.AxiomLattice.non_falsum_clause_set_admits_selfdiff' does not depend on any axioms
    'S9Obligations.AxiomLattice.falsum_clause_entails_irrefl' does not depend on any axioms
    'S9Obligations.AxiomLattice.has_falsum_clause_entails_irrefl' does not depend on any axioms
    'S9Obligations.AxiomLattice.transfers_iff_entails_irrefl' does not depend on any axioms
    'S9Obligations.AxiomLattice.transfers_iff_has_falsum_clause' does not depend on any axioms
    'S9Obligations.AxiomLattice.atom_head_clause_does_not_transfer' depends on axioms: [propext]
    'S9Obligations.AxiomLattice.entails_irrefl_iff_has_falsum_clause' does not depend on any axioms
    'S9Obligations.AxiomLattice.transfers_above_point_iff' does not depend on any axioms
    'S9Obligations.AxiomLattice.reflexivePointForcesSingleton_holds_iff' depends on axioms: [propext]
    'S9Obligations.AxiomLattice.reflexive_point_forces_singleton_irrefl_of_two_points' does not depend on any axioms
    'S9Obligations.AxiomLattice.reflexive_point_forces_singleton_transfers_above_point' depends on axioms: [propext]
    'S9Obligations.AxiomLattice.reflexive_point_forces_singleton_admits_selfdiff' depends on axioms: [propext]
    'S9Obligations.AxiomLattice.reflexive_point_forces_singleton_not_entails_irrefl' depends on axioms: [propext]
    'S9Obligations.AxiomLattice.reflexive_point_forces_singleton_f3_countermodel_above_point' depends on axioms: [propext]
    'S9Obligations.AxiomLattice.pure_non_falsum_clause_set_holds_on_full' does not depend on any axioms
    'S9Obligations.AxiomLattice.pure_one_point_full_implies_two_point_full' does not depend on any axioms
    'S9Obligations.AxiomLattice.pure_transfer_above_point_iff_has_falsum_clause' does not depend on any axioms
    'S9Obligations.AxiomLattice.pure_transfers_above_point_iff_entails_irrefl' does not depend on any axioms
    'S9Obligations.AxiomLattice.reflexivePointForcesSingleton_holds_iff_of_decidableEq' depends on axioms: [propext]
    'S9Obligations.AxiomLattice.transfers_above_point_of_entails_reflexive_point_forces_singleton' depends on axioms: [propext]
    'S9Obligations.AxiomLattice.transfers_above_point_imp_entails_reflexive_point_forces_singleton' depends on axioms: [propext]

Twenty-three reports, every one within `{propext, Quot.sound}`; `propext`
enters only through the core lemma `List.mem_singleton`, and no report
names `Classical.choice`.  These reports are a manual receipt: nothing in
`.github/workflows` runs `verify_lean.py`, and a committed report implies
no enforcement (PROMPT.md step 29; the sentence belongs in `STATUS.md` and
is repeated here so this section does not imply otherwise).

### 13.4 Commands of the Lean stage

Run from the repository root unless stated.

| command | exit | key line |
|---|---|---|
| `cd research/s9_obligations/lean && lake build` | 0 | `Build completed successfully (7 jobs).` |
| `python research/s9_obligations/verify_lean.py` | 0 | `Lean #print axioms declarations: 23 within ['Quot.sound', 'propext']`; `Lean sources scanned for forbidden tokens: 4` |
| `cd research/s9_obligations/lean && lake env lean S9Obligations/AxiomReport.lean` | 0 | the 23 lines of section 13.3 |
| `cd research/s9_obligations && python -m mypy` | 0 | `Success: no issues found in 13 source files` |
| `cd research/s9_obligations && python -m unittest discover -s . -p "test_*.py"` (whole tree) | 1 | 151 tests, 1 failure: `test_verify_pins.test_forbidden_token_scan_names_the_token_and_passes_the_sources` pins the Lean source census to `['AxiomReport.lean', 'S9Obligations.lean', 'lakefile.lean']` and `AxiomLattice.lean` is now a fourth; a census pin going red on a new module is that pin working, and the file is outside the Lean stage's ownership, so the repin is recorded in section 13.6 rather than made |
| `cd research/s9_obligations && python -m unittest test_axiom_lattice` | 0 | `Ran 55 tests`, `OK`: the P1 tests, including the ASCII/LF, step-36, step-37 (this document and the 8127 receipt strings), step-39 and step-40 checks, pass on this document as edited; the step-37 heuristic bit once on a first draft of section 13.5 (the `F3_UNTESTED` bullet), which was reworded |
| denylist scan of the four Lean-stage files against the 102-identifier working denylist | 0 leaks | all four ASCII apart from Lean's own syntax characters, LF only, no forbidden token |

### 13.5 Terminals after the Lean stage

Each `LEAN_CARRIED` names its theorems and its scope; each
`LEAN_NOT_CARRIED` names what stays finite computation and why.  Merged
cells carry the merge sentence of section 13.1.

* `LEAN_CARRIED` -- `S9_1_TRANSFER_CHARACTERIZED` under
  `TRANSFER_ALL_CARRIERS`, PURE, EQ_BEARING, and MERGED (merge sentence):
  `transfers_iff_has_falsum_clause` and `transfers_iff_entails_irrefl`
  characterize transfer under the default definition on every carrier as
  containing a falsum-headed clause, equivalently entailing
  irreflexivity, so the transferring clause sets are exactly those whose
  every model is irreflexive in the sealed sense; which lattice extents
  those are at N = 4 (5 / 5 / 6 of 75 / 37 / 147) stays finite
  computation bounded by N = 4.
* `LEAN_CARRIED` -- `S9_1_TRANSFER_CHARACTERIZED` under
  `TRANSFER_ABOVE_POINT`, PURE: `pure_transfer_above_point_iff_has_falsum_clause`
  characterizes transfer above the point for pure clause sets on every
  carrier as containing a falsum-headed clause; that W is not a pure
  extent and that the unique weakest pure transferring extent at N = 4 is
  irreflexivity's stays finite computation bounded by N = 4.
* `LEAN_CARRIED` -- `S9_1_TRANSFER_CHARACTERIZED` under
  `TRANSFER_ABOVE_POINT`, EQ_BEARING and MERGED (merge sentence):
  `transfers_above_point_iff` gives the containment reading on every
  carrier; `reflexive_point_forces_singleton_transfers_above_point` and
  `reflexive_point_forces_singleton_not_entails_irrefl` carry the named
  generator `r x x -> x = y` on every carrier (it transfers above the
  point and is not generated by irreflexivity); the identification of W
  with that clause's extent is carried in one direction on every carrier
  (`transfers_above_point_of_entails_reflexive_point_forces_singleton`)
  and in the other on every carrier with decidable identity
  (`transfers_above_point_imp_entails_reflexive_point_forces_singleton`),
  which includes every finite carrier; the counts 10 of 37 and 12 of 147
  stay finite computation bounded by N = 4.
* `LEAN_CARRIED` -- `F3_UNTESTED`, all three fragments under
  `TRANSFER_ALL_CARRIERS`: `transfers_iff_entails_irrefl` makes the
  verdict "empty by definitional identity" a theorem on every carrier;
  the terminal stays `F3_UNTESTED`, because what is now proved is that
  the conjecture can never fail under the default definition, not that
  it was tested.
* `LEAN_CARRIED` -- `F3_SUPPORTED_BOUNDED`, PURE under
  `TRANSFER_ABOVE_POINT`: `pure_transfers_above_point_iff_entails_irrefl`
  makes the step-11 set empty for pure clause sets on every carrier; the
  sweep's terminal keeps its name, since the legal vocabulary has no
  unbounded F3-supported terminal, and the two terminals together read:
  supported at N = 4 by the sweep and on every carrier by the theorem,
  within the pure fragment and this definition of transfer.
* `LEAN_CARRIED` -- `F3_REFUTED`, EQ_BEARING and MERGED (merge sentence)
  under `TRANSFER_ABOVE_POINT`:
  `reflexive_point_forces_singleton_f3_countermodel_above_point` exhibits
  the member `r x x -> x = y` on every carrier, with its identity atom and
  its failure to transfer under the default definition in the same
  statement; the member listings (5 / 6) stay finite computation bounded
  by N = 4, and the A1/A3 clause of section 7 travels unchanged: this
  refutes F3 extended to A3's bill under a soundness weaker than S7's,
  not F3 as written.
* `LEAN_NOT_CARRIED` -- `S9_1_LATTICE_COMPLETE`, all three fragments: the
  closure sizes (75 / 37 / 147), `closure_restriction`, the classifier
  rows, and every lattice membership fact (`W_in_lattice`,
  `unique_weakest`) are finite computation bounded by N = 4; no target
  was proposed for them, none was attempted, and no theorem here
  describes the lattice of extents over all carriers as an object.
* `LEAN_NOT_CARRIED` -- a syntactic characterization of the transferring
  set above the point in EQ_BEARING and MERGED (merge sentence), the
  analogue of T7 with the identity atom admitted: not proposed by P1, not
  attempted here; what is proved for those cells is listed above, and the
  membership of the other transferring extents stays bounded by N = 4.
* `LEAN_NOT_CARRIED` -- the unrestricted converse
  `TransfersAbovePoint phi -> forall alpha r, ClauseSet.Holds r phi ->
  reflexivePointForcesSingleton.Holds r` on carriers without decidable
  identity: not attempted; section 13.6 names the obstacle.
* `MANUAL_RECEIPT_DECLARED` -- the 23 reports of section 13.3 are read
  by no CI gate; `verify_lean.py` is run by hand.
* `REFUSED` -- unchanged from section 7; the Lean stage computed nothing
  at N = 5 and its theorems quantify over types, not over a carrier
  bound.

Not in scope, not claimed: OB-1, S6.6, and the S9 last bullet are
untouched by the Lean stage.

### 13.6 Residuals, and what is owed to other files

* Decidable identity.  Under `TRANSFER_ABOVE_POINT`, "phi transfers"
  gives, for every model `r` of `phi` and every `x` with `r x x`, only
  that no `y` differs from `x`; turning "no `y` differs from `x`" into
  "`x = y`" is a case split on `x = y`, which the theorem takes as
  `[DecidableEq alpha]`.  Every finite carrier has it, so every cell of
  the sweep is inside the theorem's scope; the statement without it is
  not attempted and not claimed.
* `test_verify_pins.py` line 225 pinned the Lean source census to three
  names; with `AxiomLattice.lean` present the whole-tree unit run had
  that one failure.  The Lean stage did not own that file, and the P2 and
  P3 modules moved the census again.  Repaired by the repair after
  full-run audit 1 (section 14): the pin is the six-name list.
* The step-37 heuristic in `test_axiom_lattice.py` accepts a unit that
  speaks of every carrier when the unit also contains "target" or
  "bounded", among other markers; every such unit of this section also
  names the Lean theorem that is the evidence step 37 asks for, and the
  synthesis pass may add a theorem-name marker to that heuristic, which
  is not the Lean stage's file.
* The receipt key `terminals.lean` carried the Python part's
  `LEAN_NOT_CARRIED` string until the repair after full-run audit 1
  regenerated the receipt with the Lean terminal pair (section 14); the
  ledger row for step 13 cites section 13.5, the theorem names, and now
  that key.

## 14. Repair after full-run audit 1

Written by the repair pass that followed the first full-run audit of the
tree (`STATUS.md`, "Repair round 3"), which owned every file of the tree
and changed these of P1's:

* `axiom_lattice.py`: the module constant that held one
  `LEAN_NOT_CARRIED` string under `terminals.lean` is replaced by the
  pair `terminals.lean.LEAN_CARRIED` / `terminals.lean.LEAN_NOT_CARRIED`,
  built from the declared tuple `LEAN_CARRIED_THEOREMS` (ten names of
  `S9Obligations.AxiomLattice`, the seven targets and the identification
  theorems of section 13.5); the receipt's `revision` string records it.
  No count in the receipt changed: the diff against the previous receipt
  is the `terminals.lean` value and the `revision` string.
* `test_axiom_lattice.py` (`test_terminals`): every name in
  `LEAN_CARRIED_THEOREMS` must be listed under the module in
  `verify_lean.AXIOM_REPORT_DECLARATIONS` and declared with `theorem` in
  `AxiomLattice.lean`, so a cited name is an audited report; the
  `LEAN_NOT_CARRIED` string must say "bounded by N = 4", "no Lean
  theorem", and "not attempted".
* `lean/S9Obligations/AxiomLattice.lean`: the docstring above
  `non_falsum_clause_set_admits_selfdiff` cites the proved name (it cited
  the proposed name of section 8; the rename and its reason are in
  section 13.1 and the module docstring, unchanged).  The theorem and
  its statement are unchanged; `verify_lean.py` re-run, 23 reports of
  this module unchanged, all within {propext, Quot.sound}.
* `receipts/axiom_lattice.json`: regenerated twice into two directories
  and compared byte for byte, then installed; SHA-256 above.
* This document: the pointer paragraph of section 1, the terminal bullet
  of section 7, the section 9 bullet, the section 12 item 3 note, the T2
  row of section 13.2, the two residual bullets of section 13.6, and
  this section.

Nothing about S9.1's mathematics changed: every count of sections 1-7
and every theorem of section 13 is as it was.
