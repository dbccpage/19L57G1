# Unit 24. Under irreflexivity, a witnessed pair is two things

**Claim.** If a relation has no self-pairs, every pair it does contain has
unequal ends. This is a theorem about the supplied relation and equality
on its carrier, not a process that creates new points.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** If a relation is irreflexive, then any asserted pair `r a b`
has `a ≠ b`. This is the one implication, among the three options
studied (no law, symmetry, irreflexivity), that carries an object-level
assertion to metatheoretic distinctness. It is conditional on the law.

**Status:** conditional. **Lean:** `PrimDiff.irrefl_witness_ne`
(`lean4/Derivation/PrimDiff.lean` lines 40-44). **Axioms:** none.
**Depends on:** `Irrefl` (line 28), Unit 23 (why the hypothesis is
needed), Unit 15 (A1 and A3). A1i is A1 with irreflexivity added.

</details>

## First pass

A relation is **irreflexive** when it has no self-pair: no `P → P`
for any point P. On two points, consider exactly the record `P → Q`.
It is irreflexive. If P and Q were the same point, that entry would
be a forbidden self-pair. Therefore its ends are unequal.

The proof needs both ingredients: the recorded pair and the no-self-pair
condition. An empty relation is also irreflexive, but supplies no pair
from which to draw this conclusion.

**Change:** add `Q → Q` while retaining `P → Q`. The whole relation
is no longer irreflexive. Nevertheless P and Q are still unequal.

The general equivalence below concerns **every** pair in the relation.
Irreflexivity is sufficient to justify inequality for every pair, and
that global guarantee is equivalent to irreflexivity. A particular pair
can have unequal ends even when some other pair is a self-pair.

This is reasoning inside a specified model. Applying it to objects in
the world also requires evidence that the relation represents them as
claimed.

## Question

Unit 23 refuted a general implication from assertion to inequality.
Which condition guarantees inequality for every asserted pair? Is that
conclusion an operation inside the structure, or a fact the metatheory
proves about it?

## What we already possess

- `Irrefl r := ∀ x, ¬ r x x`: no point is related to itself.
- A1i: the designated pair is asserted and the relation is irreflexive
  (Unit 23). A3: the designated points are unequal.
- The self-difference (Unit 23), which satisfies A1 and is not
  irreflexive.
- `D2 : Bool → Bool → Prop := fun x y => x = false ∧ y = true`, the
  oriented two-element difference, with `D2_irrefl` and
  `D2_witness : D2 false true` (lines 89-118).

## New concept: a two-line proof that moves a witness along an equation

Suppose `hi : Irrefl r` and `h : r a b`, and suppose for contradiction
`a = b`. Rewrite `h` along the equation: `r b b`. Irreflexivity at `b`
says `¬ r b b`. Contradiction. So `a ≠ b`.

The proof uses nothing but the law and the witness. It is also exact:
the converse holds (if every asserted pair is distinct, no self-pair is
asserted, which is irreflexivity), so "every witnessed pair is two
things" is *equivalent* to the law, not merely implied by it.

## Plain-language interpretation

A ledger with the rule "nothing is recorded as differing from itself"
can be read safely: whenever it records "x differs from y", x and y are
two. The reading is the metatheory's, and the rule is doing all the work.
Remove the rule and Unit 23's ledger returns.

For a fully specified finite relation, no-self-pairs can be checked and
proved: `D2_irrefl` is one example. Requiring that property to remain
true through future allowed extensions is a separate restriction.
Unit 26 shows that preserving positive entries alone does not ensure it.

Among the three options compared here—no extra condition, symmetry,
and irreflexivity—only the last guarantees inequality for every asserted
pair. This is the scoped comparison behind the source's “weakest”
description. It is not a search over all possible laws or a claim that
symmetry has no consequences: symmetry supplies reversed pairs.

## Pseudocode

```
# Gloss
given: Irrefl r      (for every x, not r x x)
given: r a b
suppose a = b
then r b b            (replace a by b in the witness)
but not r b b         (irreflexivity at b)
contradiction, so a ≠ b.
converse: if every r x y has x ≠ y, then r x x would give x ≠ x; so no r x x: Irrefl r.
```

## Python

```python
from derivation.primdiff import D2, S2, a1i, a3, implication_matrix

print(sorted(D2.rel), a1i(D2), a3(D2))
print(sorted(S2.rel), a1i(S2), a3(S2))
m = implication_matrix(3)
print(m["implications"]["A1i->A3"], m["implications"]["A3->A1i"])
```

Output:

```text
[(0, 1)] True True
[(0, 1), (1, 0)] True True
True False
```

## Line-by-line Python explanation

`D2` and `S2` (`primdiff.py`, module constants) are the oriented and
symmetric two-element differences as `Pointed` structures with the pair
`(0, 1)` designated. `a1i` (line 65) is `a1` together with
`irreflexive`; `a3` is `a != b`. Both hold of both.

`implication_matrix(3)["implications"]["A1i->A3"]` is `True`: among all
pointed structures with carrier at most 3, none satisfies A1i and fails
A3. That is the finite shadow of the theorem; the theorem itself has no
carrier bound. `A3->A1i` is `False` (Unit 15's direction: two distinct
points with nothing asserted).

The check script counts 196 structures within carrier 3 satisfying A1i,
every one with `a != b`, and reads the artifact's two-element report:
the smallest carrier hosting a witnessed structure is 1 under no law and
2 under irreflexivity (`minimal_carrier_by_axiom_set`).

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/PrimDiff.lean lines 28, 40-44
/-- Irreflexivity: the weakest object-level fidelity commitment studied
here. -/
def Irrefl {α : Type} (r : α → α → Prop) : Prop := ∀ x, ¬ r x x

/-- Soundness from irreflexivity (A1i → A3): an irreflexive witnessed
pair is metatheoretically distinct. -/
theorem irrefl_witness_ne {α : Type} {r : α → α → Prop} (hi : Irrefl r)
    {a b : α} (h : r a b) : a ≠ b :=
  fun he => hi b (he ▸ h)
```

```lean
-- Lean (book), textbook/checks/u24_lean.py
theorem irrefl_witness_ne' {α : Type} {r : α → α → Prop} (hi : Irrefl r)
    {a b : α} (h : r a b) : a ≠ b := by
  intro he
  have hbb : r b b := he ▸ h
  exact hi b hbb

theorem irrefl_of_witness_ne {α : Type} {r : α → α → Prop}
    (h : ∀ a b, r a b → a ≠ b) : Irrefl r :=
  fun x hx => h x x hx rfl

theorem irrefl_iff_witness_ne {α : Type} (r : α → α → Prop) :
    Irrefl r ↔ ∀ a b, r a b → a ≠ b :=
  ⟨fun hi _ _ h => irrefl_witness_ne hi h, irrefl_of_witness_ne⟩

theorem D2_endpoints_ne : false ≠ true := irrefl_witness_ne D2_irrefl D2_witness
```

## Line-by-line Lean explanation

**The statement.** `{α : Type}` and `{r}` are implicit: Lean reads them
off `hi` and `h`. `hi : Irrefl r` is the law. `{a b : α}` are implicit
too, read off `h : r a b`. The conclusion `a ≠ b` unfolds to `a = b →
False`.

**`fun he => …`.** Assume `he : a = b`.

**`he ▸ h`.** The triangle rewrites `h : r a b` along `he`, replacing
`a` by `b`: a proof of `r b b`.

**`hi b (…)`.** Irreflexivity at the point `b` is `¬ r b b`, a function
from `r b b` to `False`. Applied to the rewritten witness it returns
`False`, which is what `a ≠ b` asked for after assuming `he`.

**The book's converse** `irrefl_of_witness_ne`: to show `¬ r x x` for an
arbitrary `x`, assume `hx : r x x`; the hypothesis at `a = b = x` gives
`x ≠ x`; apply it to `rfl`. So the two are equivalent
(`irrefl_iff_witness_ne`). This equivalence concerns the guarantee for
**every** pair. It does not say irreflexivity is necessary to establish
inequality for one specified pair. The book's `mixed_specific_pair`
has an unequal asserted pair and also a self-pair elsewhere.

**`D2_endpoints_ne`.** The theorem applied to the concrete oriented
difference: `false ≠ true`. Lean knew this already (`Bool.noConfusion`);
the point is that it now follows from `D2`'s irreflexivity and witness
by the general route, with no appeal to `Bool`'s constructors.

**Axioms.** None, throughout. `D2_witness` is proved by `decide` on a
decidable `Bool` proposition and still reports no axioms; nothing here
touches lists or `propext`.

## What has been proved

- Under irreflexivity, every asserted pair is metatheoretically distinct
  (Genesis, derived; conditional on the law).
- The converse, so the law is equivalent to "every witnessed pair is
  distinct" (book).
- The instances on `D2` and `S2` (book).
- The hypothesis cannot simply be dropped from the general implication:
  Unit 23 supplies a counterexample. A particular pair may still have
  unequal ends in a non-irreflexive relation (`mixed_specific_pair`, book).
- Within carrier 3, A1i → A3 holds on every pointed structure (Genesis
  engine, verified finite).

## What has not been proved

- That any admission regime's instances automatically give this
  irreflexive relation. The primitive-difference layer is a separate
  model; no such translation is supplied here.
- That positive entries constrain every extension to stay irreflexive
  (Unit 26). Proving irreflexivity for a fixed relation is a different
  question and is possible for the examples just checked.
- Orientation. `irrefl_witness_ne` gives `a ≠ b`, not which of the two
  is "first"; `S2` satisfies it as well as `D2`. Orientation is the
  subject of the transposition and observer theorems later in the book.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `Irrefl r` | the theorem's hypothesis | proved for a specified example or supplied as a condition; protection under extensions is separate |
| `he ▸ h` | moving the witness along an equation | metatheory rewriting with `=` |
| `a ≠ b` | the conclusion | metatheory inequality; the relation `r` does not mention it |
| `Bool`, `D2` | the instance | metatheory carrier and relation |

**What the system holds.** In the primitive-difference model: a carrier,
a relation, a designated pair, and, if declared, the law. The
distinctness `a ≠ b` is not a fourth thing held; it is what the
metatheory can conclude about the first three once the law is in force.

**Phrases to read with care.**

- "Soundness from irreflexivity" (the docstring) means A1i → A3. It is
  not a soundness theorem about Genesis's engine.
- "Conditional" marks the hypothesis `Irrefl r`. This proof does not
  establish it for an arbitrary `r`; it can be proved for particular
  definitions, as `D2_irrefl` shows.

## Student exercise

Relation on `Fin 3` (three points 0, 1, 2): `r x y :⇔ x < y`. Is it
irreflexive? Apply the theorem to the pair `(0, 2)`. Then change the
relation to `x ≤ y` and say exactly where the proof breaks.

## Answer

<details>
<summary>Worked answer</summary>

`<` on `Fin 3` is irreflexive (`¬ x < x`), so `irrefl_witness_ne` with
the witness `0 < 2` gives `0 ≠ 2`. For `≤`, `0 ≤ 0` holds, so the law
fails; the proof cannot be *started*, since `hi : Irrefl (· ≤ ·)` is not
available. The conclusion `0 ≠ 2` happens to be true anyway, but the
pair `(0, 0)` is a witness of `≤` with equal endpoints, so the schema
"witnessed implies distinct" is false for `≤`, as the converse theorem
predicts.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/PrimDiff.lean` lines 28, 40-44, 89, 106-118 |
| Axiom report | `artifacts/lean_axioms.txt`: `irrefl_witness_ne`, `D2_irrefl`, `D2_witness` do not depend on any axioms |
| Paper | `paper/primitive_difference.md` S1 ("the weakest object-level axiom found"), S2 table rows "A1i → A3 holds", "A1i → A4(∅) holds" |
| Ledger | `CL-PD2-MATRIX` (the implication matrix as a whole); no `CL-*` entry names `irrefl_witness_ne` alone |
| Artifact | `artifacts/primdiff.json`, `implication_matrix.implications["A1i->A3"] = true`; `two_element.minimal_carrier_by_axiom_set = {bare: 1, irreflexive: 2, irreflexive+symmetric: 2}` |
| Test | `tests/test_primdiff.py::test_implication_matrix_structure`, `::test_two_element_report` |
| Check (Python) | `python textbook/checks/u24_irrefl_witness.py`: `D2`, `S2` satisfy A1i and A3; the matrix entries; 196 A1i structures within carrier 3, all with `a != b`; the minimal-carrier table; a particular unequal asserted pair in a non-irreflexive relation |
| Check (book Lean) | `python textbook/checks/u24_lean.py`: eight book reports plus three Genesis results kernel-checked, Lean 4.33.0, including `mixed_specific_pair`; no axioms anywhere |
