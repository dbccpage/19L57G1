# Unit 14. Factoring through a point is equality

**Claim.** The selection of two elements `a`, `b` of a carrier factors
through the one-point carrier exactly when `a = b`. So candidate A3 for
"primitive difference", non-factorization through a point, is nothing
other than the metatheory's own inequality `a ≠ b`, re-expressed once
functions are admitted. **Status:** derived. **Lean:**
`PrimDiff.factors_through_point_iff` (`lean4/Derivation/PrimDiff.lean`
lines 67-78). **Axioms:** none. **Depends on:** nothing from the regime
model; this module imports nothing of it. It needs only the metatheory's
types, functions and equality (Unit 00).

## Question

Units 01 to 13 were about regimes. The derivation now steps back and asks
a question the regime model presupposed: what is the *weakest* formal
object that deserves the name "difference"? `PrimDiff.lean` sets up five
candidate readings (A1 to A5; `paper/primitive_difference.md` §S1) and
measures each by the metatheory it needs. This unit is about A3: "`a` and
`b` are different when picking them out does not factor through a single
point." That sounds structural. Is it anything more than `a ≠ b`?

## What we already possess

- Types and functions in the metatheory (Unit 00). `Unit` is Lean's
  one-element type; its element is `()`.
- Equality and its two elementary laws: symmetry (`h.symm`) and
  transitivity (`h1.trans h2`); and the substitution `he ▸ rfl`, which
  rewrites a goal along an equation.
- The candidates, from the module header (lines 12-20): A1, a relation
  with one asserted pair and no axioms; A1i, A1 plus irreflexivity; A2,
  witness multiplicities; A3, non-factorization through a point; A4,
  irreducibility under an admitted family of maps; A5, the two-element
  carriers `D2` and `S2`.

## New concept: factoring through a point

A map `p : Unit → α` out of the one-point type has exactly one value,
`p ()`. To say that the selection of `a` and `b` **factors through the
point** is to say there is such a `p` with `p () = a` and `p () = b`: one
value that is both. A3 says a difference is present when no such `p`
exists.

The theorem is that the two conditions are the same proposition in
disguise: `(∃ p, p () = a ∧ p () = b) ↔ a = b`. Each direction is two
lines. The book's `point_map_constant` adds the one fact that makes the
picture complete: every `p : Unit → α` *is* the constant map at `p ()`.

## Plain-language interpretation

Imagine a pointer that can point at only one thing. "You cannot point at
both `a` and `b` with it" means exactly "`a` and `b` are two things". No
new notion of difference has appeared; the pointer only restates the
metatheory's equality in the language of maps. That is why the paper
concludes "A3 is therefore not a primitive: it is the metatheory's own
identity, re-expressed" (§S1).

This matters for the programme because the metatheory's `≠` is precisely
what the seed denies the object language (Unit 00). If A3 were a genuine
primitive, the system could have difference for free by admitting maps.
It cannot: admitting maps and a point imports `≠` along with them, and the
price of A3 is the price of metatheoretic identity (Unit 15 shows the
converse gap: having `≠` outside asserts nothing inside).

## Pseudocode

```
# Gloss
factors(a, b) := exists p : point -> X with p(*) = a and p(*) = b

(→)  given such p:  a = p(*) = b.                     so a = b
(←)  given a = b:   take p(*) := a.  then p(*) = a, and p(*) = b since a = b.
therefore factors(a, b) iff a = b;   not factors(a, b) iff a ≠ b.
```

## Python

```python
from derivation.primdiff import a3, all_functions_between, enumerate_pointed

print(all_functions_between(1, 3))
def factors(n, a, b):
    return any(p[0] == a and p[0] == b for p in all_functions_between(1, n))
print(all((not factors(s.n, s.a, s.b)) == a3(s) == (s.a != s.b)
          for n in (1, 2, 3) for s in enumerate_pointed(n)))
```

Output:

```text
[(0,), (1,), (2,)]
True
```

## Line-by-line Python explanation

`all_functions_between(1, 3)` (`primdiff.py` line 195) lists every map
from a one-element carrier into a three-element one, as tuples of values.
There are three, one per target element: a map out of the point is a
choice of one element.

`factors(n, a, b)` asks whether one of those maps has `a` and `b` as the
same value `p[0]`. It is the existential of the theorem, computed by
listing.

The last line runs over every pointed structure with carrier at most 3
(`enumerate_pointed`, lines 46-54: all relations and all designated pairs;
4 674 structures) and checks three things agree: non-factorization,
Genesis's predicate `a3` (line 69, defined as `s.a != s.b`), and the
inequality itself. `True`. Note that Genesis's Python *defines* A3 as the
inequality; the Lean theorem is what licenses that definition.

The check script also recomputes the implication matrix
(`implication_matrix(3)`) and compares it with `artifacts/primdiff.json`:
A3 has extent 3 104 of 4 674, equal to the extent of A4 with the empty
family, and the matrix agrees with the artifact cell for cell.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/PrimDiff.lean lines 67-78
/-- A3 stated as non-factorization: the selection of `a` and `b` factors
through the one-point carrier exactly when they are metatheoretically
equal.  Non-factorization is therefore *definitionally* metatheoretic
inequality once function composition is admitted. -/
theorem factors_through_point_iff {α : Type} (a b : α) :
    (∃ p : Unit → α, p () = a ∧ p () = b) ↔ a = b := by
  constructor
  · intro ⟨p, h1, h2⟩
    exact h1.symm.trans h2
  · intro he
    exact ⟨fun _ => a, rfl, he ▸ rfl⟩
```

## Line-by-line Lean explanation

`{α : Type} (a b : α)`: any type and any two of its elements. The theorem
is proved once for all of them.

`constructor` splits the `↔` into two implications.

Forward: `intro ⟨p, h1, h2⟩` takes the map and the two equations
`h1 : p () = a`, `h2 : p () = b`. `h1.symm` is `a = p ()`, and
`.trans h2` chains it with `p () = b` to give `a = b`.

Backward: `intro he` takes `he : a = b`. The witness is the constant map
`fun _ => a`. Its value at `()` is `a` by `rfl`. For the second conjunct,
`p () = b`, the goal is `a = b`; `he ▸ rfl` rewrites the goal along `he`
(replacing `b` by `a`, or `a` by `b`) to `a = a` and closes it by `rfl`.

**Axioms.** None. The proof uses only the rules of equality and the
introduction of an existential; no case analysis on a concrete list, no
`decide`, no extensionality. The book's `point_map_constant` does use
function extensionality (`funext`), which is why it alone reports
`Quot.sound`; the theorem does not need it.

## What has been proved

- For every type and every two elements, factoring through the point is
  equivalent to equality (Genesis, derived, axiom-free).
- Hence A3, as a predicate, is `a ≠ b` (book Lean `A3_is_ne`, derived,
  axiom-free: `not_congr` of the theorem).
- On `Bool`, `false` and `true` do not factor and `true`, `true` do (book
  Lean, derived).
- Every map out of the point is constant at its value (book Lean, derived
  with `Quot.sound` through `funext`).
- Within carrier 3, A3 and A4 with the empty family have the same extent,
  3 104 structures (Genesis, verified finite; the Lean `irred_empty_iff_ne`
  covers the general case and is taught with A4).

## What has not been proved

- That inequality is *available to the object language*. The theorem is
  about the metatheory's `=` on a Lean type. The system of Units 01 to 13
  has no equality on its data at all (Unit 08: it has collapse and
  separability, which are behavioral). A3 is a metatheoretic notion
  through and through.
- That A3 is useless. It is the right notion when the metatheory is the
  object of study; the paper keeps it as the A3 column of the implication
  matrix (§S2) and uses it as the target of `irrefl_witness_ne` (Unit 24).
- Anything about A1, A2, A4 or A5. Unit 15 handles the gap between A3 and
  A1; Units 23 to 26 the rest.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `{α : Type}` | the carrier | metatheory type; the theorem quantifies over all types |
| `Unit`, `()` | the one-point carrier | metatheory type with one element |
| `Unit → α`, `fun _ => a` | maps out of the point | metatheory function type; the paper's "A3 bill" is exactly this: "function types, composition, and a one-point carrier" |
| `=`, `≠` | the conclusion | the metatheory's identity on `α` |

**What the system holds.** Nothing in this unit is held by the regime
system; `PrimDiff.lean` is self-contained and imports none of
`Basic.lean`. The audit record (`textbook/audit/modules/PrimDiff.md`)
marks the module's carriers, maps and relations as the declared
metatheory. When a later unit applies these results to admitted data, it
must say which admissions supply the carrier and the maps.

**Phrases to read with care.**

- "Picking out `a` and `b`" is a gloss for the two equations; the system
  does no picking.
- "A3 is not a primitive" means: it costs the metatheory's identity, and
  buys exactly that. It is not a claim that `≠` is worthless.

## Student exercise

On the carrier `Fin 3` (elements 0, 1, 2), list every map out of the
point, say for which pairs `(a, b)` the selection factors, and state what
`A3_is_ne 1 2` says. Then: does `factors_through_point_iff` need the
carrier to be finite, non-empty, or decidable?

## Answer

Three maps, the constants at 0, 1 and 2 (the check script prints them as
`(0,)`, `(1,)`, `(2,)`). The selection factors for `(0, 0)`, `(1, 1)` and
`(2, 2)` only; for the six pairs with `a ≠ b` there is no map whose one
value is both. `A3_is_ne 1 2` says: "there is no `p : Unit → Fin 3` with
`p () = 1` and `p () = 2`" is equivalent to `1 ≠ 2`. The theorem needs
none of the three properties: `α` is any type, possibly empty (then the
equivalence is vacuous on no elements), possibly infinite, with no
decidability assumed; the proof never decides anything.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/PrimDiff.lean` lines 67-78; module header lines 1-21 (candidates and declared metatheory) |
| Axiom report | `artifacts/lean_axioms.txt`: `PrimDiff.factors_through_point_iff` does not depend on any axioms |
| Paper | `paper/primitive_difference.md` §S1 (A3, **[theorem]**), §S2 (matrix rows `A3 ↔ A4(∅)`), §S7 (the strongest defensible object cites this theorem) |
| Ledger | No `CL-*` entry names this theorem; the paper's §S2 table and §S8 countermodel index are its record |
| Artifact | `artifacts/primdiff.json`, `implication_matrix`: A3 extent 3 104, equal to `A4_empty`; scope all pointed structures with carrier ≤ 3 |
| Test | `tests/test_primdiff.py::test_candidate_basics`, `::test_implication_matrix_structure` (`A3->A4_empty` and back) |
| Check (Python) | `python textbook/checks/u14_factor_point.py`: 4 674 pointed structures, non-factorization = `a3` = `a ≠ b` on all; three maps out of the point into a 3-carrier; implication matrix and extents equal to the artifact |
| Check (book Lean) | `python textbook/checks/u14_lean.py`: five book theorems plus the Genesis theorem kernel-checked, Lean 4.33.0; all axiom-free except `point_map_constant` (`Quot.sound`, via `funext`) |
