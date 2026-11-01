# Unit 28. Fixed data bound rounds that add new demands

**Claim.** A finite run with a strictly increasing natural-number measure
capped by B has at most B + 1 states. That gives at most B accepted
rounds between them. Applying this to demands requires a fixed data
set and a genuinely new demand each round.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** A run whose measure strictly increases every round and never
exceeds `B` has at most `B + 1` states (`strict_bounded_length`). The
possible demands over `n` data are the pairs `i < j < n`, and there are
exactly `n(n-1)/2` of them, stated without division as
`2 * length = n * (n - 1)` (`allPairs_length`). So a run in which every
round adds one demand over a fixed set of `n` data makes at most
`n(n-1)/2` rounds (`no_supply_round_bound`).

**Status:** derived for the
two counting laws; conditional for the round bound, whose hypotheses are
about an arbitrary measure. The connection to Genesis's own rounds is
proved later, under the declared round shape, in `Rounds.lean` (Unit 34).
**Lean:** `Derivation.index_le_strict_mono` (`lean4/Derivation/Counting.lean`
lines 15-26), `strict_bounded_length` (30-39), `no_supply_round_bound`
(53-57), `allPairs` (61-63), `allPairs_length` (69-84). **Axioms:**
`propext, Quot.sound` for all four theorems. **Depends on:** demands are
pairs `i < j` below the datum count (Unit 17); collapse and separation
(Units 08, 09).

</details>

## First pass

Use [Reasoning 52–55](../reasoning_lab/52_start_then_one_more.md) for the induction method and the distinction between states, rounds and a fixed ceiling.

Three admitted data, 0, 1, and 2, permit just three different
small-first demands: `(0, 1)`, `(0, 2)`, and `(1, 2)`.
They are possible requests; they need not all be on the books already.

Suppose each accepted round adds a previously absent demand and keeps
the same three data. The demand count can rise through `0, 1, 2, 3`.
That is four recorded states with three rounds between them. It cannot
rise a fourth time while staying at most three.

Two conditions matter: strict growth of the count and a fixed ceiling.
Repeating an already recorded request gives no growth. Admitting new
data changes the available pairs and their ceiling.

**Predict:** can we use this argument to bound every successful event
when external supply is disabled?

<details>
<summary>Check your prediction</summary>

No. Successful events can leave the measure unchanged, and the response
grammar itself includes fresh-data items. The theorem needs its stated
round conditions. The two exported baselines are checked separately.

</details>

The [Search lab](../search_lab/README.md) distinguishes accepted
responses, exhaustion, and resource stops in a worked branch tree.

## Question

Under which conditions does a finite set of possible demands bound the
number of accepted rounds? How do those conditions differ from merely
disabling an external supply policy or successfully admitting an event?

## What we already possess

- A demand is a pair `(i, j)` with `i < j < r.data` (the impose guard,
  Unit 17). A regime's demands are stored in `reqs`.
- The round shape studied here imposes a new demand, responds while
  preserving prior demands, and admits no fresh datum. Unit 34 formalizes
  that declared shape. The check below confirms fixed datum counts and
  growing request counts on the creation edges of both exported baselines.
- The engine's two closed baselines, `closed_L` and `closed_F`, exported
  in `artifacts/claims.json` under `CL-CLOSURE-TERMINATION`.

## New concept: a measure that must climb, in a room with a ceiling

Attach a number to every state of a run: its *measure*. Suppose two
things: the measure goes up by at least one at every round (*strict
growth*), and it can never exceed some `B` (*the bound*). Then the run
has at most `B + 1` states. The reason is that after `i` rounds the
measure is at least `i`, so `i ≤ B`.

Here the measure is the number of demands on the books. It climbs by one
each round. Its ceiling is the number of possible demands, the pairs of
distinct data among `n` of them, which is `n(n-1)/2`.

Two small matters of form. Genesis states the pair count as
`2 * length = n * (n - 1)`, because `Nat` division rounds down and the
multiplicative form needs no lemma about `n(n-1)` being even. And the
proofs use `omega`, Lean's decision procedure for linear arithmetic over
the naturals: give it the facts `n ≤ f n`, `f n < f (n+1)` and it closes
`n + 1 ≤ f (n + 1)` without being told how.

## Plain-language interpretation

A counter that must go up every step and has a ceiling cannot be stepped
more times than the ceiling allows. That is the whole of the termination
bound, and it is deliberately abstract: it says nothing about regimes. The
second law says what the ceiling is for demands: with `n` data there are
only so many pairs to demand apart. Put together, a closed run with `n`
data, whose accepted rounds meet the growth and ceiling hypotheses,
cannot have more than `n(n-1)/2` such rounds.

What the module does *not* do is prove that Genesis's rounds have a
climbing, bounded measure. The theorem `no_supply_round_bound` takes that
as hypotheses, and its own docstring says so. The exported runs satisfy
the hypotheses, as the check shows edge by edge, and a later module proves
them under the declared round shape (Unit 34). This unit teaches the
counting, with that boundary marked.

## Pseudocode

```
# Gloss
given: f(0), f(1), ..., f(L-1) with f(i) < f(i+1) and f(i) <= B
claim: L <= B + 1
step 1 (index_le_strict_mono): i <= f(i) for every i < L
   f(0) >= 0;  if i <= f(i) and f(i) < f(i+1) then i + 1 <= f(i+1)
step 2 (strict_bounded_length): suppose L > B + 1
   then B + 1 < L, so B + 1 <= f(B + 1) <= B: impossible

pairs(0)     = []
pairs(n + 1) = pairs(n) ++ [(0, n), (1, n), ..., (n - 1, n)]
claim: 2 * len(pairs(n)) = n * (n - 1)
   2 * len(pairs(n + 1)) = 2 * len(pairs(n)) + 2n = n(n - 1) + 2n = (n + 1) n
```

## Python

The check computes Lean's `allPairs` in Python and runs both closed
baselines. Each run stops at the all-pairs-separated fixpoint within the
pair bound, and every creation edge adds one demand over a fixed datum
count.

```python
from derivation.candidates import Bounds
from derivation.engine import READING_F, READING_L, build_tree

for reading in (READING_L, READING_F):
    t = build_tree(reading, "mu1", Bounds(max_items=2, max_arity=2),
                   max_rounds=15, pre_expansion_node_guard=200, supply=False)
    n = t.nodes[0].regime.n_data()
    print(n, n * (n - 1) // 2, t.stats()["max_depth"], t.stats()["by_status"])
    print(sorted(len(x.regime.reqs) for x in t.nodes))
```

Output:

```text
2 1 1 {'expanded': 1, 'terminal_all_separated': 3}
[0, 1, 1, 1]
3 3 3 {'expanded': 4, 'terminal_all_separated': 16}
[0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
```

## Line-by-line Python explanation

`build_tree(reading, "mu1", Bounds(...), max_rounds=15,
pre_expansion_node_guard=200, supply=False)` expands the branch tree from
the Challenge 3 situation under the item-count measure, with the supply
move disabled. `max_rounds=15` and the node guard are the declared
resource bounds; neither is reached.

`t.nodes[0].regime.n_data()` is the datum count at the root: 2 in reading
L, 3 in reading F. `n * (n - 1) // 2` is the pair bound: 1 and 3.

`t.stats()["max_depth"]` is the deepest round reached: 1 and 3, equal to
the bounds in these two runs. `by_status` shows every leaf is
`terminal_all_separated`; there is no guard cut and no open branch.

The last line lists the demand count of every node. In reading L the
root has none and the three children have one. In reading F the twenty
nodes carry 0, 1, 2 or 3 demands, one more at each round: the measure
climbs by exactly one. (The root is the situation *before* the Challenge
3 demand is imposed; round 1 imposes it.)

These are the numbers of `artifacts/claims.json` (`pair_bound` 1 and 3,
`rounds_used` 1 and 3, `within_bound` true) and of the paper's table in
§8.5 (nodes 4 and 20, terminal branches 3 and 16).

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Counting.lean lines 14-39
/-- A strictly increasing `Nat`-valued measure dominates its index. -/
theorem index_le_strict_mono (f : Nat → Nat) (L : Nat)
    (hstrict : ∀ i, i + 1 < L → f i < f (i + 1)) :
    ∀ i, i < L → i ≤ f i := by
  intro i
  induction i with
  | zero => intro _; exact Nat.zero_le _
  | succ n ih =>
      intro h
      have hn : n < L := Nat.lt_of_succ_lt h
      have h1 : f n < f (n + 1) := hstrict n h
      have h2 : n ≤ f n := ih hn
      omega

/-- Termination law: a run whose measure strictly increases every round and
never exceeds `B` has at most `B + 1` rounds. -/
theorem strict_bounded_length (f : Nat → Nat) (L B : Nat)
    (hstrict : ∀ i, i + 1 < L → f i < f (i + 1))
    (hbound : ∀ i, i < L → f i ≤ B) : L ≤ B + 1 := by
  by_cases h : L ≤ B + 1
  · exact h
  · have hlt : B + 1 < L := Nat.lt_of_not_le h
    have h1 : B + 1 ≤ f (B + 1) :=
      index_le_strict_mono f L hstrict (B + 1) hlt
    have h2 : f (B + 1) ≤ B := hbound (B + 1) hlt
    omega
```

```lean
-- Lean (Genesis), lean4/Derivation/Counting.lean lines 53-84
theorem no_supply_round_bound (f : Nat → Nat) (L n : Nat)
    (hstrict : ∀ i, i + 1 < L → f i < f (i + 1))
    (hbound : ∀ i, i < L → f i ≤ n * (n - 1) / 2) :
    L ≤ n * (n - 1) / 2 + 1 :=
  strict_bounded_length f L (n * (n - 1) / 2) hstrict hbound

/-- The requirement language of a regime with `n` data: the canonical
enumeration of ordered pairs `(i, j)` with `i < j < n`. -/
def allPairs : Nat → List (Nat × Nat)
  | 0 => []
  | n + 1 => allPairs n ++ (List.range n).map (fun i => (i, n))

theorem allPairs_length (n : Nat) :
    2 * (allPairs n).length = n * (n - 1) := by
  induction n with
  | zero => rfl
  | succ m ih =>
      have hexp : (allPairs (m + 1)).length = (allPairs m).length + m := by
        simp [allPairs]
      rw [hexp]
      have hsq : (m + 1) * (m + 1 - 1) = m * (m - 1) + 2 * m := by
        cases m with
        | zero => rfl
        | succ k =>
            simp only [Nat.succ_sub_one, Nat.succ_mul, Nat.mul_succ]
            generalize k * k = a
            omega
      omega
```

The book's Lean computes `allPairs 4`, instantiates the laws at concrete
measures, and shows that each hypothesis is load-bearing.

```lean
-- Lean (book), textbook/checks/u28_lean.py
theorem allPairs_four :
    allPairs 4 = [(0, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 3)] := by
  decide

theorem id_strict (L : Nat) :
    ∀ i, i + 1 < L → (fun k : Nat => k) i < (fun k : Nat => k) (i + 1) :=
  fun i _ => Nat.lt_succ_self i

theorem run_capped_at_three (L : Nat) (hb : ∀ i, i < L → (fun k : Nat => k) i ≤ 3) :
    L ≤ 4 :=
  strict_bounded_length (fun k => k) L 3 (id_strict L) hb

theorem three_data_bound (f : Nat → Nat) (L : Nat)
    (hs : ∀ i, i + 1 < L → f i < f (i + 1))
    (hb : ∀ i, i < L → f i ≤ 3) : L ≤ 4 :=
  no_supply_round_bound f L 3 hs hb

theorem no_bound_without_growth :
    ¬ (∀ (f : Nat → Nat) (L B : Nat), (∀ i, i < L → f i ≤ B) → L ≤ B + 1) := by
  intro h
  have h2 : 2 ≤ 0 + 1 := h (fun _ => 0) 2 0 (fun _ _ => Nat.le_refl 0)
  omega
```

## Line-by-line Lean explanation

**`index_le_strict_mono`.** `f : Nat → Nat` is the measure, `L` the
length of the run, `hstrict` says the measure rises at every step that
stays inside the run. The conclusion is `i ≤ f i` for every index in the
run. `intro i; induction i with` proves it for `0` and then for `n + 1`
assuming it for `n`. Base case: `Nat.zero_le _`, zero is below anything.
Step: `h : n + 1 < L`, so `hn : n < L` by `Nat.lt_of_succ_lt`;
`h1 : f n < f (n + 1)` from the hypothesis; `h2 : n ≤ f n` from the
induction hypothesis `ih` applied to `hn`. `omega` combines `n ≤ f n` and
`f n < f (n + 1)` into `n + 1 ≤ f (n + 1)`.

**`strict_bounded_length`.** `by_cases h : L ≤ B + 1` splits on the
conclusion itself, which is decidable. If it holds, done. Otherwise
`hlt : B + 1 < L`, so index `B + 1` is inside the run; `h1 : B + 1 ≤ f (B +
1)` from the first theorem; `h2 : f (B + 1) ≤ B` from the bound; `omega`
sees `B + 1 ≤ B` and closes the goal.

Here `L` counts measure entries, interpreted as recorded states. The
quoted source comment calls them rounds; a nonempty sequence of `R + 1`
states has `R` intervening rounds. The book's `accepted_round_bound`
makes this indexing explicit. It does not count every admitted event as
an accepted separation round.

**`no_supply_round_bound`.** The previous theorem with `B := n * (n - 1) /
2`. Nothing new is proved; the name records the intended instance, and the
docstring records that the hypotheses are about the run, not discharged
here.

**`allPairs`.** Defined by recursion on `n`: no pairs for `0`; for `n + 1`,
the pairs below `n` followed by `(0, n), ..., (n - 1, n)`, which
`(List.range n).map (fun i => (i, n))` produces.

**`allPairs_length`.** Induction on `n`. Base: both sides are `0`, by
`rfl`. Step, for `m + 1`: `hexp` says the new list is `m` longer, which
`simp [allPairs]` reads off the definition (the appended list has length
`m`). `hsq` is the arithmetic `(m + 1) m = m (m - 1) + 2 m`; it needs a
case split because `m - 1` is natural-number subtraction, which is `0`
when `m = 0`. In the `succ k` case, `simp only` unfolds the products,
`generalize k * k = a` hides the one nonlinear term, and `omega` finishes
the linear remainder. The final `omega` combines `ih`, `hexp` and `hsq`.

**The book's theorems.** `allPairs_four` evaluates the definition by
`decide`: six pairs, listed in Genesis's order. `id_strict` says the
identity measure climbs. `run_capped_at_three` applies the law with the
identity measure and ceiling 3: at most four states. `three_data_bound` is
the `n = 3` instance of the conditional law, Lean reducing `3 * (3 - 1) /
2` to `3`. `no_bound_without_growth` shows the growth hypothesis is doing
work: the constant measure `0` stays below `0` for a run of length `2`,
and `2 ≤ 1` is false. Drop strict growth and there is no bound.

**Axioms.** All four Genesis theorems report `propext, Quot.sound`, which
`omega` and `simp` bring in through the `Nat` and `List` lemmas they use.
`allPairs_four` reports no axiom: `decide` on a closed term is a
computation.

## What has been proved

- A strictly climbing measure dominates its index, and a climbing,
  bounded measure bounds the run length by `B + 1` (Genesis, derived).
- There are exactly `n(n-1)/2` demands available over `n` data, in the
  division-free form (Genesis, derived).
- The instance: a run with a climbing measure capped by `n(n-1)/2` has at
  most `n(n-1)/2 + 1` states (Genesis, conditional). For a nonempty run
  of `R + 1` states this gives `R` at most the pair bound. The book's
  `accepted_round_bound` states that conversion explicitly.
- Both hypotheses are needed (book Lean: no bound without growth; the
  identity measure shows growth alone bounds nothing).

## What has not been proved

- In this module: that Genesis's closed rounds have a climbing, bounded
  measure. `no_supply_round_bound` assumes it. `Rounds.lean` proves it
  under the declared round shape (`round_reqs_succ`, `round_data_eq`,
  `closedRun_round_bound_from_empty`, Unit 34); that each *exported* round
  has that shape is checked computationally, not proved.
- A fixed ceiling for runs that admit new data. A bare `Supply` event
  changes no admitted state (Unit 03); an admission of a fresh datum
  increases the available pairs by `n`. The disabled external policy and
  absence of `.newDatum` in responses are different conditions.
- A bound on every successful event or on execution time. Repeating an
  already present request can succeed without increasing the measure.
- That the bound is attained in general. Both baselines happen to use
  exactly their bound (1 of 1, 3 of 3); the law is an upper bound only.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `Nat`, `induction`, `Nat.zero_le`, `Nat.lt_of_succ_lt` | the climbing argument | metatheory arithmetic |
| `omega` | linear arithmetic steps | metatheory decision procedure |
| `by_cases` on `L ≤ B + 1` | the contrapositive | metatheory; decidable, no `Classical.choice` |
| `List`, `List.range`, `map`, `length`, `simp` | the pair enumeration | metatheory |
| `Nat` division in `n * (n - 1) / 2` | the stated ceiling | used by the conditional bound; `allPairs_length` is stated multiplicatively |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** The demand store `reqs`, which grows by one
pair per closed round, and the datum count, which does not change. The
measure is the metatheory's count of that store.

**Phrases to read with care.**

- The two exported closed baselines reach the all-pairs-separated status
  under their stated settings. The general counting result bounds rounds
  satisfying its growth and ceiling conditions; it is not a runtime
  bound for every event sequence or every engine configuration.
- "The demands run out" is the right picture: the ceiling is the number of
  pairs, and every closed round spends one.
- "Proved in Lean" for the closed baselines means: the counting laws, and
  (in Unit 34) the round shape's growth. The exported runs having that
  shape is a computation.

## Student exercise

Why does Genesis state the pair count as `2 * (allPairs n).length = n * (n
- 1)` rather than `(allPairs n).length = n * (n - 1) / 2`? Check both
forms for `n = 5`.

## Answer

<details>
<summary>Worked answer</summary>

In `Nat`, division rounds down. The multiplicative equality already
exhibits `n * (n - 1)` as twice a natural number, so dividing it by 2
recovers the count exactly. A separate parity lemma is not compulsory:
the book's `allPairs_divided` derives the divided form from that equality.
The source presentation avoids division steps in the counting induction.
For `n = 5`,
`allPairs 5` has 10 pairs: `2 * 10 = 20 = 5 * 4`, and `5 * 4 / 2 = 10`.
`no_supply_round_bound` does use the divided form, but only as a ceiling
handed to `strict_bounded_length`, which accepts any `B`.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Counting.lean` lines 15-26, 30-39, 53-57, 61-63, 69-84 |
| Axiom report | `artifacts/lean_axioms.txt`: `index_le_strict_mono`, `strict_bounded_length`, `no_supply_round_bound`, `allPairs_length` all `[propext, Quot.sound]` |
| Paper | `paper/paper.md` §8.5 (closed-system baseline, the table and the two theorem paragraphs); ledger `CL-CLOSURE-TERMINATION` |
| Artifact | `artifacts/claims.json` `CL-CLOSURE-TERMINATION`: L `pair_bound` 1, `rounds_used` 1; F `pair_bound` 3, `rounds_used` 3; `every_maximal_branch_terminates` true |
| Check (Python) | `python textbook/checks/u28_closure_bound.py`: pair count for `n ≤ 5`; fixed data and growing demands on both exported baselines; 3 and 16 terminal nodes match the artifact; repeated successful request events give counts `[0,1,1,1]` without strict growth |
| Check (book Lean) | `python textbook/checks/u28_lean.py`: eight book reports plus four native results kernel-checked, Lean 4.33.0, including `accepted_round_bound` and `allPairs_divided` (`propext, Quot.sound`) |
