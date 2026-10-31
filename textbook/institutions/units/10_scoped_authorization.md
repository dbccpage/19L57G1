# Unit 10. Scoped authorization and the five-link chain

**Claim.** A scoped-sound authorization rule permits only recoverable reports
for its supplied carrier and family. That permission does not establish
agreement with a target or implement an access-control system.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** An authorization rule `A : List Nat → Institution → (Nat → Nat) → Bool`
is `ScopedSound` when it authorizes only claims known by the institution on the
carrier. The Boolean knowledge test `knowsB` is the largest scoped-sound rule;
every scoped-sound rule refuses every claim that has a residual pair; and
`knowsB` authorizes two claims (`fun _ => 0` and `fun _ => 1`) that disagree at
every datum of any nonempty carrier, so authorization is relative to the
institution's partition rather than an external target. Moreover, a report alone
does not in general determine its own grounding independently of the
family (`reports_do_not_certify`), and a report grounded on a
carrier can fail to be grounded when a new datum is admitted
(`grounded_here_not_there`).

**Status:** derived (`ScopedSound` consequences conditional on `ScopedSound A`).
**Lean:** `Policy.Rule`, `Policy.ScopedSound`, `Policy.knowsB_scoped_sound`,
`Policy.scoped_sound_le_knowsB`, `Policy.scoped_sound_refuses_residual`,
`Policy.authorization_not_correctness` (`actor_institution`);
`Reading.reports_do_not_certify`, `Reading.grounded_here_not_there`
(`two_theorems`). **Sources:**
`research/actor_institution/lean/ResearchActorInstitution/Policy.lean` lines
211–251; `research/two_theorems/lean/ResearchTwoTheorems/Reading.lean` lines
458–469.

Unit 09 turned `Knows D Q s` (`Grounded D Q s`) into a response policy
`respond D Q s`. This unit asks what any rule `A D Q s` that authorizes claims
solely on the basis of `Q`'s evidence on `D` can and cannot certify. Calling a
rule `ScopedSound` when `A D Q s = true → Knows D Q s` makes `knowsB` the
maximal scoped-sound rule (`knowsB_scoped_sound`, `scoped_sound_le_knowsB`) and
forces `A D Q s = false` whenever `residuals D Q s` is nonempty
(`scoped_sound_refuses_residual`). At the same time, it inherits all three
boundaries of `Knows`:
1. The same nonconstant report can be grounded for one family and not
   another (`reports_do_not_certify`). Constant reports are known for
   every family, so this is not a claim that every report fails alone.
2. Authorization on `D` does not survive enlarging `D`
   (`grounded_here_not_there`).
3. Authorization does not establish agreement with a target
   (`authorization_not_correctness`).

Together with Units 03, 08, and 09, this completes the five-link chain
recorded in ledger entry `AI-22`—from information to determination, evidence,
justified claim, and scoped authorization—and explains why there is no sixth
implication to target agreement. Admitting a target alone does not supply that implication.

</details>

## First pass

A family groups all inputs together. It determines both the constant
report 0 and the constant report 1. The largest scoped-sound rule,
knowsB, authorizes both.

Against a supplied target, the reports can disagree with each other
everywhere. Authorization here means only that the report makes no
distinction unavailable in the family's signature. It does not mean
correct prediction, ethical approval, or permission to act in a real system.

A nonconstant report can be grounded for one family and ungrounded for
another. Constant reports are a useful exception: every family knows
them. The counterexample about reports alone does not say that every
report is unknowable without examining a particular family.

**Predict:** if a rule refuses every report, is it scoped-sound?

<details><summary>Check your prediction</summary>

Yes. It authorizes no unknown report, because it authorizes none at all.
Scoped soundness alone does not require useful approvals. knowsB is
largest by the set of reports it authorizes under this definition.

</details>

## What you need first

Unit 02 (`Knows`, `knows_const`), Unit 03 (`knowsB`), Unit 08 (`Corr`,
`determination_not_truth`, `truth_from_admitted_target`), and Unit 09
(`residuals`, `residuals_nil_iff`, `Grounded`, `knows_iff_knowsB`).

### 1. Reports do not certify themselves, nor ahead of the carrier

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Reading.lean lines 458–469
theorem reports_do_not_certify :
    Grounded [0, 1] [fun x => x] (fun x => x) ∧
    ¬ Grounded [0, 1] [] (fun x => x) := by
  unfold Grounded
  decide

theorem grounded_here_not_there :
    Grounded [0, 1] [fun x => x % 2] (fun x => x) ∧
    ¬ Grounded [0, 1, 2] [fun x => x % 2] (fun x => x) := by
  unfold Grounded
  decide
```

The same report `fun x => x` is grounded on `[0, 1]` for `[fun x => x]` and
ungrounded on `[0, 1]` for `[]`, so inspecting the report `s` alone cannot
decide grounding (`reports_do_not_certify`). And for `Q = [fun x => x % 2]`, the
report `fun x => x` is grounded on `[0, 1]` (where `0 % 2 ≠ 1 % 2`) and
ungrounded on `[0, 1, 2]` (where `0 % 2 = 2 % 2` while `0 ≠ 2`,
`grounded_here_not_there`).

## The theorems

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Policy.lean lines 211–251
/-- An authorization rule reads the carrier, the institution and the claim,
and returns a verdict. -/
abbrev Rule := List Nat → Institution → (Nat → Nat) → Bool

/-- A rule is sound relative to the institution's own evidence when it
authorizes only known claims. -/
def ScopedSound (A : Rule) : Prop := ∀ D Q s, A D Q s = true → Knows D Q s

theorem knowsB_scoped_sound : ScopedSound knowsB := by
  intro D Q s h
  exact (knows_iff_knowsB D Q s).mpr h

theorem scoped_sound_le_knowsB {A : Rule} (h : ScopedSound A) :
    ∀ D Q s, A D Q s = true → knowsB D Q s = true := by
  intro D Q s hA
  exact (knows_iff_knowsB D Q s).mp (h D Q s hA)

/-- **No authorization over an unresolved relevant distinction.**  A scoped
sound rule refuses every claim with a residual. -/
theorem scoped_sound_refuses_residual {A : Rule} (h : ScopedSound A)
    {D : List Nat} {Q : Institution} {s : Nat → Nat} {x y : Nat}
    (hr : (x, y) ∈ residuals D Q s) : A D Q s = false := by
  cases hA : A D Q s with
  | false => rfl
  | true =>
    exfalso
    have hk := h D Q s hA
    rw [← residuals_nil_iff] at hk
    rw [hk] at hr
    cases hr

/-- **Authorization is relative to the certificate, not to a target.**  The
knowledge test authorizes, on any nonempty carrier, two claims that agree
nowhere. -/
theorem authorization_not_correctness (D : List Nat) (Q : Institution) (hD : D ≠ []) :
    knowsB D Q (fun _ => 0) = true ∧ knowsB D Q (fun _ => 1) = true ∧
    ¬ Corr D (fun _ => 0) (fun _ => 1) := by
  refine ⟨(knows_iff_knowsB D Q _).mp (knows_const D Q 0),
    (knows_iff_knowsB D Q _).mp (knows_const D Q 1), ?_⟩
  intro h
  cases D with
  | nil => exact hD rfl
  | cons x _ => exact Nat.zero_ne_one (h x List.mem_cons_self)
```

## The proof, step by step

**Step 1. `knowsB_scoped_sound` and `scoped_sound_le_knowsB`.**
By Unit 09's `knows_iff_knowsB`, `Knows D Q s ↔ knowsB D Q s = true`. Reading
that equivalence right to left gives `ScopedSound knowsB`; reading it left to
right shows that any rule `A` satisfying `ScopedSound A` implies
`knowsB D Q s = true` whenever `A D Q s = true`.

**Step 2. `scoped_sound_refuses_residual`.**
Suppose `(x, y) ∈ residuals D Q s`. If `A D Q s = true`, then `ScopedSound A`
gives `Knows D Q s`, which by Unit 09's `residuals_nil_iff` implies
`residuals D Q s = []`, contradicting `(x, y) ∈ residuals D Q s`. Hence
`A D Q s = false`.

**Step 3. `authorization_not_correctness`.**
For any `(D, Q)`, `knows_const` gives `Knows D Q (fun _ => 0)` and
`Knows D Q (fun _ => 1)`, so `knowsB` returns `true` on both. When `D = x :: _`,
`Corr D (fun _ => 0) (fun _ => 1)` evaluates at `x` to `0 = 1`, which is false.

**Step 4. The five-link chain (`AI-22`).**
Putting Units 02, 03, 08, 09, and 10 side by side separates five distinct
relations on `(D, Q, s)` and shows why there is no sixth arrow to external
target agreement; the listed hypotheses do not establish it:

| Link | Formal object in Lean | What it says, and what it does not |
|---|---|---|
| 1. Information | `information D Q : Nat` | Number of `Q`-signature classes on `D`; `2 ≤ information [0,1,2,3] [parity]` does not imply `Knows [0,1,2,3] [parity] half` (`information_without_determination`). |
| 2. Determination | `Knows D Q s : Prop` | `s` is constant on every `Q`-signature class on `D` (`knows_iff_determined`), equivalently `information D (Q ++ [s]) = information D Q` (`knows_iff_information_eq`). |
| 3. Evidence | `residuals D Q s : List (Nat × Nat)` | The pairs in `D × D` merged by `Q` and split by `s`; empty iff `Knows D Q s` (`residuals_nil_iff`); removable only by a new separator, never by a digest (`evidence_is_not_a_digest`). |
| 4. Justified claim | `respond D Q s`, `demurred D Q s` | Policy that asserts `s` when `residuals D Q s = []` and otherwise demurs with the residual pairs, or emits the total grounded claim `demurred D Q s` (`demurred_known`). |
| 5. Authorization | `ScopedSound A` (`A D Q s = true → Knows D Q s`) | Certification relative to `(D, Q)`: refuses every claim with a residual (`scoped_sound_refuses_residual`), and is bounded above by `knowsB` (`scoped_sound_le_knowsB`). |
| (No 6th arrow) | `Corr D s t` (`∀ x ∈ D, s x = t x`) | Not implied by Links 1–5, even with a target admitted. `truth_from_admitted_target` goes the other way: target membership plus agreement implies that the claim is known. It does not infer agreement from authorization. |

## The same fact in Python

The check verifies:

1. Over all families `Q` of at most 2 partitions of `range(3)` and all claims
   `s : range(3) → range(3)`: `knows(3, Q, s)` holds iff `residuals(3, Q, s)`
   is empty (`scoped_sound_refuses_residual` for `knowsB`), and on every `Q`
   both constant claims `(0, 0, 0)` and `(1, 1, 1)` are authorized while
   disagreeing everywhere (`authorization_not_correctness`).
2. `reports_do_not_certify` and `grounded_here_not_there` from
   `two_theorems/model.py` (`grounding_checks`).

```
python textbook/institutions/checks/i10_authorization.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `Rule` (`List Nat → Institution → (Nat → Nat) → Bool`) | `ScopedSound` | higher-order type of Boolean decision rules in the metatheory |
| `decide` | `reports_do_not_certify`, `grounded_here_not_there` | kernel evaluation on `[0, 1]` and `[0, 1, 2]` |

**What the system holds.** The carrier `D`, the family `Q`, the claim `s`, and
the Boolean output of `knowsB D Q s`.

**Admissions relied on, and their price.** Unit 00's three admissions, plus the
definition `ScopedSound A` (`AI-13`). Any rule that authorizes a claim `s` when
`¬ Knows D Q s` violates `ScopedSound` and therefore authorizes across an
unresolved residual pair `(x, y) ∈ residuals D Q s`. Conversely, any rule that
respects `ScopedSound` cannot distinguish which of two known claims (`fun _ => 0`
or `fun _ => 1`) matches an un-admitted target (`AI-14`, `AI-22`).

**Phrases to read with care.**

- "Soundness" (`ScopedSound`). It means sound *with respect to `Q`'s partition
  on `D`* (`A D Q s = true → Knows D Q s`), not sound with respect to an
  external world or target (`authorization_not_correctness`).
- "Certificate." In `Policy.lean`, the institution `Q` on `D` is the certificate
  against which `knowsB D Q s` checks `s`. A report `s` without `(D, Q)` is not
  a certificate (`reports_do_not_certify`), and extending `D` can invalidate it
  (`grounded_here_not_there`).

## What it shows, and what it does not

It shows that `knowsB` is the largest rule satisfying `ScopedSound`, that every
`ScopedSound` rule refuses every claim with a residual pair, and that `knowsB`
authorizes everywhere-disagreeing constant claims on every nonempty carrier.

It shows that grounding cannot be read off the report `s` alone without `Q`
(`reports_do_not_certify`) and does not persist when `D` is enlarged
(`grounded_here_not_there`).

It does not derive which authorization rule an institution ought to adopt
 beyond conditional consequences of `ScopedSound` (`AI-13`).

## Sources

| Item | Where |
|---|---|
| `Rule`, `ScopedSound`, `knowsB_scoped_sound`, `scoped_sound_le_knowsB`, `scoped_sound_refuses_residual`, `authorization_not_correctness` | `research/actor_institution/lean/ResearchActorInstitution/Policy.lean` lines 211–251 |
| `reports_do_not_certify`, `grounded_here_not_there` | `research/two_theorems/lean/ResearchTwoTheorems/Reading.lean` lines 458–469 |
| Python mirrors | `research/two_theorems/model.py` lines 858–859 (`reports_do_not_certify`, `grounded_here_not_there` in `grounding_checks`) |
| Check | `textbook/institutions/checks/i10_authorization.py` |
| Ledger | `research/actor_institution/CLAIMS.md` AI-13, AI-14, AI-22; `research/two_theorems/CLAIMS.md` TT-32 |
