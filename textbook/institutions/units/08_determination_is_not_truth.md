# Unit 08. Determination is not truth

**Claim.** Having classes of information is not knowing a given claim; knowing a
claim is functional determination, not agreement with a target; on any nonempty
carrier every institution knows two claims that disagree everywhere; whether a
known claim agrees with a target is itself a further question that the
institution need not know; and admitting the target as a member suffices for
both the claim and its agreement question to be known.
**Status:** derived. **Lean:** `Chain.information_without_determination`,
`Chain.Corr`, `Chain.corrB`, `Chain.corr_iff_corrB`,
`Chain.determination_not_truth`, `Chain.agreeQ`, `Chain.corr_iff_agreeQ`,
`Chain.truth_is_a_further_question`, `Chain.truth_from_admitted_target`,
`Chain.agreement_known_of_admitted` (`actor_institution`). **Sources:**
`research/actor_institution/lean/ResearchActorInstitution/Chain.lean` lines
120–188.

Units 02 and 03 defined two notions that ordinary talk often conflates with
truth: `information D Q` (how many equivalence classes `Q` carves on `D`) and
`Knows D Q q` (whether `q` factors through `Q`'s canonical representative on
`D`). This unit separates all three:
1. Information is not determination of a chosen question: on `[0, 1, 2, 3]`,
   `[parity]` has `2` classes of information and does not know `half`.
2. Determination is not agreement with a target (`Corr D q t`): on any nonempty
   carrier, every institution knows both constant claims `fun _ => 0` and
   `fun _ => 1`, which agree at no datum of `D`.
3. Agreement with a target `t` is represented by the indicator question
   `agreeQ q t`, which the institution need not know even when it knows `q`
   (`truth_is_a_further_question`); what makes a claim that agrees with `t`
   known—and makes `agreeQ q t` known—is admitting `t` as a member of `Q`.

## What you need first

Unit 00 (`SigEq`), Unit 02 (`Knows`, `knows_iff_determined`, `knows_const`,
`knows_member`), and Unit 03 (`information`).

### 1. Agreement on the carrier and its indicator question

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Chain.lean lines 127–136, 150–161
/-- `q` agrees with the target `t` on the carrier. -/
def Corr (D : List Nat) (q t : Nat → Nat) : Prop := ∀ x, x ∈ D → q x = t x

def corrB (D : List Nat) (q t : Nat → Nat) : Bool := D.all (fun x => decide (q x = t x))

theorem corr_iff_corrB (D : List Nat) (q t : Nat → Nat) : Corr D q t ↔ corrB D q t = true := by
  unfold Corr corrB
  rw [List.all_eq_true]
  constructor
  · intro h x hx; exact decide_eq_true (h x hx)
  · intro h x hx; exact of_decide_eq_true (h x hx)

/-- The agreement of `q` with `t`, as a question on the carrier. -/
def agreeQ (q t : Nat → Nat) : Nat → Nat := fun x => if q x = t x then 1 else 0

theorem corr_iff_agreeQ (D : List Nat) (q t : Nat → Nat) :
    Corr D q t ↔ ∀ x, x ∈ D → agreeQ q t x = 1 := by
  unfold Corr agreeQ
  constructor
  · intro h x hx; rw [if_pos (h x hx)]
  · intro h x hx
    have := h x hx
    cases Nat.decEq (q x) (t x) with
    | isTrue e => exact e
    | isFalse ne => rw [if_neg ne] at this; exact absurd this (by decide)
```

`Corr D q t` says `q` and `t` take the same value at every datum of `D`. Its
Boolean test is `corrB D q t`, and `agreeQ q t` turns pointwise agreement into a
question `Nat → Nat` that outputs `1` where `q x = t x` and `0` where `q x ≠ t x`.

## The theorems

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Chain.lean lines 120–122, 141–147, 166–187
/-- Information is not knowledge of a given question: `[parity]` carries
two classes on four points and does not know `half`. -/
theorem information_without_determination :
    2 ≤ information [0, 1, 2, 3] [parity] ∧ ¬ Knows [0, 1, 2, 3] [parity] half := by
  decide

/-- **Functional determination is not established truth.**  On a nonempty
carrier every institution knows two claims that agree with each other
nowhere, so knowing a claim cannot mean that it agrees with a target. -/
theorem determination_not_truth (D : List Nat) (Q : Institution) (hD : D ≠ []) :
    ∃ q t : Nat → Nat, Knows D Q q ∧ Knows D Q t ∧ ¬ Corr D q t := by
  refine ⟨fun _ => 0, fun _ => 1, knows_const D Q 0, knows_const D Q 1, ?_⟩
  intro h
  cases D with
  | nil => exact hD rfl
  | cons x _ => exact Nat.zero_ne_one (h x List.mem_cons_self)

/-- **Truth is a further question.**  The empty institution knows the
constant claim `0`; whether that claim agrees with the target `id` is a
question it does not know. -/
theorem truth_is_a_further_question :
    Knows [0, 1] [] (fun _ => 0) ∧
    ¬ Knows [0, 1] [] (agreeQ (fun _ => 0) (fun x => x)) := by
  unfold agreeQ
  decide

/-- **The price of truth.**  If the target is admitted as a member and the
claim agrees with it on the carrier, the claim is known. -/
theorem truth_from_admitted_target {D : List Nat} {Q : Institution} {q t : Nat → Nat}
    (ht : t ∈ Q) (hc : Corr D q t) : Knows D Q q := by
  rw [knows_iff_determined]
  intro x hx y hy hs
  rw [hc x hx, hc y hy]
  exact hs t ht

/-- With the target admitted, agreement with it is known too. -/
theorem agreement_known_of_admitted {D : List Nat} {Q : Institution} {q t : Nat → Nat}
    (ht : t ∈ Q) (hq : Knows D Q q) : Knows D Q (agreeQ q t) := by
  rw [knows_iff_determined] at hq ⊢
  intro x hx y hy hs
  unfold agreeQ
  rw [hq x hx y hy hs, hs t ht]
```

## The proof, step by step

**Step 1. `information_without_determination` by `decide`.**
On `[0, 1, 2, 3]`, `parity = (0, 1, 0, 1)` has two distinct signatures (`0` and
`1`), so `information [0, 1, 2, 3] [parity] = 2`. Yet `parity 0 = parity 2 = 0`
while `half 0 = 0 ≠ 1 = half 2`, so `[parity]` does not know `half`.

**Step 2. `determination_not_truth`.**
By Unit 02's `knows_const`, every institution `Q` knows `fun _ => 0` and
`fun _ => 1`. Because `D` is nonempty (`D = x :: _`), evaluating `Corr D
(fun _ => 0) (fun _ => 1)` at `x ∈ D` yields `0 = 1`, which `Nat.zero_ne_one`
refutes. Thus both constant claims are determined by `Q`, and they cannot both
agree with any single target on `D`.

**Step 3. `truth_is_a_further_question` by `decide`.**
On `[0, 1]`, the empty institution `[]` knows the constant claim `fun _ => 0`.
Against the target `fun x => x`, the agreement question `agreeQ (fun _ => 0)
(fun x => x)` takes value `1` at `0` (where `0 = 0`) and `0` at `1` (where
`0 ≠ 1`). Because `[]` merges `0` and `1`, it does not know `agreeQ (fun _ => 0)
(fun x => x)`.

**Step 4. `truth_from_admitted_target` and `agreement_known_of_admitted`.**
Assume the target `t` is admitted (`ht : t ∈ Q`).
- If `Corr D q t` holds (`q x = t x` for all `x ∈ D`), then for any `x, y ∈ D`
  with `SigEq Q x y`, `q x = t x = t y = q y` because `t ∈ Q` gives `t x = t y`.
  By `knows_iff_determined`, `Knows D Q q` (`truth_from_admitted_target`).
- If `Knows D Q q` holds, then on any `x, y ∈ D` with `SigEq Q x y`, both
  `q x = q y` (by `hq`) and `t x = t y` (by `ht : t ∈ Q`), so
  `agreeQ q t x = agreeQ q t y`. By `knows_iff_determined`,
  `Knows D Q (agreeQ q t)` (`agreement_known_of_admitted`).

## The same fact in Python

The check verifies:

1. `information_without_determination`: on `range(4)`, `(PARITY4,)` has
   information `2` and `knows(4, (PARITY4,), HALF4)` is `False`.
2. `determination_not_truth` and `truth_is_a_further_question` on `range(3)` and
   `range(2)`.
3. Exhaustively on `range(3)` over all families `Q` of at most 2 partitions, all
   presentations `q : range(3) → range(3)`, and all targets `t : range(3) →
   range(3)`: whenever `t in Q` and `q == t`, `knows(3, Q, q)` holds; and
   whenever `t in Q` and `knows(3, Q, q)` holds, `knows(3, Q, agreeQ(q, t))`
   holds (`0` violations).

```
python textbook/institutions/checks/i08_determination_not_truth.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `decide` | `information_without_determination`, `corr_iff_agreeQ`, `truth_is_a_further_question` | kernel evaluation on `[0, 1, 2, 3]` and `[0, 1]` |
| `Nat.decEq` | `corr_iff_agreeQ` | decidable equality on natural numbers `q x` and `t x` |
| `List.all` | `corrB`, `corr_iff_corrB` | finite conjunction over `x ∈ D` |

**What the system holds.** The finite carrier `D`, the family `Q`, the claim
table `q`, the target table `t`, and the agreement table `agreeQ q t`.

**Admissions relied on, and their price.** Unit 00's three admissions, plus an
explicit fourth whenever agreement with a target is invoked (`AI-09`): the
target presentation `t` must be supplied, and for the institution to know that a
claim agrees with `t`, `t` (or a family that already determines `t`) must be
admitted into `Q`.

**Phrases to read with care.**

- "Knows `q`." Throughout the textbook, `Knows D Q q` is functional
  determination of `q` by `Q`'s signature on `D`. This unit puts on record that
  functional determination is not truth (`determination_not_truth`).
- "Target `t`" and "truth." The formal predicate `Corr D q t` is pointwise
  equality `∀ x ∈ D, q x = t x` between two tables on `D`. Calling `t` a
  "target" is a gloss; in Lean `q` and `t` have the same type `Nat → Nat`.

## What it shows, and what it does not

It shows that `information D Q ≥ 2` does not imply `Knows D Q q` for a given `q`
(`information_without_determination`), and that `Knows D Q q` does not imply
`Corr D q t` for any external target `t` (`determination_not_truth`).

It shows that pointwise agreement with `t` is a separate question `agreeQ q t`
that can be unknown even when `q` is known (`truth_is_a_further_question`), and
that admitting `t ∈ Q` suffices to make both a matching claim `q` and the
agreement question `agreeQ q t` known (`truth_from_admitted_target`,
`agreement_known_of_admitted`).

It does not provide any internal test by which an institution `Q` could check
whether `t` is the "right" target to admit without already holding `t`.

## Sources

| Item | Where |
|---|---|
| `information_without_determination` | `research/actor_institution/lean/ResearchActorInstitution/Chain.lean` lines 120–122 |
| `Corr`, `corrB`, `corr_iff_corrB`, `determination_not_truth` | the same file, lines 127–147 |
| `agreeQ`, `corr_iff_agreeQ`, `truth_is_a_further_question`, `truth_from_admitted_target`, `agreement_known_of_admitted` | the same file, lines 150–187 |
| Python mirror | `research/actor_institution/model.py` line 465 (`information_without_determination`) |
| Check | `textbook/institutions/checks/i08_determination_not_truth.py` |
| Ledger | `research/actor_institution/CLAIMS.md` AI-08, AI-09 |
