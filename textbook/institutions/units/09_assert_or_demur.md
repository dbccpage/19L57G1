# Unit 09. Assert or demur, and the demurred claim

**Claim.** A residual pair agrees under the family but disagrees under the
requested report. The policy demurs with such witnesses. A separator
can remove one residual pair while other residuals remain.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** While the decidable disjunction `Wise` ("knows the claim or has a
witness pair") holds of every institution on a represented carrier and so does
not distinguish any institution from any other, a report `s` is `Grounded`
(`Knows D Q s`) exactly when it makes no distinction `Q` cannot make, which is
equivalent to its residual list `residuals D Q s` being empty. The response
policy `respond D Q s` asserts when `s` is known and otherwise demurs with
`residuals D Q s`, which is nonempty, shrinks as `Q` grows. Any chosen residual pair can be removed by
admitting a member that separates it (`residual_answerable`), while
other residual pairs may remain. A function of the current signatures
cannot separate that chosen pair (`evidence_is_not_a_digest`).
Moreover, the modified claim `demurred D Q s`—which reports `s x + 1` where `x`
is settled and `0` where `x` is unsettled—is always known (`demurred_known`)
and is total on `D` iff `s` itself is known (`demurred_total_iff`).

**Status:** derived (`Wise` refuted as a reading of wisdom; wisdom itself
open). **Lean:** `Policy.Response`, `Policy.respond`,
`Policy.respond_assert_iff`, `Policy.respond_demur_iff`,
`Policy.demur_carries_witness`, `Policy.residual_answerable`,
`Policy.evidence_is_not_a_digest`, `Policy.settledB`, `Policy.settledB_iff`,
`Policy.demurred`, `Policy.demurred_zero_iff`, `Policy.demurred_settled`,
`Policy.demurred_known`, `Policy.demurred_total_iff` (`actor_institution`);
`Institution.Wise`, `Institution.wise_of_represented`, `Reading.residuals`,
`Reading.mem_residuals`, `Reading.residuals_nil_iff`,
`Reading.residuals_antitone`, `Reading.residual_removed_iff`,
`Reading.Grounded`, `Reading.grounded_iff_no_overclaim`,
`Reading.ungrounded_iff_witness`, `Reading.silence_grounded`,
`Reading.self_report_grounded`, `Reading.member_report_grounded`,
`Reading.knows_iff_knowsB`, `Reading.grounded_or_demur` (`two_theorems`).
**Sources:**
`research/actor_institution/lean/ResearchActorInstitution/Policy.lean` lines
50–205; `research/two_theorems/lean/ResearchTwoTheorems/Institution.lean` lines
500–508; `research/two_theorems/lean/ResearchTwoTheorems/Reading.lean` lines
184–243, 356–453.

Unit 03 proved `know_or_witness`: for every institution `Q` on `D` and every
claim `q`, either `Knows D Q q` holds or some pair `x, y ∈ D` has `SigEq Q x y`
and `q x ≠ q y`. In `two_theorems`, that all-question disjunction was tested as a
candidate formalization of "wisdom" (`Wise D Q`), and immediately shown to hold
of every `(D, Q)` (`wise_of_represented`). Because a predicate that holds of
every institution separates nothing, `Wise` was retired as a candidate reading
of wisdom (`TT-15`, `TT-34`). What *does* separate claims for a fixed `(D, Q)`
is whether a proposed report `s` is determined by `Q` (`Grounded D Q s`), or has
a nonempty list of unresolved pairs (`residuals D Q s`). This unit builds the
explicit policy `respond D Q s` and the total grounded fallback `demurred D Q s`
on top of that distinction.

</details>

## First pass

On inputs 0,1,2,3, the held table [0,1,0,1] groups {0,2} and
{1,3}. Request the report [0,0,1,1]. It splits both of those groups.
Pairs 0/2 and 1/3 witness why the report is not recoverable. They are
called residual pairs.

The policy can return demur together with these witnesses. Add a new
table saying 1 only on input 0. It separates 0 from 2, removing that
residual. Inputs 1 and 3 still agree under the held tables and disagree
under the report, so their residual remains.

**Predict:** could a new calculation using only the old signatures
separate 1 from 3?

<details><summary>Check your prediction</summary>

No. Those old signatures are equal. A function of them must return
equal results. Removing this residual needs a genuinely separating
input to the model, not a different name for the same old answers.

</details>

## What you need first

Unit 01 (`pQ`), Unit 02 (`Knows`, `knows_iff_determined`, `knows_const`,
`knows_member`, `knows_actor`, `knows_mono`, `knows_iff_sigList`), and Unit 03
(`sigList`, `sigEq_iff_sigList`, `knowsB`, `not_knows_iff_witness`,
`know_or_witness`).

### 1. Why `Wise` separates no institutions, and what `Grounded` names

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Institution.lean lines 501–508
def Wise (D : List Nat) (Q : Institution) : Prop :=
  ∀ q : Nat → Nat,
    Knows D Q q ∨ ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ SigEq Q x y ∧ q x ≠ q y

theorem wise_of_represented (D : List Nat) (Q : Institution) : Wise D Q :=
  fun q => know_or_witness D Q q
```

`wise_of_represented` is a one-line application of Unit 03's `know_or_witness`.
Because `knowsB D Q q` decides `Knows D Q q` in the metatheory for every finite
`D` and `Q`, `Wise D Q` is a tautology of finite decidability rather than a
property of `Q`.

By contrast, when `s : Nat → Nat` is read as a report issued by `Q`,
`Grounded D Q s` asks whether `Q` knows `s`:

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Reading.lean lines 356–393, 411–412
def Grounded (D : List Nat) (Q : Institution) (s : Nat → Nat) : Prop :=
  Knows D Q s

theorem grounded_iff_no_overclaim (D : List Nat) (Q : Institution)
    (s : Nat → Nat) :
    Grounded D Q s ↔
      ∀ x, x ∈ D → ∀ y, y ∈ D → s x ≠ s y → ¬ SigEq Q x y := by ...

theorem silence_grounded (D : List Nat) (Q : Institution) (c : Nat) :
    Grounded D Q (fun _ => c) := knows_const D Q c

theorem self_report_grounded (D : List Nat) (Q : Institution) :
    Grounded D Q (pQ D Q) := knows_actor D Q

theorem member_report_grounded {D : List Nat} {Q : Institution} {p : Nat → Nat}
    (hp : p ∈ Q) : Grounded D Q p := knows_member hp

theorem knows_iff_knowsB (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows D Q q ↔ knowsB D Q q = true := by ...
```

A constant report (`silence_grounded`), the canonical representative
(`self_report_grounded`), and any member (`member_report_grounded`) are always
grounded; overclaiming on a merged pair is not (`grounded_iff_no_overclaim`).

### 2. The residual list `residuals D Q q`

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Reading.lean lines 184–243
def residuals (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    List (Nat × Nat) :=
  (pairs D D).filter (fun xy =>
    decide (sigList Q xy.1 = sigList Q xy.2) && decide (q xy.1 ≠ q xy.2))

theorem mem_residuals (D : List Nat) (Q : Institution) (q : Nat → Nat)
    (x y : Nat) :
    (x, y) ∈ residuals D Q q ↔ x ∈ D ∧ y ∈ D ∧ SigEq Q x y ∧ q x ≠ q y := by ...

theorem residuals_nil_iff (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    residuals D Q q = [] ↔ Knows D Q q := by ...

theorem residuals_antitone {D : List Nat} {Q Q' : Institution}
    (hsub : ∀ p, p ∈ Q → p ∈ Q') (q : Nat → Nat) :
    ∀ xy, xy ∈ residuals D Q' q → xy ∈ residuals D Q q := by ...

theorem residual_removed_iff {D : List Nat} {Q Q' : Institution}
    {q : Nat → Nat} {x y : Nat} (h : (x, y) ∈ residuals D Q q) :
    (x, y) ∉ residuals D Q' q ↔ ¬ SigEq Q' x y := by ...
```

`residuals D Q q` collects every pair `(x, y)` in `D × D` that `Q` merges and
`q` splits. It is `[]` iff `Knows D Q q` (`residuals_nil_iff`), shrinks when `Q`
is extended (`residuals_antitone`), and drops a pair `(x, y)` in an extension
`Q'` iff `Q'` splits `x` and `y` (`residual_removed_iff`).

## The theorems

First, the response policy `respond D Q s` and what removes a residual:

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Policy.lean lines 50–128
inductive Response where
  | assert
  | demur (residual : List (Nat × Nat))
  deriving DecidableEq, Repr

def respond (D : List Nat) (Q : Institution) (s : Nat → Nat) : Response :=
  if knowsB D Q s then .assert else .demur (residuals D Q s)

theorem respond_assert_iff (D : List Nat) (Q : Institution) (s : Nat → Nat) :
    respond D Q s = .assert ↔ Knows D Q s := by ...

theorem respond_demur_iff (D : List Nat) (Q : Institution) (s : Nat → Nat) :
    respond D Q s = .demur (residuals D Q s) ↔ ¬ Knows D Q s := by ...

theorem demur_carries_witness {D : List Nat} {Q : Institution} {s : Nat → Nat}
    {R : List (Nat × Nat)} (h : respond D Q s = .demur R) :
    ∃ x y, (x, y) ∈ R ∧ x ∈ D ∧ y ∈ D ∧ SigEq Q x y ∧ s x ≠ s y := by ...

theorem residual_answerable {D : List Nat} {Q : Institution} {s : Nat → Nat} {x y : Nat}
    (h : (x, y) ∈ residuals D Q s) :
    (x, y) ∉ residuals D (Q ++ [fun z => if z = x then 1 else 0]) s := by ...

theorem evidence_is_not_a_digest {D : List Nat} {Q : Institution} {s : Nat → Nat}
    {x y : Nat} (h : (x, y) ∈ residuals D Q s) (p : Nat → Nat) (hp : p x ≠ p y) :
    ¬ ∃ f : List Nat → Nat, ∀ z, p z = f (sigList Q z) := by
  rintro ⟨f, hf⟩
  obtain ⟨_, _, hs, _⟩ := (mem_residuals D Q s x y).mp h
  apply hp
  rw [hf x, hf y, (sigEq_iff_sigList Q x y).mp hs]
```

Second, the demurred claim `demurred D Q s`:

```lean
-- Lean (research), the same file, lines 134–205
def settledB (D : List Nat) (Q : Institution) (s : Nat → Nat) (x : Nat) : Bool :=
  D.all (fun y => decide (sigList Q x = sigList Q y → s x = s y))

theorem settledB_iff (D : List Nat) (Q : Institution) (s : Nat → Nat) (x : Nat) :
    settledB D Q s x = true ↔ ∀ y, y ∈ D → sigList Q x = sigList Q y → s x = s y := by ...

def demurred (D : List Nat) (Q : Institution) (s : Nat → Nat) : Nat → Nat :=
  fun x => if settledB D Q s x then s x + 1 else 0

theorem demurred_zero_iff (D : List Nat) (Q : Institution) (s : Nat → Nat) (x : Nat) :
    demurred D Q s x = 0 ↔ settledB D Q s x = false := by ...

theorem demurred_settled (D : List Nat) (Q : Institution) (s : Nat → Nat) (x : Nat)
    (h : settledB D Q s x = true) : demurred D Q s x = s x + 1 := by
  unfold demurred; rw [h, if_pos rfl]

theorem demurred_known (D : List Nat) (Q : Institution) (s : Nat → Nat) :
    Knows D Q (demurred D Q s) := by ...

theorem demurred_total_iff (D : List Nat) (Q : Institution) (s : Nat → Nat) :
    (∀ x, x ∈ D → settledB D Q s x = true) ↔ Knows D Q s := by ...
```

```python
# Python (research), research/actor_institution/model.py lines 417–423
def settled(n: int, Q: Institution, s: Presentation, x: int) -> bool:
    return all(sig(Q, x) != sig(Q, y) or s[x] == s[y] for y in range(n))


def demurred(n: int, Q: Institution, s: Presentation) -> Presentation:
    """`Policy.demurred`: the claim with its unsettled points marked 0."""
    return tuple(s[x] + 1 if settled(n, Q, s, x) else 0 for x in range(n))
```

## The proof, step by step

**Step 1. `respond_assert_iff`, `respond_demur_iff`, and `demur_carries_witness`.**
By `knows_iff_knowsB`, `knowsB D Q s = true` iff `Knows D Q s`. Case-splitting
on `knowsB D Q s` gives `respond D Q s = .assert` when `true` and
`.demur (residuals D Q s)` when `false`. In the `false` branch,
`not_knows_iff_witness` produces a pair `x, y ∈ D` with `SigEq Q x y` and
`s x ≠ s y`, which by `mem_residuals` belongs to `residuals D Q s`
(`demur_carries_witness`).

**Step 2. `residual_answerable` and `evidence_is_not_a_digest`.**
If `(x, y) ∈ residuals D Q s`, then `s x ≠ s y`, so `y ≠ x`. Admitting the
indicator `fun z => if z = x then 1 else 0` gives `1` at `x` and `0` at `y`,
so the extended family no longer merges `(x, y)` and `residual_removed_iff`
shows `(x, y)` leaves the residual list (`residual_answerable`). Conversely, if
`p x ≠ p y`, no function `f : List Nat → Nat` can satisfy `p z = f (sigList Q z)`
for all `z`, because `sigList Q x = sigList Q y` would force `p x = p y`
(`evidence_is_not_a_digest`).

**Step 3. `demurred_known` and `demurred_total_iff`.**
A datum `x` has `settledB D Q s x = true` iff `s` is constant across `x`'s
`Q`-signature class (`settledB_iff`). Therefore, if `x, y ∈ D` have the same
`Q`-signature (`sigList Q x = sigList Q y`), `settledB D Q s x` and
`settledB D Q s y` have the same truth value (`hsx`, `hsy`). If both are `true`,
then `s x = s y` by `settledB_iff`, so `demurred D Q s x = s x + 1 = s y + 1 =
demurred D Q s y`. If both are `false`, both values are `0`. By
`knows_iff_determined`, `Knows D Q (demurred D Q s)` (`demurred_known`). Finally,
every `x ∈ D` is settled for `s` iff `s` is constant on every `Q`-signature
class on `D`, which is `Knows D Q s` (`demurred_total_iff`).

## The same fact in Python

The check runs:

1. `demurred_check(3)` from `actor_institution/model.py`: across all `160`
   `(Q, s)` pairs of families of partitions of `range(3)` and partition claims
   `s`, `knows(3, Q, demurred(3, Q, s))` holds (`0` violations) and `demurred`
   is nonzero everywhere iff `knows(3, Q, s)` holds (`0` violations).
2. `residual_checks` and `grounding_checks` from `two_theorems/model.py`:
   `residuals(D, Q, q) == []` matches `knows(D, Q, q)` (`0` violations),
   extending `Q` shrinks `residuals` (`0` violations), and silence, `pQ`, and
   every member are grounded (`0` violations).

```
python textbook/institutions/checks/i09_assert_or_demur.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `knowsB`, `settledB` | `respond`, `demurred` | finite list computations (`List.all`, `decide`) over the carrier `D` |
| `s x + 1` and `0` | `demurred` | shifting values of `s` by `1` in `Nat` so `0` serves as an unambiguous demurral mark (`Nat.succ_ne_zero`) |
| `fun z => if z = x then 1 else 0` | `residual_answerable` | metatheory indicator function separating `x` from `y` |

**What the system holds.** The carrier `D`, the family `Q`, the proposed claim
`s`, the residual list `residuals D Q s : List (Nat × Nat)`, and the shifted
table `demurred D Q s`.

**Admissions relied on, and their price.** Unit 00's three admissions. The
policy `respond D Q s` and the fallback `demurred D Q s` are defined in the
metatheory from `D`, `Q`, and `s`; whether an institution adopts that policy is
a choice of policy (`AI-10`), while the properties of `respond` and `demurred`
once defined are derived theorems.

**Phrases to read with care.**

- "`Wise` holds of every institution." In `two_theorems` (`TT-15`, `TT-34`),
  `Wise D Q` was defined as `∀ q, Knows D Q q ∨ ∃ x y, ...`. Because `Knows` is
  decidable on a finite carrier, `wise_of_represented` shows `Wise D Q` is
  always true. That refutes `Wise` as a useful reading of wisdom; it does not
  settle what wisdom is (which remains OPEN in `TT-34`).
- "Grounded." `Grounded D Q s` is `Knows D Q s`: the report `s` does not split
  any pair that `Q` merges. As Unit 08 showed, a grounded report need not agree
  with an external target.

## What it shows, and what it does not

It shows why `Wise` is trivial on every represented carrier
(`wise_of_represented`), and why `Grounded` (`Knows D Q s`) and `residuals D Q s`
provide the non-trivial distinction between claims that `Q`'s partition
supports and claims that overclaim on merged pairs.

It shows that `respond D Q s` asserts iff `Knows D Q s` and demurs with a
nonempty list of witness pairs iff `¬ Knows D Q s`; that every residual pair can
be removed by a new separating member (`residual_answerable`) and never by a
digest of existing signatures (`evidence_is_not_a_digest`); and that
`demurred D Q s` is always known by `Q` (`demurred_known`).

It does not provide a formal definition of wisdom (`TT-34` remains open), and it
does not tell an institution which new observation to make beyond naming the
merged pairs `(x, y) ∈ residuals D Q s`.

## Sources

| Item | Where |
|---|---|
| `Wise`, `wise_of_represented` | `research/two_theorems/lean/ResearchTwoTheorems/Institution.lean` lines 500–508 |
| `residuals`, `mem_residuals`, `residuals_nil_iff`, `residuals_antitone`, `residual_removed_iff` | `research/two_theorems/lean/ResearchTwoTheorems/Reading.lean` lines 184–243 |
| `Grounded`, `grounded_iff_no_overclaim`, `ungrounded_iff_witness`, `silence_grounded`, `self_report_grounded`, `member_report_grounded`, `grounded_mono`, `grounded_antitone_carrier`, `knows_iff_knowsB`, `groundedB`, `grounded_or_demur` | the same file, lines 356–453 |
| `Response`, `respond`, `respond_assert_iff`, `respond_demur_iff`, `demur_carries_witness`, `residual_answerable`, `evidence_is_not_a_digest` | `research/actor_institution/lean/ResearchActorInstitution/Policy.lean` lines 50–128 |
| `settledB`, `settledB_iff`, `demurred`, `demurred_zero_iff`, `demurred_settled`, `demurred_known`, `demurred_total_iff` | the same file, lines 134–205 |
| Python mirrors | `research/actor_institution/model.py` lines 150–151, 417–440 (`residuals`, `settled`, `demurred`, `demurred_check`); `research/two_theorems/model.py` lines 772–792, 834–859 (`residual_checks`, `grounding_checks`) |
| Check | `textbook/institutions/checks/i09_assert_or_demur.py` |
| Ledger | `research/actor_institution/CLAIMS.md` AI-10, AI-11, AI-12, AI-12c; `research/two_theorems/CLAIMS.md` TT-15, TT-28, TT-31, TT-34 |
