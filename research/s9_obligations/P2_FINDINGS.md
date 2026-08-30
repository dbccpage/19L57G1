# P2 -- S9.2, morphism classes and initiality: findings

AuthorityEffect: None.  This part proposes; it amends nothing sealed.

Governing prompt: `research/s9_obligations/PROMPT.md`, Git blob
`1642e3f6ac746002678e4997f738e0fabd1248c9`, steps 14-18 and 20 (step 19's
Lean half belongs to the Lean stage; this part proposes its statements,
and the Lean stage's outcome is section 11).
Snapshot commit `db1d2b225b577d5212780ff02700efd693c8e446`.  Receipt:
`research/s9_obligations/receipts/morphism_classes.json`, written by
`run_morphism_classes.py`; every number below sits next to the receipt key
that holds it (`header` carries the prompt blob and the snapshot commit).

Numbering: S9.2 is the second bullet of section S9 of
`paper/primitive_difference.md`; the numbering is the prompt's, not the
paper's (`numbering_note`).

House rule, applied throughout: a table is not a computation, so every
"not initial" below carries a witness object; an absent separation is not
an equality, so a class that admits no initial object is reported with the
cell that fails, never as "nothing there"; and every result is finite
computation, bounded by the object carrier it reached.

Repair record (round 1).  Three reviews of the first version found that
several counts in sections 3 and 6 sat under no receipt key, that a test
the text cited did not exist, that two descriptive sentences in section 5
(a "down-set", and "two distinct maps always exist" for classes without
P) were contradicted by the receipt's own rows, that one Lean target's
hypothesis did not literally match two of the cells it was said to cover,
and that several result objects lacked the declared `bounded` keys.  Each
was verified against the receipt before being repaired; the numbers
themselves were unchanged.  Every count now has a key under
`witness_groups`, and every claim about "how a cell fails" is read off
the rows by `WitnessGroupTests` rather than stated.

## 1. Declarations (step 15), made before computing

**The menu.**  Exactly the five conditions the prompt requires, no sixth
(`menu`, `menu_size` = 5, within the declared bound of 8):

| name | one-line definition |
|---|---|
| P | designated points preserved: f a = a' and f b = b' |
| E | edges preserved: r x y -> r' (f x) (f y) |
| NE | non-edges preserved: not r x y -> not r' (f x) (f y).  Over decidable relations, as in this finite model, this is the same condition as r' (f x) (f y) -> r x y, and the fast path tests that form; a Lean statement should keep the not -> not form or prove decidability first |
| I | injective: f x = f y -> x = y |
| S | surjective: every y' in the carrier of Y is f x for some x |

A morphism class is a subset of the menu: `class_count` = 32 (within the
declared bound of 256), named in menu order, `{}` for the empty class and
`{P,E}` for point-preserving edge-preserving maps (`classes`).  A
C-morphism satisfies every condition in C.

**The object classes.**  An object is a pointed structure (n, rel, a, b)
in the sense of `derivation.primdiff.Pointed` with the asserted pair
required, (a, b) in rel.  Two object classes, computed separately and
never merged (`secondary_note`):

* `object_classes.primary` -- irreflexivity NOT imposed; a = b allowed;
  loops allowed; so the one-point self-difference ({0}, {(0,0)}, 0, 0) is
  an object.  This is the class `D2_initial_pointed` quantifies over.
* `object_classes.secondary` -- irreflexivity imposed on every object; a
  != b then follows and no one-point object exists.

**Carrier bound** (PREFLIGHT.md step 4, copied under `declared_bounds`):
objects range over carriers 1..N with N = 3 required, N = 4 attempted,
N = 5 refused by name (`declared_bounds.object_carrier`).  Candidates have
carrier exactly 2 (`declared_bounds.candidate_carrier`).

**Candidates** (steps 16-17).  Every object of the class with carrier
exactly 2, enumerated by `enumerate_pointed(2)` and filtered, not
hand-picked: `candidates.primary.raw_count` = 32 and
`candidates.secondary.raw_count` = 4.  Candidates with a = b are included
in the primary class (`candidates.primary.a_eq_b_included` = true) because
they are objects of that class; they are absent from the secondary class
because (a, a) in rel contradicts irreflexivity
(`candidates.secondary.a_eq_b_reason`).  The quotient is the implemented
`pointed_isomorphic`, representative = first member in enumeration order:
`candidates.primary.iso_class_count` = 16 (eight with a != b, eight with
a = b, two members each) and `candidates.secondary.iso_class_count` = 2,
namely D2 = `O01_0100` and S2 = `O01_0110`.  Names are `O<a><b>_<bits>`
with the bits over (0,0), (0,1), (1,0), (1,1); aliases D2, S2, FULL2 (the
full relation, `O01_1111`).  Two things the enumeration decided that a
hand-pick might not have: `primdiff.D2_REV` = (2, {(1,0)}, 0, 1) is not a
candidate at all, because its asserted pair (0, 1) is not in its relation;
and the reversed orientation with its pair asserted, `O10_0010`, is a
member of D2's isomorphism class, so orientation reversal produces no new
candidate up to pointed isomorphism.  Two a != b classes have a
representative with a = 1, b = 0 (`O10_1010` with member `O01_0101`, and
`O10_1110` with member `O01_0111`, under `candidates.primary.classes`),
because the representative is the first member in enumeration order;
section 6 says what that means for the Lean targets.

**Witness naming.**  Witness objects are named in the receipt by
`witness_groups.primary.witness_legend`: `SELF1` is the one-point
self-difference ({0}, {(0,0)}, 0, 0); `D2`, `S2`, `FULL2` as above; any
other witness is written `n<n>:<edges>:a<a>b<b>`, so `n3:01:a0b1` is the
three-point object with the single edge (0, 1) pointed at (0, 1).

**Initiality and witnesses** (step 16).  O is initial for C over an object
class up to N when every object Y with carrier 1..N has exactly one
C-morphism O -> Y.  Existence failures (no morphism) and uniqueness
failures (two morphisms) are searched independently and recorded in
separate columns, each with the FIRST failing Y in the order carrier
ascending, then `enumerate_pointed` order (`witness_order`); a uniqueness
witness carries the first two distinct morphisms.

## 2. The `D2_initial_pointed` cell (step 14)

The theorem in `lean4/Derivation/PrimDiff.lean`, quantification restated
exactly (`d2_initial_pointed_cell.quantification`):

* objects: every type alpha, every r : alpha -> alpha -> Prop, every a b
  with r a b -- no irreflexivity hypothesis, a = b not excluded;
* existence: some f : Bool -> alpha with f false = a, f true = b, and
  forall x y, D2 x y -> r (f x) (f y);
* uniqueness: every g : Bool -> alpha with g false = a and g true = b
  equals f pointwise -- NO edge condition is imposed on g.

In the menu's vocabulary (`d2_initial_pointed_cell.in_menu_terms`): the
existence half lands in class `{P,E}`, the uniqueness half ranges over
class `{P}`.  So the theorem says: D2 is initial for `{P}` over the primary
object class, and the unique `{P}`-morphism is moreover an E-morphism.  The
recorded cell is (primary, `{P}`, `O01_0100`)
(`d2_initial_pointed_cell.recorded_cell.initial_in_table` = true); the
cell (primary, `{P,E}`, `O01_0100`) follows from it and is recorded as the
corollary cell (`d2_initial_pointed_cell.corollary_cell.initial_in_table`
= true).  The theorem does NOT speak about `{P,NE}`, and the table agrees
that it must not: D2 is not initial for `{P,NE}` (existence fails at the
one-point self-difference, section 3).

The model was checked against the theorem's quantification directly, with
the slow path: over all `d2_initial_pointed_cell.direct_check.objects_checked`
= 2337 objects of the primary class with carrier at most 3, every object
has exactly one point-preserving map from D2 and that map preserves the
edge (`d2_initial_pointed_cell.direct_check.agrees_with_theorem` = true);
the fast sweep agrees at N = 4 (`d2_initial_pointed_cell.model_agrees_at_bound`
= true, `d2_initial_pointed_cell.bounded` = true).  The 2337 equals the
sealed artifact's `witnessed_structures_checked`.  No disagreement arose,
so nothing was "fixed" and the theorem was not touched.

## 3. The classification table (step 16)

`tables.primary.row_count` = 512 rows (32 classes x 16 candidates) and
`tables.secondary.row_count` = 64 rows (32 x 2).  Each row carries the
class, the object, `initial`, `existence_failure` (witness Y or null),
`uniqueness_failure` (witness Y and two morphisms, or null), `bounded` =
true and `bound_reached` = 4.  Every witness in the committed receipt is
re-checked by the slow path in `test_morphism_classes.py`
(`test_every_committed_witness_is_rechecked_by_the_slow_path`).

Cell summary (`cell_summary.primary`): 10 initial, 218 existence-only,
19 uniqueness-only, 265 both.  (`cell_summary.secondary`): 8 initial, 28
existence-only, 9 uniqueness-only, 19 both.

The required carrier gives the same table: the N = 3 sweep and the N = 4
sweep agree cell for cell, initiality and both witnesses
(`bounds_reached.primary.table_identical_at_required_carrier` = true,
`bounds_reached.secondary.table_identical_at_required_carrier` = true;
re-derived in `test_table_at_required_carrier_equals_the_committed_table`).
That is a statement about carriers 3 and 4 only.

Initial objects per class (`initial_objects_by_class`):

| object class | class | initial two-element objects |
|---|---|---|
| primary | `{P}` | all 8 candidates with a != b (`O01_0100`, `O01_1100`, `O10_1010`, `O01_0110`, `O01_1110`, `O10_1110`, `O01_1101`, `O01_1111`) |
| primary | `{P,E}` | `O01_0100` (D2) only |
| primary | `{P,NE}` | `O01_1111` (FULL2) only |
| primary | every other class | none |
| secondary | `{P}`, `{P,I}` | `O01_0100` (D2) and `O01_0110` (S2) |
| secondary | `{P,E}`, `{P,E,I}` | D2 only |
| secondary | `{P,NE}`, `{P,NE,I}` | S2 only |
| secondary | every other class | none |

**Witness groups** (`witness_groups`).  The Lean targets in section 6 each
rest on a group of cells that fail in one uniform way.  The groups are
declared as cell predicates in `morphism_classes.py` and every count
about them is computed from the rows and written under `witness_groups`,
per object class, under `witness_groups.primary.groups` and
`witness_groups.secondary.groups` by group name; the groups of each object
class partition its cells
(`witness_groups.primary.partition_is_disjoint_and_exhaustive` = true,
`witness_groups.primary.partition_cell_counts` = [256, 128, 64, 8, 8,
16, 16, 16], `witness_groups.primary.partition_cell_total` = 512;
`witness_groups.secondary.partition_is_disjoint_and_exhaustive` = true,
`witness_groups.secondary.partition_cell_counts` = [32, 16, 8, 8],
`witness_groups.secondary.partition_cell_total` = 64).
`WitnessGroupTests` recounts every group from the rows with its own
predicates.

Primary object class, by group:

* `witness_groups.primary.groups.I_classes` -- every class containing I,
  `cells` = 256: all 256 fail existence
  (`witness_groups.primary.groups.I_classes.existence_failures` = 256), and
  every one at the one-point self-difference
  (`witness_groups.primary.groups.I_classes.existence_witness_counts.SELF1`
  = 256), whose only function Bool -> {0} is constant, not injective.  The
  hand-checked cell is (primary, `{I}`, D2).
* `witness_groups.primary.groups.S_without_I_classes` -- S in the class, I
  not, `cells` = 128: all fail existence
  (`witness_groups.primary.groups.S_without_I_classes.existence_failures`
  = 128), the first witness at carrier 1, 2 or 3 depending on the class
  (`witness_groups.primary.groups.S_without_I_classes.existence_witness_carriers`
  = {1: 56, 2: 54, 3: 18}).
* `witness_groups.primary.groups.no_P_I_S_classes` -- none of P, I, S
  (classes `{}`, `{E}`, `{NE}`, `{E,NE}`), `cells` = 64: all fail
  uniqueness
  (`witness_groups.primary.groups.no_P_I_S_classes.uniqueness_failures`
  = 64).  The hand-checked cell is (primary, `{}`, D2): uniqueness fails
  at Y = ({0,1}, {(0,0)}, 0, 0) with morphisms (0,0) and (0,1); all four
  functions are `{}`-morphisms.
* `witness_groups.primary.groups.P_class_initial` -- class `{P}`, the 8
  initial cells (`cells` = 8), every candidate with a != b.
* `witness_groups.primary.groups.P_class_non_initial` -- class `{P}`, the
  8 non-initial cells: all are a = b candidates
  (`witness_groups.primary.groups.P_class_non_initial.non_initial_diagonal_candidates`
  = 8) and all fail existence at Y = D2
  (`witness_groups.primary.groups.P_class_non_initial.existence_witness_counts.D2`
  = 8): the point-preserving map would have to send the one designated
  point to both false and true.
* `witness_groups.primary.groups.P_E_class` -- class `{P,E}`, 16 cells: 1
  initial (D2), 15 fail existence, every one at Y = D2
  (`witness_groups.primary.groups.P_E_class.existence_witness_counts.D2`
  = 15); 8 of the 15 are a = b candidates and 7 are a != b
  (`witness_groups.primary.groups.P_E_class.non_initial_diagonal_candidates`
  = 8, `witness_groups.primary.groups.P_E_class.non_initial_off_diagonal_candidates`
  = 7).  For the a != b ones the point-preserving map is determined and
  carries an extra edge of the candidate onto a non-edge of D2.
* `witness_groups.primary.groups.P_NE_class` -- class `{P,NE}`, 16 cells:
  1 initial (FULL2), 15 fail existence, 14 at the one-point
  self-difference and 1 (the a = b candidate `O00_1111`) at D2
  (`witness_groups.primary.groups.P_NE_class.existence_witness_counts.SELF1`
  = 14, `witness_groups.primary.groups.P_NE_class.existence_witness_counts.D2`
  = 1).  At the one-point object the only function sends a non-edge of
  the candidate onto the loop.  The hand-checked cell is (primary,
  `{P,NE}`, D2), the negative control of section 2.
* `witness_groups.primary.groups.P_E_NE_class` -- class `{P,E,NE}`, 16
  cells, none initial: 14 fail at the one-point self-difference and 2
  (`O00_1111` and `O01_1111`) at D2
  (`witness_groups.primary.groups.P_E_NE_class.existence_witness_counts.SELF1`
  = 14, `witness_groups.primary.groups.P_E_NE_class.existence_witness_counts.D2`
  = 2).

Secondary object class, by group:

* `witness_groups.secondary.groups.S_classes` -- every class containing
  S, `cells` = 32: all fail existence
  (`witness_groups.secondary.groups.S_classes.existence_failures` = 32),
  the first witnesses being D2, S2, or the three-point object `n3:01:a0b1`
  (`witness_groups.secondary.groups.S_classes.existence_witness_counts`
  = {D2: 8, S2: 8, n3:01:a0b1: 16}).
* `witness_groups.secondary.groups.no_P_no_S_classes` -- neither P nor S,
  `cells` = 16: all fail uniqueness
  (`witness_groups.secondary.groups.no_P_no_S_classes.uniqueness_failures`
  = 16).  The hand-checked cell is (secondary, `{E}`, D2): uniqueness
  fails at Y = S2 with morphisms (0,1) and (1,0), the identity and the
  swap.
* `witness_groups.secondary.groups.P_without_S_initial` -- P in the class,
  S not, the 8 initial cells (`cells` = 8).
* `witness_groups.secondary.groups.P_without_S_non_initial` -- the other 8
  cells of those classes, all failing existence at D2 or at S2
  (`witness_groups.secondary.groups.P_without_S_non_initial.existence_witness_counts`
  = {D2: 4, S2: 4}).  Hand-checked: (secondary, `{P,E}`, S2) fails at
  Y = D2, the point-preserving map sending S2's reverse edge (1,0) to
  (1,0), which D2 lacks; (secondary, `{P,NE}`, D2) fails at Y = S2, the
  point-preserving map sending D2's non-edge (1,0) onto S2's edge (1,0).

Every count in this section is finite computation, bounded by object
carrier N = 4 (`bounds_reached.primary.carrier_reached` = 4,
`bounds_reached.secondary.carrier_reached` = 4;
`witness_groups.primary.bound_reached` = 4).

## 4. Ties retained (step 17)

Candidates were quotiented by `pointed_isomorphic`, never by hand
(`ties.primary.quotient`), and every non-isomorphic initial object is
kept:

* primary, class `{P}`: `ties.primary.per_class.{P}.count` = 8 -- every
  candidate with a != b is initial; within the sweep the candidate's
  relation plays no role in a `{P}`-morphism, which is determined by the
  pointing alone.  `ties.primary.classes_with_ties` = [`{P}`]; `{P,E}` and
  `{P,NE}` each retain one object (`ties.primary.per_class.{P,E}.count`
  = 1, `ties.primary.per_class.{P,NE}.count` = 1).
* secondary, classes `{P}` and `{P,I}`: `ties.secondary.per_class.{P}.count`
  = 2 and `ties.secondary.per_class.{P,I}.count` = 2, retaining D2 and S2
  -- the way S7 keeps both; they are not pointed-isomorphic (the test
  checks it with the implemented relation; the sealed theorem is
  `D2_not_pointed_iso_S2`).  `ties.secondary.classes_with_ties` =
  [`{P}`, `{P,I}`].

TIES_RETAINED is emitted for both object classes with these counts
(`terminals`), bounded by N = 4 (`ties.primary.bounded` = true).

## 5. The shape of the admitting set (step 18), computed

Computed as a set property (`shape`): the meet and join of the admitting
set are taken, every class between them is checked for membership, and
the minimal and maximal admitting classes under inclusion are listed.
Only an incomparable pair among the maximal classes (then the join is not
a member) or among the minimal classes (then the meet is not a member)
is printed as the reason, with its source named
(`shape.primary.incomparable_pair_source`); two incomparable non-extremal
members are not a reason, since the interval [`{}`, `{P,E}`] contains
`{P}` and `{E}`, so when both extremes are unique the gap is what is
printed.  Synthetic tests feed the routine a set with unique extremes and
a gap, a set with incomparable minima, a full interval, a singleton, and
the empty set.

* Primary (`shape.primary`): admitting classes
  `shape.primary.admitting_classes` = [`{P}`, `{P,E}`, `{P,NE}`]
  (`shape.primary.admitting_count` = 3); minimal `shape.primary.minimal`
  = [`{P}`]; maximal `shape.primary.maximal` = [`{P,E}`, `{P,NE}`];
  `shape.primary.is_interval` = false; incomparable pair
  `shape.primary.incomparable_pair` = [`{P,E}`, `{P,NE}`], both maximal
  (`shape.primary.incomparable_pair_source` = maximal); the first class
  between the meet and the join that does not admit is
  `shape.primary.gap` = `{P,E,NE}`.  Terminal S9_2_INCOMPARABLE_CLASSES,
  bounded by N = 4 (`shape.primary.bounded` = true).
* Secondary (`shape.secondary`): `shape.secondary.admitting_classes` =
  [`{P}`, `{P,E}`, `{P,NE}`, `{P,I}`, `{P,E,I}`, `{P,NE,I}`]
  (`shape.secondary.admitting_count` = 6); minimal
  `shape.secondary.minimal` = [`{P}`]; maximal `shape.secondary.maximal`
  = [`{P,E,I}`, `{P,NE,I}`]; `shape.secondary.is_interval` = false;
  incomparable pair `shape.secondary.incomparable_pair` = [`{P,E,I}`,
  `{P,NE,I}`] (`shape.secondary.incomparable_pair_source` = maximal);
  `shape.secondary.gap` = `{P,E,NE}`.  Terminal S9_2_INCOMPARABLE_CLASSES,
  bounded by N = 4 (`shape.secondary.bounded` = true).

What the computation shows, bounded by N = 4.  In both object classes the
admitting set is exactly the set of classes that contain P and are
contained in one of the two maximal classes
(`test_shape_is_computed_from_the_table` checks that equality); it is
NOT a down-set of the class lattice, because `{}`, `{E}`, `{NE}` (and in
the secondary class also `{I}`, `{E,I}`, `{NE,I}`) lie below a maximal
class and admit nothing (`initial_objects_by_class.primary.by_class.{E}`
= []).  Within the classes containing P the admitting set is the interval
[`{P}`, `{P,E,NE}`] with its top removed (`shape.primary.gap` =
`{P,E,NE}`): no admitting class contains both E and NE.  The two maximal
classes pick different objects: E selects the oriented edge D2 and NE
selects the object with no non-edges to preserve (FULL2 in the primary
class, S2 in the secondary class, where irreflexivity itself makes (a,a)
and (b,b) non-edges of every object, so S2's two non-edges cost nothing).
Adding I to a P-class changes nothing in the secondary class (a != b
holds there, so the point-preserving map is injective), which is why its
admitting set is the primary one doubled by I; that is an observed
property of the 64 cells
(`test_i_is_extensionally_redundant_under_p_in_the_irreflexive_class`),
not a theorem.

No class without P admits an initial two-element object at N = 4, and the
rows say how each such cell fails (`witness_groups.primary.no_P_classes`,
`witness_groups.secondary.no_P_classes`): of the 256 primary cells whose
class lacks P (`witness_groups.primary.no_P_classes.cells` = 256), 0 are
initial, 220 carry a uniqueness witness
(`witness_groups.primary.no_P_classes.with_uniqueness_witness` = 220),
237 carry an existence witness
(`witness_groups.primary.no_P_classes.with_existence_witness` = 237), and
36 carry NO uniqueness witness within the bound
(`witness_groups.primary.no_P_classes.without_uniqueness_witness` = 36)
-- those are the cells of the four classes `{NE,S}`, `{E,NE,S}`,
`{NE,I,S}`, `{E,NE,I,S}`
(`witness_groups.primary.no_P_classes.classes_without_uniqueness_witness`),
which fail by existence alone, all at the one-point self-difference
(`witness_groups.primary.no_P_classes.existence_witness_counts_without_uniqueness_witness.SELF1`
= 36).  In the secondary class: 32 cells, 0 initial, 28 with a uniqueness
witness, 23 with an existence witness, 4 with no uniqueness witness, the
same four classes, failing at S2
(`witness_groups.secondary.no_P_classes.with_uniqueness_witness` = 28,
`witness_groups.secondary.no_P_classes.without_uniqueness_witness` = 4,
`witness_groups.secondary.no_P_classes.with_existence_witness` = 23).  So
"a class without P admits nothing" is a bounded fact about these cells,
each with its witness, and NOT the claim that two distinct maps always
exist: for 36 + 4 cells the table exhibits no second map at all.  The
first version of this file made that claim; the receipt refutes it.

S9.2 asked "which edge-preserving morphism classes leave some two-element
object initial".  Read against the table: among classes containing E, only
`{P,E}` (primary) and `{P,E}`, `{P,E,I}` (secondary) admit one, and it is
D2 in every case.  That is the bounded answer; the carrier-general one
is the Lean stage's (section 6).

## 6. Bounded (step 19), and the Lean targets proposed

**Bounded.**  Initiality quantifies over all objects and the sweep reaches
only carrier N = 4: `bounds_reached.primary.objects_checked_total` =
526625 objects (`bounds_reached.primary.objects_checked_by_carrier.1` = 1,
`.2` = 32, `.3` = 2304, `bounds_reached.primary.objects_checked_by_carrier.4`
= 524288) and `bounds_reached.secondary.objects_checked_total` = 24772
(`bounds_reached.secondary.objects_checked_by_carrier.4` = 24576).  The
attempted carrier completed (`bounds_reached.primary.attempted_carrier_completed`
= true, `bounds_reached.secondary.attempted_carrier_completed` = true); the
required carrier N = 3 gives the same table (section 3).  N = 5 is refused
by name (`declared_bounds.object_carrier.refused_by_name` = 5; terminal
REFUSED).  Every cell is therefore finite computation, bounded by N = 4:
S9_2_CLASSES_BOUNDED is emitted for both object classes (`terminals`).
S9_2_CLASSES_CLASSIFIED is the Lean stage's terminal for the cells it
carries; P2 leaves it, with LEAN_CARRIED and LEAN_NOT_CARRIED, to the Lean
stage (`lean.carried_by_this_part` = false, `lean.note`) and writes no
prose proof.

**The one cell the sealed theorem already names.**  The recorded cell
(primary, `{P}`, `O01_0100`) is the content of `PrimDiff.D2_initial_pointed`
restated in the menu's terms (section 2): the sealed theorem's statement
implies that cell's carrier-general form by dropping the edge clause from
its existence half (`lean.sealed_theorem_cell`).  That one-step corollary
is target 1 below for the a = 0, b = 1 candidates; it is not carried
here, and whether the sealed theorem alone licenses
S9_2_CLASSES_CLASSIFIED for that cell is the Lean stage's decision.

**Lean targets.**  Statements to attempt in this tree's Lake package,
each carrier-general by a uniform argument or by exhibition of one
countermodel object, with the finite evidence from the receipt.  Names
are proposals, listed under `lean.proposed_target_names`
(`lean.proposed_target_count` = 15); each group above names under
`lean_targets` the targets that would cover it, and
`test_lean_target_names_agree_between_module_receipt_and_findings`
checks that the three lists agree.  The Lean stage's countermodel object
need not be the receipt's first witness (the receipt records the first Y
in enumeration order; the exhibited object is whichever makes the
statement uniform).  Where a target is written for a candidate pointed
at (false, true), it covers a cell whose representative is pointed at
(1, 0) -- `O10_1010`, `O10_1110` -- through that class's listed a = 0
member (`O01_0101`, `O01_0111`), since initiality is invariant under the
implemented pointed isomorphism; a target stated for a general pointing
(a0, b0) with a0 != b0 avoids the transport.  NE is to be stated in the
not -> not form (section 1).

Primary object class (no irreflexivity), positive cells:

1. `two_element_pointed_map_unique` (class `{P}`, all 8 a != b candidates):
   for every alpha, r, a, b with r a b there is f : Bool -> alpha with
   f false = a, f true = b, and every g with g false = a, g true = b equals
   f pointwise.  The candidate's relation does not occur; this is the P-only
   fragment of `D2_initial_pointed` and follows from it.  Evidence:
   `witness_groups.primary.groups.P_class_initial.cells` = 8.
2. `D2_initial_P_E` (class `{P,E}`, D2): existence of f with f false = a,
   f true = b, forall x y, D2 x y -> r (f x) (f y), and uniqueness among
   all g satisfying the same three conditions.  Corollary of
   `D2_initial_pointed`.  Evidence: `d2_initial_pointed_cell.corollary_cell`.
3. `FULL2_initial_P_NE` (class `{P,NE}`, FULL2 = fun _ _ => True on Bool):
   existence of f with f false = a, f true = b, forall x y, not FULL2 x y
   -> not r (f x) (f y) (vacuous), and uniqueness among all such g.
   Evidence: `initial_objects_by_class.primary.by_class.{P,NE}` = [`O01_1111`].

Primary object class, negative cells (one exhibited object each):

4. `no_injection_into_point`: for every f : Bool -> Unit, f false = f true.
   Refutes existence at the object (Unit, fun _ _ => True, (), ()) -- the
   object of `selfdiff_consistent` -- for every class containing I and
   every candidate: `witness_groups.primary.groups.I_classes.cells` = 256
   cells, all recorded failing at SELF1.
5. `no_surjection_onto_three`: for every f : Bool -> Fin 3 there is z
   with z != f false and z != f true.  Refutes existence at
   (Fin 3, fun _ _ => True, 0, 0) for every class containing S: the
   `witness_groups.primary.groups.S_without_I_classes.cells` = 128 cells
   with S and without I (the others are already covered by 4).
6. `two_copies_not_unique`: for every r0 : Bool -> Bool -> Prop with r0 a0
   b0, the object on Bool x Bool with r' (x,i) (y,j) := i = j and r0 x y,
   pointed at ((a0,false), (b0,false)), admits the two distinct maps
   x |-> (x,false) and x |-> (x,true), both edge-preserving and
   non-edge-preserving.  Refutes uniqueness for the four classes `{}`,
   `{E}`, `{NE}`, `{E,NE}` and every candidate:
   `witness_groups.primary.groups.no_P_I_S_classes.cells` = 64 cells, all
   recorded as uniqueness failures (at smaller first witnesses).
7. `diagonal_candidate_not_pointed_into_D2`: for every o : Bool and
   f : Bool -> Bool, not (f o = false and f o = true).  Refutes existence
   at Y = D2 for every a = b candidate and every class containing P:
   covers the 8 non-initial `{P}` cells
   (`witness_groups.primary.groups.P_class_non_initial.cells` = 8) and the
   a = b cells of `{P,E}`, `{P,NE}`, `{P,E,NE}` (8 each,
   `witness_groups.primary.groups.P_E_class.non_initial_diagonal_candidates`
   = 8), all recorded failing at D2 or earlier.
8. `extra_edge_not_into_D2`: for every pointed (Bool, r0, a0, b0) with
   r0 a0 b0, a0 != b0, and some (x, y) != (a0, b0) with r0 x y, no
   f : Bool -> Bool with f a0 = false and f b0 = true carries r0 into D2
   (the map is the transport of the pointing; the image of the extra
   edge is not (false, true)).  Stated for a general pointing so that it
   covers `O10_1010` and `O10_1110` literally.  Refutes existence at D2
   for the 7 non-initial a != b `{P,E}` cells
   (`witness_groups.primary.groups.P_E_class.non_initial_off_diagonal_candidates`
   = 7) and for (`{P,E,NE}`, `O01_1111`); the receipt has D2 as witness
   for each.
9. `non_edge_not_into_point`: for r0 on Bool with some non-edge, no
   f : Bool -> Unit satisfies not r0 x y -> not True.  Refutes existence
   at the one-point self-difference for every class containing NE and
   every candidate with a non-edge: the 14 + 14 cells of `{P,NE}` and
   `{P,E,NE}` recorded there
   (`witness_groups.primary.groups.P_NE_class.existence_witness_counts.SELF1`
   = 14, `witness_groups.primary.groups.P_E_NE_class.existence_witness_counts.SELF1`
   = 14).

If 1-9 all prove, every one of the 512 primary cells has a Lean theorem:
the eight groups of `witness_groups.primary.partition_order` partition
the table (`witness_groups.primary.partition_cell_counts` = [256, 128,
64, 8, 8, 16, 16, 16], summing to
`witness_groups.primary.partition_cell_total` = 512 =
`witness_groups.primary.table_cells`), and each group's `lean_targets`
are among 1-9.  The partition and the per-group witness counts are
recounted from the rows in `WitnessGroupTests`
(`test_partition_counts_match_a_row_recount`,
`test_named_witness_counts_match_a_row_recount`) -- as counts of
witnesses, not as proofs.  Whether that licenses S9_2_CLASSES_CLASSIFIED
for the primary table is the Lean stage's decision, not this part's.

Secondary object class (irreflexivity imposed):

10. `pointed_map_injective_of_irrefl`: Irrefl r -> r a b -> for every f
    with f false = a and f true = b, f false != f true (from
    `irrefl_witness_ne`).  With 1 and 2 this carries the cells
    (`{P,I}`, D2), (`{P,I}`, S2), (`{P,E,I}`, D2).  Evidence:
    `initial_objects_by_class.secondary.by_class.{P,I}`.
11. `S2_initial_P_NE_irrefl`: Irrefl r -> r a b -> existence of f with
    f false = a, f true = b, forall x y, not S2 x y -> not r (f x) (f y),
    and uniqueness among all such g.  The non-edges of S2 are (false,false)
    and (true,true); irreflexivity supplies not r a a and not r b b.
    Carries (`{P,NE}`, S2) and, with 10, (`{P,NE,I}`, S2).  Evidence:
    `initial_objects_by_class.secondary.by_class.{P,NE}` = [`O01_0110`].
12. `S2_not_P_E_into_D2`: no f : Bool -> Bool with f false = false, f true
    = true and forall x y, S2 x y -> D2 (f x) (f y).  Refutes existence at
    D2 for (`{P,E}`, S2), (`{P,E,I}`, S2), (`{P,E,NE}`, S2),
    (`{P,E,NE,I}`, S2); decidable on Bool
    (`witness_groups.secondary.groups.P_without_S_non_initial.existence_witness_counts.D2`
    = 4).
13. `D2_not_P_NE_into_S2`: no f : Bool -> Bool with f false = false, f true
    = true and forall x y, not D2 x y -> not S2 (f x) (f y).  Refutes
    existence at S2 for (`{P,NE}`, D2), (`{P,NE,I}`, D2), (`{P,E,NE}`, D2),
    (`{P,E,NE,I}`, D2); decidable on Bool
    (`witness_groups.secondary.groups.P_without_S_non_initial.existence_witness_counts.S2`
    = 4).
14. `no_surjection_onto_three_irrefl`: statement 5 at the irreflexive
    object (Fin 3, fun x y => x = 0 and y = 1, 0, 1), the receipt's own
    witness `n3:01:a0b1` for the carrier-3 cases; refutes existence for
    all `witness_groups.secondary.groups.S_classes.cells` = 32 secondary
    cells with S.
15. `two_irrefl_copies_not_unique`: statement 6 with the hypothesis
    Irrefl r0 and the conclusion that the doubled object is irreflexive;
    refutes uniqueness for the
    `witness_groups.secondary.groups.no_P_no_S_classes.cells` = 16
    secondary cells without P and without S.

The four secondary groups partition the 64 cells the same way
(`witness_groups.secondary.partition_cell_counts` = [32, 16, 8, 8]).
Targets 5 and 14 need constructive decidability over Fin 3 within the
axiom budget of {propext, Quot.sound}; the Lean stage should check the
available Decidable instances for bounded quantifiers before committing
to a `decide` proof.  Cells without a Lean theorem stay finite
computation, bounded by N = 4.

## 7. The fifth bullet (step 20)

Yes, plainly: this sweep reproduces S9's fifth bullet for the S9.2 table.
Its exhaustiveness over every object with carrier at most 4 lives in
Python only -- `sweep` and its slow cross-check `sweep_direct` -- and no
Lean theorem states that the finite scope was swept.  Any Lean theorem for
a cell (section 6) is carrier-general by a uniform argument or an
exhibited countermodel, not by formalizing the sweep.  PYTHON_ONLY_SCOPE_DECLARED
is emitted with that scope (`python_only_scope.reproduces_s9_fifth_bullet`
= true, `python_only_scope.statement`, `python_only_scope.bound_reached`
= 4).  This names the situation; it does not close, narrow, or price the
fifth bullet, which is not one of S9.1-S9.3.

## 8. Terminals, each with its scope (`terminals`)

* S9_2_CLASSES_BOUNDED -- object class primary: every cell of the 512-cell
  table is finite computation, bounded by object carrier N = 4 (526625
  objects); initiality quantifies over all objects and the sweep reaches
  only N.
* S9_2_CLASSES_BOUNDED -- object class secondary: every cell of the 64-cell
  table is finite computation, bounded by object carrier N = 4 (24772
  objects).
* S9_2_INCOMPARABLE_CLASSES -- object class primary: the admitting set
  [`{P}`, `{P,E}`, `{P,NE}`] is not an interval under inclusion
  (incomparable pair `{P,E}`, `{P,NE}`); minimal [`{P}`], maximal
  [`{P,E}`, `{P,NE}`]; bounded by N = 4.
* S9_2_INCOMPARABLE_CLASSES -- object class secondary: the admitting set
  [`{P}`, `{P,E}`, `{P,NE}`, `{P,I}`, `{P,E,I}`, `{P,NE,I}`] is not an
  interval under inclusion (incomparable pair `{P,E,I}`, `{P,NE,I}`);
  minimal [`{P}`], maximal [`{P,E,I}`, `{P,NE,I}`]; bounded by N = 4.
* TIES_RETAINED -- object class primary: `{P}`: 8 retained; bounded by
  N = 4.
* TIES_RETAINED -- object class secondary: `{P}`: 2, `{P,I}`: 2 (D2 and
  S2); bounded by N = 4.
* PYTHON_ONLY_SCOPE_DECLARED -- the P2 sweep reproduces S9's fifth bullet
  for the S9.2 table: its exhaustiveness over every object with carrier
  at most 4 lives in Python only, bounded by N = 4; no Lean theorem states
  that the scope was swept.
* REFUSED -- object carrier N = 5 for P2, refused by name (PREFLIGHT.md
  step 4).

Not emitted by P2: S9_2_INTERVAL_SHAPE (the computation went the other
way in both object classes), S9_2_CLASSES_CLASSIFIED, LEAN_CARRIED,
LEAN_NOT_CARRIED (the Lean stage's; they are in section 11, which the Lean
stage wrote, and not in the receipt).  Every terminal except REFUSED says
"bounded" and names N = 4 in its own scope sentence
(`test_terminals_are_legal_scoped_and_not_the_lean_stages`).

## 9. Tests (step 34) and replay (step 33)

`test_morphism_classes.py`, run with the tree's command:

* menu size and class count; class naming; the NE definition carries its
  decidability scope and the receipt's copy equals the module's;
* candidates enumerated and quotiented by `pointed_isomorphic` (32 -> 16
  primary, 4 -> 2 secondary; a = b included primary, excluded secondary;
  `D2_REV` not a candidate; the reversed asserted orientation in D2's
  class);
* object counts per carrier at N = 3 (1, 32, 2304 primary; 0, 4, 192
  secondary), the 2337 equal to the sealed artifact's count;
* the fast path equals the slow path cell for cell at N = 3, both object
  classes;
* the `D2_initial_pointed` cell: the theorem's quantification re-checked
  without the module's helpers over all 2337 objects; the `{P}` and
  `{P,E}` cells initial; the `{P,NE}` negative control;
* existence failures with witnesses re-checked by hand (`{I}`/D2 at the
  one-point object; `{P,E}`/S2 at D2; `{P,NE}`/D2 at S2);
* uniqueness failures with two distinct morphisms re-checked by hand
  (`{}`/D2; `{E}`/D2 at S2); no negative cell without a witness;
* tie retention (8 for primary `{P}`; D2 and S2 for secondary `{P}` and
  `{P,I}`, non-isomorphic);
* the shape computed from the table, with the incomparable pair's source,
  the gap, the admitting set equal to "contains P and lies under a
  maximal class", and NOT a down-set; on synthetic sets: an incomparable
  pair of maxima, a gap with unique endpoints, incomparable non-extremal
  members (no pair printed, the gap is the reason), incomparable minima,
  a full interval, a singleton, the empty set;
* how every no-P cell fails at N = 3 (256: 220 uniqueness, 36 existence
  only, in NE-and-S classes; 32: 28 and 4);
* the N = 3 table equals the committed N = 4 rows cell for cell;
* the I-redundancy observation in the secondary class, cell by cell;
* the receipt replays byte-identically into two temporary directories at
  N = 4 and equals the committed file byte for byte, LF only, in the
  tree's receipt byte convention;
* the committed receipt's headline keys; every bound-dependent result
  object carries `bounded` and `bound_reached`; every committed witness
  re-checked by the slow path (576 rows);
* terminals legal, every one but REFUSED saying "bounded" with N = 4,
  none of the Lean stage's;
* `WitnessGroupTests`: the partition of both tables recounted from the
  rows with the test's own predicates; every named witness count of
  sections 3 and 6 recounted; the no-P summary recounted;
* the Lean target names agree between the module, the receipt, and the
  numbered list in section 6, and the groups' targets are exactly them;
* every receipt key cited in this file resolves; this file makes no claim
  on the protected opens, checked by a detector that is itself tested on
  the phrasings a literal check would miss -- each forbidden verb in any
  inflection, on either side of the protected name -- and that must stay
  silent on the disclaimer sentence of section 10 (the first version of
  this section quoted those phrasings and the detector caught them);
* P2's five files are ASCII, LF, and carry none of the 102 working-denylist
  identifiers (loaded from the contact analysis, read-only).

Replay at the runner level: `run_morphism_classes.py --out receipts`, then
the same into two temporary directories under this tree and a byte
comparison (SHA-256
`6f779d207bf3ff1a8815f3521ae4ebcf9dcccdc8a7748b0916c503d9c63471bf`,
538439 bytes, for all three copies); the temporary directories were
deleted afterwards.  The commands and their exit codes are in the run's
structured report.

## 10. What this part does not do

* It does not claim OB-1, S6.6, or the S9 last bullet (the inscription
  bridge) closed, narrowed, or priced; they are out of scope
  (`not_in_scope`).
* It does not promote any cell to a carrier-general claim: every "initial"
  and every "not initial" above is finite computation, bounded by N = 4,
  until the Lean stage carries a named theorem for it.  The one cell the
  sealed theorem already names is recorded as such
  (`lean.sealed_theorem_cell`) and is still not given a terminal here.
* It does not read F3 or touch S9.1 or S9.3.
* It writes nothing sealed and nothing outside
  `research/s9_obligations/`; the receipt is written through
  `common.write_receipt` after the write-root guard.
* Recorded, not resolved: representatives are the first member in
  enumeration order, so two a != b classes are named with a = 1
  (`O10_1010`, `O10_1110`) rather than an a = 0 form; that is the declared
  rule, the members are listed under `candidates.primary.classes`, and
  section 6 says how the Lean targets reach those two cells.

## 11. Lean outcome (step 19), written by the Lean stage

AuthorityEffect: None.  This section is the Lean stage's, not P2's; it
proposes, and nothing in the receipt was changed by it
(`lean.carried_by_this_part` is still false, because the carrying is this
stage's).  Module:
`research/s9_obligations/lean/S9Obligations/MorphismClasses.lean`,
namespace `S9Obligations.MorphismClasses`, imported by
`research/s9_obligations/lean/S9Obligations.lean`; 28 theorems, each with
a `#print axioms` line in
`research/s9_obligations/lean/S9Obligations/AxiomReport.lean` and the same
name in `AXIOM_REPORT_DECLARATIONS` of `research/s9_obligations/verify_lean.py`.
Nothing under `lean4/Derivation/` was touched; the sealed names `Irrefl`,
`Transpose`, `D2`, `S2`, `D2_witness`, `D2_irrefl`, `S2_irrefl`,
`irrefl_witness_ne`, and `D2_initial_pointed` are reused, never restated,
and `D2_initial_pointed` is cited for its cell, not re-proved.

**Declared before proving.**  The menu is encoded as five predicates on a
map `f : Bool -> alpha` out of the candidate `(Bool, r0, a0, b0)` into the
object `(alpha, r, a, b)`, each the menu's one-line definition of section
1 verbatim: `PreservesPoints` (P), `PreservesEdges` (E),
`PreservesNonEdges` (NE, kept in the not -> not form and never replaced by
its contrapositive), `Injective` (I), `Surjective` (S).  A candidate is any
`r0 : Bool -> Bool -> Prop` with a pointing `a0 b0 : Bool` and `r0 a0 b0`;
that space contains the 32 raw candidates of `candidates.primary.raw_count`
and needs no transport for the two representatives pointed at `(1, 0)`, so
the transport of section 6 was not used.  The primary object class is
every `(alpha, r, a, b)` with `r a b`, on every type `alpha`; the secondary
adds `Irrefl r`.  Countermodel objects, in the receipt's legend: `SELF1`
is `(Unit, Full Unit, (), ())`, the object of the sealed
`selfdiff_consistent`; `D2` and `S2` are the sealed carriers pointed at
`(false, true)`; `FULL2` is the full relation on `Bool`; `n3:01:a0b1` is
`ThreeChain` on `Fin 3`; the doubled object `Doubled r0` on `Bool x Bool`
is this stage's uniform witness for uniqueness failures (the receipt's
first witnesses are smaller and differ, as section 6 said they might).
Every finite claim goes through `decide` with core instances (`Bool`,
`Fin 3`, the sealed `Decidable` instances for `D2` and `S2`) or explicit
case analysis; no classical choice, and `verify_lean.py` checks it.

**The fifteen proposed targets, all proved.**  Each row names the theorem
as written and what differs from section 6's proposal, if anything.

| target | theorem | statement as written | difference from the proposal |
|---|---|---|---|
| 1 | `two_element_pointed_map_unique` | for every carrier, `r a b`, and `a0 != b0`: some `f` with `PreservesPoints f a0 b0 a b`, and every `g` with `PreservesPoints g a0 b0 a b` equals `f` pointwise | stated for a general pointing, so `O10_1010` and `O10_1110` are literal instances; both pointings cite `D2_initial_pointed`, the reversed one through the sealed `Transpose`; the hypothesis `r a b` is kept although the conclusion does not use it, because the object class requires the asserted pair |
| 2 | `D2_initial_P_E` | some `f` with P at `(false, true)` and `PreservesEdges D2 r f`, and every `g` with both equals `f` | none; cites `D2_initial_pointed` |
| 3 | `FULL2_initial_P_NE` | some `f` with P at `(false, true)` and `PreservesNonEdges FULL2 r f`, and every `g` with both equals `f` | none |
| 4 | `no_injection_into_point` | `Full Unit () ()` and no `f : Bool -> Unit` is `Injective` | the proposal's `f false = f true` is the `rfl` inside; the object is stated with it |
| 5 | `no_surjection_onto_three` | `Full (Fin 3) 0 0` and no `f : Bool -> Fin 3` is `Surjective` | the proposal's existential is the internal lemma, decided over `Fin 3`; the object is stated with it |
| 6 | `two_copies_not_unique` | `Doubled r0` asserts `((a0,false),(b0,false))`, and two maps `f1`, `f2` exist that differ at some `t` and both preserve edges and non-edges | none |
| 7 | `diagonal_candidate_not_pointed_into_D2` | no `f : Bool -> Bool` has `PreservesPoints f o o false true` | none |
| 8 | `extra_edge_not_into_D2` | for `a0 != b0` and some `(x, y) != (a0, b0)` with `r0 x y`: no `f` with P into `(false, true)` has `PreservesEdges r0 D2 f` | none |
| 9 | `non_edge_not_into_point` | for some `not r0 x y`: no `f : Bool -> Unit` has `PreservesNonEdges r0 (Full Unit) f` | `Full Unit` in place of the proposal's bare `True` |
| 10 | `pointed_map_injective_of_irrefl` | `Irrefl r`, `r a b`, `a0 != b0`: every `f` with P is `Injective` | conclusion strengthened from `f false != f true` to injectivity, which the I-cells need; general pointing |
| 11 | `S2_initial_P_NE_irrefl` | `Irrefl r`, `r a b`: some `f` with P at `(false, true)` and `PreservesNonEdges S2 r f`, and every such `g` equals `f` | none |
| 12 | `S2_not_P_E_into_D2` | no `f` with P at `(false, true)` into `(false, true)` has `PreservesEdges S2 D2 f` | none |
| 13 | `D2_not_P_NE_into_S2` | no `f` with P at `(false, true)` into `(false, true)` has `PreservesNonEdges D2 S2 f` | none |
| 14 | `no_surjection_onto_three_irrefl` | `Irrefl ThreeChain`, `ThreeChain 0 1`, and no `f : Bool -> Fin 3` is `Surjective` | none |
| 15 | `two_irrefl_copies_not_unique` | `Irrefl (Doubled r0)`, the asserted pair, and `f1`, `f2` as in 6 with `Injective f1` and `Injective f2` added | injectivity added, so the classes containing I are covered too |

**Thirteen further theorems.**  Two helpers, `not_both` and
`injective_of_ne`.  Three literal initiality statements for the I-cells of
the secondary class, each with I as a hypothesis on the morphism:
`two_element_initial_P_I_irrefl` for (`{P,I}`, D2) and (`{P,I}`, S2),
`D2_initial_P_E_I_irrefl` for (`{P,E,I}`, D2), `S2_initial_P_NE_I_irrefl`
for (`{P,NE,I}`, S2).  Four per-class verdicts over the primary object
class, stated with a class as data (`MClass`, one flag per menu condition,
`C.Cond` the conjunction of the conditions in `C`, `C.InitialPrimary` the
initiality of a candidate for `C` over every object on every carrier):

* `initial_P_iff`: a candidate is initial for `{P}` exactly when
  `a0 != b0`;
* `initial_P_E_iff`: a candidate is initial for `{P,E}` exactly when
  `a0 != b0` and it asserts no pair beyond `(a0, b0)`;
* `initial_P_NE_iff`: a candidate with decidable `r0` is initial for
  `{P,NE}` exactly when `a0 != b0` and it asserts every pair --
  decidability of the candidate's relation, which every finite candidate
  has, is what turns "no non-edge" into "every pair", and is the one
  place it is assumed;
* `not_initial_P_E_NE`: no candidate is initial for `{P,E,NE}`.

And four class-level statements, over all 32 classes at once:

* `admits_primary_iff`: `C` leaves some two-element object initial over
  the primary object class exactly when `C` contains P, contains neither
  I nor S, and does not contain both E and NE;
  `admits_primary_exactly`: exactly `{P}`, `{P,E}`, `{P,NE}`, decided over
  the 32 classes.  That is `shape.primary.admitting_classes` on every
  carrier.
* `admits_secondary_iff`: over the secondary object class, exactly when
  `C` contains P, does not contain S, and does not contain both E and NE;
  `admits_secondary_exactly`: exactly `{P}`, `{P,E}`, `{P,NE}`, `{P,I}`,
  `{P,E,I}`, `{P,NE,I}`.  That is `shape.secondary.admitting_classes` on
  every carrier, and the I-redundancy observation of section 5 is now
  the theorem `pointed_map_injective_of_irrefl` inside it.

**Which cells are carried, and by what.**  Every cell of both tables.
Primary, by the receipt's partition
(`witness_groups.primary.partition_cell_counts` = [256, 128, 64, 8, 8, 16,
16, 16]): `I_classes` (256) by `no_injection_into_point`;
`S_without_I_classes` (128) by `no_surjection_onto_three`;
`no_P_I_S_classes` (64) by `two_copies_not_unique`; `P_class_initial` (8)
and `P_class_non_initial` (8) by `initial_P_iff` (the former also by
`two_element_pointed_map_unique`, the latter also by
`diagonal_candidate_not_pointed_into_D2`); `P_E_class` (16) by
`initial_P_E_iff` (its one initial cell also by `D2_initial_P_E`, its 8
diagonal cells also by target 7, its 7 off-diagonal cells also by target
8); `P_NE_class` (16) by `initial_P_NE_iff` (its one initial cell also by
`FULL2_initial_P_NE`, its diagonal cells also by target 7, its
off-diagonal non-full cells also by target 9); `P_E_NE_class` (16) by
`not_initial_P_E_NE`.  Secondary
(`witness_groups.secondary.partition_cell_counts` = [32, 16, 8, 8]):
`S_classes` (32) by `no_surjection_onto_three_irrefl`;
`no_P_no_S_classes` (16) by `two_irrefl_copies_not_unique`;
`P_without_S_initial` (8) by `two_element_pointed_map_unique` (`{P}`, both
candidates), `two_element_initial_P_I_irrefl` (`{P,I}`, both),
`D2_initial_P_E` (`{P,E}`, D2), `D2_initial_P_E_I_irrefl` (`{P,E,I}`, D2),
`S2_initial_P_NE_irrefl` (`{P,NE}`, S2), `S2_initial_P_NE_I_irrefl`
(`{P,NE,I}`, S2); `P_without_S_non_initial` (8) by `S2_not_P_E_into_D2`
(the four S2 cells, whose classes all contain P and E) and
`D2_not_P_NE_into_S2` (the four D2 cells, whose classes all contain P and
NE).  Cells without a Lean theorem: none.

What that assignment is, and is not.  For the per-class verdict theorems
the table's verdict in a cell is the right-hand side evaluated at the
candidate: for `{P,E}` it holds of `O01_0100` alone among the 16
representatives listed under `candidates.primary.classes`, for `{P,NE}`
of `O01_1111` alone, for `{P}` of the 8 with `a0 != b0`, and for
`{P,E,NE}` of none -- which is the table
(`witness_groups.primary.groups.P_E_class.initial` = 1,
`witness_groups.primary.groups.P_NE_class.initial` = 1,
`witness_groups.primary.groups.P_class_initial.cells` = 8,
`initial_objects_by_class.primary.by_class.{P,E,NE}` = []).  Reading the
right-hand side off the 16 listed relations was a finite inspection
recorded here by the Lean stage, which did not own P2's test file; since
the repair after full-run audit 1 it is the test
`test_per_class_right_hand_sides_match_the_table_at_the_candidates` in
`test_morphism_classes.py`, which evaluates the four right-hand sides at
every primary candidate (and at every member of its class) and compares
them with the sweep at N = 3 and with the committed rows at N = 4 --
finite computation bounded by N = 4; no Lean statement reads the
receipt.  The class-level theorems do not depend on that assignment.

**What stays finite computation, bounded by N = 4.**  The sweep as a
procedure: `sweep` and `sweep_direct` still live in Python only, and no
Lean statement says that every object with carrier at most 4 was visited
(`python_only_scope.reproduces_s9_fifth_bullet` stays true; the terminal
PYTHON_ONLY_SCOPE_DECLARED stands as P2 emitted it).  The 576 table rows
with their first-witness columns (`tables.primary.row_count`,
`tables.secondary.row_count`), the witness-carrier counts, and the
per-group witness counts of section 3 are facts about the sweep's
enumeration order and remain finite computation; this stage's
countermodel objects are uniform and are not the receipt's first
witnesses.  The tie count 8 for `{P}` is the number of isomorphism
classes with `a0 != b0` under the implemented `pointed_isomorphic`, a
Python quotient (`ties.primary.per_class.{P}.count`); that the 8 are all
initial on every carrier is `initial_P_iff`.  Nothing was computed at
N = 5; the theorems set no carrier bound, and REFUSED stands unchanged.

**Terminals of the Lean stage, each with its scope.**  These are not in
the receipt (`terminals` holds P2's own), by the receipt's own rule
(`lean.note`).

* LEAN_CARRIED -- targets 1-15 of `lean.proposed_target_names`, every one
  proved under the theorem named in the table above, with the stated
  differences; no target was weakened, and nothing was dropped from any
  statement.
* LEAN_CARRIED -- the thirteen further theorems named above, including
  the four per-class verdicts and the four class-level statements.
* S9_2_CLASSES_CLASSIFIED -- object class primary: on every carrier,
  within the declared five-condition menu and for candidates that are
  pointed relations on `Bool` with the asserted pair, the classes leaving
  some two-element object initial are exactly `{P}`, `{P,E}`, `{P,NE}`
  (`admits_primary_exactly`); which candidates are initial for those
  classes and for `{P,E,NE}` is `initial_P_iff`, `initial_P_E_iff`
  (`initial_P_NE_iff` for decidable candidates), `not_initial_P_E_NE`;
  every other class has no initial candidate by `no_injection_into_point`,
  `no_surjection_onto_three`, `two_copies_not_unique`.  Each of the 512
  cells of `tables.primary` therefore has a Lean theorem for its verdict,
  the per-class right-hand sides being evaluated at the 16 candidates by
  the test named in section 11 since the repair after full-run audit 1
  (a finite inspection before it; this clause added by the synthesis
  pass's repair round 1 and revised by that repair); the table as an
  artifact, and the sweep that produced it, stay finite computation
  bounded by N = 4.
* S9_2_CLASSES_CLASSIFIED -- object class secondary: on every carrier,
  within the same menu and for irreflexive candidates on `Bool` with the
  asserted pair, the classes leaving some two-element object initial are
  exactly `{P}`, `{P,E}`, `{P,NE}`, `{P,I}`, `{P,E,I}`, `{P,NE,I}`
  (`admits_secondary_exactly`); each of the 64 cells of `tables.secondary`
  has a Lean theorem for its verdict, by the per-cell theorems of the
  assignment above; the table as an artifact stays finite computation
  bounded by N = 4.  No per-class "which candidate" theorem was stated
  over irreflexive candidates in general; the cells are the two
  representatives D2 and S2.
* LEAN_CARRIED -- S9_2_INCOMPARABLE_CLASSES, both object classes: the
  admitting sets are carrier-general by `admits_primary_exactly` and
  `admits_secondary_exactly`; that each set is not an interval under
  inclusion, with the incomparable maximal pair and the gap `{P,E,NE}`
  that P2 printed, is the same finite set property read off the listed
  classes, and no Lean statement of "not an interval" was written.
* LEAN_CARRIED -- TIES_RETAINED, both object classes: every candidate with
  `a0 != b0` is initial for `{P}` on every carrier (`initial_P_iff`), and
  D2 and S2 are both initial for `{P}` and `{P,I}` over irreflexive
  objects (`two_element_pointed_map_unique`,
  `two_element_initial_P_I_irrefl`) while not pointed-isomorphic (the
  sealed `D2_not_pointed_iso_S2`); the counts 8, 2, 2 are the sizes of
  Python quotients and stay finite computation bounded by N = 4.
* LEAN_NOT_CARRIED -- the receipt's table as an object: no Lean statement
  reads the 576 rows, the first-witness columns, or the sweep's
  enumeration, and their agreement with the theorems is the finite
  inspection recorded above; that scope is Python's, bounded by N = 4,
  and PYTHON_ONLY_SCOPE_DECLARED names it.
* MANUAL_RECEIPT_DECLARED -- the 51 `#print axioms` reports of this tree
  (23 of P1, 28 of this stage) are read by no CI gate; `verify_lean.py` is
  run by hand, and a committed report implies no enforcement.
* REFUSED -- unchanged from P2: nothing was computed at N = 5; the
  theorems of this stage quantify over types and set no carrier bound.

The three protected opens of step 36 are untouched by this stage, which
says nothing about them.  It names no external theory and writes no
prose proof: every argument is inside the Lean file.

**Receipts of this stage.**  `cd research/s9_obligations/lean && lake
build`: exit 0, last line `Build completed successfully (8 jobs)`.
`python research/s9_obligations/verify_lean.py`: exit 0, counts line
`Lean #print axioms declarations: 51 within ['Quot.sound', 'propext']`,
5 sources scanned for forbidden tokens.  The 28 report lines, verbatim
from `lake env lean S9Obligations/AxiomReport.lean`:

```
'S9Obligations.MorphismClasses.not_both' does not depend on any axioms
'S9Obligations.MorphismClasses.injective_of_ne' does not depend on any axioms
'S9Obligations.MorphismClasses.two_element_pointed_map_unique' does not depend on any axioms
'S9Obligations.MorphismClasses.D2_initial_P_E' does not depend on any axioms
'S9Obligations.MorphismClasses.FULL2_initial_P_NE' does not depend on any axioms
'S9Obligations.MorphismClasses.no_injection_into_point' does not depend on any axioms
'S9Obligations.MorphismClasses.no_surjection_onto_three' depends on axioms: [propext, Quot.sound]
'S9Obligations.MorphismClasses.two_copies_not_unique' does not depend on any axioms
'S9Obligations.MorphismClasses.diagonal_candidate_not_pointed_into_D2' does not depend on any axioms
'S9Obligations.MorphismClasses.extra_edge_not_into_D2' depends on axioms: [propext, Quot.sound]
'S9Obligations.MorphismClasses.non_edge_not_into_point' does not depend on any axioms
'S9Obligations.MorphismClasses.pointed_map_injective_of_irrefl' does not depend on any axioms
'S9Obligations.MorphismClasses.two_element_initial_P_I_irrefl' does not depend on any axioms
'S9Obligations.MorphismClasses.D2_initial_P_E_I_irrefl' does not depend on any axioms
'S9Obligations.MorphismClasses.S2_initial_P_NE_irrefl' does not depend on any axioms
'S9Obligations.MorphismClasses.S2_initial_P_NE_I_irrefl' does not depend on any axioms
'S9Obligations.MorphismClasses.S2_not_P_E_into_D2' does not depend on any axioms
'S9Obligations.MorphismClasses.D2_not_P_NE_into_S2' does not depend on any axioms
'S9Obligations.MorphismClasses.no_surjection_onto_three_irrefl' depends on axioms: [propext, Quot.sound]
'S9Obligations.MorphismClasses.two_irrefl_copies_not_unique' does not depend on any axioms
'S9Obligations.MorphismClasses.initial_P_iff' does not depend on any axioms
'S9Obligations.MorphismClasses.initial_P_E_iff' depends on axioms: [propext, Quot.sound]
'S9Obligations.MorphismClasses.initial_P_NE_iff' does not depend on any axioms
'S9Obligations.MorphismClasses.not_initial_P_E_NE' does not depend on any axioms
'S9Obligations.MorphismClasses.admits_primary_iff' depends on axioms: [propext, Quot.sound]
'S9Obligations.MorphismClasses.admits_primary_exactly' depends on axioms: [propext, Quot.sound]
'S9Obligations.MorphismClasses.admits_secondary_iff' depends on axioms: [propext, Quot.sound]
'S9Obligations.MorphismClasses.admits_secondary_exactly' depends on axioms: [propext, Quot.sound]
```

Files of this stage: the module, the root import line, the 28 report
lines, the 28 inventory entries, and this section.  Nothing else in this
tree, and nothing sealed, was written; the receipt and P2's tests were
not edited, and the tree's denylist scan (102 identifiers) finds no leak
in any of them.
