# Unit 15. An outside difference is not an asserted one

**Claim.** Metatheoretic inequality does not bring an asserted difference
with it: on the two-element carrier `Bool`, the empty relation asserts
nothing about `(false, true)`, and yet `false ≠ true`. So A3 does not imply
A1. A difference that exists outside the object language is not thereby
admitted inside it.

<details>
<summary>Source and classification record (optional on a first reading)</summary>

**Status:** derived (a countermodel proved in Lean).
**Lean:** `PrimDiff.meta_diff_without_assertion`
(`lean4/Derivation/PrimDiff.lean` lines 60-66). **Axioms:** none.
**Depends on:** the candidates A1 and A3 (Unit 14); `Bool.noConfusion`
(the metatheory's proof that `false ≠ true`).

</details>

## First pass

Draw two positions A and B and leave the arrow relation empty.
The labels let us distinguish the positions outside the model, but
there is no admitted arrow from A to B. Knowing the positions differ
does not write an arrow into the record.

This is the separate `PrimDiff` relation setting. No `Regime` event
or transport from that model is being applied here.

The source uses the two Boolean values as position labels: A is
`false` and B is `true`. Those labels do not mean one position is a
false claim and the other a true claim. The empty relation separately
answers false on every ordered pair.

Predict whether adding a rule that forbids self-arrows would create
the A-to-B arrow. It would not; a restriction does not itself assert
a pair. This countermodel refutes the proposed implication from
outside inequality to an asserted relation. It does not deny that
we could separately admit such a relation.

## Question

Unit 14 showed that A3 is the metatheory's `≠`. The metatheory can tell
`false` from `true`. Does that fact, by itself, put a difference *into* a
relation on `Bool`? If it did, every outside distinction would be an
inside assertion for free, and the seed's wall between the inscription
and the system (Unit 00) would already be breached at the first carrier
with two elements.

## What we already possess

- A1: a relation `r` with the pair asserted, `r a b`, no axioms. A3: `a ≠
  b` (Unit 14).
- `Bool` has two constructors, `false` and `true`, and `Bool.noConfusion`
  proves they are distinct: it is the metatheory's own `false ≠ true`.
- A relation on a type is a function `α → α → Prop`. The relation that
  asserts nothing is `fun _ _ => False`.

## New concept: a countermodel is a theorem

To refute "A3 implies A1" one does not argue in prose; one exhibits a
structure where A3 holds and A1 fails, and proves both facts. The Lean
statement is an existential: *there is* a relation on `Bool` such that the
pair is not asserted and the points are unequal. The witness is the empty
relation. The book marks such a result **derived**: it is proved in Lean
from the definitions, and what it proves is a negative.

The paper's §S8 keeps an index of these countermodels. This one is the row
"empty relation on two points", refuting A3 → A1.

## Plain-language interpretation

You, outside, can see that two marks on the page are two. The page says
nothing. Seeing is not writing. Unless a sentence asserting the difference
is admitted, the system holds no difference, however plain it is to the
onlooker. This is the mirror image of Unit 14: there, admitting maps
imports the metatheory's identity; here, having the metatheory's identity
imports no assertion. The two readings of "different" are, in the paper's
word, **orthogonal**: neither implies the other (§S2, "Reading"). Unit 23
proves the other half, that an asserted pair does not give inequality
(`selfdiff_consistent`).

For the derivation this is the formal shape of the finitude rule's
"silent observer" clause (README, **No imports from nowhere**): the
observer's knowledge that `a ≠ b` is not a state of the system.

## Pseudocode

```
# Gloss
carrier: {false, true}
relation r: asserts nothing (r x y is False for all x, y)
check A1 at (false, true):  r false true  -- False.  A1 fails.
check A3 at (false, true):  false ≠ true  -- holds in the metatheory.
so A3 holds and A1 fails:  A3 does not imply A1.
```

## Python

```python
from derivation.primdiff import Pointed, a1, a1i, a3, implication_matrix, irreflexive

empty = Pointed(2, frozenset(), 0, 1)
print(a3(empty), a1(empty), irreflexive(empty.rel))
m = implication_matrix(3)
print(m["implications"]["A3->A1"], m["countermodels"]["A3->A1"]["structure"])
```

Output:

```text
True False True
False {'n': 2, 'rel': [], 'a': 0, 'b': 1}
```

## Line-by-line Python explanation

`Pointed(2, frozenset(), 0, 1)` (`primdiff.py` lines 31-43): a carrier of
two elements, the empty relation, designated points 0 and 1. This is the
Lean witness with `Bool` written as `range(2)`.

`a3(empty)`: `0 != 1`, `True`. `a1(empty)`: `(0, 1) in frozenset()`,
`False`. `irreflexive(empty.rel)`: `True`, vacuously; the book's
`emptyRel_irrefl` is the same observation in Lean. So A1i's *law* can be in
force while nothing is asserted: the law alone asserts nothing.

`implication_matrix(3)` (lines 129-182) runs every candidate over every
pointed structure with carrier at most 3 and records, for each pair of
candidates, whether the implication ever fails and the first failing
structure. `A3->A1` is `False`, and the recorded countermodel is the very
structure above. This is the artifact's cell.

The check script also counts, within carrier 3, the structures where A3
holds and A1 fails (1 552) and, for Unit 23, where A1 holds and A3 fails
(785).

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/PrimDiff.lean lines 60-66
/-- Countermodel (A3 ⇏ A1): metatheoretic inequality with an empty
relation — a difference that exists outside the object language is not
thereby admitted inside it. -/
theorem meta_diff_without_assertion :
    ∃ r : Bool → Bool → Prop,
      ¬ r false true ∧ false ≠ true :=
  ⟨fun _ _ => False, id, Bool.noConfusion⟩
```

## Line-by-line Lean explanation

The statement: there exists a relation `r` on `Bool` with two properties,
`¬ r false true` and `false ≠ true`.

The proof is one anonymous constructor `⟨_, _, _⟩` with three parts.

1. The witness `fun _ _ => False`: the relation that is `False` at every
   pair.
2. `id` proves `¬ r false true`. Unfolding, `r false true` is `False`, and
   `¬ False` is `False → False`, which the identity function proves.
3. `Bool.noConfusion` proves `false ≠ true`, that is `false = true →
   False`. `noConfusion` is the principle Lean generates for every
   inductive type: distinct constructors are unequal. This is the
   metatheory's identity on `Bool` doing its work.

**Axioms.** None. The witness is a lambda, the two proofs are an identity
function and a generated constructor-distinctness principle.

## What has been proved

- A3 does not imply A1: on `Bool`, the empty relation has `false ≠ true`
  without `r false true` (Genesis, derived, axiom-free).
- The same on any type at any two distinct points (book Lean
  `meta_diff_without_assertion_any`, derived).
- The empty relation is irreflexive, so the fidelity law of A1i by itself
  asserts nothing (book Lean `emptyRel_irrefl`, derived).
- The oriented carrier `D2` asserts the same pair on the same carrier
  (book Lean `D2_asserts`): same points, different relation, A1 now holds.
- Within carrier 3, the implication `A3 → A1` fails with this very
  structure recorded (Genesis, verified finite, `artifacts/primdiff.json`).

## What has not been proved

- That A1 does not imply A3. That is the other countermodel, the one-point
  self-difference `selfdiff_consistent` (Unit 23). Together the two give
  the paper's orthogonality; this unit alone gives one direction.
- That nothing can bridge the two. Irreflexivity does, in one direction:
  A1 plus `Irrefl` gives A3 (`irrefl_witness_ne`, Unit 24). The paper
  isolates it as "the unique studied axiom that ties them" (§S2).
- Anything about the regime model. `PrimDiff.lean` imports none of it.
  The regime analogue of this unit is Unit 10: data the metatheory tells
  apart by token are collapsed inside until an instance mentions them.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `Bool`, `false`, `true` | the carrier and its two points | metatheory type |
| `Bool → Bool → Prop`, `fun _ _ => False` | relations; the empty one | metatheory function type into `Prop` |
| `Bool.noConfusion` | `false ≠ true` | the metatheory's identity on an inductive type |
| `∃ r, …` | the countermodel's shape | metatheory existential with an explicit witness |

**What the supplied relation says.** `r` asserts no ordered pairs.
The metatheoretic carrier still has two elements. The inequality
`false ≠ true` is a separate fact about that carrier; it writes no pair
into the relation. Calling that outside fact an assertion already
present in `r` would change the model's admitted data.

**Phrases to read with care.**

- "Outside the object language" (the docstring) means: provable in the
  metatheory from the carrier alone. It is not a place.
- "Not thereby admitted" means the pair is absent from the supplied
  relation. This `PrimDiff` setting defines no event history from which
  we could infer that a particular admission event did or did not occur.

## Student exercise

Take the carrier `Fin 3` and the relation that asserts exactly the pair
`(0, 2)`. At the designated pair `(0, 1)`: does A3 hold? A1? Is the
relation irreflexive? Now at the designated pair `(0, 2)`: which of A1,
A1i, A3 hold? Which implication from the paper's §S2 table does each
designated pair illustrate?

## Answer

At `(0, 1)`: A3 holds (`0 ≠ 1`); A1 fails (`(0, 1)` is not asserted); the
relation is irreflexive (its only pair is off the diagonal). So this is
again A3 without A1, this unit's direction, now with a non-empty relation.
At `(0, 2)`: A1 holds, the relation is irreflexive so A1i holds, and A3
holds (`0 ≠ 2`). This illustrates `A1i → A3` (Unit 24), not a
countermodel. Neither designated pair gives A1 without A3; for that one
needs an asserted pair on the diagonal (Unit 23).

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/PrimDiff.lean` lines 60-66 |
| Axiom report | `artifacts/lean_axioms.txt`: `PrimDiff.meta_diff_without_assertion` does not depend on any axioms |
| Paper | `paper/primitive_difference.md` §S2 table row "A3 → A1 **fails**", §S7 (**[counterexample]**), §S8 countermodel index row "empty relation on two points" |
| Ledger | No `CL-*` entry names this theorem; the paper's §S2 table and §S8 index are its record |
| Artifact | `artifacts/primdiff.json`, `implication_matrix.implications["A3->A1"]: false`, `countermodels["A3->A1"]`: `{n: 2, rel: [], a: 0, b: 1}` |
| Test | `tests/test_primdiff.py::test_candidate_basics` (the `empty` structure), `::test_implication_matrix_structure` |
| Check (Python) | `python textbook/checks/u15_meta_diff.py`: the countermodel's three predicates; 1 552 structures with A3 and not A1 within carrier 3; matrix cell and recorded countermodel equal to the artifact |
| Check (book Lean) | `python textbook/checks/u15_lean.py`: five book theorems plus the Genesis theorem and `D2` kernel-checked, Lean 4.33.0; all axiom-free |
