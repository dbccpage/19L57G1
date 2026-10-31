# Unit 11. Same and apart outcomes

**Claim.** The declared pair policy supports apartness when a member
separates the pair, and otherwise leaves it unresolved. Its treatment
of same is a policy definition, not a theorem that literal identity
cannot be proved.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Against an institution `Q`, a pair claim `.same x y` is either
`.refuted` (when some member of `Q` separates `x` and `y`) or `.unresolved`
(when `SigEq Q x y`), and is never `.supported`; a pair claim `.apart x y` is
either `.supported` (when some member separates `x` and `y`) or `.unresolved`,
and is never `.refuted`. Both `.supported` for `.apart x y` and `.refuted` for
`.same x y` persist under every extension of `Q`; for any two distinct data
`x ≠ y`, every institution has an extension that refutes `.same x y`
(`same_never_established`), so `SigEq Q' x y` holds across all extensions `Q'`
of `Q` iff `x = y` (`established_iff_eq`); and the institution-scoped identity
test `sameRel Q x y` is relative to `Q` (`scoped_identity_not_absolute`).

**Status:** derived. **Lean:** `Policy.PairClaim`, `Policy.Outcome`,
`Policy.separatesB`, `Policy.separatesB_iff`, `Policy.outcome`,
`Policy.same_refuted_iff`, `Policy.same_unresolved_iff`,
`Policy.same_never_supported`, `Policy.apart_supported_iff`,
`Policy.apart_never_refuted`, `Policy.apart_persists`,
`Policy.same_refuted_persists`, `Policy.same_never_established`,
`Policy.established_iff_eq`, `Policy.sameRel`, `Policy.sameRel_iff`,
`Policy.scoped_identity_not_absolute` (`actor_institution`). **Sources:**
`research/actor_institution/lean/ResearchActorInstitution/Policy.lean` lines
255–393.

Units 09 and 10 studied claims of the form `s : Nat → Nat` over the whole
carrier. The most basic relational question about two data `x` and `y` asks
whether they are the same (`PairClaim.same x y`) or apart
(`PairClaim.apart x y`). Because a family `Q` is a finite list of presentations
and can always be extended by further presentations, "same" and "apart" behave
asymmetrically under `Q`: one member `p ∈ Q` with `p x ≠ p y` suffices to
support `.apart x y` and refute `.same x y` across all extensions of `Q`,
whereas every member of `Q` agreeing (`SigEq Q x y`) leaves `.same x y`
`.unresolved`, because whenever `x ≠ y` an extension of `Q` can still split
them.

</details>

## First pass

Ask whether inputs A and B are apart. If a held table gives them
different values, the policy returns supported. Ask whether they are
the same, and that very separation makes the policy return refuted.

If every held table agrees on A and B, the policy returns unresolved
for either question. It does not promote agreement under current tests
to absolute identity.

Even the claim same A A is never given the label supported by this
particular function. Literal equality A = A still has its ordinary
mathematical proof. The label records this policy's branch, not a
limitation of logic.

**Predict:** can adding a new separating table turn an unresolved pair
into supported apartness?

<details><summary>Check your prediction</summary>

Yes. Under extensions that retain old members, an existing separating
member remains present, so the supported-apart outcome then persists.
Replacing or deleting members is a different operation.

</details>

## What you need first

Unit 00 (`SigEq`), Unit 03 (`sigList`, `sigEq_iff_sigList`), Unit 04
(`exists_separator_of_not_sigEq`), and Unit 07 (`Extends`).

### 1. Pair claims, outcomes, and the separator test

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Policy.lean lines 255–283
inductive PairClaim where
  | same (x y : Nat)
  | apart (x y : Nat)
  deriving DecidableEq, Repr

inductive Outcome where
  | supported
  | refuted
  | unresolved
  deriving DecidableEq, Repr

/-- Some member tells `x` and `y` apart. -/
def separatesB (Q : Institution) (x y : Nat) : Bool := Q.any (fun p => decide (p x ≠ p y))

theorem separatesB_iff (Q : Institution) (x y : Nat) :
    separatesB Q x y = true ↔ ¬ SigEq Q x y := by
  unfold separatesB
  rw [List.any_eq_true]
  constructor
  · rintro ⟨p, hp, hd⟩ hs
    exact (of_decide_eq_true hd) (hs p hp)
  · intro hs
    obtain ⟨p, hp, hne⟩ := exists_separator_of_not_sigEq Q x y hs
    exact ⟨p, hp, decide_eq_true hne⟩

/-- The outcome of a pair claim against an institution's evidence. -/
def outcome (Q : Institution) : PairClaim → Outcome
  | .same x y => if separatesB Q x y then .refuted else .unresolved
  | .apart x y => if separatesB Q x y then .supported else .unresolved
```

`separatesB Q x y` walks `Q` and returns `true` iff some member `p ∈ Q` gives
`p x ≠ p y`. By Unit 04's `exists_separator_of_not_sigEq`, that holds iff
`¬ SigEq Q x y` (`separatesB_iff`). `outcome Q` maps `.same x y` to `.refuted`
or `.unresolved`, and `.apart x y` to `.supported` or `.unresolved`.

```python
# Python (research), research/actor_institution/model.py lines 375–385
def separates(Q: Institution, x: int, y: int) -> bool:
    return any(p[x] != p[y] for p in Q)


def outcome(Q: Institution, kind: str, x: int, y: int) -> str:
    """`Policy.outcome` on `same x y` and `apart x y`."""
    if kind == "same":
        return "refuted" if separates(Q, x, y) else "unresolved"
    if kind == "apart":
        return "supported" if separates(Q, x, y) else "unresolved"
    raise ValueError(kind)
```

## The theorems

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Policy.lean lines 285–393
theorem same_refuted_iff (Q : Institution) (x y : Nat) :
    outcome Q (.same x y) = .refuted ↔ ¬ SigEq Q x y := by ...

theorem same_unresolved_iff (Q : Institution) (x y : Nat) :
    outcome Q (.same x y) = .unresolved ↔ SigEq Q x y := by ...

theorem same_never_supported (Q : Institution) (x y : Nat) :
    outcome Q (.same x y) ≠ .supported := by ...

theorem apart_supported_iff (Q : Institution) (x y : Nat) :
    outcome Q (.apart x y) = .supported ↔ ¬ SigEq Q x y := by ...

theorem apart_never_refuted (Q : Institution) (x y : Nat) :
    outcome Q (.apart x y) ≠ .refuted := by ...

theorem apart_persists {Q Q' : Institution} (hext : Extends Q Q') {x y : Nat}
    (h : outcome Q (.apart x y) = .supported) : outcome Q' (.apart x y) = .supported := by
  rw [apart_supported_iff] at h ⊢
  intro hs
  exact h (fun p hp => hs p (hext p hp))

theorem same_refuted_persists {Q Q' : Institution} (hext : Extends Q Q') {x y : Nat}
    (h : outcome Q (.same x y) = .refuted) : outcome Q' (.same x y) = .refuted := by
  rw [same_refuted_iff] at h ⊢
  intro hs
  exact h (fun p hp => hs p (hext p hp))

theorem same_never_established {x y : Nat} (hxy : x ≠ y) (Q : Institution) :
    ∃ Q', Extends Q Q' ∧ outcome Q' (.same x y) = .refuted := by
  refine ⟨Q ++ [fun z => if z = x then 1 else 0], fun p hp => List.mem_append_left _ hp, ?_⟩
  rw [same_refuted_iff]
  intro hs
  have h1 : (if x = x then 1 else 0) = (if y = x then 1 else 0) :=
    hs (fun z => if z = x then 1 else 0) (List.mem_append_right _ List.mem_cons_self)
  rw [if_pos rfl, if_neg (fun e => hxy e.symm)] at h1
  exact absurd h1 (by decide)

theorem established_iff_eq (Q : Institution) (x y : Nat) :
    (∀ Q', Extends Q Q' → SigEq Q' x y) ↔ x = y := by
  constructor
  · intro h
    cases Nat.decEq x y with
    | isTrue e => exact e
    | isFalse ne =>
      exfalso
      obtain ⟨Q', hext, hr⟩ := same_never_established ne Q
      rw [same_refuted_iff] at hr
      exact hr (h Q' hext)
  · intro e Q' _ p _
    rw [e]

def sameRel (Q : Institution) (x y : Nat) : Bool := Q.all (fun p => decide (p x = p y))

theorem sameRel_iff (Q : Institution) (x y : Nat) : sameRel Q x y = true ↔ SigEq Q x y := by ...

theorem scoped_identity_not_absolute :
    sameRel [] 0 1 = true ∧ sameRel [fun z => z] 0 1 = false := by
  decide
```

## The proof, step by step

**Step 1. Outcomes of `.same` and `.apart`.**
Case-splitting on `separatesB Q x y` in the definition of `outcome` shows that
`outcome Q (.same x y)` is `.refuted` when `separatesB Q x y = true` (which is
`¬ SigEq Q x y` by `separatesB_iff`) and `.unresolved` when `false` (`SigEq Q x y`),
never `.supported` (`same_never_supported`). Symmetrically,
`outcome Q (.apart x y)` is `.supported` when `¬ SigEq Q x y` and `.unresolved`
when `SigEq Q x y`, never `.refuted` (`apart_never_refuted`).

**Step 2. Persistence under extension (`apart_persists`, `same_refuted_persists`).**
If `Extends Q Q'`, then `SigEq Q' x y` implies `SigEq Q x y` (since every member
of `Q` belongs to `Q'`). Contrapositively, `¬ SigEq Q x y` implies
`¬ SigEq Q' x y`. Rewriting with `apart_supported_iff` and `same_refuted_iff`
gives persistence of both outcomes.

**Step 3. `same_never_established` and `established_iff_eq`.**
When `x ≠ y`, appending the indicator `fun z => if z = x then 1 else 0` to `Q`
produces an extension `Q'` whose new member gives `1` at `x` and `0` at `y`, so
`outcome Q' (.same x y) = .refuted` (`same_never_established`). Therefore, if
`SigEq Q' x y` holds for *every* extension `Q'` of `Q`, `Nat.decEq x y` cannot
be `isFalse ne` and must be `x = y`; conversely, if `x = y`, `p x = p y` holds
for every `p` in every `Q'` (`established_iff_eq`).

**Step 4. `scoped_identity_not_absolute`.**
The Boolean test `sameRel Q x y` decides `SigEq Q x y` (`sameRel_iff`). On the
pair `0, 1`, `sameRel [] 0 1 = true` while `sameRel [fun z => z] 0 1 = false`.

## The same fact in Python

The check runs `outcome_check(3)` from `actor_institution/model.py` across all
subsets `Q ⊆ Q2` of the `5` partitions of `range(3)` and all pairs `x, y ∈
range(3)` (`2187` checks, `0` violations):
- `outcome(Q, "same", x, y)` is never `"supported"`, and `outcome(Q, "apart",
  x, y)` is never `"refuted"`;
- `"supported"` for `"apart"` and `"refuted"` for `"same"` persist from `Q` to
  every extension `Q2`;
- for every `x != y` and every `Q`, some extension `Q2` of pool partitions
  refutes `"same"`;
- `sameRel([], 0, 1)` is `True` and `sameRel([id], 0, 1)` is `False`.

```
python textbook/institutions/checks/i11_outcomes.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `Q.any`, `Q.all`, `decide` | `separatesB`, `sameRel` | finite list tests over the members of `Q` |
| `Nat.decEq` | `same_unresolved_iff`, `established_iff_eq` | decidable equality on natural numbers `x, y` and signature lists `sigList Q x, sigList Q y` |
| `fun z => if z = x then 1 else 0` | `same_never_established` | metatheory indicator function separating `x` from `y` |

**What the system holds.** The finite list `Q`, the pair claim
`PairClaim.same x y` or `PairClaim.apart x y`, and the three-valued `Outcome`.

**Admissions relied on, and their price.** Unit 00's three admissions, plus the
outcome mapping `outcome Q` (`AI-15`). Notice that `outcome Q (.same x y)` is
defined never to return `.supported`: this encodes the open-endedness of `Q`
under `Extends Q Q'` (`same_never_established`), where any distinct pair `x ≠ y`
can be split by a future member.

**Phrases to read with care.**

- "Same" (`sameRel Q x y` vs `x = y`). `sameRel Q x y = true` means `SigEq Q x y`
  (indistinguishable by `Q`), which is scoped to `Q`
  (`scoped_identity_not_absolute`). Only persistence of `SigEq Q' x y` across
  all extensions `Q'` matches `x = y` (`established_iff_eq`).

## What it shows, and what it does not

It shows the exact asymmetry between `.apart x y` and `.same x y` under
extensions `Extends Q Q'`: a single separating member supports `.apart x y` and
refutes `.same x y` permanently across all extensions (`apart_persists`,
`same_refuted_persists`), while for `x ≠ y` no institution `Q` can prevent an
extension from refuting `.same x y` (`same_never_established`,
`established_iff_eq`).

It does not claim that an institution in a closed finite pool of allowed
members can always split `x ≠ y` if the pool itself merges `x` and `y`;
`same_never_established` uses the indicator `fun z => if z = x then 1 else 0`
from the unrestricted presentation type `Nat → Nat`.

## Sources

| Item | Where |
|---|---|
| `PairClaim`, `Outcome`, `separatesB`, `separatesB_iff`, `outcome` | `research/actor_institution/lean/ResearchActorInstitution/Policy.lean` lines 255–283 |
| `same_refuted_iff`, `same_unresolved_iff`, `same_never_supported`, `apart_supported_iff`, `apart_never_refuted` | the same file, lines 285–335 |
| `apart_persists`, `same_refuted_persists`, `same_never_established`, `established_iff_eq` | the same file, lines 339–377 |
| `sameRel`, `sameRel_iff`, `scoped_identity_not_absolute` | the same file, lines 380–393 |
| Python mirrors | `research/actor_institution/model.py` lines 375–414 (`separates`, `outcome`, `outcome_check`) |
| Check | `textbook/institutions/checks/i11_outcomes.py` |
| Ledger | `research/actor_institution/CLAIMS.md` AI-15, AI-15c |
