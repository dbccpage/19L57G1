# Unit 04. A family knows what no member knows

**Claim.** A nonempty family can determine a question that none of its
members determines alone. The smallest such case has three distinct
inputs and two members. The empty-family constant-question case is separate.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** A family can know a claim that none of its members knows, and
it does so exactly when every pair the claim tells apart is told apart by
some member, while every member merges some pair the claim tells apart.
For a nonempty family this needs at least three distinct data and two
members, and three data with two
two-valued members suffice.

**Status:** derived. **Lean:** `Inst.exceeds_iff`, `Inst.exceeds_three_data`,
`Inst.exceeds_three_two` (`actor_institution`). **Sources:**
`research/actor_institution/lean/ResearchActorInstitution/Institution.lean`
lines 45–196; `lean4/Derivation/Compression.lean` lines 296–322.

This is the first theorem of the part about the gap between a family and
its members. Unit 02 defined what a family knows through its
representative. A member, taken alone, is a one-member family with its
own representative. The two can come apart: the family's representative
can determine a claim that no member's does. The unit says exactly when,
how small the smallest such case is, and shows it. Nothing in it is about
anyone being aware of anything.

</details>

## First pass

Use the three-input example from I00, now with a requested answer:

| Input | First member | Second member | Requested answer |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 0 |
| 2 | 0 | 1 | 1 |

The first member merges 0 with 2, whose requested answers differ. It
cannot determine the answer alone. The second merges 1 with 2 and
fails for the same reason. Together their answer pairs are all distinct,
so a lookup from those pairs can return the requested answer.

The minimum-size theorem assumes a nonempty family. With no members,
the phrase no member knows it has no member to test: a constant question
is a degenerate case, not an example of useful cooperation.

**Predict:** must one member have access to the combined table?

<details><summary>Check your prediction</summary>

No. The theorem supplies recoverability from the family signature. It
does not define communication, access, or an actor who performs the lookup.

</details>

## What you need first

Use I00’s answer signatures, I02’s one-lookup condition and I03’s conflicting-pair test. Here we apply those checks to the full family and then to each member separately.

<details>
<summary>Prerequisite source names (optional)</summary>

Unit 00 (`SigEq`), Unit 02 (`Knows`, `knows_iff_determined`) and Unit 03
(`not_knows_iff_witness`).

</details>

Keep two checks separate. First ask whether the combined answers recover
the requested table. Then test each member on its own. A family can pass
the first check while every member fails the second.

### 1. Exceeding

For the running example, the combined lookup sends `[0,0]` to 0,
`[1,1]` to 0 and `[0,1]` to 1. It works on all three supplied inputs.
Now examine the pairs on which the requested answers differ:

| Pair | First member | Second member |
|---|---|---|
| 0 and 2 | Merges the pair | Separates the pair |
| 1 and 2 | Separates the pair | Merges the pair |

For each required pair, at least one member separates it. The successful
member can depend on the pair. This does not say that one member must
separate every required pair. Each member also has its own failure pair.

<details>
<summary>Lean source: Exceeds (optional)</summary>

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Institution.lean lines 45–47
/-- The family knows `q`, and no single member does. -/
def Exceeds (D : List Nat) (Q : Institution) (q : Nat → Nat) : Prop :=
  Knows D Q q ∧ ∀ p, p ∈ Q → ¬ Knows D [p] q
```

</details>

The family `Q` knows `q`, and for every member `p`, the one-member family
`[p]` does not. "No single member" is literal: it is about each member on
its own, as a family of one.

```python
# Python (research), research/actor_institution/model.py lines 145–147
def exceeds(n: int, Q: Institution, q: Presentation) -> bool:
    """`Inst.Exceeds`: the family knows `q` and no member alone does."""
    return knows(n, Q, q) and all(not knows(n, (p,), q) for p in Q)
```

### 2. One-member families

<details>
<summary>Lean source: sigEq_single, not_knows_single_iff (optional)</summary>

```lean
-- Lean (research), the same file, lines 49–62
theorem sigEq_single (p : Nat → Nat) (x y : Nat) : SigEq [p] x y ↔ p x = p y := by
  constructor
  · intro h; exact h p List.mem_cons_self
  · intro h q hq
    rw [List.mem_singleton.mp hq]; exact h

theorem not_knows_single_iff (D : List Nat) (p q : Nat → Nat) :
    ¬ Knows D [p] q ↔ ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ p x = p y ∧ q x ≠ q y := by
  rw [not_knows_iff_witness]
  constructor
  · rintro ⟨x, hx, y, hy, hs, hne⟩
    exact ⟨x, hx, y, hy, (sigEq_single p x y).mp hs, hne⟩
  · rintro ⟨x, hx, y, hy, hs, hne⟩
    exact ⟨x, hx, y, hy, (sigEq_single p x y).mpr hs, hne⟩
```

</details>

A one-member family merges two data exactly when its member gives them
the same value (`sigEq_single`: the signature is the one-entry list
`[p x]`). So, by Unit 03's witness theorem, a member fails to know `q`
exactly when it merges some pair that `q` tells apart
(`not_knows_single_iff`).

### 3. A witnessed difference has a separating member

<details>
<summary>Lean source: exists_separator_of_not_sigEq (optional)</summary>

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 309–322
/-- From disagreement, a witnessing question is constructed by list
recursion. -/
theorem exists_separator_of_not_sigEq (Q : List (Nat → Nat))
    (x x' : Nat) (h : ¬ SigEq Q x x') :
    ∃ q, q ∈ Q ∧ q x ≠ q x' := by
  induction Q with
  | nil => exact absurd (fun q hq => by cases hq) h
  | cons q T ih =>
    cases sigEq_decompose q T x x' h with
    | inl hq => exact ⟨q, List.mem_cons_self, hq⟩
    | inr ht =>
      obtain ⟨q', hm, hne⟩ := ih ht
      exact ⟨q', List.mem_cons_of_mem _ hm, hne⟩
```

</details>

If the family tells `x` from `x'`, some member does. The proof walks the
family: the empty family merges everything, so the hypothesis is absurd
there; at a member `q` with tail `T`, `sigEq_decompose` (lines 298–308)
decides, with `decide (q x = q x')`, whether `q` itself separates the
pair, and if not, the tail must. The proof supplies the separating member
by a list search.

## The theorem

<details>
<summary>Lean source: exceeds_iff (optional)</summary>

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Institution.lean lines 64–88
/-- **Exact condition.**  The family exceeds its members on `q` iff every
pair that `q` tells apart is told apart by some member, and every member
merges some pair that `q` tells apart. -/
theorem exceeds_iff (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Exceeds D Q q ↔
      (∀ x, x ∈ D → ∀ y, y ∈ D → q x ≠ q y → ∃ p, p ∈ Q ∧ p x ≠ p y) ∧
      (∀ p, p ∈ Q → ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ p x = p y ∧ q x ≠ q y) := by
  unfold Exceeds
  constructor
  · rintro ⟨hk, hm⟩
    refine ⟨?_, fun p hp => (not_knows_single_iff D p q).mp (hm p hp)⟩
    intro x hx y hy hne
    apply exists_separator_of_not_sigEq
    intro hs
    exact hne ((knows_iff_determined D Q q).mp hk x hx y hy hs)
  · rintro ⟨hsep, hm⟩
    refine ⟨?_, fun p hp => (not_knows_single_iff D p q).mpr (hm p hp)⟩
    rw [knows_iff_determined]
    intro x hx y hy hs
    cases Nat.decEq (q x) (q y) with
    | isTrue h => exact h
    | isFalse hne =>
      exfalso
      obtain ⟨p, hp, hpne⟩ := hsep x hx y hy hne
      exact hpne (hs p hp)
```

</details>

Read: the family exceeds its members on `q` exactly when two things hold.
First, the members between them cover `q`: whenever `q` gives two data
different values, some member does too. Second, no member covers `q`
alone: each member gives the same value to some pair that `q` tells
apart.

The combined lookup can recover q only if some member separates each pair on which q differs. Conversely, if those pairs are all separated, equal combined signatures force equal q-values, so a lookup exists. Testing each member separately supplies the additional failure-pair condition.

<details>
<summary>Detailed proof steps (optional)</summary>

## The proof, step by step

**Step 1. `unfold Exceeds`.** The left side becomes `Knows D Q q ∧ ∀ p,
p ∈ Q → ¬ Knows D [p] q`.

**Step 2. `constructor`.** Two implications.

**Step 3. Left to right, `rintro ⟨hk, hm⟩`.** Assume `hk`: the family
knows `q`, and `hm`: no member does. The goal is the two clauses.

**Step 4. `refine ⟨?_, fun p hp => (not_knows_single_iff D p q).mp (hm p hp)⟩`.**
The second clause is section 2 read left to right: for each member `p`,
`hm p hp` says `[p]` does not know `q`, which is a pair `p` merges and `q`
splits. The first clause is left as the goal.

**Step 5. `intro x hx y hy hne`.** Fix two data on the carrier with
`hne : q x ≠ q y`. The goal is a member that tells them apart.

**Step 6. `apply exists_separator_of_not_sigEq`.** By section 3, it is
enough that the family tells them apart: the goal becomes `¬ SigEq Q x y`.

**Step 7. `intro hs; exact hne (…)`.** Suppose `hs`: the family merges
`x` and `y`. The family knows `q`, so by Unit 02 `q x = q y`. That
contradicts `hne`. So the family does not merge them, and Step 6 produces
the separating member.

**Step 8. Right to left, `rintro ⟨hsep, hm⟩`.** Assume the two clauses:
`hsep` (the members cover `q`) and `hm` (each member merges a pair `q`
splits).

**Step 9. `refine ⟨?_, fun p hp => (not_knows_single_iff D p q).mpr (hm p hp)⟩`.**
No member knows `q`: section 2 read right to left. Left as the goal: the
family knows `q`.

**Step 10. `rw [knows_iff_determined]; intro x hx y hy hs`.** By Unit 02,
it is enough to show that whenever the family merges two data (`hs :
SigEq Q x y`), `q` gives them the same value. Fix such a pair.

**Step 11. `cases Nat.decEq (q x) (q y)`.** Either `q x = q y` or not.
This is decidable equality of two numbers, a computation, not excluded
middle.

**Step 12. `isTrue h => exact h`.** If they are equal, done.

**Step 13. `isFalse hne => exfalso; obtain ⟨p, hp, hpne⟩ := hsep x hx y hy hne; exact hpne (hs p hp)`.**
If `q` tells them apart, `hsep` gives a member `p` that tells them apart;
but `hs` says every member merges them, in particular `p`. Contradiction.
So the second case cannot occur, and `q x = q y`.

The theorem turns "the family knows what no member knows" into two
conditions that mention only pairs of data and single members, which is
what the counting below and the Python check use.

</details>

## How small the smallest case is

<details>
<summary>Lean source: exceeds_two_members (optional)</summary>

```lean
-- Lean (research), the same file, lines 103–113
/-- **Two members that disagree are necessary.** -/
theorem exceeds_two_members {D : List Nat} {Q : Institution} {q : Nat → Nat}
    (h : Exceeds D Q q) (hne : Q ≠ []) :
    ∃ p, p ∈ Q ∧ ∃ p', p' ∈ Q ∧ ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ p x = p y ∧ p' x ≠ p' y := by
  obtain ⟨hsep, hm⟩ := (exceeds_iff D Q q).mp h
  cases Q with
  | nil => exact absurd rfl hne
  | cons p Q' =>
    obtain ⟨x, hx, y, hy, hpxy, hq⟩ := hm p List.mem_cons_self
    obtain ⟨p', hp', hp'ne⟩ := hsep x hx y hy hq
    exact ⟨p, List.mem_cons_self, p', hp', x, hx, y, hy, hpxy, hp'ne⟩
```

</details>

Take the first member `p`. By the second clause it merges a pair `x`,
`y` that `q` splits; by the first clause some member `p'` splits that
pair. So `p` and `p'` disagree on the pair, and they are two members
(they cannot be the same function, since one merges the pair and the
other does not).

<details>
<summary>Lean source: exceeds_three_data (optional)</summary>

```lean
-- Lean (research), the same file, lines 115–152
/-- **Three distinct data are necessary.**  Two data cannot carry a
distinction that one member merges, another separates, and a third pair
that the second member merges. -/
theorem exceeds_three_data {D : List Nat} {Q : Institution} {q : Nat → Nat}
    (h : Exceeds D Q q) (hne : Q ≠ []) :
    ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ ∃ z, z ∈ D ∧ x ≠ y ∧ y ≠ z ∧ x ≠ z := by
  obtain ⟨hsep, hm⟩ := (exceeds_iff D Q q).mp h
  cases Q with
  | nil => exact absurd rfl hne
  | cons p Q' =>
    obtain ⟨x, hx, y, hy, _, hqxy⟩ := hm p List.mem_cons_self
    obtain ⟨p', hp', hp'ne⟩ := hsep x hx y hy hqxy
    obtain ⟨u, hu, v, hv, hp'uv, hquv⟩ := hm p' hp'
    have hxy : x ≠ y := fun e => hqxy (by rw [e])
    have huv : u ≠ v := fun e => hquv (by rw [e])
    cases Nat.decEq u x with
    | isTrue hux =>
      cases Nat.decEq v y with
      | isTrue hvy =>
        exfalso
        apply hp'ne
        rw [← hux, ← hvy]
        exact hp'uv
      | isFalse hvy =>
        exact ⟨x, hx, y, hy, v, hv, hxy, fun e => hvy e.symm, fun e => huv (hux.trans e)⟩
    | isFalse hux =>
      cases Nat.decEq u y with
      | isTrue huy =>
        cases Nat.decEq v x with
        | isTrue hvx =>
          exfalso
          apply hp'ne
          rw [← hvx, ← huy]
          exact hp'uv.symm
        | isFalse hvx =>
          exact ⟨x, hx, y, hy, v, hv, hxy, fun e => huv (huy.trans e), fun e => hvx e.symm⟩
      | isFalse huy =>
        exact ⟨x, hx, y, hy, u, hu, hxy, fun e => huy e.symm, fun e => hux e.symm⟩
```

</details>

The argument: the first member `p` merges a pair `x ≠ y` that `q` splits;
some member `p'` splits `x`, `y`; `p'` in turn merges a pair `u ≠ v` that
`q` splits. The pair `u`, `v` cannot be the pair `x`, `y` in either order,
because `p'` splits that pair and merges this one. So among `x`, `y`,
`u`, `v` there are at least three distinct data. The case analysis checks
the ways `u` and `v` could coincide with `x` and `y`: if `u = x` and
`v = y` (or `u = y` and `v = x`) then `p'` both merges and splits the same
pair, absurd; otherwise one of `u`, `v` is a third datum, and the proof
names it.

<details>
<summary>Lean source: mem_pair, no_exceeding_on_two_points, no_exceeding_single_member (optional)</summary>

```lean
-- Lean (research), the same file, lines 154–173
theorem mem_pair {x : Nat} (h : x ∈ [0, 1]) : x = 0 ∨ x = 1 := by
  rcases List.mem_cons.mp h with h0 | h1
  · exact Or.inl h0
  · exact Or.inr (List.mem_singleton.mp h1)

/-- On two data no nonempty institution exceeds its members. -/
theorem no_exceeding_on_two_points (Q : Institution) (q : Nat → Nat) (hne : Q ≠ []) :
    ¬ Exceeds [0, 1] Q q := by
  intro h
  obtain ⟨x, hx, y, hy, z, hz, hxy, hyz, hxz⟩ := exceeds_three_data h hne
  have hx' := mem_pair hx
  have hy' := mem_pair hy
  have hz' := mem_pair hz
  omega

/-- A single member never exceeds itself. -/
theorem no_exceeding_single_member (D : List Nat) (p q : Nat → Nat) :
    ¬ Exceeds D [p] q := by
  rintro ⟨hk, hm⟩
  exact hm p List.mem_cons_self hk
```

</details>

The two bounds as refusals: on the two-point carrier `[0, 1]`, three
distinct data cannot be found (each of `x`, `y`, `z` is `0` or `1`, and
`omega` finds the contradiction in those six facts); and a one-member
family cannot both know `q` and have its only member not know it.

The empty family is a degenerate case, put on record rather than hidden
(`exceeds_nil_iff`, lines 90–101): it "exceeds its members" exactly on
claims constant on the supplied carrier. This does not require a function
to be constant at every natural number. The no-member clause has no
member to test. The
bounds above are therefore stated for nonempty families.

## The smallest case

<details>
<summary>Lean source: p1, p2, q3, exceeds_three_two, exceeds_three_two_resolution (optional)</summary>

```lean
-- Lean (research), the same file, lines 177–196
/-- Merges `0` and `2`. -/
def p1 : Nat → Nat := fun x => if x = 1 then 1 else 0
/-- Merges `1` and `2`. -/
def p2 : Nat → Nat := fun x => if x = 0 then 0 else 1
/-- Tells `2` from `0` and `1`. -/
def q3 : Nat → Nat := fun x => if x = 2 then 1 else 0

/-- **Three data, two members, two values suffice.**  Each member merges a
pair that `q3` separates; together they separate everything `q3` does. -/
theorem exceeds_three_two : Exceeds [0, 1, 2] [p1, p2] q3 := by
  unfold Exceeds
  decide

/-- The same witness, read through the exact condition: both members are
two-valued and the question is two-valued, so no cheaper resolution exists
on either side. -/
theorem exceeds_three_two_resolution :
    classCount [0, 1, 2] [p1] = 2 ∧ classCount [0, 1, 2] [p2] = 2 ∧
    classCount [0, 1, 2] [q3] = 2 ∧ information [0, 1, 2] [p1, p2] = 3 := by
  decide
```

</details>

These are Unit 00's three presentations. On `[0, 1, 2]`: `p1 = (0, 1, 0)`
merges `0` and `2`; `p2 = (0, 1, 1)` merges `1` and `2`; `q3 = (0, 0, 1)`
tells `2` from both `0` and `1`. Check the two clauses by hand. The pairs
`q3` splits are `{0, 2}` and `{1, 2}`; `p2` splits the first, `p1` the
second, so the members cover `q3`. And `p1` merges `{0, 2}`, `p2` merges
`{1, 2}`, each a pair `q3` splits, so neither covers `q3` alone. Lean
checks the same by `decide`: `Knows` is decidable on a represented
carrier (`knowsDecidable`, `two_theorems` `Institution.lean` lines 92–96,
built from Unit 02's pairwise form), the quantifier over `[p1, p2]` is a
bounded list quantifier, and the kernel evaluates the whole statement on
the three data. The second theorem says the witness is as small as it can
be in values as well: each member and the claim take two values, and the
family's information is three, the whole carrier. Here the joint count
is 3, while each member and the requested table have 2 classes.

## The same fact in Python

The check compares `model.exceeds` with the two clauses of `exceeds_iff`,
written out directly, for `range(n)`, `1 ≤ n ≤ 4`, the empty family and
one ordering of every subset of at most three distinct partitions,
with every partition as the
claim: 8780 (family, claim) pairs, no disagreement. It then runs the
tree's census (`model.exceeding_census`, `model.exceeding_minimum`): over
nonempty families, no family exceeds with fewer than three data or fewer
than two members, which is the Lean bound; and the three-point example
exceeds, with class counts 2, 2, 2 and 3. These cases do not enumerate
all ordered lists or repeated members, and say nothing outside their
declared population (ledger AI-03c).

```
python textbook/institutions/checks/i04_exceeds.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `Nat.decEq` | "either `q x = q y` or not" | decidable equality of numbers, computed; not excluded middle |
| `decide` | `exceeds_three_two`, `exceeds_three_two_resolution` | kernel evaluation of a closed statement on the concrete carrier `[0, 1, 2]`; needs a `Decidable` instance, here `knowsDecidable` and the bounded list quantifier |
| `omega` | `no_exceeding_on_two_points` | arithmetic on the six membership facts `x = 0 ∨ x = 1`, …; metatheory |
| `∃ p, p ∈ Q ∧ …` | the separating member | discharged by the sealed list recursion, never by choice; the tree's axiom report lists `propext` and `Quot.sound` only |
| `fun x => if x = 1 then 1 else 0` | the concrete members | metatheory functions; the system holds their tables on `[0, 1, 2]` |
| `∀ x, x ∈ D → …`, `∀ p, p ∈ Q → …` | both clauses | over the finite carrier and the finite family |

**What the system holds.** In the example: the carrier `[0, 1, 2]` and
three tables, nine values in all. In general: the carrier and the tables
of the members and the claim. The representative of the family (Unit 01)
is computed from them; nothing is added when the family turns out to
exceed its members.

**Admissions relied on, and their price.** Unit 00's three. The third,
the shared carrier, is what makes the clauses meaningful: "`p1` merges `0`
and `2`" and "`p2` splits `0` and `2`" are about the same data only
because both tables are indexed by one carrier. Unit 05 shows this
admission has teeth: re-indexing one member's data by a swap destroys the
exceeding.

**Phrases to read with care.**

- "The family knows more than any member." "More" is one claim, known by
  the family's representative and by no one-member family's. The counts
  in `exceeds_three_two_resolution` give it a number (three classes
  against two), but the theorem is about a claim, not a quantity.
- "Together", "pooling", "collective". No process combines the members.
  The representative is computed from the tables by a list search in the
  metatheory (Unit 01); the family holds no view of its own.
- "No member knows." No member is unaware; the member's table does not
  determine the claim on some pair.
- "Necessary", "suffice". The bounds are about the carrier and the family
  as lists: at least three data on the carrier, at least two members in
  the list; three and two attained. They say nothing about any other
  representation.

## What it shows, and what it does not

It shows the exact condition for a family to know what no member knows,
in terms of pairs and single members only.

Among nonempty families, three distinct data and two members are needed
and enough. The empty-family case is separate: it exceeds on questions
constant on D, because there is no member to test in the second clause.
The two-member bound is a disagreement: two members that differ
on a pair one of them merges. The witness is smaller than the four-point
parity and half witness of `two_theorems` (`institution_exceeds_members`
there), which was the first proof that the gap exists at all.

It does not show that the family's extra knowledge is available to
anyone. No member's table determines the claim; the combined table does.
Access and communication have not been specified by this definition.

It does not show that exceeding is common or rare. The census counts
cases on at most four data and at most three members (AI-03c); beyond
that bound the unit says nothing.

The displayed example can fail after a change of correspondence. The
specific re-indexing in Unit 05 makes the family lose `q3` (see
`Inst.correspondence_matters`). What a family knows depends on the
admission that its members' tables are tables of the same data.

## Sources

| Item | Where |
|---|---|
| `Exceeds`, `sigEq_single`, `not_knows_single_iff` | `research/actor_institution/lean/ResearchActorInstitution/Institution.lean` lines 45–62 |
| `exceeds_iff` | the same file, lines 64–88 |
| `exceeds_nil_iff`, `exceeds_two_members`, `exceeds_three_data` | the same file, lines 90–152 |
| `mem_pair`, `no_exceeding_on_two_points`, `no_exceeding_single_member` | the same file, lines 154–173 |
| `p1`, `p2`, `q3`, `exceeds_three_two`, `exceeds_three_two_resolution` | the same file, lines 177–196; axiom reports emitted by the tree's `AxiomReport.lean` and checked by `research/actor_institution/verify.py --check` (`propext`, `Quot.sound`; `RECEIPT.md`) |
| `knowsDecidable` | `research/two_theorems/lean/ResearchTwoTheorems/Institution.lean` lines 92–96 |
| `sigEq_decompose`, `exists_separator_of_not_sigEq` | `lean4/Derivation/Compression.lean` lines 296–322 |
| Python mirror | `research/actor_institution/model.py` lines 145–147 (`exceeds`), 166–193 (the census) |
| Check | `textbook/institutions/checks/i04_exceeds.py` |
| Ledger | `research/actor_institution/CLAIMS.md` AI-01 (the condition), AI-02 (the bounds), AI-03 (attained), AI-03c (the census) |
