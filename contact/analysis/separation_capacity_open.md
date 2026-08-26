# The separation-capacity bound — CLOSED, with two exact residuals

Status: **CAPACITY BOUND PROVED**. Exactly two obligations remain OPEN in
this investigation: the general-`n` correspondence between
`Generator.profile2` and `SeparationCapacity.profileD · · 1`, and a
repair-strategy-class consequence built from the capacity theorem. This
document records the proved boundary and those residuals so neither is
mistaken for an unproved capacity bound.

`lean4/Derivation/SeparationCapacity.lean` proves the STRUCTURAL half
and the two sealed radius correspondences. The companion modules
`Pigeonhole.lean` and `CapacityBound.lean` prove the finite-alphabet
coloured capacity bound. A strategy-class consequence remains OPEN.
Identity-grade observation, absolute interior, and "no outside" are
outside this investigation's statement language; they are not counted
as additional OPEN residuals here.

---

## 1. What is proved (on disk, axiom-checked)

| theorem | statement | axioms |
|---|---|---|
| `SeparationCapacity.profileD_deep` | every deep radius-`d` ball has the constant profile | `propext, Quot.sound` |
| `SeparationCapacity.depth_d_outrun` | all deep-interior points share one depth-`d` profile; horizon-free | `propext, Quot.sound` |
| `SeparationCapacity.depth_d_obstruction` | a colliding deep pair exists from `n ≥ 2d + 3` | `propext, Quot.sound` |
| `SeparationCapacity.radius_one_agrees_with_sealed_depth2_n5` | over the interior of `reflState 5`, sealed `Generator.profile2` equality and radius-one `profileD` equality are the same relation; plus the sealed `Generator.depth2_obstruction_n5` collision carried across it | `propext, Quot.sound` |
| `SeparationCapacity.radius_one_agrees_with_sealed_depth2_n4` | the same equivalence over the interior of `reflState 4`; plus the sealed `Generator.depth2_separates_near_ends_n4` separation carried across it, and the arithmetic fact that at `n = 4`, radius 1, the deep interior is `{2}` | `propext, Quot.sound` |

`profileD` is built from `Generator.profile1` on `Generator.reflState`,
and `profileD_deep` spends `Generator.middle_profile`, so these
statements are about the sealed chain rather than a private mirror. The
two §3 theorems go further and consume the sealed theorems themselves;
the next paragraph says exactly how far that reaches and where it stops.

**Radius convention (sealed instances transported; general `n` OPEN).**
Sealed `Generator.profile2` (`Generator.lean:277`) reads the centre plus
its in- and out-neighbour profiles — the ball `{i-1, i, i+1}`, radius
ONE. Under that reading sealed "depth `k`" indexes radius `k-1`, and
`2 * d + 3` at `d = 1` is `n = 5`, the length of
`Generator.depth2_obstruction_n5`. A prior mirror that put the first
depth-2 collision at `n = 7` was computing radius 2, i.e. sealed depth
3. Both were correct; they indexed differently.

What §3 of the module proves is a typed equivalence, one per sealed
chain: over the interior indices of `reflState 5` (resp. `reflState 4`),
`Generator.profile2 s i = Generator.profile2 s j` holds exactly when
`profileD n i 1 = profileD n j 1`, decided elementwise. Each sealed
theorem is then carried across its own equivalence, so
`profileD 5 2 1 = profileD 5 3 1` is derived FROM
`Generator.depth2_obstruction_n5` rather than re-instantiated from
`depth_d_obstruction`, and `profileD 4 1 1 ≠ profileD 4 3 1` is derived
from `Generator.depth2_separates_near_ends_n4`.

**What that does not settle.** The equivalence is decided on those two
chains only. No general-`n` statement relating `Generator.profile2` to
`profileD · · 1` is proved, so the radius convention is reconciled at
the sealed instances and remains OPEN as a general claim. An earlier
version of this document called that residual closed, and the module
docstring said both sealed instances were "recovered"; at that time §3
contained no theorem mentioning `Generator.profile2` at all and neither
of its theorems consumed a sealed theorem. Both statements are
withdrawn and replaced by the scope above.

---

## 2. What remains OPEN

**The capacity bound is now PROVED and this section is narrowed
accordingly.** It reads, as stated here originally: "a view that
factors through the depth-`d` colour ball, with at most `B`
distinguishable encoded balls, fails to separate some deep pair once
`n ≥ B + 2d + 2`". It is `CapacityBound.capacity_bound` in
`lean4/Derivation/CapacityBound.lean`, within `{propext, Quot.sound}`,
with `B = k ^ (2d + 1)` for a `k`-colour alphabet. The earlier text of
this section — that the bound is "**not** in this repository" and that
"the pigeonhole is the blocker" — is WITHDRAWN; §3 records how the
blocker was closed and §5 records exactly what the theorem does and
does not say.

Note what changed and what did not. `B` is no longer an assumption: it
is DERIVED by counting the colourings of a radius-`d` ball, so it
depends on the radius and the alphabet and not on `n`. That is what
makes the statement a capacity bound rather than the ordinary global
pigeonhole §4 warns about.

The following former residual statement is WITHDRAWN as of 2026-08-26:
"Exactly two residuals remain OPEN: the general-`n` radius
correspondence, and a `LocalStrategy` / repair-strategy-class exclusion
derived from the capacity theorem." Both are now closed in their exact
declared scopes. `radius_one_agrees_with_sealed_depth2` proves the first
for arbitrary interior indices and chain length.
`LocalFiniteAlphabet.strategy_capacity_collision` applies
`CapacityBound.capacity_bound` to every member of the explicitly
declared class, and `G1Class.g1_class_exclusion` proves the class-relative
cycle exclusion. The latter does not quantify over every possible repair
channel and leaves OB-1 unchanged.

Identity-grade observation, absolute interior, and "no outside" are
outside this investigation's statement language. This document makes no
claim about them and does not list them as additional OPEN obligations.

---

## 3. The choice-free pigeonhole — CLOSED

The gate is `ci/check_lean_audit.py`: every `#print axioms` report must
lie within `{propext, Quot.sound}`. The pigeonhole must therefore avoid
`Classical.choice`.

**Why the obvious routes fail.** Each of these core lemmas is itself
`Classical.choice`-dependent, verified by `#print axioms`:

- `List.length_erase`
- `List.Nodup.mem_erase_iff`
- `List.filter_eq_nil_iff`
- `List.nodup_range`

Mathlib is not a dependency of this project, and would not help anyway:
`Fintype.card_le_of_injective` carries `Classical.choice` too.

**The working approach.** Rebuild the counting argument from `filter`
rather than `erase`. Target lemma:

> `nodup_length_le : ∀ B l, l.Nodup → (∀ x ∈ l, x < B) → l.length ≤ B`

by induction on `B`, splitting `l` into `filter (· == B)` (length ≤ 1
because `l` is duplicate-free) and `filter (!· == B)` (length ≤ `B` by
the induction hypothesis, since its elements are `< B`). From it,
`pigeonhole` follows via `Decidable.byContradiction` — whose enumerated
axiom report is choice-free, provided the existential is written so each
binder is immediately guarded by its bound:

```
∃ p, p < B + 1 ∧ ∃ q, q < B + 1 ∧ p ≠ q ∧ f p = f q
```

The shape `∃ p q, p < B + 1 ∧ q < B + 1 ∧ …` does NOT synthesize a
`Decidable` instance, because `p < B + 1` then sits inside the `q`
binder. This is a real trap and cost a full debugging pass.

**Status of that approach.** Five of six supporting lemmas were brought
within the gate in a scratch development:

| lemma | axioms |
|---|---|
| `beq_false_of_ne` | `propext, Quot.sound` |
| `length_filter_split` | `propext, Quot.sound` |
| `filter_eq_nil_of_none` | `propext` |
| `nodup_filter_eq_le_one` | `propext, Quot.sound` |
| `filter_nodup` | `propext` |
| `nodup_length_le` | **`propext, Classical.choice, Quot.sound`** |

Only `nodup_length_le` still leaks, and the source was not isolated.
The following were each checked directly with `#print axioms` and are
clean, so none of them is the cause: `List.mem_filter`,
`List.mem_cons_self`, `List.nodup_cons`, `List.Nodup.sublist`,
`List.filter_sublist`, `List.filter_cons`, `beq_self_eq_true`,
`ne_of_beq_false`, `Bool.noConfusion`, `absurd`, `Nat.not_lt_zero`,
`Nat.le_refl`, `Nat.lt_of_le_of_ne`, `Nat.le_of_lt_succ`,
`Decidable.byContradiction`, and `omega` on the relevant goal shape.
Replacing the `erase` step, the `beq`/`rw` step, and the
`omega`-on-disequality step with self-proved or explicit terms did not
remove the dependency.

**Resolution.** The leak was NOT inside `nodup_length_le`, and the
bisection proposed above would not have found it. Every lemma listed as
"checked and clean" was checked at the wrong place: `#print axioms F`
reports the axioms of `F`'s own proof term, NOT of the instances a use
site supplies. The carrier was the `ReflBEq Nat` INSTANCE, required by
`beq_self_eq_true` at `Nat`, measured on Lean 4.33.0:

| probe | axioms |
|---|---|
| `LawfulBEq Nat` | `propext, Quot.sound` |
| `ReflBEq Nat` | **`propext, Classical.choice, Quot.sound`** |
| `(B == B) = true` at `Nat` | **`propext, Classical.choice, Quot.sound`** |
| `(b == b) = true` at `Bool` | `propext, Quot.sound` |

So every route through `x == B` on `Nat` carried the dependency,
however the surrounding proof was written. Controls: the equation
compiler alone reports no axioms, and the `induction`-tactic variant
leaked identically, so neither the recursion machinery nor any cited
lemma was responsible.

The fix is to use `decide (x = B)` in place of `x == B`;
`of_decide_eq_true`, `of_decide_eq_false` and `decide_eq_false` have
choice-free enumerated reports. `List.range` is still avoided, since
`List.nodup_range` is
choice-dependent; `Pigeonhole.upto` is used instead. The development is
`lean4/Derivation/Pigeonhole.lean`: `nodup_length_le` and `pigeonhole`
both report `propext, Quot.sound`.

A second instance of the same trap appeared while proving
`CapacityBound.encode_inj`: a bare `simp` closing a length-mismatch
case pulled `Classical.choice` in from the default simp set. Replacing
it with `Nat.noConfusion` cleared it. **Neither leak was in a cited
lemma; both were in something the proof text did not name.**

---

## 4. Discipline note

`depth_d_outrun` is a statement about STRUCTURAL profiles on the
reflective chain. It is not a locality theorem about arbitrary
observation regimes, and it does not by itself bound what a coloured or
encoded view can distinguish. Any argument that wants the latter must
go through the capacity bound, which is now proved — see §5. In
particular, a capacity statement whose `view` is an unconstrained
`Nat → Fin A` proves nothing about depth-bounded observation: without a
hypothesis forcing `view` to factor through the ball, the radius plays
no role in the proof and the result is ordinary global pigeonhole.

That warning is retained because it is exactly the condition the proof
had to meet, and `CapacityBound.ViewLocal` is what meets it.

---

## 5. The capacity bound, and its exact scope

`CapacityBound.capacity_bound`. Let `colour` take values below `k`, and
let `v` factor through the radius-`d` colour ball
(`CapacityBound.ViewLocal`). Then once

    n ≥ k ^ (2d + 1) + 2d + 2

the deep interior of `reflState n` holds two distinct points that `v`
does not separate. Axioms: `propext, Quot.sound`.

**Why the radius is load-bearing here.** `B = k ^ (2d + 1)` is not
assumed, it is DERIVED: it counts the colourings of a radius-`d` ball,
so it is a function of the radius and the alphabet and of nothing else.
It does not grow with `n`. The deep interior holds `n - 2d - 1` points,
so the threshold is exactly where that interior first holds `B + 1`
points. Remove `ViewLocal` and `B` reverts to an assumption, the radius
becomes inert, and the statement degenerates to §4's warning.

**What this does NOT settle.**

- `k ^ (2d + 1)` is an UPPER bound on the number of distinguishable
  balls, obtained by counting colourings. No matching lower bound is
  proved and no tightness is claimed.
- Nothing is claimed for views that do NOT factor through the ball.
- `colour` is an arbitrary bounded colouring. Nothing is claimed about
  the sealed `Generator.profile2` colouring in particular, and nothing
  here relates the two.
- The former sentence saying the general-`n` correspondence and a
  repair-strategy-class consequence remained OPEN is WITHDRAWN. Their
  exact scoped closures are recorded in §2. Unrestricted repair channels
  remain outside the theorem, so OB-1 is unchanged.
- Identity-grade observation, absolute interior, and "no outside" remain
  outside this investigation's statement language.
- Non-vacuity is exhibited rather than assumed:
  `capacity_at_one_colour` is the degenerate end, and
  `local_view_can_separate` fixes `k = 2`, `d = 0`, and `n = 3`, proves
  that indices `1` and `2` are deep and below the threshold `4`, and
  exhibits a local parity view separating every distinct deep pair (and
  explicitly `1` from `2`). Thus the forced-collision conclusion is
  false at this below-threshold instance rather than merely false for
  one selected pair.
