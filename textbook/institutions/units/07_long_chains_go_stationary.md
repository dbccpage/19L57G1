# Unit 07. Long chains go stationary

**Claim.** Any extension chain of institutions on a nonempty carrier `D` that
contains more than `D.length` institutions has a stationary step at which
information does not increase; at any stationary step every member of the newer
institution was already known by the older one, so nothing new becomes known;
and replacing a subfamily by its canonical representative (`pQ D Q'`) or keeping
members already known by one fine member adds no information and no knowledge.
**Status:** derived. **Lean:** `Chain.Extends`, `Chain.ExtChain`,
`Chain.HasStationary`, `Chain.stationary_of_bound`,
`Chain.long_chain_stationary`, `Chain.stationary_step_known`,
`Chain.stationary_step_inert` (`actor_institution`); `Reading.nest_sigEq`,
`Reading.nest_inert`, `Reading.nest_information`,
`Reading.participation_collapse` (`two_theorems`). **Sources:**
`research/actor_institution/lean/ResearchActorInstitution/Chain.lean` lines
34–116; `research/two_theorems/lean/ResearchTwoTheorems/Reading.lean` lines
247–298.

Unit 03 proved two bounds on `information D Q`: it is at least `1` on a
nonempty carrier (`classCount_pos`), and at most `D.length`
(`information_le_carrier`). It also proved that extending a family never lowers
its information (`information_mono`). Putting those three facts together along
a chain of extensions forces a pigeonhole stall: a chain with more than
`D.length` institutions cannot strictly increase its information at every step,
so some step must be stationary (`long_chain_stationary`, which closes the
open item `TT-35o` from `two_theorems`). And by Unit 03's equivalence
`knows_iff_information_eq`, a stationary extension step adds only members the
older family already knew, so the step changes knowledge of no claim at all.
Finally, nesting a subfamily as its single representative `pQ D Q'` or pooling
members that one member already knows (`participation_collapse`) leaves both
knowledge and information unchanged.

## What you need first

Unit 01 (`pQ`, `pQ_exact`), Unit 02 (`Knows`, `knows_iff_determined`,
`knows_mono`, `knows_iff_sigList`), and Unit 03 (`information`, `classCount`,
`classCount_pos`, `information_le_carrier`, `information_mono`,
`information_member_le`, `knows_iff_information_eq`, `count_le_of_determines`).

### 1. Extension chains and stationary steps

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Chain.lean lines 34–45
/-- `Q'` retains every member of `Q`. -/
def Extends (Q Q' : Institution) : Prop := ∀ p, p ∈ Q → p ∈ Q'

/-- A list of institutions, each extending the previous one. -/
def ExtChain : List Institution → Prop
  | [] => True
  | [_] => True
  | Q :: Q' :: t => Extends Q Q' ∧ ExtChain (Q' :: t)

/-- Some step of the chain leaves the information on `D` unchanged. -/
def HasStationary (D : List Nat) : List Institution → Prop
  | Q :: Q' :: t => information D Q' = information D Q ∨ HasStationary D (Q' :: t)
  | _ => False
```

`Extends Q Q'` says every member of `Q` belongs to `Q'`. `ExtChain L` says each
adjacent pair in `L` satisfies `Extends`. `HasStationary D L` says some adjacent
pair `Q, Q'` in `L` has `information D Q' = information D Q`.

```python
# Python (research), research/actor_institution/model.py lines 339–341
def has_stationary(n: int, chain: list[Institution]) -> bool:
    infos = [information(n, Q) for Q in chain]
    return any(a == b for a, b in zip(infos, infos[1:]))
```

### 2. Nesting a subfamily as one member

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Reading.lean lines 247–260
theorem nest_sigEq (D : List Nat) (Q' Q : Institution) {x y : Nat}
    (hx : x ∈ D) (hy : y ∈ D) :
    SigEq (pQ D Q' :: Q) x y ↔ SigEq (Q' ++ Q) x y := by
  constructor
  · intro h p hp
    rcases List.mem_append.mp hp with hp | hp
    · exact (pQ_exact D Q' x hx y hy).mp (h (pQ D Q') List.mem_cons_self) p hp
    · exact h p (List.mem_cons_of_mem _ hp)
  · intro h p hp
    rcases List.mem_cons.mp hp with hp | hp
    · rw [hp]
      exact (pQ_exact D Q' x hx y hy).mpr
        (fun p' hp' => h p' (List.mem_append_left _ hp'))
    · exact h p (List.mem_append_right _ hp)
```

Because `pQ D Q'` agrees on `x, y ∈ D` iff every member of `Q'` agrees on `x, y`
(`pQ_exact`, Unit 01), replacing the prefix `Q'` in `Q' ++ Q` by the single
member `pQ D Q'` gives the exact same signature relation `SigEq` on `D`.

## The theorems

First, the stationary step theorem and its consequences:

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Chain.lean lines 49–116
theorem stationary_of_bound (D : List Nat) :
    ∀ (t : List Institution) (Q : Institution), ExtChain (Q :: t) →
      D.length < information D Q + t.length → HasStationary D (Q :: t) := by
  intro t
  induction t with
  | nil =>
    intro Q _ hlt
    have := information_le_carrier D Q
    simp only [List.length_nil] at hlt
    show False
    omega
  | cons Q' t ih =>
    intro Q hc hlt
    have hext : Extends Q Q' := hc.1
    have hc' : ExtChain (Q' :: t) := hc.2
    show information D Q' = information D Q ∨ HasStationary D (Q' :: t)
    cases Nat.decEq (information D Q') (information D Q) with
    | isTrue h => exact Or.inl h
    | isFalse hne =>
      apply Or.inr
      apply ih Q' hc'
      have hmono : information D Q ≤ information D Q' := information_mono hext
      simp only [List.length_cons] at hlt
      omega

theorem long_chain_stationary (D : List Nat) (hD : D ≠ []) (L : List Institution)
    (hc : ExtChain L) (hlen : D.length < L.length) : HasStationary D L := by
  cases L with
  | nil => simp only [List.length_nil] at hlen; exact absurd hlen (Nat.not_lt_zero _)
  | cons Q t =>
    apply stationary_of_bound D t Q hc
    have h1 := classCount_pos D Q hD
    simp only [List.length_cons] at hlen
    show D.length < classCount D Q + t.length
    omega

theorem stationary_step_known {D : List Nat} {Q Q' : Institution} (hext : Extends Q Q')
    (hstat : information D Q' = information D Q) : ∀ p, p ∈ Q' → Knows D Q p := by
  intro p hp
  rw [knows_iff_information_eq]
  apply Nat.le_antisymm
  · have h1 : information D (Q ++ [p]) ≤ information D Q' := by
      apply information_mono
      intro r hr
      rcases List.mem_append.mp hr with hr | hr
      · exact hext r hr
      · rw [List.mem_singleton.mp hr]; exact hp
    rw [hstat] at h1
    exact h1
  · exact information_mono (fun r hr => List.mem_append_left _ hr)

theorem stationary_step_inert {D : List Nat} {Q Q' : Institution} (hext : Extends Q Q')
    (hstat : information D Q' = information D Q) (q : Nat → Nat) :
    Knows D Q' q ↔ Knows D Q q := by
  constructor
  · intro h
    rw [knows_iff_determined] at h ⊢
    intro x hx y hy hs
    apply h x hx y hy
    intro p hp
    have hk := stationary_step_known hext hstat p hp
    exact (knows_iff_determined D Q p).mp hk x hx y hy hs
  · exact knows_mono hext
```

Second, nesting and participation collapse:

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Reading.lean lines 265–298
theorem nest_inert (D : List Nat) (Q' Q : Institution) (q : Nat → Nat) :
    Knows D (pQ D Q' :: Q) q ↔ Knows D (Q' ++ Q) q := by
  rw [knows_iff_determined, knows_iff_determined]
  constructor
  · intro h x hx y hy hs; exact h x hx y hy ((nest_sigEq D Q' Q hx hy).mpr hs)
  · intro h x hx y hy hs; exact h x hx y hy ((nest_sigEq D Q' Q hx hy).mp hs)

theorem nest_information (D : List Nat) (Q' Q : Institution) :
    information D (pQ D Q' :: Q) = information D (Q' ++ Q) := by
...

theorem participation_collapse {D : List Nat} {Q : Institution}
    {p : Nat → Nat} (hp : p ∈ Q) (h : ∀ q, q ∈ Q → Knows D [p] q) :
    information D Q = classCount D [p] := by
  apply Nat.le_antisymm
  · unfold information classCount
    apply count_le_of_determines (sigList [p]) (sigList Q) D
    intro a ha b hb hab
    apply (sigEq_iff_sigList Q a b).mp
    intro q hq
    exact (knows_iff_sigList D [p] q).mp (h q hq) a ha b hb hab
  · exact information_member_le hp
```

## The proof, step by step

**Step 1. `stationary_of_bound` by induction on the tail `t`.**
For a chain `Q :: t`, assume `D.length < information D Q + t.length`.
- Base `t = []`: `D.length < information D Q`, which contradicts Unit 03's
  `information_le_carrier D Q` (`information D Q ≤ D.length`).
- Step `t = Q' :: t'`: compare `information D Q'` and `information D Q` with
  `Nat.decEq`. If they are equal, the first step is stationary (`Or.inl h`). If
  not, since `Extends Q Q'` implies `information D Q ≤ information D Q'`
  (`information_mono`), we have `information D Q + 1 ≤ information D Q'`, so
  `D.length < information D Q' + t'.length`, and the induction hypothesis gives a
  stationary step in `Q' :: t'`.

**Step 2. `long_chain_stationary`.**
When `L = Q :: t` has `D.length < L.length = t.length + 1` and `D ≠ []`, Unit 03's
`classCount_pos D Q hD` gives `1 ≤ information D Q`. Therefore
`D.length < information D Q + t.length`, and `stationary_of_bound` applies.

**Step 3. `stationary_step_known` and `stationary_step_inert`.**
Fix `p ∈ Q'`. Every member of `Q ++ [p]` belongs to `Q'` (by `hext` and `hp`),
so `information_mono` gives `information D (Q ++ [p]) ≤ information D Q'`. Since
`information D Q' = information D Q`, sandwiching with `information D Q ≤
information D (Q ++ [p])` gives `information D (Q ++ [p]) = information D Q`,
which by Unit 03's `knows_iff_information_eq` is `Knows D Q p`. Then any pair
`x, y ∈ D` merged by `Q` is also merged by every `p ∈ Q'`, so `Knows D Q' q`
implies `Knows D Q q` (`stationary_step_inert`).

**Step 4. `nest_inert`, `nest_information`, and `participation_collapse`.**
Rewriting with `nest_sigEq` shows that `pQ D Q' :: Q` and `Q' ++ Q` merge the
exact same pairs of `D`, giving both `nest_inert` (by `knows_iff_determined`)
and `nest_information` (by `count_le_of_determines` in both directions). And if
some `p ∈ Q` knows every `q ∈ Q`, then `[p]`-agreement determines `Q`-agreement,
so `information D Q ≤ classCount D [p]`, while `hp : p ∈ Q` gives the reverse
inequality `information_member_le hp` (`participation_collapse`).

## The same fact in Python

The check runs two exhaustive tests:

1. `chain_check(3)` from `actor_institution/model.py`: over all `4000` extension
   chains of `3 + 1 = 4` institutions drawn from the `5` partitions of
   `range(3)`, every chain has a stationary step (`0` violations); and there
   exists a chain of `3` institutions (`()`, `((0, 0, 1),)`,
   `((0, 0, 1), (0, 1, 0))`, with informations `1, 2, 3`) that has no stationary
   step, showing the bound `D.length < L.length` is tight.
2. `nest_checks` on `D = (0, 1, 2, 3)` from `two_theorems/model.py`: over all
   pairs of families `Q', Q` of at most 2 pool members, replacing `Q'` by its
   joint presentation `pQ D Q'` preserves both `information` and `knows` (`0`
   violations), and whenever one member of `Q` knows all members of `Q`, the
   family's information equals that member's class count (`10` cases, `0`
   violations).

```
python textbook/institutions/checks/i07_chain_stationary.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| Induction on `t : List Institution` | `stationary_of_bound` | structural induction along the chain of institutions |
| `Nat.decEq` | `stationary_of_bound` | decidable equality on natural numbers `information D Q'` and `information D Q` |
| `omega` | `stationary_of_bound`, `long_chain_stationary` | linear arithmetic combining `information_le_carrier`, `classCount_pos`, and strict inequality |

**What the system holds.** A finite list `L : List Institution` of finite lists
of presentations on the carrier `D`.

**Admissions relied on, and their price.** Unit 00's three admissions. The
pigeonhole bound `D.length < L.length` relies on `D` being a fixed finite
carrier throughout the chain (`AI-07`). If new data are added to `D` along the
chain, `information_le_carrier` moves with `D` and the stationary bound for a
fixed `D` does not apply.

**Phrases to read with care.**

- "Crash by compression" (`TT-35o` / `AI-07`). The Lean theorem is a pigeonhole
  bound on `information D Q` along an `ExtChain`: because `1 ≤ information D Q ≤
  D.length`, a chain of more than `D.length` institutions cannot strictly refine
  the partition at every step. No dynamical failure or physical crash is
  modeled (`TT-36o`).
- "Participation collapse." When one member `p ∈ Q` already determines every
  other member of `Q`, the other members are redundant (`information D Q =
  classCount D [p]`). Nothing collapses over time; their partitions were coarser
  than `p`'s from the start.

## What it shows, and what it does not

It shows that any extension chain of institutions on a nonempty carrier `D` with
`D.length < L.length` has at least one stationary step (`long_chain_stationary`),
and that the bound is tight on `range(3)` (`AI-07`, `AI-07c`).

It shows that at a stationary extension step, every new member was already known
by the previous institution (`stationary_step_known`), so the set of known
claims does not change (`stationary_step_inert`).

It shows that compressing a subfamily `Q'` into its representative `pQ D Q'`
inside a larger family `Q' ++ Q` changes neither information nor knowledge
(`nest_inert`, `nest_information`), and that a family dominated by one of its
members has the information of that member alone (`participation_collapse`).

It does not model chains that drop old members while adding new ones (where
`Extends Q Q'` fails), or chains across which the carrier `D` grows.

## Sources

| Item | Where |
|---|---|
| `Extends`, `ExtChain`, `HasStationary`, `stationary_of_bound`, `long_chain_stationary` | `research/actor_institution/lean/ResearchActorInstitution/Chain.lean` lines 34–85 |
| `stationary_step_known`, `stationary_step_inert` | the same file, lines 89–116 |
| `nest_sigEq`, `nest_inert`, `nest_information`, `participation_collapse` | `research/two_theorems/lean/ResearchTwoTheorems/Reading.lean` lines 247–298 |
| Python mirrors | `research/actor_institution/model.py` lines 339–368 (`has_stationary`, `chain_check`); `research/two_theorems/model.py` lines 795–818 (`nest_checks`) |
| Check | `textbook/institutions/checks/i07_chain_stationary.py` |
| Ledger | `research/actor_institution/CLAIMS.md` AI-07, AI-07c; `research/two_theorems/CLAIMS.md` TT-29, TT-35o (closed by AI-07), TT-36o |
