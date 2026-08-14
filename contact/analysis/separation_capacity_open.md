# The separation capacity bound — OPEN, with the exact residual

Status: **OPEN**. This document records what is proved, what is not, and
precisely where the remaining obstruction sits, so that the gap is not
mistaken for a gap in motivation.

`lean4/Derivation/SeparationCapacity.lean` proves the STRUCTURAL half
only. Nothing about coloured views, finite view alphabets, repair
strategies, or "no absolute interior" is proved anywhere in this
repository, and no declaration in `lean4/` carries those names.

---

## 1. What is proved (on disk, axiom-checked)

| theorem | statement | axioms |
|---|---|---|
| `SeparationCapacity.profileD_deep` | every deep radius-`d` ball has the constant profile | `propext, Quot.sound` |
| `SeparationCapacity.depth_d_outrun` | all deep-interior points share one depth-`d` profile; horizon-free | `propext, Quot.sound` |
| `SeparationCapacity.depth_d_obstruction` | a colliding deep pair exists from `n ≥ 2d + 3` | `propext, Quot.sound` |
| `SeparationCapacity.sealed_depth2_is_radius_one` | the sealed `depth2_obstruction_n5` threshold is the `d = 1` instance | `propext, Quot.sound` |
| `SeparationCapacity.deep_interior_singleton_at_four` | at `n = 4`, radius 1, the deep interior is `{2}` | `propext, Quot.sound` |

These are bound to the sealed generator: `profileD` is built from
`Generator.profile1` on `Generator.reflState`, and `profileD_deep`
spends `Generator.middle_profile`. They are not a private mirror.

**Radius convention (residual closed).** Sealed `Generator.profile2`
(`Generator.lean:277`) reads the centre plus its in- and out-neighbour
profiles — the ball `{i-1, i, i+1}`, radius ONE. So sealed "depth `k`"
indexes radius `k-1`, and `2 * d + 3` at `d = 1` is `n = 5`, exactly
`Generator.depth2_obstruction_n5`. A prior mirror that put the first
depth-2 collision at `n = 7` was computing radius 2, i.e. sealed depth
3. Both were correct; they indexed differently. The two theorems in §3
of the module record the correspondence.

---

## 2. What is NOT proved

The capacity bound — "a view that factors through the depth-`d` colour
ball, with at most `B` distinguishable encoded balls, fails to separate
some deep pair once `n ≥ B + 2d + 2`" — is **not** in this repository.
It needs a finite pigeonhole, and the pigeonhole is the blocker.

Consequently none of the following exists here, and none should be
cited as if it did:

- any coloured-ball capacity theorem;
- any `LocalStrategy` / repair-strategy class exclusion;
- any statement about identity-grade observation;
- any "no absolute interior" or "no outside" result.

---

## 3. The exact residual: a choice-free pigeonhole

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
`pigeonhole` follows via `Decidable.byContradiction` — which is
axiom-free, provided the existential is written so each binder is
immediately guarded by its bound:

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

**Next step for whoever resumes this.** Bisect `nodup_length_le` by
splitting it into separately-reported lemmas and running
`#print axioms` on each fragment; the leak is inside it, not in any
lemma it cites. Do not add Mathlib for this — it does not help.

---

## 4. Discipline note

`depth_d_outrun` is a statement about STRUCTURAL profiles on the
reflective chain. It is not a locality theorem about arbitrary
observation regimes, and it does not by itself bound what a coloured or
encoded view can distinguish. Any argument that wants the latter must
go through the capacity bound, which is OPEN. In particular, a capacity
statement whose `view` is an unconstrained `Nat → Fin A` proves nothing
about depth-bounded observation: without a hypothesis forcing `view` to
factor through the ball, the radius plays no role in the proof and the
result is ordinary global pigeonhole.
