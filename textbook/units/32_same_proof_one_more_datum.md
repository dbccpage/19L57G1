# Unit 32. The same proof with one more datum

**Claim.** In reading F, the cheapest responses under `mu2` still mark one of
the two required data. Marking the extra genesis datum does not separate
that target pair. The two successful labelled marks give one result class
within reading F.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Reading F admits the opaque genesis datum `<>` before `<a>` and
`<ab>`, so Challenge 3 is imposed on the pair `(1, 2)` of a three-datum
regime `R2F`. Under `mu2`, every valid two-item response with new-form
arity sum at most 1 still yields a regime isomorphic to the unary mark on
a required datum, `U0F` (`mu2_unique_F`). The proof is Unit 22's case
tree with one new terminal case, the mark on the genesis datum `0`, and
that case is closed by the mention lemma: the mark mentions neither
required datum, so `(1, 2)` stays collapsed and the response is not valid
(`genesis_mark_not_separable`).

**Status:** derived (R5, discharged
2026-08-18). **Lean:** `Derivation.U0F`
(`lean4/Derivation/MinimalityF.lean` line 37), `U2F` (40), `swap12` (43),
`isoU2F_U0F` (47-65), `genesis_mark_not_separable` (72-81),
`mu2_unique_F` (86-195); from `Minimality.lean`: `cost1_insufficient_F`
(149-151), `deltaU0F_valid` (155-166). **Axioms:** `propext, Quot.sound`
(`cost1_insufficient_F`: `propext`). **Depends on:** the two readings of
genesis (Unit 05); `mu2_unique` and its case tree (Unit 22); the mention
lemma R3 (Unit 30); `Iso` (Unit 21).

</details>

## First pass

Reading F starts with three data. Call them Spare, A, and B, at
indices 0, 1, and 2. No form or instance has been admitted. The recorded
demand is “tell A and B apart.”

Try a response consisting of a new one-place form `marked` and one
instance of it:

| Mark placed on | Answer on A | Answer on B | Target separated? |
|---|---|---|---|
| Spare | No | No | No |
| A | Yes | No | Yes |
| B | No | Yes | Yes |

The Spare mark does distinguish Spare from A and B. It simply answers
the wrong question. “Invalid for this demand” does not mean “changes
nothing.”

Under `mu2`, count response items first, then the arities of newly
admitted forms. The two successful marks cost `(2,1)` and are the same
kind of result after exchanging A and B. No particular labelled mark is
forced. Reading L has only two data; its result is not literally
isomorphic to this three-datum result. Each reading has its own one-class
minimum.

## Question

Unit 22 proved, grammar-wide, that reading L has one `mu2` minimum up to
isomorphism. Reading F differs by one admitted datum that nothing
mentions. Does the extra datum open a new cheapest response, or change
which result class is cheapest under `mu2`? The engine's enumeration found
the same mark shape, within its bounds. Two labelled choices remain.
The paper's residual R5 asked for the proof over the whole grammar, and
the question is what, exactly, the extra datum adds to the case analysis.

## What we already possess

- `R2F = ⟨3, [], [], [], [(1, 2)]⟩`: three data, nothing else, the demand
  on `(1, 2)` (Unit 05; Basic line 209).
- `mu2_unique` for `R2L` (Unit 22): a case tree over the shapes of the two
  items, with every dead branch killed by `no_insts_no_separation` or by
  a failed guard, and the two live leaves `U0`, `U1` tied by `isoU1U0`.
- `cost1_insufficient_F`: no delta of at most one item is valid on `R2F`
  (Unit 18's general lemma instantiated).
- `deltaU0F_valid`: the mark on datum 1 is valid, so cost 2 is attained.
- R3, `collapsed_append_unmentioning` (Unit 30).
- `Iso` and the way `decide` discharges its fields on concrete regimes
  (Unit 21).

## New concept: a case that is dead for a new reason

The L proof's terminal match is on the single argument `x` of the one
instance, with `x < 2`: two cases, `U0` and `U1`. On `R2F` the bound is
`x < 3`, so a third case appears, `x = 0`: the mark on the genesis datum.
The earlier dead branches died because *no instance was created*
(`no_insts_no_separation`). This branch creates an instance, so that lemma
does not apply. It dies for a different reason: the instance mentions
datum 0 only, and the demand is on `(1, 2)`. By R3, appending an instance
that mentions neither 1 nor 2 to the instance-less base leaves `(1, 2)`
collapsed, so the result is not separable at the demand, and the validity
hypothesis is contradicted. The theorem never has to count the branch,
because validity excludes it.

The module header is explicit that nothing else changes: the L case tree
"never uses anything about `R2L` beyond three structural facts", and
`R2F` shares two of them verbatim.

## Plain-language interpretation

Give the room one more object that nobody has said anything about, and
ask again what is the cheapest way to tell `<a>` from `<ab>`. One new
candidate appears: say something about the new object instead. It is a
genuine sentence, it even distinguishes the new object from the other
two, but it does not answer the question asked, because the question was
about `<a>` and `<ab>`, and a sentence about `<>` leaves those two exactly
as indistinguishable as before. So the cheapest answers are the same two
as before, marking `<a>` or marking `<ab>`, and they are one answer up to
renaming.

## Pseudocode

```
# Gloss, the F proof
given: items a, b with [a, b] valid on R2F for (1, 2) and aritySum <= 1
open validity: a result s, applyDelta R2F [a, b] = some s, s separates (1, 2)
split on a:
  newInst, newRuleAll: no form exists yet; guard fails   [dead: no result]
  newDatum: then split on b: datum / form / rule leave no instance
                                           [dead: no_insts_no_separation]
  newForm c: 1 <= c (guard); then split on b:
    datum / form / rule: no instance                 [dead, as above]
    newInst f args: aritySum forces c = 1; guard forces f = 0, args = [x], x < 3
      x = 0: s is the genesis mark; R3 says (1, 2) collapsed; contradicts validity
      x = 1: s = U0F, isoRefl
      x = 2: s = U2F, isoU2F_U0F
```

## Python

```python
from derivation.candidates import Bounds, NewForm, NewInst, apply_delta, min_responses, response_valid_naive
from derivation.engine import GENESIS_F, delta_label
from derivation.iso import isomorphic
from derivation.model import Impose, replay
from derivation.observe import collapsed_pairs, separable

base = replay((*GENESIS_F, Impose(1, 2)))
marks = [(NewForm(1), NewInst(0, (x,))) for x in range(3)]
print([(x, response_valid_naive(base, (1, 2), d)) for x, d in enumerate(marks)])
mr = min_responses(base, (1, 2), "mu2", Bounds(2, 2))
r1, r2 = (apply_delta(base, d) for d in mr.deltas)
print(mr.cost, [delta_label(base, d) for d in mr.deltas], isomorphic(r1, r2))
gm = apply_delta(base, marks[0])
print(collapsed_pairs(gm), separable(gm, 0, 1), separable(gm, 1, 2))
```

Output:

```text
[(0, False), (1, True), (2, True)]
(2, 1) ['form1+inst1', 'form1+inst1'] True
((1, 2),) True False
```

## Line-by-line Python explanation

`GENESIS_F` admits `<>`, `<a>`, `<ab>` in that order: datum 0 is the
genesis datum. `Impose(1, 2)` records the challenge, so `base` matches
Lean's `R2F`, including its demand store. The three `marks` are the deltas
"one unary form, one instance on datum `x`". The isomorphism check below
therefore compares results carrying that demand, rather than results
whose demand stores are empty.

The first line is the case split of the proof, run: `x = 0` is not a
valid response to `(1, 2)`; `x = 1` and `x = 2` are. In reading L the
same list has two entries, both valid (the check script prints both
readings side by side).

`min_responses(..., "mu2", ...)` returns cost `(2, 1)` and two deltas,
both labelled `form1+inst1`, and `isomorphic(r1, r2)` is `True`: one
class, as in L. The artifact `challenges.json` records
`challenge3.F.mu2.minimum_cost = [2, 1]` with one class (Unit 22's
verification row).

`gm` is the genesis mark applied. Its collapsed pairs are exactly
`((1, 2),)`: the demand pair is still collapsed, which is why the delta is
invalid. But `separable(gm, 0, 1)` is `True`: the mark is not inert, it
separates the genesis datum from the others. The branch is dead because
it is aimed at the wrong pair, not because it does nothing.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/MinimalityF.lean lines 37-43, 72-81
def U0F : Regime := ⟨3, [1], [(0, [1])], [], [(1, 2)]⟩
def U2F : Regime := ⟨3, [1], [(0, [2])], [], [(1, 2)]⟩

def swap12 (d : Nat) : Nat :=
  if d = 1 then 2 else if d = 2 then 1 else d

theorem genesis_mark_not_separable :
    ¬ separable (⟨3, [1], [(0, [0])], [], [(1, 2)]⟩ : Regime) 1 2 := by
  intro hsep
  have base : collapsed (⟨3, [1], [], [], [(1, 2)]⟩ : Regime) 1 2 :=
    collapsed_of_no_insts _ rfl 1 2
  have hcol : collapsed (⟨3, [1], [(0, [0])], [], [(1, 2)]⟩ : Regime) 1 2 :=
    (collapsed_append_unmentioning ⟨3, [1], [], [], [(1, 2)]⟩
      [(0, [0])] 1 2 (by decide) (by decide)).mpr base
  exact separable_not_collapsed hsep hcol
```

```lean
-- Lean (Genesis), lean4/Derivation/MinimalityF.lean lines 86-91 and 164-195
-- (the statement and the live branch; the dead branches are as in Unit 22)
theorem mu2_unique_F (a b : Item) (hval : validResponse R2F 1 2 [a, b])
    (har : aritySum [a, b] ≤ 1) :
    ∃ s, applyDelta R2F [a, b] = some s ∧ Nonempty (Iso s U0F) := by
  cases hval with
  | intro s hs =>
    ...
          | newInst f args =>
              have hcsum : c ≤ 1 := by
                have : aritySum [Item.newForm c, Item.newInst f args] = c := by
                  simp [aritySum]
                omega
              have hc : c = 1 := by omega
              subst hc
              simp only [applyItem] at happ2
              split at happ2
              next hcond =>
                have hz := Option.some.inj happ2
                have hf : f = 0 := by
                  have := hcond.1
                  simp at this
                  omega
                subst hf
                have hargs1 : args.length = 1 := by
                  have := hcond.2.1
                  simpa using this
                match args, hargs1 with
                | [x], _ =>
                  have hx3 : x < 3 := by
                    have := hcond.2.2 x (by simp)
                    simpa using this
                  subst hz
                  match x, hx3 with
                  | 0, _ => exact absurd hsep genesis_mark_not_separable
                  | 1, _ => exact ⟨isoRefl U0F (by decide)⟩
                  | 2, _ => exact ⟨isoU2F_U0F⟩
              next => cases happ2
```

The book's Lean spells out the new case as a statement about the delta,
checks the second mark, and applies Genesis's theorem to it.

```lean
-- Lean (book), textbook/checks/u32_lean.py
def genesisMark : Regime := ⟨3, [1], [(0, [0])], [], [(1, 2)]⟩

theorem genesis_mark_separates_01 : separable genesisMark 0 1 :=
  ⟨⟨0, [none]⟩, by decide, by decide⟩

theorem genesis_mark_delta_invalid :
    ¬ validResponse R2F 1 2 [.newForm 1, .newInst 0 [0]] := by
  rintro ⟨s, hs, hsep, -⟩
  have happ : applyDelta R2F [.newForm 1, .newInst 0 [0]] = some genesisMark := by
    decide
  rw [happ] at hs
  injection hs with hs
  subst hs
  exact genesis_mark_not_separable hsep

theorem deltaU2F_valid : validResponse R2F 1 2 [.newForm 1, .newInst 0 [2]] := by
  refine ⟨U2F, by decide, ?_, ?_⟩
  · exact ⟨⟨0, [none]⟩, by decide, by decide⟩
  · intro q hq
    have : q = (1, 2) := by
      cases hq with
      | head => rfl
      | tail _ h => cases h
    rw [this]
    exact ⟨⟨0, [none]⟩, by decide, by decide⟩

theorem u2f_is_u0f_class :
    ∃ s, applyDelta R2F [.newForm 1, .newInst 0 [2]] = some s ∧ Nonempty (Iso s U0F) :=
  mu2_unique_F _ _ deltaU2F_valid (by decide)

theorem three_cases (x : Nat) (hx : x < 3) : x = 0 ∨ x = 1 ∨ x = 2 := by omega
```

## Line-by-line Lean explanation

**`U0F`, `U2F`, `swap12`.** The two marks on the required data, and the
transposition of 1 and 2 that fixes 0. `isoU2F_U0F` (lines 47-65) fills
every field of `Iso` with `decide`, exactly as `isoU1U0` did in Unit 21;
it has `swap12` as both `dmap` and `dinv` and the identity on forms.

**`genesis_mark_not_separable`.** `intro hsep`: assume the required pair
is separable in the genesis-mark regime. `base`: in the instance-less
regime with the same data and forms, `(1, 2)` is collapsed
(`collapsed_of_no_insts`, Unit 10). `hcol`: the genesis-mark regime is
that base with `[(0, [0])]` appended to `insts`; R3's two side conditions,
that no appended instance mentions 1 or 2, are decided on the one
instance; `.mpr base` carries the collapse across. `separable_not_collapsed
hsep hcol` is the contradiction (Unit 09).

**`mu2_unique_F`, the live branch.** Everything up to the final `match`
is Unit 22's argument with `R2F` in place of `R2L`: `a` must be a form
(instances and rules have no form to attach to; a datum leaves no
instance), `c = 1` by the arity budget, `b` must be an instance, `f = 0`
and `args = [x]` by the guard. The one difference is `hx3 : x < 3`, read
off the guard's datum bound, and the three-way `match` that follows. Case
`0`: `hsep` says the result separates `(1, 2)`, and the result *is* the
genesis mark (after `subst hz`), so `genesis_mark_not_separable` refutes
it. Case `1`: the result is `U0F` itself, `isoRefl`. Case `2`: `U2F`, and
the explicit isomorphism.

**The book's `genesis_mark_delta_invalid`.** Open validity, keeping the
result `s`, the application `hs` and the separability `hsep`. `happ`
computes the delta by `decide`: the result is `genesisMark`. Rewrite,
`injection` and `subst` identify `s` with it, and Genesis's lemma closes.
This is the F proof's dead branch stated on its own, as a fact about a
delta rather than a case inside a match.

**`deltaU2F_valid`, `u2f_is_u0f_class`.** The twin of `deltaU0F_valid`,
with the same shape: the result, the application decided, the witness
context for the target, and the one standing demand (which is the target)
handled by showing `q = (1, 2)`. Then Genesis's theorem, applied with the
arity bound decided, says the result is `U0F` up to isomorphism; the
isomorphism inside is `isoU2F_U0F`.

**`three_cases`.** The arithmetic fact behind the three-way `match`,
proved by `omega`. It reports `propext, Quot.sound`, because `omega`'s
normalization goes through `decide`-style reductions on `Nat`; the
proposition is elementary.

**Axioms.** `genesis_mark_not_separable` and `mu2_unique_F` report
`propext, Quot.sound`, through `decide` on concrete regimes and `simp`.
`cost1_insufficient_F` reports `propext` alone: it is the general lemma
instantiated, with no concrete decision.

## What has been proved

- Below two items nothing is valid on `R2F` (Genesis, derived).
- The mark on datum 1 is valid, so the minimum cost is exactly two
  (Genesis, derived).
- Every valid two-item response of arity sum at most 1 is `U0F` up to
  isomorphism, grammar-wide (Genesis, derived).
- The genesis mark leaves the required pair collapsed, and the
  genesis-mark delta is not a valid response (Genesis; book Lean for the
  delta form).
- The genesis mark does separate datum 0 from datum 1 (book Lean): the
  branch is dead for being off-target, not for being empty.

## What has not been proved

- That `mu2` is the right measure. Unit 22's caveat stands: uniqueness is
  measure-relative, and under `mu1` reading F has the same three-way tie
  as L (`CL-3-TIE-MU1`).
- Anything about the genesis datum beyond this: that it carries meaning,
  that it is "the empty mark", or that its admission is forced. Reading F
  is a *chosen* reading (Unit 05); this unit shows both readings have
  minimum cost `(2,1)` and one unary-mark result class within each reading
  under `mu2`. Their two- and three-datum results are not isomorphic to
  one another.
- That the two readings agree beyond Challenge 3. The engine's trees from
  `GENESIS_L` and `GENESIS_F` differ in size (Unit 28's closed baselines:
  4 nodes against 20), because the third datum opens more demands later.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `match x, hx3 with \| 0 \| 1 \| 2` | the three terminal cases | metatheory case split on a bounded `Nat` |
| `omega` | `c = 1`, `f = 0`, `x < 3` | metatheory arithmetic |
| `decide` on `Iso` fields and on `applyDelta` | the concrete regimes | metatheory; derived `DecidableEq` |
| `collapsed_append_unmentioning` | the new case | a Genesis theorem of Unit 30 |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** Three admitted data and, after the response,
one form and one instance. The genesis datum is an admitted index with
nothing said about it; whether it is "opaque" or "empty" is the paper's
gloss, not a property the regime records.

**Phrases to read with care.**

- "The genesis datum is inert" is too strong: a mark on it separates it
  from the others (`genesis_mark_separates_01`). It is inert *for the
  demand on `(1, 2)`*.
- "Reading F reduces to reading L" is what the module header says of the
  *proof*, with the one exception named. The regimes are different, and
  later rounds differ.

## Student exercise

The L proof's `match` on `x` has two cases and the F proof's has three.
Suppose a fourth datum were admitted before `<a>` (a "reading G" with
`R2G = ⟨4, [], [], [], [(2, 3)]⟩`). How many cases would the final
`match` have, how many would be closed by `genesis_mark_not_separable`'s
argument, and would any new lemma be needed?

## Answer

<details>
<summary>Worked answer</summary>

Four cases, `x = 0, 1, 2, 3`. The two marks on the required data `2` and
`3` would be the live leaves, one isomorphic to the other by the
transposition of 2 and 3. The marks on `0` and on `1` would each be
closed by the same argument as `genesis_mark_not_separable`: the instance
`(0, [x])` with `x ∉ {2, 3}` mentions neither required datum, so R3 keeps
`(2, 3)` collapsed over the instance-less base, and validity fails. This
reuses the mention lemma; `mu2_unique_F` itself is about `R2F` and cannot
simply be applied to this four-datum regime. A formal four-datum result
would need its own application, case analysis, and isomorphism witness.
The book's Python check tests the four unary marks and finds verdicts
`[False, False, True, True]`; that is a finite example, not a new
grammar-wide uniqueness theorem.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/MinimalityF.lean` lines 37-65, 72-81, 86-195; `Minimality.lean` lines 149-151, 155-166 |
| Axiom report | `artifacts/lean_axioms.txt`: `genesis_mark_not_separable`, `mu2_unique_F`, `deltaU0F_valid` `[propext, Quot.sound]`; `cost1_insufficient_F` `[propext]` |
| Paper | `paper/paper.md` §7.4 (**[theorem]** `mu2_unique_F`) and §12 residual R5 (discharged 2026-08-18); ledger `CL-3-UNIQUE-MU2-F` |
| Artifact | `artifacts/challenges.json`, `challenge3.F.mu2.minimum_cost = [2, 1]`, one class; `artifacts/claims.json`, `CL-3-UNIQUE-MU2.F = 1` |
| Check (Python) | `python textbook/checks/u32_minimality_f.py`: the unary-mark deltas by marked datum in both readings (L: 0 and 1 valid; F: 1 and 2 valid, 0 not); `mu2` minimum `(2, 1)` with two isomorphic marks in F; the genesis mark leaves `(1, 2)` collapsed and separates `(0, 1)` |
| Check (book Lean) | `python textbook/checks/u32_lean.py`: eight book theorems plus four Genesis theorems kernel-checked, Lean 4.33.0 |
