# Unit 22. Under the finer measure the answer is unique

**Claim.** If price compares item count first and new forms' places second,
the unary mark is cheapest. Under this declared price rule, all cheapest
responses belong to one class under renaming; the literal responses can
still differ.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Measure a delta by `mu2 = (number of items, total arity of
new forms)`, compared lexicographically. Then every valid two-item
response to Challenge 3 whose new-form arity sum is at most 1 yields a
regime isomorphic to the unary mark `U0`. With the cost floor of Unit 18
and the absence of valid two-item deltas of arity sum 0, the `mu2`
minimum is `(2, 1)` and is unique up to isomorphism.

**Status:** derived
(reading L; reading F by `mu2_unique_F`). **Lean:** `Derivation.mu2_unique`
(`lean4/Derivation/Minimality.lean` lines 371-485), `aritySum` (15-18).
**Axioms:** `propext, Quot.sound`. **Depends on:** Units 18, 21
(`applyDelta_pair`, `no_insts_no_separation`, `isoRefl`, `isoU1U0`).

</details>

## First pass

Keep the same responses, but change the price rule. First compare item
counts. Only if those tie, compare the total number of places in newly
admitted forms. This is **lexicographic order**: first number first.

| Response | Item count | New-form places | Cost pair |
|---|---:|---:|---|
| Unary mark | 2 | 1 | `(2, 1)` |
| Binary link | 2 | 2 | `(2, 2)` |
| Binary loop | 2 | 2 | `(2, 2)` |

The unary mark now wins. Marking 0 and marking 1 are still two different
literal responses, but renaming exchanges them: one minimum class.

**Predict:** would a three-item response with no new form places beat
`(2, 1)`?

<details>
<summary>Check your prediction</summary>

No. `(3, 0)` loses because its first number is larger. The second
number matters only when the first numbers tie.

</details>

The price rule is supplied. The theorem establishes uniqueness up to
the declared renaming under that rule, not a preference forced by the
demand itself. The formal proof checks all item pairs, beyond this table.

## Question

Unit 21 left the minimum underdetermined. Is that a fact about the
problem, or about the yardstick? If the metatheory declares a finer
yardstick, does a unique answer appear, and what does it take to prove
"unique" over the *whole* grammar rather than within an enumeration?

## What we already possess

- Three tied two-item classes under `mu1` (Unit 21): the mark (one form
  of arity 1), the link and the loop (one form of arity 2 each).
- `applyDelta_pair`: a two-item delta is the first item, then the second
  (Minimality lines 27-33).
- `no_insts_no_separation`: no instance, no separation (Unit 18).
- `isoRefl`, `isoU1U0` (Unit 21).

## New concept: a lexicographic cost, and a proof by exhausting shapes

`aritySum` adds the arities of the `newForm` items in a delta and ignores
everything else. `mu2` is the pair `(length, aritySum)`, smaller first
component first. So `(2, 1)` beats `(2, 2)`: among two-item deltas, the
one admitting less form structure wins.

`mu2_unique` takes *any* two items `a`, `b` such that `[a, b]` is valid
and `aritySum [a, b] ≤ 1`, and produces an isomorphism from the result
to `U0`. The proof is a case analysis on the shape of `a`, then of `b`,
over all sixteen shape pairs. Most branches die for the reasons of
Unit 18: an instance or rule cannot be first (no form yet); a datum or
form first followed by anything but an instance leaves no instance, so no
separation. The one live shape is **form then instance**, and there the
arity bound forces the form to be unary, well-formedness forces the
instance onto that form with one argument, and the argument is datum 0
or datum 1: `U0` or `U1`, each isomorphic to `U0`.

## Plain-language interpretation

The yardstick changed, and with it the verdict: "yes, unique". The
paper is careful to say which question that answers. Uniqueness is
*measure-relative*. The declared metatheory chose `mu1` and `mu2`;
neither was derived from the demand or from the system. Under one, the
system's next shape is open; under the other, it is the one-place mark.

What the proof earns is the word *every*. The Python enumeration finds
one class within its bounds; the Lean quantifies over any two items of
the grammar, any arity, any argument list, and shows the live case has
no room to vary. That is the difference between "we looked and found
one" and "there is one".

## Pseudocode

```
# Gloss
given a, b with [a, b] valid and aritySum [a, b] <= 1:
  a is an instance or rule:  does not apply (no forms).  ✗
  a is a datum:   result still has no forms; b cannot be an instance/rule;
                  b a datum or form leaves no instance; not separable.  ✗
  a is a form of arity c (c >= 1, else it does not apply):
      b a datum / form / rule: no instance; not separable.  ✗
      b an instance (f, args):  aritySum = c <= 1, so c = 1;
          well-formed: f = 0, args = [x], x < 2
          x = 0: result is U0, isoRefl
          x = 1: result is U1, isoU1U0.                           ✓
```

## Python

```python
from derivation.candidates import Bounds, apply_delta, min_responses, mu2
from derivation.engine import GENESIS_L, delta_label
from derivation.iso import isomorphic
from derivation.model import replay

base = replay(GENESIS_L)
mr = min_responses(base, (0, 1), "mu2", Bounds(2, 2))
print(mr.cost, [delta_label(base, d) for d in mr.deltas], [mu2(d) for d in mr.deltas])
r0, r1 = (apply_delta(base, d) for d in mr.deltas)
print(isomorphic(r0, r1))
```

Output:

```text
(2, 1) ['form1+inst1', 'form1+inst1'] [(2, 1), (2, 1)]
True
```

## Line-by-line Python explanation

`mu2(delta)` (`candidates.py` lines 107-111) returns
`(len(delta), sum of arities of NewForm items)`.

`min_responses(..., "mu2", ...)` (lines 370-420) first finds the least
item count with a valid delta, 2, then among the valid two-item deltas
keeps those with the least `mu2`: the two unary marks, `(2, 1)`. The
links and loops, at `(2, 2)`, drop out.

`isomorphic(r0, r1)` is `True`: one class. The check script goes beyond
the engine's bounds, trying every pair of items with arities up to 3 and
form indices up to 1 on the base, and finds exactly two valid deltas of
arity sum at most 1 (both marks) and none of arity sum 0. That is the
Lean case analysis run on a finite slice, in both readings.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Minimality.lean lines 15-18, 371-379,
-- 445-485 (the live branch; the dead branches are summarized below)
def aritySum : List Item → Nat
  | [] => 0
  | .newForm a :: rest => a + aritySum rest
  | _ :: rest => aritySum rest

theorem mu2_unique (a b : Item) (hval : validResponse R2L 0 1 [a, b])
    (har : aritySum [a, b] ≤ 1) :
    ∃ s, applyDelta R2L [a, b] = some s ∧ Nonempty (Iso s U0) := by
  cases hval with
  | intro s hs =>
    have happ := hs.1
    have hsep := hs.2.1
    refine ⟨s, happ, ?_⟩
    rw [applyDelta_pair] at happ
    cases ha : applyItem R2L a with
    | none => rw [ha] at happ; cases happ
    | some r1 =>
      rw [ha] at happ
      have happ2 : applyItem r1 b = some s := happ
      cases a with
      -- … newInst, newRuleAll: do not apply; newDatum: no instance can follow …
      | newForm c =>
          -- … c ≥ 1; r1 = ⟨2, [c], [], [], [(0, 1)]⟩; b a datum/form/rule: dead …
          cases b with
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
                  have hx2 : x < 2 := by
                    have := hcond.2.2 x (by simp)
                    simpa using this
                  subst hz
                  match x, hx2 with
                  | 0, _ => exact ⟨isoRefl U0 (by decide)⟩
                  | 1, _ => exact ⟨isoU1U0⟩
              next => cases happ2
```

```lean
-- Lean (book), textbook/checks/u22_lean.py: the prose lemma the paper
-- uses alongside mu2_unique, proved
theorem no_arity_zero_response (a b : Item)
    (hval : validResponse R2L 0 1 [a, b]) (har : aritySum [a, b] = 0) :
    False := by
  obtain ⟨s, happ, hsep, -⟩ := hval
  rw [applyDelta_pair] at happ
  have hab := aritySum_cons a [b]
  have ha0 : aritySum [a] = 0 := by omega
  have hb0 : aritySum [b] = 0 := by omega
  cases h1 : applyItem R2L a with
  | none => rw [h1] at happ; cases happ
  | some r1 =>
      rw [h1] at happ
      have hr1 := applyItem_zero_keeps_bare R2L rfl rfl a ha0 r1 h1
      have hs := applyItem_zero_keeps_bare r1 hr1.1 hr1.2 b hb0 s happ
      exact no_insts_no_separation hs.2 hsep
```

## Line-by-line Lean explanation

**Opening.** `hval` is opened into the result `s`, `happ` (the delta
lands on `s`) and `hsep` (`s` separates 0 from 1). The goal's first two
parts are `s` and `happ`; what remains is `Nonempty (Iso s U0)`.
`applyDelta_pair` splits `happ` into "apply `a`, then apply `b`".

**First item.** `cases ha : applyItem R2L a` keeps the equation `ha`.
If it is `none`, `happ` is `none = some s`, impossible. Otherwise `r1` is
the regime after `a`, and `happ2 : applyItem r1 b = some s`.

**Dead first items.** `newInst` and `newRuleAll` cannot apply to `R2L`
(no forms): `if_neg` with `simp [R2L]` and `cases ha`. `newDatum` gives
`r1 = ⟨3, [], [], [], [(0, 1)]⟩`; then `b` is examined: an instance or
rule still cannot apply, and a datum or form leaves `s.insts = []`, so
`no_insts_no_separation rfl hsep` contradicts `hsep`. (The proof writes
`absurd (…) id`, turning the proof of `False` into the goal.)

**Live first item: `newForm c`.** First `hc1 : 1 ≤ c`, by cases on
`c < 1` or `c ≥ 1`: in the first case the form does not apply, so `ha`
is impossible. Then `r1 = ⟨2, [c], [], [], [(0, 1)]⟩`. For `b` a datum,
form or rule, the same dead end: no instance.

**Live second item: `newInst f args`.**

- `hcsum`: `aritySum [newForm c, newInst f args]` computes to `c` (the
  instance contributes nothing), so `c ≤ 1`; with `hc1`, `c = 1`.
- `split at happ2` on the instance guard. In the live branch `hcond` is
  the three-part guard: `f < [1].length`, `args.length = [1].getD f 0`,
  all arguments below `2`. From the first, `f = 0`; from the second,
  `args.length = 1`; `match args, hargs1 with | [x], _` names the one
  argument; from the third, `x < 2`.
- `subst hz` replaces `s` by the computed result, and `match x, hx2`
  splits `x` into `0` and `1`. For `0` the result is `U0` itself and
  `isoRefl U0` (its demand `(0, 1)` is sorted, by `decide`) is the
  isomorphism; for `1` the result is `U1` and `isoU1U0` is.
- The `next => cases happ2` branch is the guard failing: `none = some s`.

**The book's `no_arity_zero_response`.** The paper's §7.4 says the
`mu2` minimum is `(2, 1)` "together with … the absence of valid (2, 0)
deltas", a lemma stated in prose and not in Genesis's Lean. The book
proves it: split `aritySum [a, b] = 0` into the two items; a one-item
step of arity sum 0 on a form-less, instance-less regime either fails or
keeps it form-less and instance-less (`applyItem_zero_keeps_bare`, a
four-way case split like Unit 18's); apply that twice; the final regime
has no instance, so it cannot separate. This is book Lean, outside the
frozen inventory, and the audit record for `Minimality` notes the gap.

**Axioms.** `propext, Quot.sound` for `mu2_unique`, `mu2_unique_F`,
`isoRefl` and the book theorems that use `omega` or `decide`; `propext`
for `aritySum_cons` and `applyItem_zero_keeps_bare`.

## What has been proved

- Every valid two-item response of arity sum at most 1 is isomorphic to
  `U0` (Genesis, derived, grammar-wide, reading L).
- Reading F: every such response is isomorphic to `U0F`, the one extra
  case (a mark on the genesis datum) being refuted by the mention lemma
  (`mu2_unique_F`, Genesis, derived; taught with the mention lemma later
  in the book).
- No valid two-item response has arity sum 0 (book, derived). Hence,
  with Unit 18, the `mu2` minimum is exactly `(2, 1)`.
- The link and loop are excluded by the hypothesis (`aritySum deltaBL =
  2`), not by failing validity (book, by `decide`).
- Within the bounds, the engine finds one class in both readings
  (Genesis, verified finite).
- The alternative cost counting new instances assigns the same pair
  `(2, 1)` to a valid mark and a valid link with non-isomorphic results
  (book, `instance_count_tie`). This comparison needs no arity bound.

## What has not been proved

- That `mu2` is "the" cost. It is declared. The paper's own framing:
  the answer to "is a minimum necessarily unique?" is *no under `mu1`,
  yes up to isomorphism under `mu2`*, and the choice between them is a
  metatheoretic act.
- Uniqueness on the nose. `U0` and `U1` are different regimes; they are
  one class under the implemented isomorphism.
- A classification of three-item responses, or a corresponding theorem
  on regimes with existing forms. `mu2_unique` classifies selected
  two-item responses on `R2L` and `R2F`. Under the stated lexicographic
  order, every three-item response costs more than `(2, 1)` regardless
  of its second cost component.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `aritySum`, `mu2` | the finer cost | declared measure (paper §3 definition 6, §7.4) |
| the sixteen shape cases | exhausting the grammar | metatheory case analysis over `Item` |
| `match args, hargs1` | reading a one-element list | metatheory pattern matching |
| `Nonempty (Iso s U0)` | "unique up to isomorphism" | metatheory existence of a relabelling |

**What the system holds.** After the `mu2`-minimal response: two data,
one unary form, one instance marking one of them, one demand. The
system does not hold the measure and did not choose this shape; the
responder did, under a yardstick the metatheory declared.

**Phrases to read with care.**

- "The unique minimum" always carries "under `mu2`, up to isomorphism".
- "Grammar-wide" means: over every pair of items of the declared `Item`
  type. The grammar itself is admitted (Unit 18).

## Student exercise

Suppose a third measure `mu3 = (items, number of new instances)`. Is the
`mu3` minimum unique up to isomorphism? Use Units 21 and 22 to answer
without a new enumeration.

## Answer

<details>
<summary>Worked answer</summary>

No. The mark and link from Unit 21 are already enough to decide this:
both are valid, both contain two items and one new instance, and their
results are not isomorphic. Both cost `(2, 1)` under `mu3`.

Could either be beaten? No delta with fewer than two items is valid
(Unit 18). A two-item delta without a new instance leaves the initial
instance list empty and cannot separate. Thus `(2, 0)` cannot beat
them. The two different classes remain tied minima. This argument needs
no assumption that an arity bound from `mu2_unique` applies to `mu3`.
Other declared measures could make other distinctions; this unit
examines these particular measures.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Minimality.lean` lines 15-18, 27-33, 371-485; `MinimalityF.lean` line 86 (`mu2_unique_F`) |
| Axiom report | `artifacts/lean_axioms.txt`: `mu2_unique`, `mu2_unique_F`, `isoRefl` `[propext, Quot.sound]` |
| Paper | `paper/paper.md` §7.4 (**[theorem]** `mu2_unique`; **[theorem]** `mu2_unique_F`; **[finite computation]** "uniqueness is measure-relative") |
| Ledger | `paper/paper_claim_ledger.md`, `CL-3-UNIQUE-MU2-L`, `CL-3-UNIQUE-MU2-F` |
| Artifact | `artifacts/challenges.json`, `challenge3.{L,F}.mu2.minimum_cost = [2, 1]`, `valid_deltas_at_minimum = 2`, one class `form1+inst1`; `artifacts/claims.json`, `CL-3-UNIQUE-MU2 = {L: 1, F: 1}` |
| Test | `tests/test_candidates.py::test_c3_mu2_minimum_is_unary_mark` |
| Check (Python) | `python textbook/checks/u22_mu2_unique.py`: `mu2` minimum `(2, 1)` with two isomorphic marks in both readings; comparisons include the recorded demand; over a 3-arity slice, two valid deltas of arity sum ≤ 1 and none of sum 0; the instance-count cost leaves mark and link tied; `(2, 1)` beats `(3, 0)` |
| Check (book Lean) | `python textbook/checks/u22_lean.py`: eight book reports plus three Genesis theorems kernel-checked, Lean 4.33.0, including `no_arity_zero_response` and `instance_count_tie`; `propext, Quot.sound` for those two and the class witness, `propext` for the cost equations and general zero-cost preservation lemma |
