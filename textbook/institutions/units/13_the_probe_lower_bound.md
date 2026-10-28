# Unit 13. The probe lower bound and the merge adversary

**Claim.** Whenever the transcript of an adaptive protocol `π` against the
identity actor `fun z => z` on `List.range n` has fewer than
`(allPairs n).length = n(n - 1)/2` entries, some pair `x < y < n` was never
probed (`uncovered_pair`), and the actor `merge x y` (which identifies `y` with
`x` and leaves every other datum fixed) produces the exact same transcript as
`fun z => z` (`lower_bound`). Consequently, for any admission rule
`rule : Transcript → Evaluator` and any step budget `k < n(n - 1)/2`, at least
one of the two actors `fun z => z` or `merge x y` fails to be sharply presented
by `rule (run π p k)` (`no_acquisition_below_bound`,
`no_acquisition_in_fewer_steps`, `no_acquisition_below_half_square`), and two
actors of different capability have identical transcripts
(`transcripts_identical_capabilities_differ`). Analogously, at the static
observer level, wherever an observer `E` merges two distinct data `x ≠ y ∈ D`,
two actors (`pQ D (questions E)` and `markOne (pQ D (questions E)) x`) are both
consistent with `E` while one merges `(x, y)` and the other splits it
(`observer_cannot_read_resolution`).
**Status:** derived. **Lean:** `Acquisition.merge`, `Acquisition.merge_agrees`,
`Acquisition.askedB`, `Acquisition.askedB_iff`, `Acquisition.norm`,
`Acquisition.mem_allPairs`, `Acquisition.nodup_subset_length`,
`Acquisition.allPairs_nodup`, `Acquisition.uncovered_pair`,
`Acquisition.lower_bound`, `Acquisition.no_acquisition_below_bound`,
`Acquisition.no_acquisition_in_fewer_steps`,
`Acquisition.no_acquisition_below_half_square`,
`Acquisition.transcripts_identical_capabilities_differ` (`actor_institution`);
`Reading.Consistent`, `Reading.actor_consistent`, `Reading.markOne`,
`Reading.observer_cannot_read_resolution` (`two_theorems`). **Sources:**
`research/actor_institution/lean/ResearchActorInstitution/Acquisition.lean`
lines 155–423; `research/two_theorems/lean/ResearchTwoTheorems/Reading.lean`
lines 99–156.

> **Scope warning — pairwise equality-query complexity vs. general information-acquisition complexity.**
> The $\frac{n(n - 1)}{2}$ lower bound proved in this unit applies **specifically to the unpromised pairwise equality-query model**, in which each query asks a single pair `(x, y)` and learns only the one-bit answer `decide (p x = p y)` (`Acquisition.entry`). It does **not** establish that every institution or observation model needs $\frac{n(n - 1)}{2}$ observations to identify an unknown partition. Stronger query models carry strictly more information per query and acquire the same partition in fewer steps: for example, a **fiber-reveal (class-membership) oracle** that returns the entire equivalence class $\{y \in D \mid p(x) = p(y)\}$ of a queried element $x$ acquires every partition on `List.range n` in at most $n - 1$ queries (at most $3 < 6$ queries on `n = 4`), because revealing the fibers of at most $n - 1$ class representatives forces the remaining elements (`i13_lower_bound.py`).

Unit 12 showed `run_congr`: two actors that answer every asked probe alike have
identical transcripts. This unit constructs the adversary that exploits
`run_congr`. On `List.range n` there are `(allPairs n).length = n(n - 1)/2`
unordered pairs `x < y < n`. If a transcript against the identity actor has
fewer than `(allPairs n).length` entries, a constructive list-length bound
(`nodup_subset_length`) finds an unprobed pair `x < y < n` (`uncovered_pair`).
The presentation `merge x y` agrees with the identity on every pair except
`{x, y}` (`merge_agrees`), so by `run_congr` it produces the same transcript as
the identity (`lower_bound`). Any evaluator `rule T` built from that single
transcript either separates `x` and `y` (failing sharpness for `merge x y`) or
merges `x` and `y` (failing sharpness for `fun z => z`). This resolves both the
lower-bound half of `TT-43o (i)` (`AI-16`) and the transcript indistinguishability
statement `TT-39o` (`AI-20`). It is paired with the static observer theorem
`observer_cannot_read_resolution` (`TT-27`): an observer `E` that merges `x ≠ y`
cannot tell from its own separations whether the observed actor merges or splits
`x` and `y`.

## What you need first

Unit 01 (`pQ`, `pQ_exact`), Unit 05 (`Evaluator`, `verdictB`), and Unit 12
(`Transcript`, `Protocol`, `run`, `run_length_le`, `run_congr`). From the sealed
Genesis spine (`lean4/Derivation/Counting.lean`), `allPairs n` is the list of
all pairs `(i, j)` with `i < j < n`, and `allPairs_length n` shows in Lean
`2 * (allPairs n).length = n * (n - 1)`.

### 1. The merge presentation and unprobed pairs

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Acquisition.lean lines 155–159, 187–197
/-- The presentation that identifies `y` with `x` and nothing else. -/
def merge (x y : Nat) : Nat → Nat := fun z => if z = y then x else z

theorem merge_agrees {x y a b : Nat} (hab : ¬ (a = x ∧ b = y)) (hba : ¬ (a = y ∧ b = x)) :
    (merge x y a = merge x y b) ↔ a = b := by ...

def askedB (T : Transcript) (x y : Nat) : Bool :=
  T.any (fun e => (decide (e.1 = x) && decide (e.2.1 = y)) || (decide (e.1 = y) && decide (e.2.1 = x)))

def norm (e : Nat × Nat × Bool) : Nat × Nat := (min e.1 e.2.1, max e.1 e.2.1)

theorem mem_allPairs (i j : Nat) : ∀ n : Nat, (i, j) ∈ allPairs n ↔ i < j ∧ j < n := by ...
```

`merge x y` maps `y` to `x` and every `z ≠ y` to `z`. Whenever `{a, b} ≠ {x, y}`,
`merge x y a = merge x y b ↔ a = b` (`merge_agrees`). `askedB T x y` checks
whether `T` probed `(x, y)` or `(y, x)`.

### 2. Static consistency and `markOne`

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Reading.lean lines 99–104, 121–122
def Consistent (D : List Nat) (E : Evaluator) (p : Nat → Nat) : Prop :=
  ∀ x, x ∈ D → ∀ y, y ∈ D → verdictB E x y = true → p x ≠ p y

theorem actor_consistent (D : List Nat) (E : Evaluator) :
    Consistent D E (pQ D (questions E)) := by ...

def markOne (p : Nat → Nat) (x : Nat) : Nat → Nat :=
  fun z => 2 * p z + (if z = x then 1 else 0)
```

An observer `E` is `Consistent` with an actor `p` when every pair separated by
`E` is also separated by `p`. Refining `p` to `markOne p x` splits `x` away from
any `y ≠ x` that shared `p`'s fiber (`markOne_separates`) while keeping every
separation `p` already had (`markOne_eq`).

## The theorems

First, the uncovered-pair lemma, the merge adversary, and the lower bound:

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Acquisition.lean lines 277–278, 308, 327–423
theorem nodup_subset_length {α : Type} [DecidableEq α] :
    ∀ (l₁ l₂ : List α), l₁.Nodup → l₁ ⊆ l₂ → l₁.length ≤ l₂.length := by ...

theorem allPairs_nodup : ∀ n : Nat, (allPairs n).Nodup := by ...

theorem uncovered_pair (n : Nat) (T : Transcript) (hshort : T.length < (allPairs n).length) :
    ∃ x y, x < y ∧ y < n ∧ askedB T x y = false := by ...

theorem lower_bound (n : Nat) (π : Protocol) (k : Nat)
    (hshort : (run π (fun z => z) k).length < (allPairs n).length) :
    ∃ x y, x < y ∧ y < n ∧ run π (merge x y) k = run π (fun z => z) k := by ...

theorem no_acquisition_below_bound (n : Nat) (π : Protocol) (rule : Transcript → Evaluator)
    (k : Nat) (hshort : (run π (fun z => z) k).length < (allPairs n).length) :
    ∃ p : Nat → Nat, ¬ Sharp (List.range n) (rule (run π p k)) p := by ...

theorem no_acquisition_in_fewer_steps (n : Nat) (π : Protocol) (rule : Transcript → Evaluator)
    (k : Nat) (hk : k < (allPairs n).length) :
    ∃ p : Nat → Nat, ¬ Sharp (List.range n) (rule (run π p k)) p :=
  no_acquisition_below_bound n π rule k (Nat.lt_of_le_of_lt (run_length_le π _ k) hk)

theorem no_acquisition_below_half_square (n : Nat) (π : Protocol)
    (rule : Transcript → Evaluator) (k : Nat) (hk : 2 * k < n * (n - 1)) :
    ∃ p : Nat → Nat, ¬ Sharp (List.range n) (rule (run π p k)) p := by ...

theorem transcripts_identical_capabilities_differ (n : Nat) (π : Protocol) (k : Nat)
    (hshort : (run π (fun z => z) k).length < (allPairs n).length) :
    ∃ p p' : Nat → Nat, run π p k = run π p' k ∧
      ∃ x y, x ∈ List.range n ∧ y ∈ List.range n ∧ p x = p y ∧ p' x ≠ p' y := by ...
```

Second, the static counterpart on observers:

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Reading.lean lines 147–156
theorem observer_cannot_read_resolution (D : List Nat) (E : Evaluator)
    {x y : Nat} (hx : x ∈ D) (hy : y ∈ D) (hxy : x ≠ y)
    (hv : verdictB E x y = false) :
    ∃ p₀ p₁ : Nat → Nat, Consistent D E p₀ ∧ Consistent D E p₁ ∧
      p₀ x = p₀ y ∧ p₁ x ≠ p₁ y := by
  have hm : pQ D (questions E) x = pQ D (questions E) y :=
    (pQ_exact D (questions E) x hx y hy).mpr
      ((verdictB_false_iff_sigEq E x y).mp hv)
  exact ⟨pQ D (questions E), markOne (pQ D (questions E)) x,
    actor_consistent D E, markOne_consistent D E x, hm, markOne_separates hxy hm⟩
```

## The proof, step by step

**Step 1. `uncovered_pair` via `nodup_subset_length`.**
Test `(allPairs n).all (fun pr => askedB T pr.1 pr.2)`. If it evaluates to
`false`, `all_false_witness` returns a pair `(x, y) ∈ allPairs n` (so
`x < y < n` by `mem_allPairs`) with `askedB T x y = false`. If it evaluates to
`true`, every `(x, y) ∈ allPairs n` was asked in `T`, so `allPairs n ⊆
T.map norm`. Because `(allPairs n).Nodup` holds (`allPairs_nodup`),
`nodup_subset_length` gives `(allPairs n).length ≤ (T.map norm).length =
T.length`, contradicting `hshort : T.length < (allPairs n).length`.

**Step 2. `lower_bound`.**
Apply `uncovered_pair` to `T = run π (fun z => z) k` to get `x < y < n` with
`askedB T x y = false`. For every entry `e ∈ T`, `{e.1, e.2.1} ≠ {x, y}`, so
`merge_agrees` shows `merge x y e.1 = merge x y e.2.1 ↔ e.1 = e.2.1`. By Unit
12's `run_congr`, `run π (merge x y) k = run π (fun z => z) k`.

**Step 3. `no_acquisition_below_bound` and `transcripts_identical_capabilities_differ`.**
Let `T = run π (fun z => z) k = run π (merge x y) k`, and inspect
`hv : verdictB (rule T) x y`:
- If `hv = true`, `rule T` separates `x` and `y`, whereas `merge x y x = x =
  merge x y y`, so `rule T` is not sharp for `merge x y`.
- If `hv = false`, `rule T` merges `x` and `y`, whereas `(fun z => z) x = x ≠
  y = (fun z => z) y`, so `rule T` is not sharp for `fun z => z`.
And the same pair of actors `p = merge x y`, `p' = fun z => z` witnesses
`transcripts_identical_capabilities_differ` (`TT-39o` / `AI-20`).

**Step 4. `observer_cannot_read_resolution`.**
If `verdictB E x y = false` for `x ≠ y ∈ D`, then `p₀ = pQ D (questions E)`
merges `x` and `y` (`hm`), while `p₁ = markOne p₀ x` splits `x` and `y`
(`markOne_separates hxy hm`), and both `p₀` and `p₁` satisfy `Consistent D E`
(`actor_consistent`, `markOne_consistent`).

## The same fact in Python

The check verifies:

1. For `n = 1, 2, 3, 4`, the minimax game value `game_value(n, all_partitions)`
   from `actor_institution/model.py` equals `n * (n - 1) // 2` (`0, 1, 3, 6`),
   confirming that no adaptive protocol can fix every actor's partition in fewer
   than `n(n - 1)/2` probes.
2. On `range(4)`, for any transcript against the identity of length `< 6`, the
   uncovered pair `(x, y)` gives an actor `merge(x, y)` with the identical
   transcript and a different partition on `(x, y)`.
3. `cannot_read_checks` from `two_theorems/model.py` on `D = (0, 1, 2)` (`m = 1`)
   and `D = (0, 1, 2, 3)` (`m = 2`): across all `111` merged-pair cases, `p₀`
   and `p₁ = markOne(p₀, x)` are both consistent with `E` while `p₀(x) == p₀(y)`
   and `p₁(x) != p₁(y)` (`0` failures).
4. **Countermodel to query-model overgeneralization (fiber-reveal oracle):** on
   `range(4)` (all `15` partitions), an adaptive fiber-reveal oracle that
   queries the smallest uncovered element `x` and receives its full class
   `{y in range(4) : p[x] == p[y]}` uniquely acquires every partition in at most
   `n - 1 = 3` queries (`max_queries = 3 < 6 = n(n - 1)/2`, `0` failures),
   showing that the `n(n - 1)/2` lower bound is specific to pairwise equality
   queries rather than all observation models.

```
python textbook/institutions/checks/i13_lower_bound.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `dropAll`, `nodup_subset_length` | `uncovered_pair` | constructive list-length induction on `[DecidableEq α]` |
| `all_false_witness` | `uncovered_pair` | constructive search finding the first unprobed pair in `allPairs n` |
| `Nat.decEq`, `omega` | `merge_agrees`, `no_acquisition_below_half_square`, `markOne_eq` | decidable equality and linear arithmetic on `Nat` |

**What the system holds.** The finite carrier `List.range n`, the transcript `T`,
and the finite view list `rule T : Evaluator`.

**Admissions relied on, and their price.** Unit 12's probe grammar (`AI-16`).
Crucially, `no_acquisition_below_bound` quantifies over *all* presentations `p`
on `List.range n` (specifically `{fun z => z} ∪ {merge x y | x < y < n}`). As
Unit 15 will show (`complete_evaluator_for_two`), if the actor is promised in
advance to belong to a smaller fixed family, fewer probes can suffice.

**Phrases to read with care.**

- "An observer cannot read another's resolution" (`TT-27`) and "identical
  transcripts, different capabilities" (`TT-39o` / `AI-20`). In both theorems,
  the limitation is scoped: `observer_cannot_read_resolution` assumes `E` merges
  `x ≠ y` (`verdictB E x y = false`), and
  `transcripts_identical_capabilities_differ` assumes the transcript is shorter
  than `n(n - 1)/2`. Unrestricted claims that finite observers can never
  evaluate or acquire another actor's partition do not follow from these
  theorems; indeed, Unit 14 shows that `n(n - 1)/2` probes acquire every actor's
  partition on `List.range n`.

## What it shows, and what it does not

It shows that any protocol taking fewer than `n(n - 1)/2` probes on `List.range n`
leaves some pair `x < y < n` unprobed against `fun z => z`, so `merge x y` and
`fun z => z` produce the same transcript and no evaluator `rule T` can be sharp
for both (`no_acquisition_below_bound`, `no_acquisition_below_half_square`,
`transcripts_identical_capabilities_differ`).

It shows that whenever a static observer `E` merges `x ≠ y ∈ D`, two actors
consistent with `E` disagree on `(x, y)` (`observer_cannot_read_resolution`).

It does not show that acquisition is unachievable at budget `n(n - 1)/2` (Unit
14 shows it is achieved there), it does not apply to stronger query oracles that
return more than one pairwise equality bit per query (such as a class-membership
oracle, which acquires any partition on `n` points in at most `n - 1` queries),
and it does not support unrestricted impossibility claims beyond the stated step
budget or merged pairs.

## Sources

| Item | Where |
|---|---|
| `merge`, `merge_agrees`, `askedB`, `askedB_iff`, `norm`, `mem_allPairs` | `research/actor_institution/lean/ResearchActorInstitution/Acquisition.lean` lines 155–218 |
| `dropAll`, `nodup_subset_length`, `allPairs_nodup`, `uncovered_pair` | the same file, lines 223–351 |
| `lower_bound`, `no_acquisition_below_bound`, `no_acquisition_in_fewer_steps`, `no_acquisition_below_half_square`, `transcripts_identical_capabilities_differ` | the same file, lines 355–423 |
| `Consistent`, `actor_consistent`, `sharp_consistent`, `markOne`, `observer_cannot_read_resolution` | `research/two_theorems/lean/ResearchTwoTheorems/Reading.lean` lines 99–156 |
| Python mirrors | `research/actor_institution/model.py` lines 195–262 (`game_value`, `acquisition_values`); `research/two_theorems/model.py` lines 747–769 (`consistent`, `cannot_read_checks`) |
| Check | `textbook/institutions/checks/i13_lower_bound.py` |
| Ledger | `research/actor_institution/CLAIMS.md` AI-16, AI-20 (closes TT-39o); `research/two_theorems/CLAIMS.md` TT-27 |
