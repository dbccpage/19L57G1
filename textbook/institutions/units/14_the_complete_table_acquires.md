# Unit 14. The complete table acquires, and representation versus acquisition

**Claim.** The complete pair table determines the unknown partition and
supports a sharp observer. Acquiring that table and representing the
result with Boolean views are different costs.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Probing all `(allPairs n).length = n(n - 1)/2` unordered pairs on
`List.range n` via `scripted (allPairs n)` produces the complete transcript
`fullT n p`, from which `tableE n (fullT n p)` builds an `n`-view evaluator that
is sharp for every actor `p` (`table_sharp`, `complete_table_acquires`).
Combined with Unit 13's lower bound, the worst-case number of probes required to
acquire an arbitrary actor on `List.range n` is `n(n - 1)/2`
(`acquisition_cost_exact`). Moreover, an actor `p` is sharply observable by some
`m`-view observer on `D` iff `classCount D [p] ≤ 2 ^ m` (`sharp_observable_iff`),
sharpness factors into sufficiency and consistency (`sharp_iff_sufficient_and_consistent`),
the binary-code observer `sharpObserver D p m` depends on `p` only through `p`'s
partition (`sharpObserver_congr`), and once the complete probe table `fullT n p`
has been acquired, an `m`-view sharp evaluator `logE n (fullT n p) m` can be
computed from the transcript alone whenever `classCount (List.range n) [p] ≤ 2 ^ m`
(`log_views`).

**Status:** derived. **Lean:** `Acquisition.scripted`,
`Acquisition.run_scripted`, `Acquisition.fullT`, `Acquisition.run_complete`,
`Acquisition.fullT_length`, `Acquisition.sameT`, `Acquisition.sameT_full`,
`Acquisition.tableE`, `Acquisition.table_sharp`,
`Acquisition.complete_table_acquires`, `Acquisition.acquisition_cost_exact`,
`Acquisition.acquired`, `Acquisition.acquired_kernel`, `Acquisition.logE`,
`Acquisition.log_views` (`actor_institution`); `Observer.Sharp`,
`Observer.bitObserver`, `Observer.fiberIdx`, `Observer.sharp_observable_iff`,
`Sufficiency.Sufficient`, `Sufficiency.sufficient_iff`,
`Sufficiency.sharp_iff_sufficient_and_consistent`,
`Sufficiency.sufficient_not_sharp`, `Sufficiency.consistent_not_sufficient`,
`Sufficiency.sharp_fixes_partition`, `Sufficiency.sharpObserver`,
`Sufficiency.sharpObserver_views`, `Sufficiency.sharpObserver_congr`
(`two_theorems`). **Sources:**
`research/actor_institution/lean/ResearchActorInstitution/Acquisition.lean`
lines 451–630; `research/two_theorems/lean/ResearchTwoTheorems/Observer.lean`
lines 132–133, 238–239, 438–439, 518–526;
`research/two_theorems/lean/ResearchTwoTheorems/Sufficiency.lean` lines 44–221.

> **Scope warning — pairwise equality-query complexity vs. general information-acquisition complexity.**
> The exact threshold $\frac{n(n - 1)}{2}$ in `acquisition_cost_exact` holds **specifically for the unpromised pairwise equality-query model** (`Acquisition.Protocol` and `Acquisition.entry`), where each step probes a single pair `(x, y)` and receives only the Boolean equality bit `decide (p x = p y)`. It does **not** establish that every institution or observation model requires $\frac{n(n - 1)}{2}$ observations to identify an unknown partition. Under richer query models — such as a **fiber-reveal (class-membership) oracle** that returns the entire equivalence class of a queried element $x$ in at most $n - 1$ queries, or a promised restriction on the candidate family (Unit 15) — the same partition is acquired with strictly fewer queries (`i14_acquisition_exact.py`).

Unit 13 proved that fewer than `n(n - 1)/2` probes cannot acquire every actor on
`List.range n`. This unit derives the matching upper bound: the non-adaptive
protocol `scripted (allPairs n)` asks all `n(n - 1)/2` pairs and builds an
evaluator `tableE n (fullT n p)` that is sharp for every `p`
(`acquisition_cost_exact`, closing `TT-43o (i)`). It then connects probe
acquisition to the static representation theorems of `two_theorems`:
- In `Observer.lean` and `Sufficiency.lean`, `sharp_observable_iff` shows in
  Lean that an `m`-view sharp observer exists iff `classCount D [p] ≤ 2 ^ m`, and
  `sharpObserver_congr` shows that the binary-code construction
  `sharpObserver D p m` consumes `p`'s partition (`fiberIdx D p`) as input. That
  is a theorem of *representation capacity*: given the partition of `p` with
  `k ≤ 2 ^ m` classes, `m = ⌈log₂ k⌉` views suffice to represent it.
- In `Acquisition.lean`, the partition of `p` is *not* given in advance; it must
  first be acquired by `n(n - 1)/2` pairwise probes (`fullT n p`), which yield
  the canonical representative `acquired n (fullT n p)` having `p`'s partition
  (`acquired_kernel`), and then `logE n (fullT n p) m` compresses the acquired
  table into `m` views (`log_views`, closing the sufficiency direction of
  `TT-43o (iii)`).

</details>

## First pass

For three inputs there are three unordered pairs: 0/1, 0/2, and
1/2. Record all three equality answers. The complete table determines
which inputs share the actor's value, even though the numeric labels
remain unknown.

Once three separate classes are known, two Boolean views can label
them by patterns 00, 01, and 10. Two views offer four possible patterns,
enough for three classes. This representational capacity does not
explain how the unknown classes were discovered.

**Predict:** does a two-view representation imply that two pair probes
always suffice to acquire a three-input actor?

<details><summary>Check your prediction</summary>

No. I13's all-different run still requires the third pair probe in the
worst case. The views encode a partition after acquisition. They are
not an extra oracle for discovering it. Both results remain within the
declared finite model.

</details>

## What you need first

Unit 01 (`pQ`, `pQ_exact`), Unit 02 (`Knows`, `knows_iff_determined`), Unit 03
(`classCount`, `count_le_of_determines`), Unit 12 (`Transcript`, `Protocol`,
`entry`, `run`), and Unit 13 (`allPairs`, `mem_allPairs`,
`no_acquisition_in_fewer_steps`, `Consistent`).

### 1. Sharpness, sufficiency, and the binary-code observer (`two_theorems`)

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Observer.lean lines 132–133, 438–439, 518–526
def Sharp (D : List Nat) (E : Evaluator) (p : Presentation) : Prop :=
  ∀ x, x ∈ D → ∀ y, y ∈ D → (verdictB E x y = false ↔ p x = p y)

def fiberIdx (D : List Nat) (p : Presentation) (x : Nat) : Nat :=
  posOf (sigList [p] x) (classList D p)

theorem sharp_observable_iff (D : List Nat) (p : Presentation) (m : Nat) :
    (∃ E : Evaluator, E.length = m ∧ Sharp D E p) ↔
      classCount D [p] ≤ 2 ^ m := by ...
```

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Sufficiency.lean lines 44–45, 65–67, 114–125, 213–215
def Sufficient (D : List Nat) (E : Evaluator) (p : Presentation) : Prop :=
  Knows D (questions E) p

theorem sharp_iff_sufficient_and_consistent (D : List Nat) (E : Evaluator)
    (p : Presentation) :
    Sharp D E p ↔ Sufficient D E p ∧ Consistent D E p := by ...

theorem sharp_fixes_partition {D : List Nat} {E : Evaluator} {p p' : Presentation}
    (h : Sharp D E p) (h' : Sharp D E p') :
    ∀ x, x ∈ D → ∀ y, y ∈ D → (p x = p y ↔ p' x = p' y) := by ...

def sharpObserver (D : List Nat) (p : Presentation) (m : Nat) : Evaluator :=
  bitObserver D (fiberIdx D p) m

theorem sharpObserver_sharp (D : List Nat) (p : Presentation) (m : Nat)
    (h : classCount D [p] ≤ 2 ^ m) : Sharp D (sharpObserver D p m) p := ...

theorem sharpObserver_congr (D : List Nat) (p p' : Presentation) (m : Nat)
    (h : ∀ x, x ∈ D → ∀ y, y ∈ D → (p x = p y ↔ p' x = p' y)) :
    sharpObserver D p m = sharpObserver D p' m := by ...
```

`Sharp D E p` holds iff `E`'s views neither merge what `p` splits (`Sufficient`)
nor split what `p` merges (`Consistent`). Neither half implies the other
(`sufficient_not_sharp`, `consistent_not_sufficient`, lines 82–96). An `m`-view
observer can be sharp for at most `2 ^ m` classes, and when `classCount D [p] ≤
2 ^ m`, `sharpObserver D p m` cuts `D` by the `m` binary bits of `fiberIdx D p`.

### 2. Scripted probing and the complete table (`actor_institution`)

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Acquisition.lean lines 451–454, 476, 490–493, 527–528
def scripted (L : List (Nat × Nat)) : Protocol := fun T =>
  match L.drop T.length with
  | [] => none
  | pr :: _ => some pr

def fullT (n : Nat) (p : Nat → Nat) : Transcript := (allPairs n).map (entry p)

def sameT (T : Transcript) (a b : Nat) : Bool :=
  decide (a = b) ||
    T.any (fun e =>
      ((decide (e.1 = a) && decide (e.2.1 = b)) || (decide (e.1 = b) && decide (e.2.1 = a))) && e.2.2)

def tableE (n : Nat) (T : Transcript) : Evaluator :=
  (List.range n).map (fun a => (List.range n).filter (fun b => sameT T a b))
```

`scripted L` asks the pairs in `L` in order by indexing at `T.length`. On
`L = allPairs n`, after `(allPairs n).length` steps it produces `fullT n p`
(`run_complete`). From `T`, `sameT T a b` reads off whether `a = b` or `T`
recorded `true` on `(a, b)` or `(b, a)`, and `tableE n T` forms one view per
datum `a ∈ List.range n` containing all `b ∈ List.range n` with
`sameT T a b = true`.

## The theorems

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Acquisition.lean lines 495–496, 535–579, 603–630
theorem sameT_full (n : Nat) (p : Nat → Nat) (a b : Nat) (ha : a < n) (hb : b < n) :
    sameT (fullT n p) a b = true ↔ p a = p b := by ...

theorem table_sharp (n : Nat) (p : Nat → Nat) : Sharp (List.range n) (tableE n (fullT n p)) p := by ...

theorem complete_table_acquires (n : Nat) (p : Nat → Nat) :
    Sharp (List.range n) (tableE n (run (scripted (allPairs n)) p (allPairs n).length)) p := by
  rw [run_complete]
  exact table_sharp n p

theorem acquisition_cost_exact (n : Nat) :
    (∀ (π : Protocol) (rule : Transcript → Evaluator) (k : Nat), k < (allPairs n).length →
      ∃ p : Nat → Nat, ¬ Sharp (List.range n) (rule (run π p k)) p) ∧
    (∀ p : Nat → Nat,
      Sharp (List.range n) (tableE n (run (scripted (allPairs n)) p (allPairs n).length)) p) :=
  ⟨fun π rule k hk => no_acquisition_in_fewer_steps n π rule k hk,
   fun p => complete_table_acquires n p⟩

def acquired (n : Nat) (T : Transcript) : Nat → Nat :=
  pQ (List.range n) (questions (tableE n T))

theorem acquired_kernel (n : Nat) (p : Nat → Nat) :
    ∀ x, x ∈ List.range n → ∀ y, y ∈ List.range n →
      (acquired n (fullT n p) x = acquired n (fullT n p) y ↔ p x = p y) := by ...

def logE (n : Nat) (T : Transcript) (m : Nat) : Evaluator :=
  sharpObserver (List.range n) (acquired n T) m

theorem log_views (n : Nat) (p : Nat → Nat) (m : Nat) (h : classCount (List.range n) [p] ≤ 2 ^ m) :
    Sharp (List.range n) (logE n (fullT n p) m) p := by
  have hk := acquired_kernel n p
  have hc : classCount (List.range n) [acquired n (fullT n p)] ≤ 2 ^ m := by
    rw [classCount_congr (p := p) (p' := acquired n (fullT n p)) (fun x hx y hy => (hk x hx y hy).symm)]
    exact h
  exact sharp_congr (sharpObserver_sharp _ _ m hc) hk
```

## The proof, step by step

**Step 1. `run_scripted` and `sameT_full`.**
By induction on `j ≤ L.length`, `run (scripted L) p j = (L.take j).map (entry p)`.
At `j = (allPairs n).length`, this equals `fullT n p` (`run_complete`). For any
`a, b < n`, either `a = b`, or `a < b` so `(a, b) ∈ allPairs n`, or `b < a` so
`(b, a) ∈ allPairs n`. In all three cases `sameT (fullT n p) a b = true ↔
p a = p b` (`sameT_full`).

**Step 2. `table_sharp` and `acquisition_cost_exact`.**
Let `E = tableE n (fullT n p)` and `x, y ∈ List.range n`.
- If `verdictB E x y = false`, then no view of `E` separates `x` and `y`. In
  particular, the view for `x`—which contains `x` because `sameT_full` is
  reflexive—must also contain `y`, so `sameT (fullT n p) x y = true`, hence
  `p x = p y` by `sameT_full`.
- Conversely, if `p x = p y`, then for every `a < n`, `p a = p x ↔ p a = p y`,
  so `sameT (fullT n p) a x = sameT (fullT n p) a y` by `sameT_full`. Thus `x`
  and `y` belong to the exact same views of `E`, giving `verdictB E x y = false`.
Combining `no_acquisition_in_fewer_steps` (Unit 13) and `complete_table_acquires`
gives `acquisition_cost_exact`.

**Step 3. From the acquired table to `log_views`.**
Because `tableE n (fullT n p)` is sharp for `p`, the canonical representative of
its view questions—`acquired n (fullT n p) = pQ (List.range n) (questions (tableE n (fullT n p)))`—has
the exact same partition on `List.range n` as `p` (`acquired_kernel`), and
therefore the same `classCount` (`classCount_congr`). Applying
`sharpObserver_sharp` to `acquired n (fullT n p)` produces `logE n (fullT n p) m`
of length `m` (`logE_length`), which is sharp for `acquired n (fullT n p)` and
hence by `sharp_congr` sharp for `p` (`log_views`).

## The same fact in Python

The check verifies:

1. On `range(4)`, for every partition `p`, the complete transcript `fullT(4, p)`
   of `6` probes yields `tableE(4, fullT(4, p))` sharp for `p`, and for
   `2^m ≥ blocks(p)` (`m = 2`) the binary-code evaluator `logE` built from
   `acquired(4, fullT(4, p))` is also sharp for `p` (`0` violations).
2. `sufficiency_checks` and `sharp_fixes_partition_check` from
   `two_theorems/model.py` on `D = (0, 1, 2)` and `D = (0, 1, 2, 3)`:
   `sharp(D, E, p)` matches `sufficient(D, E, p) and consistent(D, E, p)` across
   all `3699` `(E, p)` pairs (`0` violations), both one-sided witnesses exist,
   and `sharpObserver` depends only on `p`'s partition (`0` violations).
3. **Countermodel to query-model overgeneralization (stronger query oracle):** on
   `range(4)`, while pairwise equality queries require `6` probes in the worst
   case (`fullT`), a fiber-reveal oracle that returns the equivalence class of a
   queried element acquires every partition in at most `3 < 6` queries and feeds
   the exact same `m = 2`-view binary compression `logE` (`0` violations).

```
python textbook/institutions/checks/i14_acquisition_exact.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `List.drop`, `List.take`, `Nat.decLt` | `scripted`, `run_scripted`, `sameT_full` | list slicing and linear order on `Nat` in the metatheory |
| `Nat.testBit`, `2 ^ m` | `bitObserver`, `sharpObserver`, `logE` | binary bit extraction on the class index `fiberIdx` |

**What the system holds.** The complete transcript `fullT n p` of length
`n(n - 1)/2`, the `n`-view evaluator `tableE n (fullT n p)`, and the `m`-view
evaluator `logE n (fullT n p) m`.

**Admissions relied on, and their price.** Unit 12's probe cost model (`AI-16`).
This unit makes explicit the price difference between *representing* a known
partition (`⌈log₂ k⌉` binary views via `sharpObserver`) and *acquiring* an
unknown partition from pairwise probes (`n(n - 1)/2` probes in the worst case via
`acquisition_cost_exact`, followed by compression into `⌈log₂ k⌉` views via
`log_views`, `AI-17`, `TT-42`, `TT-44`).

**Phrases to read with care.**

- "`m` views suffice" vs "`n(n - 1)/2` probes are required." Views are subsets
  of `D` held by a static `Evaluator` (`sharp_observable_iff`: `m` views can
  encode `2 ^ m` fibers because each datum's membership across `m` views is an
  `m`-bit vector). Probes are pairwise equality queries `decide (p x = p y)`
  made to discover which points share a fiber (`acquisition_cost_exact`).

## What it shows, and what it does not

It shows that `n(n - 1)/2` probes are both necessary and sufficient in the worst
case to acquire an arbitrary actor on `List.range n` (`acquisition_cost_exact`),
and that once the `n(n - 1)/2`-entry transcript `fullT n p` is in hand, an
`m`-view sharp evaluator `logE n (fullT n p) m` can be constructed from the
transcript alone whenever `classCount (List.range n) [p] ≤ 2 ^ m` (`log_views`).

It shows that `Sharp` is the conjunction of `Sufficient` and `Consistent`
(`sharp_iff_sufficient_and_consistent`), and that `sharpObserver D p m` is a
function of `p`'s partition alone (`sharpObserver_congr`).

It does not claim that `n(n - 1)/2` probes are needed when the observation
interface allows stronger queries than pairwise equality (for instance, a
fiber-reveal oracle acquires any partition on `n` elements in at most `n - 1`
queries), or when the actor is promised to come from a restricted class; Unit 15
examines promised class counts.

## Sources

| Item | Where |
|---|---|
| `scripted`, `run_scripted`, `fullT`, `run_complete`, `fullT_length`, `sameT`, `sameT_full`, `tableE`, `table_sharp`, `complete_table_acquires`, `acquisition_cost_exact` | `research/actor_institution/lean/ResearchActorInstitution/Acquisition.lean` lines 451–579 |
| `sharp_congr`, `classCount_congr`, `acquired`, `acquired_kernel`, `logE`, `log_views` | the same file, lines 583–630 |
| `Sharp`, `bitObserver`, `fiberIdx`, `sharp_observable_of_fibers_le`, `not_sharp_observable_of_fibers_gt`, `sharp_observable_iff` | `research/two_theorems/lean/ResearchTwoTheorems/Observer.lean` lines 132–133, 238–239, 438–526 |
| `Sufficient`, `sufficient_iff`, `sharp_iff_sufficient_and_consistent`, `sufficient_not_sharp`, `consistent_not_sufficient`, `sharp_fixes_partition`, `sharpObserver`, `sharpObserver_views`, `sharpObserver_congr` | `research/two_theorems/lean/ResearchTwoTheorems/Sufficiency.lean` lines 44–221 |
| Python mirrors | `research/actor_institution/model.py` lines 240–262 (`acquisition_values`); `research/two_theorems/model.py` lines 934–980 (`sufficient`, `sufficiency_checks`, `sharp_fixes_partition_check`) |
| Check | `textbook/institutions/checks/i14_acquisition_exact.py` |
| Ledger | `research/actor_institution/CLAIMS.md` AI-16, AI-16c, AI-17; `research/two_theorems/CLAIMS.md` TT-05, TT-05c, TT-42, TT-42c, TT-44, TT-44c |
