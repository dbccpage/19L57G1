# Unit 17. Demands are irreflexive by guard

**Claim.** A request is admitted only for two different, already admitted
positions, written smaller first. This guard is declared; it does not
supply a test that meets the request.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** The event `impose i j` records a separation demand only when
`i < j` and `j < r.data`. So a demand never names a datum against itself,
never names a datum that is not there, and is always written with the
smaller index first. This is a definition, chosen by the external
constructor; nothing derives it.

**Status:** admitted. **Lean:**
`Derivation.stepE`, case `.impose` (`lean4/Derivation/Basic.lean` lines
159-162). **Axioms:** `propext` in the definition (through `insertNew`).
**Depends on:** `Regime`, `Event`, `stepE` (Units 01, 03).

</details>

## First pass

There are two admitted data, at positions 0 and 1. A caller submits
the request “tell 0 and 1 apart.” The request is accepted because
both positions exist and the smaller comes first.

| Submitted pair | Accepted? | Reason |
|---|---|---|
| (0,1) | Yes | Both exist; smaller first |
| (0,0) | No | Same position twice |
| (1,0) | No | Wrong order |
| (0,2) | No | Position 2 is absent |

Acceptance records a task. It does not add a question that can tell
the data apart, and it does not establish that the task is achievable.
Submitting the same accepted request again leaves the record unchanged.

**Predict:** after recording the request, are 0 and 1 separated if
there are still no forms or instances?

<details>
<summary>Check your prediction</summary>

No. The request changes the task list, not the available tests.
A successful response must supply the missing distinction.

</details>

The guard also does not repair a malformed starting record. To conclude
that every recorded pair is sorted after replay, start with sorted pairs;
the empty starting record meets that condition.

## Question

A demand is the caller saying "tell these two apart". What stops the
caller from demanding that ⟨A⟩ be told apart from ⟨A⟩? Or from naming a
fourth datum when three are admitted? And when a theorem later needs
"every recorded demand is sorted", where does that come from?

## What we already possess

- `stepE r e` returns `some s` when the event is admissible and `none`
  when it is not (Unit 03). Rejection poisons the whole history under
  `replayE`.
- `insertNew` adds an element to a list unless it is already there
  (Unit 06).
- `reqs : List (Nat × Nat)` is the fifth field of a regime (Unit 01).

## New concept: a guard

A **guard** is the condition in front of an admission. `impose i j` has
the guard `i < j ∧ j < r.data`. If it holds, the pair is inserted into
`reqs`; if not, the event is rejected. Three consequences are built into
this one line:

1. **No self-demand.** `i < i` is false, so `impose d d` is always
   rejected.
2. **No demand on an absent datum.** `j < r.data` and `i < j` keep both
   indices among the admitted data.
3. **One writing per pair.** `(1, 0)` is rejected; only `(0, 1)` can be
   newly recorded. Starting from the empty record, a pair cannot enter
   under two spellings. An arbitrary raw `Regime` can already contain
   unsorted pairs; this guard does not remove them.

The first consequence explains *irreflexive by guard*: this event records
no self-demand. That is a declared choice of request language. Separately,
the definition of separation makes self-separation impossible: any context
gives the same answer when filled with the same datum twice. The book
proves this second fact without using the request guard. A caller could
instead record an impossible task; Genesis chooses to reject it at admission.

## Plain-language interpretation

A demand form with two boxes, "first" and "second", that the clerk will
only accept if the first number is smaller than the second and both
numbers are on the register. The rule is sensible, and it is a rule the
clerk was given. A rejected event returns no successor state; it does not
insert a rejected-request entry. A separate caller may keep a refusal log,
but that log is not a field of this regime.

There is a point of method here for the whole book. Later theorems (for
instance `isoRefl`, Unit 21) take as a hypothesis that every demand is
sorted. The hypothesis is dischargeable because of this guard, and the
book proves that in Lean: every regime reached by replay from a regime
with sorted demands has sorted demands. That is a **derived invariant of
an admitted guard**, and the two words should stay apart.

<details>
<summary>Programs and proof walkthroughs (optional)</summary>

## Pseudocode

```
# Gloss
impose(r, i, j):
  if i < j and j < r.data:  return r with (i, j) inserted into reqs
  else:                      reject
Consequences:
  impose(r, d, d) rejects, for every r, d          (d < d is false)
  impose(r, j, i) with i < j rejects                (j < i is false)
  if the initial reqs are sorted and replay succeeds:
    every resulting pair has i < j                 (induction on the history)
```

## Python

```python
from derivation.engine import GENESIS_L
from derivation.model import AdmissionError, Impose, replay, step

r = replay(GENESIS_L)
print(sorted(step(r, Impose(0, 1)).reqs))
for bad in (Impose(0, 0), Impose(1, 0), Impose(0, 2)):
    try:
        step(r, bad)
    except AdmissionError as e:
        print(bad, "->", e)
```

Output:

```text
[(0, 1)]
Impose(i=0, j=0) -> requirement out of range: (0, 0)
Impose(i=1, j=0) -> requirement out of range: (1, 0)
Impose(i=0, j=2) -> requirement out of range: (0, 2)
```

## Line-by-line Python explanation

`Impose(i, j)` (`model.py` lines 95-100) is a frozen dataclass whose
docstring says what it is: an external requirement, a persistent
constraint.

In `step` (lines 136-139) the `Impose` branch is the last one. It checks
`0 <= e.i < e.j < len(r.data)` and raises `AdmissionError` otherwise;
Python's chained comparison is the Lean guard with `0 <=` added, which
is automatic for `Nat` in Lean. On success it returns a new regime whose
`reqs` is the old set with the pair added. `reqs` is a `frozenset`, so
insertion deduplicates, as `insertNew` does in Lean.

The three refusals print the same message with different pairs; the
guard does not distinguish "same datum", "wrong order" and "not
admitted". Neither does Lean's.

The check script replays every history of length at most 5 over a
ten-event alphabet (111 111 histories, 2 883 admissible) and finds 990
recorded demands, all with `i < j < data`.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Basic.lean lines 159-162
  | .impose i j =>
      if i < j ∧ j < r.data then
        some { r with reqs := insertNew r.reqs (i, j) }
      else none
```

```lean
-- Lean (book), textbook/checks/u17_lean.py
theorem impose_self_rejected (r : Regime) (d : Nat) :
    stepE r (.impose d d) = none := by
  simp [stepE]

theorem impose_succeeds_iff (r : Regime) (i j : Nat) :
    (∃ s, stepE r (.impose i j) = some s) ↔ (i < j ∧ j < r.data) := by
  constructor
  · intro ⟨s, hs⟩
    simp only [stepE] at hs
    split at hs
    · assumption
    · cases hs
  · intro h
    refine ⟨{ r with reqs := insertNew r.reqs (i, j) }, ?_⟩
    simp [stepE, h]

theorem replay_keeps_reqs_ordered (h : List Event) (r s : Regime)
    (hr : ∀ q ∈ r.reqs, q.1 < q.2) (hs : replayE h r = some s) :
    ∀ q ∈ s.reqs, q.1 < q.2 := by
  induction h generalizing r with
  | nil => cases Option.some.inj hs; exact hr
  | cons e rest ih =>
      simp only [replayE, List.foldlM] at hs
      cases he : stepE r e with
      | none => rw [he] at hs; cases hs
      | some r1 =>
          rw [he] at hs
          exact ih r1 (step_keeps_reqs_ordered r r1 e hr he) hs
```

## Line-by-line Lean explanation

The Genesis case is an `if`. `r.data` is a number, the count of admitted
data (Unit 01), so `j < r.data` says "the index `j` is one of the
admitted indices `0 … r.data − 1`". The `some { r with reqs := … }`
copies every other field.

`impose_self_rejected` (book): `simp [stepE]` unfolds the case and
reduces `d < d ∧ …` to `False`, so the `if` takes its `else` branch.

`impose_succeeds_iff` (book) is the guard read as a specification.
Forward: from `hs : stepE r (.impose i j) = some s`, unfold, and `split`
on the `if`. In the `then` branch the condition is a hypothesis, so
`assumption`; in the `else` branch `hs : none = some s` is impossible,
`cases hs`. Backward: name the successor explicitly and let `simp` check
the `if` with the condition `h` supplied.

`step_keeps_reqs_ordered` (book, quoted in the check file) is a case
split on the event. Five of the six cases leave `reqs` untouched; after
`Option.some.inj` identifies `s` with the successor, the old hypothesis
`hr` is the answer. In the `impose` case, `split at hs` exposes the guard
`hij : i < j ∧ j < r.data`; a `q` in the new `reqs` is either in the old
list (`hr`) or is `(i, j)` itself, where `hij.1` gives `i < j`.
`insertNew` is unfolded so that its own `if` can be split.

`replay_keeps_reqs_ordered` (book) is induction on the history. For the
empty history `s = r`. For `e :: rest`, the fold's first step is
`stepE r e`; if it is `none` the replay is `none`, contradicting `hs`;
if it is `some r1`, the one-step lemma gives the invariant at `r1` and
the induction hypothesis carries it through `rest`.

`R2L_selfIso` (book) shows the invariant doing work: `isoRefl` needs
every demand of `R2L` sorted, and the only demand is `(0, 1)`.

**Axioms.** `propext` for the Genesis definition and all the book's
proofs by `simp`/`decide` on `stepE`; `propext, Quot.sound` for the
`isoRefl` instance, which decides a concrete membership.

</details>

## What has been proved

- `impose d d` is rejected on every regime (book, derived).
- An `impose` succeeds exactly when the guard holds (book, derived).
- The invariant "every demand has `i < j`" is kept by every step and
  every replay (book, derived). From `genesis`, whose `reqs` is empty, it
  holds in every reachable regime.
- `impose 0 1` on the two-datum regime yields exactly `R2L` (book, by
  `decide`). Repeating an admissible, already recorded demand leaves the
  regime unchanged. A raw reversed pair survives a later valid `impose`,
  illustrating why the invariant's initial-state condition is needed.

## What has not been proved

- That the guard is the right one. It is a definition. A different
  constructor might allow `impose j i` and sort on insertion, or allow a
  self-demand and let it be unmeetable. Genesis chose to refuse at the
  door, and the paper records the choice as declared challenge semantics
  (§3, definition 7).
- Anything about *meeting* a demand. The guard admits the demand; Units
  16 and 18 to 22 are about satisfying it.
- An irreflexivity law for every admitted binary form. Instances may
  repeat an index: Unit 20's self-loop is permitted. The guard concerns
  requests; the separate relation laws of Units 23–26 concern their
  supplied relation models. Neither should be read into every form here.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `i < j`, `j < r.data` | the guard | the metatheory's order on `Nat` indices |
| `insertNew` | deduplicated insertion | metatheory list function (Unit 06) |
| `impose` as an event | the caller's request | admitted; the caller is outside (Unit 00) |
| the invariant `∀ q ∈ reqs, q.1 < q.2` | a hypothesis of `isoRefl` | derived from the guard, in the metatheory, by the book |

**What the system holds.** After an admissible `impose`, one more pair in
`reqs` if it was absent; otherwise the same record. The system has no
object-language operation for inspecting that list; the metatheory's
`separable` predicate (Unit 08) and the Python `satisfies` relate the
demand to the state.

**Phrases to read with care.**

- "Irreflexive by guard" is the book's phrase. It means the guard refuses
  `(d, d)`; it does not mean an irreflexive relation exists in the
  system.
- "Requirement out of range" (the Python message) covers three distinct
  refusals. The Lean guard makes the same three refusals with one
  condition.

## Student exercise

In reading F the data are `⟨⟩, ⟨A⟩, ⟨AB⟩` at indices 0, 1, 2. List every
pair the guard accepts, and say which of them the derivation actually
demands. Then: a history `[admitDatum, impose 0 1, admitDatum]`, from
`genesis`. Is it admissible? Why?

## Answer

<details>
<summary>Check the exercise (optional)</summary>

Accepted pairs: `(0, 1)`, `(0, 2)`, `(1, 2)`, the pairs with `i < j < 3`.
At this checkpoint the recorded demand is `(1, 2)` (`R2F.reqs`), the pair
of the two retained tokens; no request names datum 0. The
history is not admissible: after one `admitDatum` the regime has
`data = 1`, so `impose 0 1` needs `1 < 1`, which fails, and `stepE`
returns `none`; `replayE` then returns `none` for the whole history,
whatever follows. The Python check script's enumeration contains this
event pattern and classifies it as inadmissible.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Basic.lean` lines 159-162 (the guard), 145-146 (`stepE` header), 208-209 (`R2L`, `R2F`); `Minimality.lean` lines 199-221 (`isoRefl` and its `hreqs` hypothesis) |
| Axiom report | `artifacts/lean_axioms.txt`: `Derivation.stepE` and `Derivation.insertNew` `[propext]`; the guard is a definition, not a theorem |
| Paper | `paper/paper.md` §3 definition 7 (valid response; "requirements are persistent constraints — declared challenge semantics"); `model.py` docstring, `reqs: (i, j) with i < j` |
| Ledger | No `CL-*` entry is about the guard itself; `CL-3-FAIL-CURRENT` and every Challenge 3 entry presuppose the recorded demand |
| Artifact | `artifacts/challenges.json`, `challenge3.L.reading = "L"` with target `(0, 1)`; the demand itself is not an artifact field |
| Test | `tests/test_model.py` (admission errors); `tests/test_engine.py::test_challenge3_reading_l_classes` |
| Check (Python) | `python textbook/checks/u17_impose_guard.py`: one accepted demand, seven refusals; repeated demand unchanged; malformed base not repaired; 111 111 histories, 2 883 admissible, 990 recorded demands all sorted; reading F accepts `(1, 2)` where reading L refuses it |
| Check (book Lean) | `python textbook/checks/u17_lean.py`: eleven book reports plus `stepE` and `insertNew` kernel-checked, Lean 4.33.0; `propext` for the guard/invariant proofs and `self_not_separable`, both listed axioms for `R2L_selfIso` |
