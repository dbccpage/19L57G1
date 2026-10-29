# Unit 37. An inventory is not a derivation

**Claim.** With two fixed points and no arrows from a point to itself,
there are exactly four possible arrow patterns. Listing them does not
choose one of them.

**Status:** conditional classification for decidable relations on the
declared two-point carrier; the classification scheme is admitted.
**Lean:** `ObserverInventory.bool_irrefl_full_classification`.

## Question

Does listing every pattern allowed by a rule also tell us which pattern
to choose?

## First pass: two dots and two separate questions

Draw two dots called A and B. We will keep their labels fixed.
An arrow from A to B means that the ordered pair `(A, B)` belongs to
our **relation**: a collection of allowed ordered pairs. An arrow back
from B to A is a different ordered pair.

For this example, adopt one rule: **no arrow may start and end at the
same dot**. Such an arrow is called a *self-loop*. The formal name for
our rule is **irreflexivity**.

After ruling out the two self-loops, two questions remain:

1. Is there an arrow from A to B?
2. Is there an arrow from B to A?

Answering each question with yes or no gives this complete table:

| A to B? | B to A? | Picture | Source name |
|---|---|---|---|
| No | No | A and B, with no arrows | `EmptyRel` |
| Yes | No | A → B | `D2` |
| No | Yes | A ← B | `D2rev` |
| Yes | Yes | A ↔ B | `S2` |

The Lean version uses `false` for dot A and `true` for dot B.
Those are the dots' labels; they are separate from the yes/no answer
about whether an arrow is present. The Python version uses 0 and 1.

The points stay labelled. Swapping the labels can relate the two
one-arrow pictures, but they are different relations on these fixed
points: they answer the question “A to B?” differently.

## A complete list still leaves a choice

The table is a **classification**: every pattern allowed by the rule
appears in one of its rows. You can check completeness without guessing:
the first answer is yes or no; for either answer, the second is yes or
no. That produces the four rows.

The rule has not told us which row to use. The empty picture obeys it,
and so does A → B. These two different examples are enough to refute
“the no-self-loop rule determines one relation.”

If we add a requirement that *exactly one* arrow be present, two rows
remain. If we further require an arrow from A to B, one row remains.
The extra selection came from extra requirements. It was not hidden
inside the original rule.

The formal classification takes a decidability assumption: for every
ordered pair, an answer to its membership question is available. It
proves that the relation equals one of the four named relations. That
statement by itself does not also prove the names denote distinct
relations; the book supplies the pairwise distinction arguments.

## A word can hide a choice of operation or question

“Reverse the picture” can mean two different operations:

- **Transpose:** reverse each arrow, keeping the dots in place.
- **Swap:** exchange the dots' labels, carrying each arrow along.

Both turn A → B into A ← B. Agreement on that example does not make
them the same operation on every relation. To test the difference, allow
a self-loop temporarily. Transposing a loop at A leaves it at A;
swapping the dots moves it to B. This test relation is outside our
no-self-loop classification, but inside the larger set of all relations
on the two dots.

Likewise, “summarize the picture with a number” does not specify a
question. Counting its arrows gives 1 on A → B. Reporting 1 if *both*
opposite arrows are present, and 0 otherwise, gives 0 on that same
picture. Each number answers its own declared question. The source
calls these two summaries *residuals*.

## Outside the system: using the lesson elsewhere

These are results about the declared two-dot model. The theorem does not
establish that a real situation has only four possible explanations.

Ask three questions separately: **What are the candidates? What rules
restrict them? What further evidence or requirement selects among them?**
A list of possible explanations does not by itself identify the true
explanation of an event. In the arrow model we can prove the list is
complete because we declared the dots and rules. Applying a similar
list to real observations requires checking whether those modelling
choices fit the situation and whether alternatives were left out.
The four-row theorem does not perform that empirical check.

The same caution applies to this textbook's coverage index. A source
name on a list establishes a reference. Whether its meaning is explained
well requires reading the lesson and testing understanding.

## Student exercise: try before opening the answers

With fixed dots C and D and no self-loops, require exactly one arrow.
Which patterns remain?

1. Require exactly one arrow. Describe every remaining picture.
2. Also forbid an arrow from C to D. Which picture remains? Which new
   requirement made that selection possible?
3. Someone tests transpose and swap on all four no-self-loop pictures
   and concludes the operations agree on every relation. What test
   picture would challenge that conclusion, and what happens to it?
4. Someone says the arrow table proves that a real situation has only
   four possible explanations. What must they justify before using it
   that way?

The answers are at the end. The formal walkthrough below is optional
on a first reading. The [formal-reading guide](../reading_formal_statements.md)
explains how to read its assumptions and symbols.

<details>
<summary>Formal definitions, source record, proofs, and executable checks</summary>

**Claim.** On the two-point carrier `Bool`, every decidable irreflexive
relation is one of exactly four: the empty relation, `D2`, `D2rev` or `S2`
(`bool_irrefl_full_classification`). Around that census the module files
nine *slots* of existing objects (`carrier`, `local_state`, `support`,
`defect`, `reversal`, `closure`, `residual`, `maps`, `terminal`), and in
each slot it proves that a tempting uniqueness claim fails: two witness
assignments exist as data, two reversal maps agree on `D2` and differ
elsewhere, two residuals disagree on `D2`, two local states satisfy the
irreflexivity law. The slot names are a *declared* classification; the
theorems are derived; nothing here authorizes a response to a demand.
**Status:** derived (census and residuals), declared metatheory (the slot
classification). **Lean:** `ObserverInventory.bool_irrefl_full_classification`
(`lean4/Derivation/ObserverInventory.lean` lines 74-111), `witnesses_are_data`
(124-138), `collision_is_not_obstruction` (145-147), `transpose_ne_pushNot`
(185-194), `residuals_not_unique` (212-216), with the supporting
equalities at 63-66, 154-183, 198-229. **Axioms:**
`bool_irrefl_full_classification` `propext, Quot.sound`;
`witnesses_are_data` `propext`; `transpose_ne_pushNot`,
`residuals_not_unique` none. **Depends on:** `Irrefl`, `Sym`, `Transpose`,
`D2`, `D2rev`, `S2` and their facts (Units 14, 15, 23-25); the carrier swap
(`PrimDiff.swap_auto_of_S2_not_of_D2`) and Bridge's equivariance obstruction
(`Bridge.equivariant_not_D2`, `lean4/Derivation/Bridge.lean` lines 244-281;
audited in `textbook/audit/modules/Bridge.md`, not yet a unit of its own).

## Question

Units 23 to 25 proved facts *about* `D2` under irreflexivity. A reader
may now want to know what else is on the table. On two points, how many
irreflexive relations are there at all? Is the oriented witness forced?
Is "reversal" one operation? Is "the residual" one number? Does the
irreflexivity law pick out a state? The module answers each by exhibiting
the objects, and the unit's title is its moral: a list of what exists,
with its names, is not a derivation of what must exist.

## What we already possess

- `Irrefl r := ∀ x, ¬ r x x` (PrimDiff line 28); `Sym r x y := r x y ∨ r y x`
  (31); `Transpose r x y := r y x` (35).
- `D2 x y := x = false ∧ y = true` (89), `D2rev x y := x = true ∧ y = false`
  (92), `S2 := Sym D2` (95); `D2_irrefl` (106), `D2_witness : D2 false true`
  (118).
- The carrier swap `Bool.not` is an automorphism of `S2` and not of `D2`
  (`swap_auto_of_S2_not_of_D2`, PrimDiff 379; the obstruction is Bridge's
  `equivariant_not_D2`).
- `CollapseCollision` and `obstruction_under_irrefl` (Unit 25).
- `Clos` and `clos_empty_id` (PrimDiff 491-502).

## New concept: a census by cases, and a slot that only names

**The census.** A relation on `Bool` is fixed by four truth values. If it
is irreflexive, the two diagonal values are `false`, leaving `r false true`
and `r true false`. Four combinations, four relations. The theorem takes
any decidable `r` with `Irrefl r`, splits on the two off-diagonal values,
and in each of the four branches proves `r = <that relation>` by
function extensionality and `propext` at each of the four points. That is
the whole proof, written out.

**The slots.** `Slot` is an inductive type with nine constructors;
`slotList` lists them; `slot_count` says the list has length nine and
`slots_nodup` that it repeats nothing. Those two theorems pin a list of
names. They derive nothing about relations. The paper's §1 records that
the names were chosen after an outside grid of single-letter names was
offered and refused (author ruling, 2026-08-31): the *content* of each
slot is internal, the names are the repository's own, and any future
claim that this inventory independently converged on an outside grid is
false by construction. The textbook repeats that note and does not
reproduce the refused names, because it does not have them.

**The per-slot refutations.** Each remaining theorem exhibits two
objects where one might have been expected.

| slot | tempting claim | what is proved instead |
|---|---|---|
| witnesses | the oriented witness is forced | `zeroW` and `oneW` both exist; `oneW`'s presence is `D2`; `zeroW ≠ oneW` |
| defect | collision is obstruction | a relation asserts its pair and is not irreflexive (`Unit`, constantly true) |
| reversal | reversal is one map | `Transpose` and `pushNot` agree on `D2`, differ on the self-loop at `false` |
| residual | the residual is one number | `edgeCount` and `isSymBit` differ on `D2` (1 vs 0) |
| terminal | `Irrefl` determines the local state | empty and `D2` both satisfy it and differ |
| maps | the swap is an automorphism | of `S2` only; not of `D2`, not of `D2rev` |
| closure | | the empty operation family closes to the identity (`clos_empty_id`, restated) |

## Plain-language interpretation

Suppose you have two dots and may draw arrows between them, but never
from a dot to itself. You can draw nothing, an arrow one way, an arrow
the other way, or both. That is all. Nothing in that list is special
unless something *else* makes it special: the rule "no arrow to itself"
is satisfied by the empty picture as much as by the one-arrow picture, so
the rule does not choose. "Reverse the picture" sounds like one
instruction, but "flip every arrow" and "swap the two dots" are different
instructions that happen to agree on the one-arrow picture. "How much is
drawn" sounds like one number, but counting arrows and asking "is it
symmetric?" are different numbers. And "a drawing in which an arrow comes
back to its own dot" is a thing that can exist; it is only *forbidden*
once you adopt the no-self-arrow rule, which is Unit 24's conditional.

What the inventory does not do is tell you which picture to draw next.
The irreflexivity law of Units 24 and 25 is a hypothesis, not a derived
fact (Unit 26 proves the facts never entail it); the inventory is
consistent with that and adds nothing to it.

## Pseudocode

```
# Gloss
census(r):                     -- r irreflexive, decidable
  case (r false true, r true false) of
    (true,  true)  -> r = S2
    (true,  false) -> r = D2
    (false, true)  -> r = D2rev
    (false, false) -> r = EmptyRel
  -- in each case: for all x y, r x y <-> <relation> x y, by the four points

transpose r x y := r y x                       -- flip every arrow
pushNot   r x y := r (not x) (not y)           -- swap the two dots
edgeCount r := [r false true] + [r true false]
isSymBit  r := [r false true and r true false]
```

## Python

```python
import itertools
from derivation.observer_inventory import local_states, edge_count, is_sym_bit
from derivation.primdiff import CARRIER_SWAP, pushforward, transpose

pairs = [(x, y) for x in range(2) for y in range(2)]
every = [frozenset(p for p, on in zip(pairs, bits) if on)
         for bits in itertools.product((False, True), repeat=4)]
irr = [r for r in every if all((x, x) not in r for x in range(2))]
states = local_states()
print(len(every), len(irr), frozenset(irr) == frozenset(states.values()))
D2, S2 = states["D2"], states["S2"]
print(transpose(D2) == pushforward(D2, CARRIER_SWAP))
loop = frozenset({(0, 0)})
print(set(transpose(loop)), set(pushforward(loop, CARRIER_SWAP)))
print(edge_count(D2), is_sym_bit(D2), edge_count(S2), is_sym_bit(S2))
```

Output:

```text
16 4 True
True
{(0, 0)} {(1, 1)}
1 0 2 1
```

The check script's full output, each line compared with
`artifacts/observer_inventory.json`:

```text
relations on two points: 16; irreflexive: 4; they are exactly ['D2', 'D2rev', 'S2', 'empty']: True
reversal: transpose(D2) = D2rev True, push_swap(D2) = D2rev True, agree on D2 True; on the self-loop {(0, 0)}: transpose {(0, 0)}, push_swap {(1, 1)}
residuals: edge_count D2 1, S2 2; is_sym_bit D2 0, S2 1; disagree on D2 True
witnesses: zero != one True, presence of one is D2 True; defect: D2 collides under the merge True and stays irreflexive True; the one-point self-loop is not irreflexive True
slots: 9 ['carrier', 'local_state', 'support', 'defect', 'reversal', 'closure', 'residual', 'maps', 'terminal']
failures: []
```

## Line-by-line Python explanation

`every` builds all sixteen relations on `{0, 1}` as frozensets of pairs by
running through the sixteen choices of four bits. `irr` keeps those with
no diagonal pair; there are four, and they are the four named states
from Genesis's `local_states()`. This is the Python census: brute force
where Lean does cases.

`transpose(D2) == pushforward(D2, CARRIER_SWAP)`: on `D2` the two
reversal maps agree. On the self-loop `{(0, 0)}` they do not: flipping
the arrow leaves it at `0`; swapping the dots moves it to `1`. The
self-loop is not irreflexive, so it is outside the census, and that is
exactly where the two maps come apart. On the four irreflexive states
they agree everywhere (`transpose` and `pushNot` both exchange `D2` and
`D2rev` and fix the other two), so a reader who only ever looks at
irreflexive states cannot tell the maps apart. Lean's witness is the
same relation, written `fun x y => x = false ∧ y = false`.

`edge_count` and `is_sym_bit` are two numbers one might call "the
residual". On `D2` they are `1` and `0`. Neither is wrong; they are
different questions.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/ObserverInventory.lean lines 58-66, 74-83
def EmptyRel : Bool → Bool → Prop := fun _ _ => False

theorem empty_irrefl : Irrefl EmptyRel := fun _ h => h

theorem empty_ne_D2 : EmptyRel ≠ D2 := by
  intro h
  have : EmptyRel false true := h ▸ D2_witness
  exact this

theorem bool_irrefl_full_classification (r : Bool → Bool → Prop)
    [inst : ∀ x y, Decidable (r x y)] (hi : Irrefl r) :
    r = EmptyRel ∨ r = D2 ∨ r = D2rev ∨ r = S2 := by
  by_cases hft : r false true
  · by_cases htf : r true false
    · right; right; right
      funext x y
      apply propext
      cases x <;> cases y
      · exact ⟨fun h => absurd h (hi false), fun h => absurd h (by decide)⟩
      · exact ⟨fun _ => Or.inl (by decide), fun _ => hft⟩
      · exact ⟨fun _ => Or.inr (by decide), fun _ => htf⟩
      · exact ⟨fun h => absurd h (hi true), fun h => absurd h (by decide)⟩
    · right; left
      ...   -- the D2 branch, the same four points
  · by_cases htf : r true false
    · right; right; left
      ...   -- the D2rev branch
    · left
      ...   -- the empty branch
```

```lean
-- Lean (Genesis), lean4/Derivation/ObserverInventory.lean lines 145-147, 151, 185-194, 204-216
theorem collision_is_not_obstruction :
    ∃ r : Unit → Unit → Prop, r () () ∧ ¬ Irrefl r :=
  ⟨fun _ _ => True, trivial, fun hi => hi () trivial⟩

def pushNot (r : Bool → Bool → Prop) : Bool → Bool → Prop :=
  fun x y => r (Bool.not x) (Bool.not y)

theorem transpose_ne_pushNot :
    ∃ r : Bool → Bool → Prop, Transpose r ≠ pushNot r := by
  let r : Bool → Bool → Prop := fun x y => x = false ∧ y = false
  refine ⟨r, ?_⟩
  intro h
  have ht : Transpose r false false := ⟨rfl, rfl⟩
  have eqp : Transpose r false false = pushNot r false false :=
    congrFun (congrFun h false) false
  have hp : pushNot r false false := eqp ▸ ht
  exact Bool.noConfusion hp.1

def edgeCount (r : Bool → Bool → Prop)
    [∀ x y, Decidable (r x y)] : Nat :=
  (if r false true then 1 else 0) + (if r true false then 1 else 0)

def isSymBit (r : Bool → Bool → Prop)
    [∀ x y, Decidable (r x y)] : Nat :=
  if r false true then (if r true false then 1 else 0) else 0

theorem residuals_not_unique :
    edgeCount D2 = 1 ∧ edgeCount S2 = 2 ∧
      isSymBit D2 = 0 ∧ isSymBit S2 = 1 ∧
      edgeCount D2 ≠ isSymBit D2 := by
  decide
```

The book's Lean shows the four census members are distinct, applies the
census at a member Genesis does not apply it to, exhibits a relation
outside the census, proves `pushNot` is an involution as Genesis proves
`Transpose` is, finds the fixed point of transposition, fills in the
residuals on the other two states, and reads the witness data at the
oriented pair.

```lean
-- Lean (book), textbook/checks/u37_lean.py
theorem D2_ne_D2rev : D2 ≠ D2rev := by
  intro h
  have : D2rev false true := h ▸ D2_witness
  exact Bool.noConfusion this.1

theorem D2rev_irrefl : Irrefl D2rev := by
  intro x ⟨h1, h2⟩
  rw [h1] at h2
  exact Bool.noConfusion h2

theorem census_at_D2rev :
    D2rev = EmptyRel ∨ D2rev = D2 ∨ D2rev = D2rev ∨ D2rev = S2 :=
  bool_irrefl_full_classification D2rev D2rev_irrefl

theorem loop_not_irrefl : ¬ Irrefl (fun x y : Bool => x = false ∧ y = false) :=
  fun hi => hi false ⟨rfl, rfl⟩

theorem pushNot_involutive (r : Bool → Bool → Prop) : pushNot (pushNot r) = r := by
  funext x y
  simp [pushNot]

theorem transpose_S2 : Transpose S2 = S2 := by
  funext x y
  apply propext
  show (D2 y x ∨ D2 x y) ↔ (D2 x y ∨ D2 y x)
  exact Or.comm

theorem residuals_rest :
    edgeCount EmptyRel = 0 ∧ isSymBit EmptyRel = 0 ∧
    edgeCount D2rev = 1 ∧ isSymBit D2rev = 0 := by
  decide

theorem witness_presence : (0 < oneW false true) ∧ ¬ (0 < zeroW false true) := by
  decide

theorem irrefl_underdetermined : Irrefl EmptyRel ∧ Irrefl D2 ∧ EmptyRel ≠ D2 :=
  ⟨empty_irrefl, D2_irrefl, empty_ne_D2⟩

theorem swap_auto_S2_only :
    (∀ x y, S2 x y ↔ S2 (!x) (!y)) ∧ ¬ (∀ x y, D2 x y ↔ D2 (!x) (!y)) := by
  decide
```

## Line-by-line Lean explanation

**`EmptyRel`, `empty_irrefl`, `empty_ne_D2`.** The empty relation is irreflexive because it holds at no pair,
including every self-pair. It is
not `D2`: if it were, rewriting `D2_witness` along the equality would give
a proof of `False`.

**`bool_irrefl_full_classification`.** `by_cases` on `r false true`, then
on `r true false`: four branches. In each, `right`/`left` select the
disjunct, `funext x y` reduces the equation of relations to an equation
of propositions at each `x y`, `propext` reduces that to an iff, and
`cases x <;> cases y` gives the four points. At a diagonal point both
sides are false: the left by `hi`, the right by `decide` on the concrete
relation. At an off-diagonal point the hypothesis `hft` or `htf`, or its
negation, decides the left and `decide` the right. Sixteen pointwise equivalences across the four branches. Each branch checks
the four ordered pairs; the displayed excerpt abbreviates three branches. The decidability
instance is what lets `by_cases` run on an arbitrary `r`.

**`collision_is_not_obstruction`.** On the one-point carrier `Unit`, the
constantly true relation asserts `() ()` and is not irreflexive. That is
all the statement says. The docstring draws a further moral, that
"collision of a map is not the same reading as obstruction relative to
`Irrefl`"; the audit records that neither collision (Unit 25's
`CollapseCollision`) nor obstruction occurs in the statement, so the
moral rests on PrimDiff's `collapse_unobstructed_without_fidelity` and
`obstruction_under_irrefl`, which the ledger cites alongside it. The
name promises more than the theorem; read the theorem.

**`pushNot`, `transpose_ne_pushNot`.** `pushNot` is pushforward along the
carrier swap. The witness `r` holds only at `(false, false)`. Its
transpose still holds there (`⟨rfl, rfl⟩`); if the two maps were equal,
`pushNot r false false`, which unfolds to `r true true`, would hold, and
its first conjunct `true = false` is refuted by `Bool.noConfusion`.

**`edgeCount`, `isSymBit`, `residuals_not_unique`.** Two `Nat`-valued
readings of a decidable relation. `decide` evaluates all five conjuncts
on the concrete `D2` and `S2`.

**Book: the four are four.** `D2_ne_D2rev`, `D2rev_ne_S2`, `empty_ne_S2`
use a pair where one relation holds and the other does not. Transporting
membership along a proposed equality gives a contradiction. Together with
the native `empty_ne_D2` and the exercise's `empty_ne_D2rev` and `D2_ne_S2`,
these cover all six pairs of names. The two exercise solutions are now
also kernel-checked in the book script; try the exercise before reading
them.

**Book: `D2rev_irrefl`, `census_at_D2rev`.** `D2rev x x` would give
`x = true` and `x = false`; rewriting one into the other gives
`true = false`. The census then applies to `D2rev` and returns a
disjunction whose third disjunct is `rfl`. This is the sanity check a
reader should run on any classification theorem: feed it one of its own
members.

**Book: `loop_not_irrefl`.** The reversal witness is outside the census,
by exhibiting `false` as a point with a self-loop.

**Book: `pushNot_involutive`, `transpose_S2`.** Genesis proves
`Transpose` is an involution; the book proves the same for `pushNot`
(`Bool.not` is an involution, which `simp` knows). `transpose_S2`: the
symmetrization is its own transpose, by commuting a disjunction. So on
the census, transposition fixes two members and swaps two, and so does
`pushNot`; they are different maps that induce the same permutation of
the four irreflexive states.

**Book: `residuals_rest`, `witness_presence`.** The residual table is
completed on `EmptyRel` and `D2rev`; the witness data are read at
`(false, true)`: `oneW` is positive there and `zeroW` is not. Note the
axioms: `witness_presence` reports `propext` because `¬ (0 < 0)` is
decided through a `Decidable` instance built with propositional
rewriting; the other `decide` theorems report none.

**Book: `irrefl_underdetermined`, `swap_auto_S2_only`.** The terminal
slot's content as one conjunction, from three Genesis theorems; and the
maps slot re-decided on the concrete relations.

**Axioms.** The census uses `propext` (for `funext` on `Prop`-valued
functions) and `Quot.sound` (through `funext`). The two `decide` theorems
of Genesis and most of the book's use none.

## What has been proved

- Every decidable irreflexive relation on `Bool` is one of four named
  ones (Genesis, derived); the four are pairwise distinct (Genesis for
  one pair, book for three more).
- In the witness, defect, reversal, residual, terminal and maps slots,
  the specific uniqueness claim named in the table above fails, each by
  an explicit pair of objects (Genesis, derived).
- The nine slot names form a list of nine distinct constructors
  (Genesis, `decide`): a fact about a list, not about relations.

## What has not been proved

- That the nine slots are the right carving, or a complete one. The
  paper's header says so: "a declared classification of existing
  objects", "nothing below treats the carving as derived".
- That `Irrefl` is the law to adopt. The module assumes it where it
  assumes anything (the census hypothesis) and otherwise studies its
  consequences; Unit 26 proves the facts never entail it.
- Anything about carriers with three or more points. The census is
  `Bool`-specific; on three points there are 64 irreflexive relations and
  no classification is attempted.
- That `collision_is_not_obstruction` relates collision to obstruction
  (see the Lean explanation). The ledger's wording is the one to cite.
- An earlier terminal-slot sentence, "no next state is a function of the
  carrier and local state", was withdrawn by the authors as a
  non-sequitur (the identity is such a function). The current sentence,
  "irreflexivity does not determine the local state", is what
  `irrefl_underdetermined` proves.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `Bool` as the carrier | the two points | metatheory type standing for an admitted two-element carrier |
| `[∀ x y, Decidable (r x y)]` | `by_cases`, `edgeCount`, `decide` | metatheory; the census is over *decidable* relations only |
| `Nat` in `zeroW`, `oneW`, `edgeCount`, `isSymBit` | witness counts and residuals | metatheory data supplied from outside; the paper calls them "data", not derived |
| `funext`, `propext` | equality of relations | inside the declared boundary |
| the slot names | the classification | declared by the author after refusing an outside grid |

**What the system holds.** Four relations and the facts among them. The
witness counts, the residual numbers and the slot names are things the
metatheory says *about* those relations; none is admitted into a regime.

**Phrases to read with care.**

- "Inventory" means a list of what is already there. It is not a
  derivation of the next step and the paper says it "authorizes no
  response to a challenge".
- "Reversal" is two operations here. Prose that says "the reversal"
  should say which.
- "Collision is not obstruction" is a true sentence supported by
  PrimDiff; the theorem bearing that name proves a smaller thing.

## Student exercise

The census says `r = EmptyRel ∨ r = D2 ∨ r = D2rev ∨ r = S2`. State and
prove the two book-style inequalities it does not include: `EmptyRel ≠
D2rev` and `D2 ≠ S2`. Then say why the census theorem itself does not need
them.

## Answer

`EmptyRel ≠ D2rev`: if equal, `D2rev true false`, which holds by
`⟨rfl, rfl⟩`, would transport to `EmptyRel true false`, a proof of `False`.
`D2 ≠ S2`: if equal, `S2 true false`, which holds as `Or.inr D2_witness`,
would transport to `D2 true false`, whose first conjunct `true = false` is
refuted by `Bool.noConfusion`. The census does not need either: a
disjunction is true as soon as one disjunct is, and the proof picks the
disjunct by cases. The inequalities are what make the disjunction
*informative*, by showing the four names are four relations, and that is
why the book adds them. The book script also checks these two solutions
as `Textbook.U37.empty_ne_D2rev` and `Textbook.U37.D2_ne_S2`, with no
axiom dependencies.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/ObserverInventory.lean` lines 43-56 (slots), 58-111 (census), 115-138 (witnesses), 145-147 (defect), 151-194 (reversal), 198 (closure), 204-216 (residuals), 220-229 (maps) |
| Axiom report | `artifacts/lean_axioms.txt`: `bool_irrefl_full_classification` `[propext, Quot.sound]`; `witnesses_are_data` `[propext]`; `transpose_ne_pushNot`, `residuals_not_unique` none |
| Paper | `paper/observer_inventory.md` §1 (the refused grid), §2-§7; ledger `CL-PD-INVENTORY` (with the withdrawn terminal sentence recorded) |
| Python | `code/derivation/observer_inventory.py`; `artifacts/observer_inventory.json`; `tests/test_observer_inventory.py` (`test_irrefl_census_is_exactly_the_four`, `test_reversal_transpose_and_swap_agree_on_D2_and_differ`, `test_residuals_are_not_unique`) |
| Check (Python) | `python textbook/checks/u37_inventory.py`: brute-force census of 16 relations, the two reversal maps on `D2` and on the self-loop, the two residuals, the witness and defect reports, the nine slots, all against the artifact |
| Check (book Lean) | `python textbook/checks/u37_lean.py`: fourteen book theorems plus four Genesis theorems kernel-checked, Lean 4.33.0 |

</details>

<details>
<summary>Answers to the first-pass practice</summary>

1. C → D and C ← D. The empty and two-arrow pictures violate the
   exactly-one-arrow requirement.
2. C ← D remains. The additional prohibition rules out C → D; the
   original no-self-loop rule alone allowed all four pictures.
3. Use a self-loop at C. Transpose leaves it at C; swap moves it to D.
   Testing the four restricted pictures established agreement only on
   that restricted collection.
4. They need a justified correspondence between the actual situation
   and the declared two-dot model, including reasons the candidates and
   restrictions capture the alternatives relevant to the question.
   The classification theorem alone supplies no such correspondence.

</details>
