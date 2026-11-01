# Unit 01. The representative merges exactly what the family cannot tell apart

**Claim.** On the supplied carrier, the first-match representative gives equal
labels exactly to inputs with equal family signatures. The list order
selects the labels; the theorem concerns the resulting groups.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** For data `x` and `x'` on the carrier, the family's
representative gives them the same value exactly when the family cannot
tell them apart: `pQ D Q x = pQ D Q x' ↔ SigEq Q x x'`.

**Status:** derived. **Lean:** `Compression.pQ_exact`. **Sources:**
`lean4/Derivation/Compression.lean` lines 223–264.

A family is a list of presentations (Unit 00). This unit shows that one
presentation can stand for the whole list without losing any distinction
the list makes, and without adding one. That single presentation is what
`two_theorems` calls the institution's `actor`, and Unit 02 defines
knowledge through it.

</details>

## First pass

Use I00's first table: it reports 0 on cards A and C, and 1 on B. Its
groups are {A,C} and {B}. Scan the supplied order A, B, C and keep the first card
from each group:

| Input | Representative | Original answer |
|---|---|---|
| A | A | 0 |
| B | B | 1 |
| C | A | 0 |

The representative reports the same label on A and C, exactly because
their original answers agree. Reordering the scan to C, B, A would
choose C for that group. It would change the representative label,
while keeping the same grouping.

**Predict:** does this prove that every input outside the supplied list
has also been represented faithfully?

<details><summary>Check your prediction</summary>

No. The theorem assumes that both compared inputs belong to the carrier.
An outside input might match an existing signature, or the search might
fail and use its default. Neither case extends the theorem's coverage.

</details>

## What you need first

Unit 00: `sigList`, `SigEq`, `sigEq_iff_sigList`.

The representative chooses an **input as a label** for a whole signature
group. For the first table, the original answers are `[0,1,0]` and the
representative labels happen also to be `[0,1,0]`. These have different
jobs. Changing the original answers to `[7,9,7]` leaves the groups and
first-input labels unchanged. A label need not be the answer it represents.

### 1. First match

<details>
<summary>Lean source: pick (optional)</summary>

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 109–113
/-- First element of `D` satisfying the boolean test, if any. -/
def pick (D : List Nat) (P : Nat → Bool) : Option Nat :=
  match D with
  | [] => none
  | a :: t => if P a then some a else pick t P
```

</details>

`pick` walks the carrier from the front and returns the first datum that
passes the test `P`, as `some a`; if none passes, `none`. Three facts
about it are proved in the same file by walking the list, and are used
below without being re-proved here: a picked datum is in the carrier
(`pick_mem`, line 117), a picked datum passes the test (`pick_holds`,
line 134), and if some datum of the carrier passes the test then
something is picked (`pick_some_of_mem`, line 151).

```
# Gloss
pick [0, 1, 2] (is_even)  =  some 0
pick [1, 3]    (is_even)  =  none
```

### 2. The representative

<details>
<summary>Lean source: pQ (optional)</summary>

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 223–225
def pQ (D : List Nat) (Q : List (Nat → Nat)) : Nat → Nat :=
  fun x =>
    (pick D (fun z => decide (sigList Q z = sigList Q x))).getD 0
```

</details>

The representative of `x` is the first datum of the carrier whose
signature equals the signature of `x`. There are three steps: find x's
signature, scan the carrier in its declared order, and return the first
input with that signature.

`decide (… = …)` turns the
equality of two lists into the `true` or `false` that `pick` needs.
`.getD 0` unwraps the `Option`: `some a` becomes `a`, and `none` becomes
`0`. On the carrier, `none` never happens, because `x` itself has the
signature of `x`. If the search does return `none`, the default supplies
a value so that the function is defined at every natural number.
The numeral 0 alone does not reveal whether it was picked or used as a
fallback; the on-carrier theorem supplies that distinction.

The docstring above the definition (lines 213–222) states the scope
exactly: `pQ` is adequate for `Q` and factors through every `Q`-adequate
presentation, "uniquely on that presentation's image over `D`; nothing is
claimed off-image or for undeclared question families."

```python
# Python (research), research/actor_institution/model.py lines 154–159
def representative(n: int, Q: Institution, x: int) -> int:
    """`pQ`: the first datum with the signature of `x`."""
    for z in range(n):
        if sig(Q, z) == sig(Q, x):
            return z
    raise AssertionError("x is its own witness")
```

```
# Gloss
on [0, 1, 2] with Q = (p1, p2) from Unit 00, signatures (0,0), (1,1), (0,1):
    representative of 0 is 0,  of 1 is 1,  of 2 is 2    (all signatures differ)
with Q = (p1) alone, signatures 0, 1, 0:
    representative of 0 is 0,  of 1 is 1,  of 2 is 0    (2 is merged with 0)
```

### 3. What the representative carries

<details>
<summary>Lean source: pQ_spec (optional)</summary>

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 227–245
/-- On `D`, the representative is in `D` and carries the point's
signature. -/
theorem pQ_spec (D : List Nat) (Q : List (Nat → Nat)) (x : Nat)
    (hx : x ∈ D) :
    pQ D Q x ∈ D ∧ sigList Q (pQ D Q x) = sigList Q x := by
  obtain ⟨r, hr⟩ :=
    pick_some_of_mem D
      (fun z => decide (sigList Q z = sigList Q x)) x hx
      (decide_eq_true rfl)
  have hval : pQ D Q x = r := by
    show (pick D
      (fun z => decide (sigList Q z = sigList Q x))).getD 0 = r
    rw [hr]
    rfl
  constructor
  · rw [hval]
    exact pick_mem D _ r hr
  · rw [hval]
    exact of_decide_eq_true (pick_holds D _ r hr)
```

</details>

Read: for `x` on the carrier, its representative is on the carrier and
has the same signature as `x`. The proof: `x` passes its own test
(`decide_eq_true rfl`: the signature of `x` equals itself), so
`pick_some_of_mem` says something is picked, call it `r`. `hval` says the
representative is that `r` (unfold `pQ`, replace the pick by `some r`,
and `some r` unwrapped is `r`). Then `pick_mem` puts `r` on the carrier
and `pick_holds` says `r` passed the test, that is, its signature equals
the signature of `x`.

## The theorem

<details>
<summary>Lean source: pQ_exact (optional)</summary>

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 247–264
/-- The fibers of `pQ` over `D` are exactly the signature classes. -/
theorem pQ_exact (D : List Nat) (Q : List (Nat → Nat)) :
    ∀ x, x ∈ D → ∀ x', x' ∈ D →
      (pQ D Q x = pQ D Q x' ↔ SigEq Q x x') := by
  intro x hx x' hx'
  constructor
  · intro h
    apply (sigEq_iff_sigList Q x x').mpr
    have s1 := (pQ_spec D Q x hx).2
    have s2 := (pQ_spec D Q x' hx').2
    rw [← s1, ← s2, h]
  · intro h
    have hs := (sigEq_iff_sigList Q x x').mp h
    show (pick D
        (fun z => decide (sigList Q z = sigList Q x))).getD 0 =
      (pick D
        (fun z => decide (sigList Q z = sigList Q x'))).getD 0
    rw [hs]
```

</details>

Read it aloud: "for every datum `x` on the carrier and every datum `x'`
on the carrier, the representative merges `x` and `x'` exactly when every
member of the family gives `x` and `x'` the same value." A *fiber* of a
presentation is a set of data it gives one value to; a *signature class*
is a set of data with one signature. The docstring says the two
collections of sets coincide.

Equal signatures start the same first-match search and return the same input. Conversely, equal representative inputs have one signature; each selected input carries the signature it represents. Therefore the original signatures agree too.

<details>
<summary>Detailed proof steps (optional)</summary>

## The proof, step by step

**Step 1. `intro x hx x' hx'`.** Fix two data on the carrier: `x` with
`hx : x ∈ D` and `x'` with `hx' : x' ∈ D`. The goal is the `↔`.

**Step 2. `constructor`.** An `↔` is two implications. The first bullet
proves left to right, the second right to left.

**Step 3. Left to right, `intro h`.** Assume `h : pQ D Q x = pQ D Q x'`.
The goal is `SigEq Q x x'`.

**Step 4. `apply (sigEq_iff_sigList Q x x').mpr`.** By Unit 00's
theorem, read right to left, it is enough to prove the signatures are
equal: the goal becomes `sigList Q x = sigList Q x'`.

**Step 5. `have s1`, `have s2`.** From `pQ_spec`, second half: `s1 :
sigList Q (pQ D Q x) = sigList Q x` and `s2 : sigList Q (pQ D Q x') =
sigList Q x'`. The representative of each datum has that datum's
signature.

**Step 6. `rw [← s1, ← s2, h]`.** Rewrite the goal from right to left
with `s1`: `sigList Q x` becomes `sigList Q (pQ D Q x)`. Likewise with
`s2` on the other side. The goal now reads `sigList Q (pQ D Q x) =
sigList Q (pQ D Q x')`. Rewrite with `h`: the representative of `x` is
the representative of `x'`, so both sides are the same expression, and
`rw` closes a goal whose two sides are identical.

**Step 7. Right to left, `intro h`.** Assume `h : SigEq Q x x'`. The goal
is `pQ D Q x = pQ D Q x'`.

**Step 8. `have hs`.** By Unit 00's theorem read left to right, `hs :
sigList Q x = sigList Q x'`.

**Step 9. `show …`.** Unfold both representatives to what `pQ` computes:
a `pick` over the carrier with the test "signature equals the signature
of `x`", and the same with `x'`. The two sides differ in one place only,
`x` against `x'` inside the test.

**Step 10. `rw [hs]`.** Replace `sigList Q x` by `sigList Q x'` on the
left. The two sides are now the same expression, letter for letter, and
the goal closes.

That is the whole proof: the representative is defined through the
signature, so equal signatures give the same first match (Step 10), and
the same first match carries one signature (Step 6).

</details>

## The same fact in Python

`model.representative` is the same first-match search, written as a loop.
The check compares it with equality of signatures on every pair of data
for `range(n)`, `1 ≤ n ≤ 4`. Its families are the empty family, each
single partition, and one ordering of each pair of distinct partitions:
2098 pairs, no disagreement. It does not enumerate all ordered lists or
repeated members, and does not check outside those carriers. The Lean
theorem covers arbitrary carrier lists and families.

```
python textbook/institutions/checks/i01_representative.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `Option Nat`, `some`, `none`, `.getD 0` | the result of a search that may find nothing | metatheory. The default `0` is a value Lean needs so that `pQ D Q` is defined at every number; inside the theorem (`x ∈ D`) the search always finds `x` at the latest, and the default is never used. |
| `decide` | turning list equality into a Boolean for `pick` | metatheory: equality of lists of numbers is decidable by comparing entries |
| `Nat → Nat` for `pQ D Q` | the representative as a presentation | metatheory function type; the system holds its table on `D` |
| `∀ x, x ∈ D → …` | both quantifiers | over the finite carrier |
| `obtain`, `rw`, `show`, `constructor` | checking the proof | metatheory |

**What the system holds.** The carrier and the family's tables, and now
one more table, the representative's values on the carrier. It is
computed from the tables by a list search; no new datum is admitted. Off
the carrier the function `pQ D Q` has values (`0`, or whatever the search
returns for a number that is not in `D`), and nothing in this part reads
them.

**Admissions relied on, and their price.** Unit 00's three (a presentation
is a function, a family is a list, the carrier is shared). One convention,
not an admission: the representative of a class is the *first* datum of
the class in carrier order. Any other choice of one datum per class would
give the same fibers, and the theorem is about fibers. The choice of the
first supplies a deterministic list-search rule. Other explicitly
specified choices could also be computable; this source uses the first.

**Phrases to read with care.**

- "The institution as one actor" names the representative. It is a table
  computed from the members' tables. No member holds it, and the system
  gained no viewpoint by computing it.
- "The family cannot tell `x` from `x'`" means the signatures agree; it
  does not mean anyone tried.
- "Exactly" in the claim means both directions of the `↔`, nothing more:
  the representative loses no distinction the family makes and adds none.

## What it shows, and what it does not

It shows that a family, however many members it has, is summarized by one
presentation as far as merging and telling apart go: the representative's
fibers are the signature classes. That is why Unit 02 can define what the
family knows through one function.

It shows the summary is exact, not approximate: no pair the family tells
apart is merged, no merged pair is told apart.

It does not show that the representative is the only such presentation.
The sealed file proves more about its place among presentations
(`pQ_adequate`, `pQ_coarsest`, lines 267–280): it factors through every
presentation that is adequate for the family. This unit uses only
exactness.

It does not show anything about what the values of the representative
mean. They are data numbers, the first datum of each class; the meaning
of a class is nothing beyond which data are in it.

## Sources

| Item | Where |
|---|---|
| `pick`, `pick_mem`, `pick_holds`, `pick_some_of_mem` | `lean4/Derivation/Compression.lean` lines 109–160 |
| `pQ` and its scope docstring | `lean4/Derivation/Compression.lean` lines 213–225 |
| `pQ_spec` | `lean4/Derivation/Compression.lean` lines 227–245 |
| `pQ_exact` | `lean4/Derivation/Compression.lean` lines 247–264; sealed axiom report in `artifacts/lean_axioms.txt` |
| Python mirror | `research/actor_institution/model.py` lines 154–159 |
| Check | `textbook/institutions/checks/i01_representative.py` |
| Ledger | `paper/paper_claim_ledger.md`, `CL-PD2-COMPRESSION` (part B: `pQ` exact, adequate, coarsest); consumed by `research/two_theorems` as `actor` (TT-08) |
