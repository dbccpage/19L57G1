# Unit 08. Determination is not truth

**Claim.** Determining an answer does not establish agreement with a target.
Target membership and agreement are separate hypotheses. Repeated
partitions do not supply a statistical independence model.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Having classes of information is not knowing a given claim; knowing a
claim is functional determination, not agreement with a target; on any nonempty
carrier every institution knows two claims that disagree everywhere; whether a
known claim agrees with a target is itself a further question that the
institution need not know. If the target is a member and the claim
already agrees with it, the claim is known. If the target is a member
and the claim is known, their agreement question is known. Neither
statement makes an arbitrary claim agree with the target.

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
   (`truth_is_a_further_question`). Target membership plus agreement makes
   q known; target membership plus knowledge of q makes `agreeQ q t` known.
   Neither conclusion creates agreement. Target membership is sufficient
   under those premises, not necessary in every agreement example.
4. **Report count is not partition count (multi-level correlated
   blind spots):** three subordinate actors $p_1, p_2, p_3$ that share the same
   observational blind spot can submit three unanimous reports (even in
   distinct surface encodings and through intermediate regional supervisors),
   raising the **report count** to $3$ while keeping the **signature-class
   count** (`information D Q`) frozen at the single-actor level and leaving
   the aggregated verdict wrong (`Agreement ≠ Correctness`, `Determination ≠ Truth`).

</details>

## First pass

With no reporting tables, inputs 0 and 1 have the same empty
signature. Constant answers [0,0] and [1,1] are both recoverable.
They cannot both agree with one fixed target at both inputs.

Take the target [0,1] and the answer [0,0]. Their agreement table is
[1,0]: 1 for agreement, 0 for disagreement. The empty family determines
the constant answer, but cannot determine this agreement table.

Admit the target table. Both the answer and target can now be read, so
their agreement table is recoverable. Its second entry remains 0.
More access makes the mismatch visible; it does not repair the answer.

**Predict:** does admitting a target make every authorized answer true?

<details><summary>Check your prediction</summary>

No. The theorem derives knowledge of an already-matching answer from
target membership and agreement. It does not derive agreement from
membership. Even the target's correspondence with reality requires
separate evidence outside this model of tables.

</details>

For a separate worked model of formula evaluation and panel reports, see
[Reasoning 56–61](../../reasoning_lab/56_a_claim_needs_an_interpretation.md).
That optional X301 route uses its own definitions; it is not a proved
translation of this institution model.

## What you need first

Use I02’s recovery rule and I03’s class count. This unit adds a separately supplied target and a rule comparing the report with it.

<details>
<summary>Prerequisite source names (optional)</summary>

Unit 00 (`SigEq`), Unit 02 (`Knows`, `knows_iff_determined`, `knows_const`,
`knows_member`), and Unit 03 (`information`).

</details>

### 1. Agreement on the carrier and its indicator question

Keep three questions separate. Can the family's labels recover the
report? Does the report match the supplied target at this input? Does
it match at every input on the carrier?

For report `[0,0]` and target `[0,1]`, the pointwise answers form `[1,0]`.
Knowing that agreement table means recovering its entries correctly,
including its 0. It does not mean every entry is 1. The whole-carrier
comparison returns false because one entry disagrees.

<details>
<summary>Lean source: Corr, corrB, corr_iff_corrB, agreeQ, corr_iff_agreeQ (optional)</summary>

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

</details>

`Corr D q t` says `q` and `t` take the same value at every datum of `D`. Its
Boolean test is `corrB D q t`, and `agreeQ q t` turns pointwise agreement into a
question `Nat → Nat` that outputs `1` where `q x = t x` and `0` where `q x ≠ t x`.

On an empty carrier, the whole-carrier condition has no entry that can
fail. That is not evidence of physical agreement. The nonempty-carrier
hypothesis below ensures an input at which constants 0 and 1 differ.

## The theorems

<details>
<summary>Lean source: information_without_determination, determination_not_truth, truth_is_a_further_question, truth_from_admitted_target, agreement_known_of_admitted (optional)</summary>

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

</details>

A family can recover both constant reports 0 and 1. On a nonempty carrier those reports cannot both agree everywhere with one fixed target. When both report and target are recoverable, equal old signatures give equal report and target values, so their agreement marks also agree. Recovering a mismatch mark does not repair the mismatch.

<details>
<summary>Detailed proof steps (optional)</summary>

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

</details>

### Worked institutional example: Correlated errors across levels of authority (`Report Count ≠ Distinct Partitions`)

This is a supplied table scenario, with no observations of an actual
organization. Keep three counts separate:

| What is counted | Count in the example |
|---|---|
| Subordinate reports | 3 |
| Different groupings made by the individual member tables | 1 |
| Groups distinguished by the combined signature | 2 |

The last row is `information`. It counts groups within the shared
grouping, not the number of different member groupings.

Consider carrier $D = [0, 1, 2, 3]$ and target table $t = \mathrm{half} = (0, 0, 1, 1)$.
Suppose three subordinate actors $p_1, p_2, p_3$ observe $D$ using distinct
codebooks that all suffer from the **same observational blind spot**: none of
them can distinguish datum $1$ from datum $2$ (each merges $\{0, 1, 2\}$ into one
fiber and places $\{3\}$ in the other):

- $p_1 = (0, 0, 0, 1)$
- $p_2 = (10, 10, 10, 11)$
- $p_3 = (20, 20, 20, 21)$

The raw values differ, so numerical unanimity cannot be read directly
from those codes. Supply decoders 0/1→0/1, 10/11→0/1 and 20/21→0/1.
All three decoded assessments are `[0,0,0,1]`. Those decoders are extra
specified rules, not meanings inferred from the numbers themselves.

Each subordinate determines the defective binary assessment
$q_{\text{err}} = (0, 0, 0, 1)$, which misclassifies datum $2$ ($q_{\text{err}}(2) = 0 \neq 1 = t(2)$).
Now trace this through two levels of institutional authority:

1. **First-level aggregation (`Q = [p_1, p_2, p_3]`):** A supervisor collects all
   three reports. The **report count** is $3$, and all three subordinates
   unanimously support $q_{\text{err}}$. Yet because $p_1, p_2, p_3$ induce the
   exact same partition $\{\{0, 1, 2\}, \{3\}\}$ on $D$, adding $p_2$ and $p_3$
   contributes **no additional signature classes**:
   $$\mathrm{information}(D, [p_1]) = \mathrm{information}(D, [p_1, p_2]) = \mathrm{information}(D, [p_1, p_2, p_3]) = 2.$$
   The institution $Q$ determines $q_{\text{err}}$ (`Knows D Q q_err`), fails to
   determine the target $t$ (`¬ Knows D Q t`), and disagrees with $t$ at datum $2$
   (`corrB D q_err t = false`).
2. **Second-level hierarchy (`Q_top = [S_A, S_B]`):** Suppose division $A$
   combines $[p_1, p_2]$ into its canonical summary $S_A = \mathrm{pQ}(D, [p_1, p_2])$
   and division $B$ combines $[p_2, p_3]$ into $S_B = \mathrm{pQ}(D, [p_2, p_3])$,
   and both divisions report up to a director $Q_{\text{top}} = [S_A, S_B]$.
   The director sees two concurring division-level assessments backed by three
   field reports, yet $\mathrm{information}(D, Q_{\text{top}}) = 2$,
   $\mathrm{Knows}(D, Q_{\text{top}}, q_{\text{err}})$ still holds, and the error at
   datum $2$ is untouched. Repetition across levels of authority increases the
   **report count** without increasing the **number of distinct represented partitions**
   (compare [I06's known-summary invariance](06_degradation_and_loss.md)
   and the concrete Python check below).

Both canonical summaries have labels `[0,0,0,3]`: 0 and 3 are the first
inputs of their two groups. Decoder 0→0, 3→1 recovers the binary assessment
from either summary. The unchanged error concerns that decoded assessment;
a representative label is not itself the target answer.

The repeated tables in this example induce the same partition.
This is not a statistical independence calculation: no sampling
distribution or reliability model is defined.

## The same fact in Python

The check verifies:

1. `information_without_determination`: on `range(4)`, `(PARITY4,)` has
   information `2` and `knows(4, (PARITY4,), HALF4)` is `False`.
2. `determination_not_truth` and `truth_is_a_further_question` on `range(3)` and
   `range(2)`.
3. On `range(3)`, each singleton family and one ordering of each distinct
   partition pair are used. Each target is selected from that family;
   all 27 report tables with values in `range(3)` are tried. These give
   675 cases: a matching report is known, and a known report's agreement
   question is known (`0` violations). Targets are not independently
   enumerated arbitrary tables. Empty families, repeated members and
   every list order are not enumerated in this loop.
4. **Three-actor correlated blind-spot and multi-level hierarchy check:** three
   actors `p1, p2, p3` on `range(4)` sharing the blind spot `p(0) == p(1) == p(2)`
   yield `report_count = 3` while `information(4, (p1,)) == information(4, (p1, p2, p3)) == 2`
   (only `1` distinct represented partition), and neither direct aggregation
   `Q = (p1, p2, p3)` nor two-tier supervisory aggregation `Q_top = (S_A, S_B)`
   eliminates the error against target `HALF4 = (0, 0, 1, 1)`.

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
target presentation `t` must be specified to formulate this comparison.
Knowing both `q` and `t` suffices to know the agreement question, but
is not necessary: with `q = t = id` on `[0,1]`, the empty family knows
the constant agreement answer 1 without knowing either identity table.
Supplying a target does not verify its correspondence with reality.

**Phrases to read with care.**

- "Knows `q`." Throughout the textbook, `Knows D Q q` is functional
  determination of `q` by `Q`'s signature on `D`. This unit puts on record that
  functional determination is not truth (`determination_not_truth`).
- "Target `t`" and "truth." The formal predicate `Corr D q t` is pointwise
  equality `∀ x ∈ D, q x = t x` between two tables on `D`. Calling `t` a
  "target" is a gloss; in Lean `q` and `t` have the same type `Nat → Nat`.

## What it shows, and what it does not

It shows that `information D Q ≥ 2` does not imply `Knows D Q q` for a given `q`
(`information_without_determination`). Knowing q does not, by itself,
establish agreement with an arbitrary separately supplied target t
(`determination_not_truth`). This does not prevent q from agreeing with
a particular target, including q itself.

It shows that pointwise agreement with `t` is a separate question `agreeQ q t`
that can be unknown even when `q` is known (`truth_is_a_further_question`), and
that admitting `t ∈ Q` makes an already-matching q known. To conclude
that the agreement question is known, the second theorem also assumes
that q is known. These are separate sufficient conditions
(`truth_from_admitted_target`, `agreement_known_of_admitted`).

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
