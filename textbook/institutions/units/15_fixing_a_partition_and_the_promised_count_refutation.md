# Unit 15. Fixing a partition, and the promised-count refutation

**Claim.** An exact-class-count promise can change acquisition cost. On two
inputs, exactly two classes implies separation without a probe; at
most two classes does not. The two promise readings stay distinct.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** A transcript `T` fixes the partition on `D` (`Fixes D T`) when every
two actors consistent with `T` have the same partition on `D`. Any evaluator `E`
that is sharp for all actors consistent with `T` forces `Fixes D T`
(`acquires_implies_fixes`), while the empty transcript on `[0, 1]` does not fix
the partition (`empty_transcript_fixes_nothing`). For a fixed two-actor family
`{fun z => z, merge 0 1}` on `List.range 2`, one probe on `(0, 1)` and the
two-case rule `admit01` acquire both actors (`complete_evaluator_for_two`).
When an actor is promised to have *exactly* `N` classes (`classCount D [p] = N`),
the proposed formula `N(N - 1)/2 + (n - N)(N - 1)` (`TT-43o (ii)`) gives `1` at
`n = N = 2` (`proposal_count_two`), whereas `0` probes suffice because the one-view
evaluator `[[0]]` is already sharp for every two-class actor on `[0, 1]`
(`exact_promise_zero_probes_two`).

**Status:** derived (`acquires_implies_fixes`, `complete_evaluator_for_two`),
refuted (`TT-43o (ii)` under the "exactly `N` classes" reading at `n = N`), and
open (`AI-18o`: constructive converse of `acquires_implies_fixes` in Lean;
`AI-19o`: general proof of `N(N - 1)/2 + (n - N)(N - 1)` under the "at most `N`
classes" reading). **Lean:** `Acquisition.probe01`, `Acquisition.admit01`,
`Acquisition.complete_evaluator_for_two`, `Acquisition.probe01_transcripts`,
`Acquisition.Fixes`, `Acquisition.acquires_implies_fixes`,
`Acquisition.empty_transcript_fixes_nothing`, `Acquisition.classCount_two_iff`,
`Acquisition.exact_promise_zero_probes_two`, `Acquisition.proposal_count_two`
(`actor_institution`). **Sources:**
`research/actor_institution/lean/ResearchActorInstitution/Acquisition.lean`
lines 428–446, 636–708.

Units 13 and 14 resolved `TT-43o (i)` and `(iii)`: without a promise on the
actor, `n(n - 1)/2` probes are necessary and sufficient in the worst case, and
the acquired table compresses into `⌈log₂ k⌉` views. This unit addresses the
remaining parts of `TT-43o` (`(ii)` and `(iv)`) and the retained two-actor
counterexample (`AI-21`):
1. Relative to the fixed two-member family `{fun z => z, merge 0 1}` on two
   points, `1` probe and a two-case rule (`admit01`) acquire every member
   (`complete_evaluator_for_two`).
2. A transcript `T` can admit an evaluator sharp for all actors consistent with
   `T` only if `T` already fixes the partition on `D` (`acquires_implies_fixes`,
   the necessity half of `TT-43o (iv)`). In the Python model (`fixes_converse_check`),
   the equivalence-closure evaluator `closure_evaluator` checks the converse on
   `n ≤ 4` (`AI-18c`), while the general Lean proof of the converse remains
   open (`AI-18o`).
3. Conjecture `TT-43o (ii)` proposed `N(N - 1)/2 + (n - N)(N - 1)` as the
   worst-case probe cost when the actor is promised `N` classes. That statement
   has two readings—"at most `N` classes" and "exactly `N` classes"—and they
   come apart at `n = N`. Under "exactly `N` classes" on `[0, 1]` (`n = N = 2`),
   every actor with `classCount [0, 1] [p] = 2` satisfies `p 0 ≠ p 1`
   (`classCount_two_iff`), so the fixed evaluator `[[0]]` is sharp for `p` with
   `0` probes (`exact_promise_zero_probes_two`), refuting the formula's value
   `1` (`proposal_count_two`, `AI-19`). Under "at most `N` classes", the
   minimax game check in Python matches `N(N - 1)/2 + (n - N)(N - 1)` for every
   `1 ≤ N ≤ n ≤ 5` (`AI-19c`), and its general Lean proof remains open
   (`AI-19o`).

</details>

## First pass

There are two inputs, 0 and 1. Compare two promises:

| Promise | Possibilities left | Is a pair probe needed? |
|---|---|---|
| Exactly two classes | {0}, {1} | No |
| At most two classes | {0}, {1} or {0,1} | Yes, to distinguish these cases |

With the exact promise, the observer [[0]] already distinguishes the
only two classes. The proposed positive probe-count formula therefore
fails on this boundary case. Its different at-most reading remains a
separately stated open problem.

**Predict:** has the exact-promise counterexample refuted every possible
bounded-class acquisition formula?

<details><summary>Check your prediction</summary>

No. A counterexample refutes the specific statement whose assumptions
it satisfies. Changing exactly to at most changes the permitted actor
family; the same zero-probe argument no longer applies.

</details>

## What you need first

Unit 03 (`classCount`, `dedupL`, `memB`), Unit 12 (`Transcript`, `Protocol`,
`run`, `Consistent`), Unit 13 (`merge`), and Unit 14 (`Sharp`,
`sharp_fixes_partition`).

### 1. The two-actor family on `List.range 2`

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Acquisition.lean lines 428–446
/-- Probe `(0, 1)`, always. -/
def probe01 : Protocol := fun _ => some (0, 1)

/-- Two cases: if the pair answered "same", present nothing; otherwise one
view separating `0` from `1`. -/
def admit01 (T : Transcript) : Evaluator := if (0, 1, true) ∈ T then [] else [[0]]

theorem complete_evaluator_for_two :
    Sharp (List.range 2) (admit01 (run probe01 (fun z => z) 1)) (fun z => z) ∧
    Sharp (List.range 2) (admit01 (run probe01 (merge 0 1) 1)) (merge 0 1) := by
  unfold Sharp
  decide

theorem probe01_transcripts :
    run probe01 (fun z => z) 1 = [(0, 1, false)] ∧ run probe01 (merge 0 1) 1 = [(0, 1, true)] := by
  decide
```

On `List.range 2 = [0, 1]`, `probe01` asks `(0, 1)` at step `1`. The identity
answers `false`, so `admit01` returns `[[0]]`, which separates `0` and `1`;
`merge 0 1` answers `true`, so `admit01` returns `[]`, which merges `0` and `1`.

### 2. Fixing the partition (`Fixes`)

```lean
-- Lean (research), the same file, lines 636–638
/-- The transcript fixes the partition on `D`: all consistent actors agree on
every pair. -/
def Fixes (D : List Nat) (T : Transcript) : Prop :=
  ∀ p p', Consistent T p → Consistent T p' →
    ∀ x, x ∈ D → ∀ y, y ∈ D → (p x = p y ↔ p' x = p' y)
```

`Fixes D T` says that any two actors `p, p'` consistent with `T` carve the
exact same partition on `D`.

```python
# Python (research), research/actor_institution/model.py lines 308–311
def fixes(n: int, T: Transcript, parts: list[Presentation]) -> bool:
    """`Acquisition.Fixes`: every two consistent actors agree on every pair."""
    cons = [p for p in parts if consistent(p, T)]
    return all((p[x] == p[y]) == (q[x] == q[y]) for p in cons for q in cons for x in range(n) for y in range(n))
```

## The theorems

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Acquisition.lean lines 642–707
theorem acquires_implies_fixes (D : List Nat) (T : Transcript) (E : Evaluator)
    (h : ∀ p, Consistent T p → Sharp D E p) : Fixes D T := by
  intro p p' hp hp' x hx y hy
  rw [← (h p hp) x hx y hy, ← (h p' hp') x hx y hy]

theorem empty_transcript_fixes_nothing : ¬ Fixes [0, 1] [] := by
  intro h
  have := (h (fun z => z) (merge 0 1) (fun _ he => by cases he) (fun _ he => by cases he)
    0 (by decide) 1 (by decide)).mpr (by decide)
  exact absurd this (by decide)

theorem classCount_two_iff (p : Nat → Nat) : classCount [0, 1] [p] = 2 ↔ p 0 ≠ p 1 := by ...

theorem exact_promise_zero_probes_two (p : Nat → Nat) (hN : classCount [0, 1] [p] = 2) :
    Sharp [0, 1] [[0]] p := by
  have hne := (classCount_two_iff p).mp hN
  intro x hx y hy
...

theorem proposal_count_two : 2 * (2 - 1) / 2 + (2 - 2) * (2 - 1) = 1 := by decide
```

## The proof, step by step

**Step 1. `acquires_implies_fixes` and `empty_transcript_fixes_nothing`.**
Suppose `E` is sharp for every `p` consistent with `T`. For any two consistent
actors `p, p'` and any `x, y ∈ D`, both `p x = p y` and `p' x = p' y` are
equivalent to `verdictB E x y = false`, so `p x = p y ↔ p' x = p' y`
(`acquires_implies_fixes`). For `T = []` on `[0, 1]`, both `fun z => z` and
`merge 0 1` are vacuously consistent with `[]`, yet `merge 0 1 0 = merge 0 1 1`
while `(fun z => z) 0 ≠ (fun z => z) 1` (`empty_transcript_fixes_nothing`).

**Step 2. `classCount_two_iff`.**
On `[0, 1]`, `classCount [0, 1] [p]` is the length of `dedupL [[p 0], [p 1]]`.
Case-splitting on `Nat.decEq (p 0) (p 1)`: if `p 0 = p 1`, the deduplicated
list is `[[p 1]]` of length `1 ≠ 2`; if `p 0 ≠ p 1`, the deduplicated list is
`[[p 0], [p 1]]` of length `2`.

**Step 3. `exact_promise_zero_probes_two` and `proposal_count_two`.**
If `classCount [0, 1] [p] = 2`, then `p 0 ≠ p 1` by `classCount_two_iff`. For
the one-view evaluator `[[0]]`, `verdictB [[0]] x y` is `false` on `(0, 0)` and
`(1, 1)` (where `p x = p y` holds by reflexivity) and `true` on `(0, 1)` and
`(1, 0)` (where `p x ≠ p y` holds by `p 0 ≠ p 1`). Hence `Sharp [0, 1] [[0]] p`
holds without running any protocol (`0` probes), whereas `proposal_count_two`
evaluates `2 * (2 - 1) / 2 + (2 - 2) * (2 - 1)` to `1`.

## The same fact in Python

The check runs `fixes_converse_check(n)` for `n = 1..4` and
`acquisition_values(5)` from `actor_institution/model.py`:

1. Across all `3^0 + 3^1 + 3^3 + 3^6 = 760` transcripts on `n = 1..4`, whenever
   a transcript `T` is consistent with at least one actor and satisfies
   `fixes(n, T, parts)`, the equivalence-closure evaluator
   `closure_evaluator(n, T)` is sharp for every consistent actor (`0`
   violations, `AI-18c`).
2. Under the "at most `N` classes" promise (`at_most`), the minimax game value
   equals `proposal_count(n, N) = N(N - 1)//2 + (n - N)*(N - 1)` for every
   `1 ≤ N ≤ n ≤ 5` (`at_most_mismatches == []`, `AI-19c`).
3. Under the "exactly `N` classes" promise (`exactly`), the minimax game value
   disagrees with `proposal_count(n, N)` at `"2,2"`, `"3,3"`, `"4,4"`, `"5,5"`
   (where the game value is `0` because the only partition of `n` points into
   `n` classes is the discrete partition, `AI-19`).

```
python textbook/institutions/checks/i15_promise_refuted.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `decide` | `complete_evaluator_for_two`, `probe01_transcripts`, `empty_transcript_fixes_nothing`, `exact_promise_zero_probes_two`, `proposal_count_two` | kernel evaluation on `[0, 1]` |
| `Nat.decEq` | `classCount_two_iff` | decidable equality on `p 0` and `p 1` |

**What the system holds.** On `[0, 1]`: the transcripts `[(0, 1, false)]`,
`[(0, 1, true)]`, and `[]`, and the evaluators `[]` and `[[0]]`.

**Admissions relied on, and their price.** Unit 12's probe grammar (`AI-16`),
plus an explicit prior promise (`classCount D [p] = N` or `classCount D [p] ≤ N`)
restricting the set of candidate actors (`AI-19`). The refutation at `n = N = 2`
shows why the exact wording of a prior promise ("at most `N`" vs "exactly `N`")
must be stated in the theorem's premise: when `n = N`, promising `classCount = n`
leaves only one partition on `D`, so the probe cost drops to `0`.

**Phrases to read with care.**

- "`Fixes D T` characterizes acquisition." The Lean file derives one direction
  (`acquires_implies_fixes`, `AI-18`). The converse—that whenever `Fixes D T`
  holds for a consistent transcript `T`, the closure evaluator is sharp for
  every consistent actor—is checked exhaustively in Python for `n ≤ 4`
  (`AI-18c`) and remains an open Lean target (`AI-18o`).
- "The promised-count formula `N(N - 1)/2 + (n - N)(N - 1)`." Under "exactly `N`
  classes" it is refuted at every `n = N ≥ 2` (`exact_promise_zero_probes_two`,
  `AI-19`). Under "at most `N` classes" it holds in the Python minimax game for
  all `1 ≤ N ≤ n ≤ 5` (`AI-19c`) and remains an open Lean target (`AI-19o`).

## What it shows, and what it does not

It shows that `acquires_implies_fixes` holds on every carrier `D`, that the
empty transcript fails `Fixes [0, 1] []`, and that `1` probe acquires the
two-actor family `{id, merge 0 1}` on `List.range 2`.

It shows that promising `classCount [0, 1] [p] = 2` makes `[[0]]` sharp for `p`
with `0` probes (`exact_promise_zero_probes_two`), refuting the "exactly `N`"
reading of `TT-43o (ii)` at `n = N = 2`.

It does not prove the Lean converse of `acquires_implies_fixes` (`AI-18o` is
open) or the general Lean theorem for the "at most `N`" reading of `TT-43o (ii)`
(`AI-19o` is open); both are checked only within the finite bounds `n ≤ 4` and
`n ≤ 5` in Python (`AI-18c`, `AI-19c`).

## Sources

| Item | Where |
|---|---|
| `probe01`, `admit01`, `complete_evaluator_for_two`, `probe01_transcripts` | `research/actor_institution/lean/ResearchActorInstitution/Acquisition.lean` lines 428–446 |
| `Fixes`, `acquires_implies_fixes`, `empty_transcript_fixes_nothing` | the same file, lines 636–653 |
| `classCount_two_iff`, `exact_promise_zero_probes_two`, `proposal_count_two` | the same file, lines 658–707 |
| Python mirrors | `research/actor_institution/model.py` lines 200–262 (`game_value`, `proposal_count`, `acquisition_values`), 280–332 (`closure_evaluator`, `fixes`, `fixes_converse_check`) |
| Check | `textbook/institutions/checks/i15_promise_refuted.py` |
| Ledger | `research/actor_institution/CLAIMS.md` AI-18, AI-18c, AI-18o, AI-19, AI-19c, AI-19o, AI-21 |
