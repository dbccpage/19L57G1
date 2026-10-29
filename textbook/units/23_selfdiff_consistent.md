# Unit 23. Asserting a difference does not make two things

**Claim.** In the separate relation model, a recorded pair can use the same
point twice. Calling it a difference does not by itself prove that its
two ends are unequal.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** There is a relation on a one-point carrier that holds of the
point and itself. So a bare asserted pair `r a b` does not entail that
`a` and `b` are metatheoretically distinct: A1 (assertion) does not imply
A3 (inequality). Requiring the relation to be symmetric does not change
this.

**Status:** derived (a countermodel). **Lean:**
`PrimDiff.selfdiff_consistent` (`lean4/Derivation/PrimDiff.lean` lines
46-49), `PrimDiff.symm_selfdiff_consistent` (53-58). **Axioms:** none.
**Depends on:** Unit 15 (A1, assertion; A3, inequality; and the other
direction, A3 ⇏ A1). A1i adds the no-self-pair condition explained below.

</details>

## First pass

Switch to a relation model. Its **carrier** is the supplied collection
of points. A **relation** records which ordered pairs hold. This is a
different model from the admission regimes of Units 17–22.

Give it just one point, P, and record `P → P`. Both ends name P.
The record contains a pair, but it contains no pair of unequal points.
Here the arrow is a relation entry, not motion or a physical connection.

**Predict:** does requiring every arrow's reverse to be present rule
out this example?

<details>
<summary>Check your prediction</summary>

No. Reversing `P → P` gives the same arrow. The example is symmetric
and still has equal ends.

</details>

This one example defeats the proposed rule “every asserted pair has
unequal ends” across all structures. It does not say every structure
has a self-pair. For example, a record containing only `P → Q` on
two different points has none. The next chapter supplies a condition
under which every recorded pair really does have unequal ends.

## Question

Unit 22 reached a regime marking one of two admitted data. We now switch
to a separate model consisting of a carrier and a relation. Suppose it asserts a
difference between `a` and `b`: an edge `r a b`. Does the assertion by
itself guarantee that `a` and `b` are two things and not one?

## What we already possess

- The candidate commitments: A1, the designated pair is asserted;
  A3, its two ends are unequal (Unit 15). A1i means A1 together with
  irreflexivity: no point is related to itself.
- Unit 15: A3 does not imply A1 (an empty relation on two points).
- The notion of a countermodel: one structure satisfying the premise and
  failing the conclusion refutes the claim that the implication holds
  in all structures.

## New concept: the one-point self-difference

Take the carrier `Unit`, which has exactly one element `()`. Take the
relation that always holds. Then `r () ()` is asserted: a difference
between `()` and itself. A1 holds with `a = b = ()`. A3 fails, since
`() = ()`. This refutes the proposed implication quantified over all
carriers and structures. It does not refute every instance of that
implication on each particular carrier or relation.

The structure is symmetric too, trivially: `r x y → r y x` because
everything holds. So adding symmetry to A1 does not recover A3. Among
the three options studied (no axiom, symmetry, irreflexivity), only
irreflexivity will (Unit 24).

## Plain-language interpretation

Writing "x differs from y" in a ledger does not create two things. If x
and y are the same thing, the ledger now says that thing differs from
itself, and nothing in the bare act of asserting prevents that. The
distinctness has to come from somewhere else: either the metatheory
already knows it (and then it was never *derived* from the assertion), or
an extra law is in force that forbids self-difference. This unit is the
negative half; it says what a bare assertion cannot do.

For Genesis this is the formal shape of a recurring caution: the
responder admitted an instance `(0, [0])` or `(0, [0, 1])`, and the
metatheory reads it as "about ⟨A⟩" or "⟨A⟩ linked to ⟨AB⟩". That the
indices 0 and 1 are different is the metatheory's knowledge. The
instance does not say so, and could not.

## Pseudocode

```
# Gloss
carrier: one point *
relation: r(*, *) holds
A1: the designated pair (*, *) is asserted   -- yes
A3: the two designated points are unequal    -- no, * = *
so A1 does not imply A3.
symmetric? r(x, y) -> r(y, x): yes, everything holds.
so symmetry + A1 does not imply A3 either.
```

## Python

```python
from derivation.primdiff import Pointed, a1, a3, implication_matrix, irreflexive

one = Pointed(1, frozenset({(0, 0)}), 0, 0)
print(a1(one), a3(one), irreflexive(one.rel))
m = implication_matrix(3)
print(m["implications"]["A1->A3"], m["countermodels"]["A1->A3"]["structure"])
```

Output:

```text
True False False
False {'n': 1, 'rel': [(0, 0)], 'a': 0, 'b': 0}
```

## Line-by-line Python explanation

`Pointed(n, rel, a, b)` (`primdiff.py` line 31) is a carrier of size `n`,
a set of ordered pairs, and the designated pair. `Pointed(1, {(0, 0)},
0, 0)` is the self-difference.

`a1(one)` (line 57) asks whether `(a, b)` is in the relation: `True`.
`a3(one)` (line 69) asks whether `a != b`: `False`. `irreflexive` (line
61) is `False`, since `(0, 0)` is present.

`implication_matrix(3)` (line 129) enumerates every pointed structure
with carrier at most 3 and, for each pair of candidate predicates, either
confirms the implication on all of them or records the first
countermodel. For `A1->A3` it records this very structure, and the
artifact holds the same record.

The check script also counts: among structures with carrier at most 3,
785 satisfy A1 and not A3 (1, 16 and 768 by carrier size), and every one
of them has `a = b`, as it must.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/PrimDiff.lean lines 46-58
/-- Countermodel (A1 ⇏ A3): bare assertion is consistent with
metatheoretic identity — the one-point carrier hosts a self-difference. -/
theorem selfdiff_consistent :
    ∃ r : Unit → Unit → Prop, r () () :=
  ⟨fun _ _ => True, trivial⟩

/-- Countermodel (symmetry does not restore soundness): the self-difference
model is symmetric.  Among {no axiom, symmetry, irreflexivity}, only
irreflexivity entails metatheoretic inequality. -/
theorem symm_selfdiff_consistent :
    ∃ r : Unit → Unit → Prop,
      (∀ x y, r x y → r y x) ∧ r () () :=
  ⟨fun _ _ => True, fun _ _ h => h, trivial⟩
```

```lean
-- Lean (book), textbook/checks/u23_lean.py
def selfDiff : Unit → Unit → Prop := fun _ _ => True
theorem selfDiff_witness : selfDiff () () := trivial
theorem selfDiff_same : (() : Unit) = () := rfl
theorem selfDiff_not_irrefl : ¬ Irrefl selfDiff := fun h => h () trivial

/-- A1 does not imply A3: the schema refuted, with the carrier, relation
and pair exhibited. -/
theorem A1_not_A3 :
    ¬ ∀ (α : Type) (r : α → α → Prop) (a b : α), r a b → a ≠ b :=
  fun h => h Unit selfDiff () () trivial rfl
```

## Line-by-line Lean explanation

**`selfdiff_consistent`.** The statement is an existence: some relation
on `Unit` relates `()` to `()`. The proof is an anonymous constructor
`⟨witness, proof⟩`. The witness is `fun _ _ => True`, the relation that
ignores both arguments and returns the always-true proposition. The
proof that it relates `()` to `()` is `trivial`, Lean's proof of `True`.

**`symm_selfdiff_consistent`.** The same witness, now with a two-part
property: symmetry and the self-pair. Symmetry is
`fun _ _ h => h`: given `r x y` (a proof `h` of `True`), return a proof
of `r y x`, which is the same `True`, so `h` itself. The self-pair is
`trivial` again.

**The book's `A1_not_A3`.** The implication "A1 → A3" as a schema over
all carriers is the universal statement inside the negation. To refute
it, assume it as `h` and instantiate: carrier `Unit`, relation
`selfDiff`, points `()` and `()`, the asserted pair `trivial`. `h` then
promises `() ≠ ()`; feed it `rfl : () = ()` and it yields `False`. Every
piece of the countermodel appears as an argument, which is what makes a
countermodel checkable rather than described.

**`selfDiff_not_irrefl`.** `Irrefl r` is `∀ x, ¬ r x x`. Apply it to
`()` and to the witness `trivial`: `False`. So the countermodel also
refutes "A1 → A1i" (the artifact's second countermodel is the same
structure), and it marks irreflexivity as the thing it lacks.

**Axioms.** None, for every theorem in this unit, Genesis and book
alike. The proofs are constructions in the core logic; no `decide`, no
list computation.

## What has been proved

- A1 does not imply A3; symmetry with A1 does not imply A3 (Genesis,
  derived, by countermodel).
- The countermodel is not irreflexive, so A1 does not imply A1i either
  (book; also the artifact's `A1->A1i` record).
- Any relation with a self-pair refutes irreflexivity on any carrier
  (book, general).
- A self-difference exists on `Bool` as well: the phenomenon is not a
  quirk of the one-point carrier (book).
- Within carrier 3, every structure satisfying A1 and not A3 has `a = b`
  (Genesis engine, verified finite).

## What has not been proved

- That any Genesis regime *is* a self-difference. The regimes of
  Units 19 to 22 are the metatheory's objects, and their indices are
  distinct by metatheory. The point is that this distinctness is not a
  consequence of the admitted instance.
- That irreflexivity is available. It is a sufficient condition for every
  witnessed pair to be unequal (Unit 24). Unit 26 distinguishes proving
  it for a specified relation from requiring it of every unrestricted
  positive extension.
- A4, irreducibility under an admitted family of maps. Unit 14's
  factorization-through-a-point criterion describes A3, not A4. The later
  `irred_*` results require their specified operation family.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `Unit`, `()` | the one-point carrier | metatheory type with one inhabitant |
| `fun _ _ => True` | the self-difference | a metatheory relation; no Genesis regime is this object |
| `=`, `rfl` | A3 | metatheory equality |
| `∃ r : Unit → Unit → Prop` | "there is a structure" | metatheory quantification over relations |

**What the system holds.** Nothing in this unit is a state of the
Genesis system. The unit is about what a bare assertion, in any
structure, fails to carry. Read back into Genesis: an admitted instance
asserts; it does not make its arguments two.

**Phrases to read with care.**

- "Self-difference" names the countermodel, not a claim that something
  differs from itself in the system.
- "Bare" means: no law beyond the assertion. The whole unit is about the
  bare case; Unit 24 adds one law.

## Student exercise

Give a countermodel to "A1 → A3" on the two-element carrier `Bool`,
with `a = b = true`, and say which of its edges you needed and which you
did not.

## Answer

<details>
<summary>Worked answer</summary>

Take the relation that holds exactly of `(true, true)`, with the
designated pair `(true, true)`. A1 holds (the pair is asserted); A3
fails (`true = true`). The only edge needed is the self-pair at the
designated point; whether `(false, false)`, `(false, true)` or
`(true, false)` are asserted is irrelevant to the refutation. The book's
`selfdiff_on_Bool` is this structure.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/PrimDiff.lean` lines 46-58; `Irrefl` line 28 |
| Axiom report | `artifacts/lean_axioms.txt`: `selfdiff_consistent`, `symm_selfdiff_consistent` do not depend on any axioms |
| Paper | `paper/primitive_difference.md` S2 table (rows "A1 → A3 fails", "A1 → A1i fails", "symmetry restores A1 → A3 fails"), S8 countermodel index (the one-point self-difference) |
| Ledger | No `CL-*` entry names this theorem by itself; `CL-PD-INVENTORY` cites the one-point self-difference as the structure that "can assert its pair while failing irreflexivity" |
| Artifact | `artifacts/primdiff.json`, `implication_matrix.implications["A1->A3"] = false`, `countermodels["A1->A3"].structure = {n: 1, rel: [[0, 0]], a: 0, b: 0}`, and the same for `A1->A1i` |
| Test | `tests/test_primdiff.py::test_implication_matrix_structure`, `::test_candidate_basics` |
| Check (Python) | `python textbook/checks/u23_selfdiff.py`: the one-point structure's predicates; the two matrix entries and their countermodels against the artifact; 785 A1-without-A3 structures within carrier 3, all with `a = b` |
| Check (book Lean) | `python textbook/checks/u23_lean.py`: nine book theorems plus two Genesis theorems kernel-checked, Lean 4.33.0; no axioms anywhere |
